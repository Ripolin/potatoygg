# coding: utf8
from bs4 import BeautifulSoup
from couchpotato.core.helpers.encoding import simplifyString, tryUrlencode
from couchpotato.core.helpers.variable import getImdb, tryFloat, tryInt
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
from couchpotato.core.media.movie.providers.base import MovieProvider
from datetime import datetime, timedelta

import re
import traceback


class YGG(TorrentProvider, MovieProvider):
    """
    Couchpotato plugin to search movies torrents on www.yggtorrent.com.
    """

    url_scheme = 'https'
    domain_name = 'yggtorrent.com'
    limit = 15
    # Used by YarrProvider.login()
    login_fail_msg = 'Ces identifiants sont invalides'
    http_time_between_calls = 0  # Used by Plugin.wait()
    log = CPLog(__name__)

    def __init__(self):
        """
        Default constructor
        """
        TorrentProvider.__init__(self)
        MovieProvider.__init__(self)
        path_www = YGG.url_scheme+'://'+YGG.domain_name
        self.urls = {
            'login': path_www+'/user/login',  # Used by YarrProvider.login()
            'login_check': path_www,  # Used by YarrProvider.login()
            'search': path_www+'/engine/search?{0}'
        }

    def getLoginParams(self):
        """
        Return YGG login parameters.

        .. seealso:: YarrProvider.getLoginParams
        """
        return {
            'id': self.conf('username'),
            'pass': self.conf('password'),
            'submit': ''
        }

    def loginSuccess(self, output):
        """
        Check server's response on authentication.

        .. seealso:: YarrProvider.loginSuccess
        """
        return 0 == len(output)

    def loginCheckSuccess(self, output):
        """
        Check if we are still connected.

        .. seealso:: YarrProvider.loginCheckSuccess
        """
        result = False
        soup = BeautifulSoup(output, 'html.parser')
        if soup.find(text='Mon compte'):
            result = True
        return result

    def getMoreInfo(self, nzb):
        """
        Get details about a torrent.

        .. seealso:: MovieSearcher.correctRelease
        """
        data = self.getHTMLData(nzb['detail_url'])
        soup = BeautifulSoup(data, 'html.parser')
        description = soup.find(id='description')
        if description:
            nzb['description'] = description.prettify()

    def extraCheck(self, nzb):
        """
        Exclusion when movie's description contains more than one IMDB
        reference to prevent a movie bundle downloading. CouchPotato
        is not able to extract a specific movie from an archive.

        .. seealso:: MovieSearcher.correctRelease
        """
        result = True
        ids = getImdb(nzb.get('description', ''), multiple=True)
        if len(ids) not in [0, 1]:
            YGG.log.info('Too much IMDB ids: {0}'.format(', '.join(ids)))
            result = False
        return result

    def parseAge(self, str):
        """
        Retrieve age in days from the date of torrent addition.
        """
        delta = 0
        matcher = re.search('il y a (\d+) (\S+)', str.strip())
        if matcher:
            now = datetime.now()
            value = tryInt(matcher.group(1))

            if matcher.group(2) in ['minute', 'minutes', 'heure', 'heures',
                                    'jour']:
                delta = now - timedelta(days=1)
            if matcher.group(2) == 'jours':
                delta = now - timedelta(days=value)
            if matcher.group(2) == 'mois':
                delta = now - timedelta(days=value*30)
            if matcher.group(2) == 'an':
                delta = now - timedelta(days=365)
            if matcher.group(2) == 'ans':
                delta = now - timedelta(days=value*365)
        return (now - delta).days

    def _searchOnTitle(self, title, media, quality, results, offset=0):
        """
        Do a search based on possible titles. This function doesn't check
        the quality because CouchPotato do the job when parsing results.
        Furthermore the URL must stay generic to use native CouchPotato
        caching feature.

        .. seealso:: YarrProvider.search
        """
        try:
            params = {
                'q': simplifyString(title)
            }
            if offset > 0:
                params['page'] = offset*YGG.limit
            url = self.urls['search'].format(tryUrlencode(params))
            data = self.getHTMLData(url)
            soup = BeautifulSoup(data, 'html.parser')
            links = soup.find_all('a', class_='torrent-name')
            for link in links:
                detail_url = link['href']
                if u'/filmvidéo/' in detail_url:
                    name = link.text.strip()
                    td = link.parent
                    url = td.find('a', target='_blank')['href']
                    id_ = tryInt(re.search('\?id=(\d+)', url).group(1))
                    infos = td.parent.find_all('td')
                    age = self.parseAge(infos[1].text)
                    size = self.parseSize(infos[2].text)
                    seeders = tryInt(infos[3].string)
                    leechers = tryInt(infos[4].string)
                    result = {
                        'id': id_,
                        'name': name,
                        'seeders': seeders,
                        'leechers': leechers,
                        'size': size,
                        'age': age,
                        'url': url,
                        'detail_url': detail_url,
                        'verified': True,
                        'get_more_info': self.getMoreInfo,
                        'extra_check': self.extraCheck
                    }
                    results.append(result)
                    YGG.log.debug(result)
            # Get next page if we don't have all results
            pagination = soup.find('ul', class_='pagination')
            if pagination:
                pages = pagination.find_all('li')
                if pages and len(pages) > 0:
                    for page in pages:
                        next_ = tryInt(page.find('a').text)
                        if next_ > offset:
                            self._searchOnTitle(title, media, quality,
                                                results, offset+1)
                            break
        except:
            YGG.log.error('Failed searching release from {0}: {1}'.
                          format(self.getName(), traceback.format_exc()))
