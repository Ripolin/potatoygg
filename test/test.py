# coding: utf8
import logging
import os
import requests
import sys
import time

from cache import BaseCache
from couchpotato.core.logger import CPLog
from couchpotato.core.plugins.quality import QualityPlugin
from couchpotato.core.settings import Settings
from couchpotato.environment import Env
from os.path import dirname
from ygg import YGG

base_path = dirname(os.path.abspath(__file__))
plug = QualityPlugin()
qualities = plug.qualities
handler = logging.StreamHandler()
log = CPLog(__name__)
log.logger.setLevel('DEBUG')
log.logger.addHandler(handler)
requests.packages.urllib3.disable_warnings()


class NoCache(BaseCache):
    def get(self, key):
        pass


class TestPotatoYGG:
    def setUp(self, conf='/test.cfg'):
        settings = Settings()
        settings.setFile(base_path + conf)
        Env.set('settings', settings)
        Env.set('http_opener', requests.Session())
        Env.set('cache', NoCache())
        return YGG()

    def test_loginKO(self):
        ygg = self.setUp('/wrong.cfg')
        assert not ygg.login()

    def test_login(self):
        ygg = self.setUp()
        assert ygg.login()

    def test_loginCheck(self):
        ygg = self.setUp()
        isLogged = ygg.login()
        assert isLogged
        if isLogged:
            ygg.last_login_check = time.time() - 7200
            assert ygg.login()

    def test_searchMovie(self):
        ygg = self.setUp()
        results = []
        media = {
            'identifier': 'tt0258463',
            'type': 'movie',
            'category': {'required': ''},
            'info': {'year': 2002}
        }
        isLogged = ygg.login()
        assert isLogged
        if isLogged:
            ygg._searchOnTitle(u'the bourne identity', media, qualities[2],
                               results)
            assert len(results) > 0
            for result in results:
                assert 0 < result['size']

    def test_searchMoviePagination(self):
        ygg = self.setUp()
        results = []
        media = {
            'identifier': 'tt0120737',
            'type': 'movie',
            'category': {'required': ''},
            'info': {'year': 2001}
        }
        isLogged = ygg.login()
        assert isLogged
        if isLogged:
            ygg._searchOnTitle(u'seigneur', media, qualities[2], results)
            ids = list()
            for result in results:
                if result['id'] not in ids:
                    ids.append(result['id'])
            assert len(results) == len(ids)  # No duplication

    def test_searchAnim(self):
        ygg = self.setUp()
        results = []
        media = {
            'identifier': 'tt2948356',
            'type': 'movie',
            'category': {'required': ''},
            'info': {'year': 2016}
        }
        isLogged = ygg.login()
        assert isLogged
        if isLogged:
            ygg._searchOnTitle(u'zootopia', media, qualities[2], results)
            assert len(results) > 0

    def test_extraCheck(self):
        ygg = self.setUp()
        isLogged = ygg.login()
        assert isLogged
        if isLogged:
            path_torrent = ygg.urls['torrent']
            nzb = {
                'detail_url': path_torrent + '/filmvid%C3%A9o/film/41240-integ'
                                             'rale+alien+multi+1080p+hdlight+x'
                                             '264+ac3-mhdgz'
            }
            ygg.getMoreInfo(nzb)
            assert nzb['description'] is not None
            assert not ygg.extraCheck(nzb)

    def test_moreInfo(self):
        ygg = self.setUp()
        isLogged = ygg.login()
        assert isLogged
        if isLogged:
            path_torrent = ygg.urls['torrent']
            nzb = {
                'detail_url': path_torrent + '/filmvid%C3%83%C2%A9o/film/84032'
                                             '-gremlins%201984%20multi%201080p'
                                             '%20hdlight%20x264%20ac3-mhdgz'
            }
            ygg.getMoreInfo(nzb)
            assert nzb['age'] is not None

    def test_download(self):
        ygg = self.setUp()
        url = ygg.urls['url'].format('6103')
        data = ygg.loginDownload(url)
        assert len(data) > 0

    def test_exception(self):
        ygg = self.setUp()
        media = {
            'identifier': 'tt0258463',
            'type': 'movie',
            'category': {'required': ''},
            'info': {'year': 2002}
        }
        isLogged = ygg.login()
        assert isLogged
        if isLogged:
            ygg._searchOnTitle(u'the bourne identity', media, qualities[2],
                               None)
