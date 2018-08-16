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

log = CPLog(__name__)


class YGG(TorrentProvider, MovieProvider):
    """
    Couchpotato plugin to search movies torrents on YGG.

    .. seealso:: YarrProvider.login, Plugin.wait
    """

    url_scheme = 'https'
    url_hostname = 'www.yggtorrent.is'
    limit = 50
    http_time_between_calls = 0

    def __init__(self):
        """
        Default constructor.
        """
        TorrentProvider.__init__(self)
        MovieProvider.__init__(self)
        self.urls = {
            'login': YGG.getBasePath() + '/user/login',
            'login_check': YGG.getBasePath() + '/user/account',
            'search': YGG.getBasePath() + '/engine/search?{}',
            'torrent': YGG.getBasePath() + '/torrent',
            'url': YGG.getBasePath() + '/engine/download_torrent?id={}'
        }
        self.size_gb.append('go')
        self.size_mb.append('mo')
        self.size_kb.append('ko')

    @staticmethod
    def getBasePath():
        """
        Get YGG's base path URL.

        :return: YGG's base path URL
        :rtype: str
        """
        return '{}://{}'.format(YGG.url_scheme, YGG.url_hostname)

    @staticmethod
    def parseText(node):
        """
        Retrieve the text content from a HTML node.

        :return: Text content of a HTML node
        :rtype: str
        """
        return node.getText().strip()

    def getLoginParams(self):
        """
        Return YGG login parameters.

        :return: A login object with a login and a password attributes
        :rtype: dict
        .. seealso:: YarrProvider.getLoginParams
        """
        return {
            'id': self.conf('username'),
            'pass': self.conf('password')
        }

    def loginSuccess(self, output):
        """
        Check server's response on authentication.

        :param output: HTML body returned by a login request
        :type output: str
        :return: The signin operation result
        :rtype: bool
        .. seealso:: YarrProvider.loginSuccess
        """
        return len(output) == 0

    def loginCheckSuccess(self, output):
        """
        Check if we are still connected.

        :param output: HTML body returned by a login request
        :type output: str
        :return: The checking result
        :rtype: bool
        .. seealso:: YarrProvider.loginCheckSuccess
        """
        result = False
        soup = BeautifulSoup(output, 'html.parser')
        if soup.find(text=u' Déconnexion'):
            result = True
        return result

    def getMoreInfo(self, nzb):
        """
        Get details about a torrent.

        :param nzb: Representation of a torrent
        :type nzb: dict
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
        log.debug(nzb['age'])

    def extraCheck(self, nzb):
        """
        Exclusion when movie's description contains more than one IMDB
        reference to prevent a movie bundle downloading. CouchPotato
        is not able to extract a specific movie from an archive.

        :param nzb: Representation of a torrent
        :type nzb: dict
        :return: The checking result
        :rtype: bool
        .. seealso:: MovieSearcher.correctRelease
        """
        result = True
        ids = getImdb(nzb.get('description', ''), multiple=True)
        if len(ids) not in [0, 1]:
            log.info('Too much IMDB ids: {}'.format(', '.join(ids)))
            result = False
        return result

    def buildUrl(self, title, offset):
        """
        Build encoded searchin URL for YGG.

        :param title: Movie's title
        :type title: str
        :param offset: Page index
        :type offset: int
        :return: Searching URL
        :rtype: str
        """
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
        return self.urls['search'].format(tryUrlencode(params))

    def _searchOnTitle(self, title, media, quality, results, offset=0):
        """
        Do a search based on possible titles. This function doesn't check
        the quality because CouchPotato do the job when parsing results.

        :param title: Movie's title
        :type title: str
        :param media: Movie's metadata
        :type media: dict
        :param quality: Movie's quality target
        :type quality: dict
        :param results: Where to append finded torrents
        :type results: list
        :param offset: Page index when pagination is on
        :type offset: int
        .. seealso:: YarrProvider.search
        """
        try:
            data = self.getHTMLData(self.buildUrl(title, offset))
            soup = BeautifulSoup(data, 'html.parser')
            filter_ = '^{}'.format(self.urls['torrent'])
            for link in soup.find_all(href=re.compile(filter_)):
                detail_url = link['href']
                if re.search(u'/filmvidéo/(film|animation|documentaire)/',
                             detail_url):
                    name = YGG.parseText(link)
                    id_ = tryInt(re.search('/(\d+)-[^/\s]+$', link['href']).
                                 group(1))
                    columns = link.parent.parent.find_all('td')
                    size = self.parseSize(YGG.parseText(columns[5]))
                    seeders = tryInt(YGG.parseText(columns[7]))
                    leechers = tryInt(YGG.parseText(columns[8]))
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
                    log.debug(result)
            # Get next page if we don't have all results
            pagination = soup.find('ul', class_='pagination')
            if pagination:
                for page in pagination.find_all('li'):
                    next_ = tryInt(YGG.parseText(page.find('a')))
                    if next_ > offset + 1:
                        self._searchOnTitle(title, media, quality, results,
                                            offset + 1)
                        break
        except:
            log.error('Failed searching release from {}: {}'.
                      format(self.getName(), traceback.format_exc()))
