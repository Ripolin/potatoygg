# coding: utf8
import re
import traceback

from bs4 import BeautifulSoup
from couchpotato.core.helpers.encoding import simplifyString, tryUrlencode
from couchpotato.core.helpers.variable import getImdb, tryInt
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
from couchpotato.core.media.movie.providers.base import MovieProvider
from datetime import datetime


class YGG(TorrentProvider, MovieProvider):
    """
    Couchpotato plugin to search movies torrents on www.yggtorrent.com.

    .. seealso:: YarrProvider.login, Plugin.wait
    """

    url_scheme = 'https'
    domain_name = 'yggtorrent.is'
    limit = 50
    http_time_between_calls = 0
    log = CPLog(__name__)

    def __init__(self):
        """
        Default constructor
        """
        TorrentProvider.__init__(self)
        MovieProvider.__init__(self)
        path_www = YGG.url_scheme + '://' + YGG.domain_name
        self.urls = {
            'login': path_www + '/user/login',
            'login_check': path_www + '/user/account',
            'search': path_www + '/engine/search?{0}',
            'torrent': path_www + '/torrent',
            'url': path_www + '/engine/download_torrent?id={0}'
        }

    def getLoginParams(self):
        """
        Return YGG login parameters.

        .. seealso:: YarrProvider.getLoginParams
        """
        return {
            'id': self.conf('username'),
            'pass': self.conf('password')
        }

    def loginSuccess(self, output):
        """
        Check server's response on authentication.

        .. seealso:: YarrProvider.loginSuccess
        """
        return len(output) == 0

    def loginCheckSuccess(self, output):
        """
        Check if we are still connected.

        .. seealso:: YarrProvider.loginCheckSuccess
        """
        result = False
        soup = BeautifulSoup(output, 'html.parser')
        if soup.find(text=u'Déconnexion'):
            result = True
        return result

    def getMoreInfo(self, nzb):
        """
        Get details about a torrent.

        .. seealso:: MovieSearcher.correctRelease
        """
        data = self.getHTMLData(nzb['detail_url'])
        soup = BeautifulSoup(data, 'html.parser')
        description = soup.find(class_='description-header').find_next('div')
        if description:
            nzb['description'] = description.prettify()
        line = soup.find(text=u'Uploadé le').find_next('td')
        added = datetime.strptime(line.getText().split('(')[0].strip(),
                                  '%d/%m/%Y %H:%M')
        nzb['age'] = (datetime.now() - added).days
        self.log.debug(nzb['age'])

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

    def parseText(self, node):
        """
        Retrieve the text content from a HTML node.
        """
        return node.getText().strip()

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
                'category': 2145,  # Film/Vidéo
                'description': '',
                'do': 'search',
                'file': '',
                'name': simplifyString(title),
                'sub_category': 'all',
                'uploader': ''
            }
            if offset > 0:
                params['page'] = offset * YGG.limit
            url = self.urls['search'].format(tryUrlencode(params))
            data = self.getHTMLData(url)
            soup = BeautifulSoup(data, 'html.parser')
            filter_ = '^{0}'.format(self.urls['torrent'])
            for link in soup.find_all(href=re.compile(filter_)):
                detail_url = link['href']
                if re.search(u'/filmvidéo/(film|animation|documentaire)/',
                             detail_url):
                    name = self.parseText(link)
                    id_ = tryInt(re.search('/(\d+)-[^/\s]+$', link['href']).
                                 group(1))
                    columns = link.parent.parent.find_all('td')
                    size = self.parseSize(self.parseText(columns[5]))
                    seeders = tryInt(self.parseText(columns[7]))
                    leechers = tryInt(self.parseText(columns[8]))
                    result = {
                        'id': id_,
                        'name': name,
                        'seeders': seeders,
                        'leechers': leechers,
                        'size': size,
                        'url': self.urls['url'].format(id_),
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
                for page in pagination.find_all('li'):
                    next_ = tryInt(self.parseText(page.find('a')))
                    if next_ > offset + 1:
                        self._searchOnTitle(title, media, quality, results,
                                            offset + 1)
                        break
        except:
            YGG.log.error('Failed searching release from {0}: {1}'.
                          format(self.getName(), traceback.format_exc()))
