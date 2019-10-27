# coding: utf-8
import logging
import os
import requests
import sys
import time

from . import base_path
from cache import BaseCache
from couchpotato.core.event import fireEvent
from couchpotato.core.loader import Loader
from couchpotato.core.logger import CPLog
from couchpotato.core.plugins.quality import QualityPlugin
from couchpotato.core.settings import Settings
from couchpotato.environment import Env
from os.path import dirname


class NoCache(BaseCache):
    def get(self, key):
        pass

plug = QualityPlugin()
qualities = plug.qualities

handler = logging.StreamHandler()
log = CPLog(__name__)
log.logger.setLevel('DEBUG')
log.logger.addHandler(handler)

Env.set('cache', NoCache())
Env.set('http_opener', requests.Session())
Env.set('loader', Loader())
Env.set('settings', Settings())


class TestPotatoYGG:
    def setUp(self, conf='/test.cfg'):
        Env.get('settings').setFile(base_path + conf)
        loader = Env.get('loader')
        module = loader.loadModule('ygg')
        assert module is not None
        assert loader.loadSettings(module, 'ygg', save=False)
        return module.autoload()

    def test_loginKO(self):
        ygg = self.setUp('/wrong.cfg')
        assert not ygg.login()

    def test_login(self):
        ygg = self.setUp()
        assert ygg.login()
        ygg.last_login_check = time.time() - 7200
        assert ygg.login()  # Test loginCheckSuccess
        url = ygg.urls['url'].format('6103')
        data = ygg.loginDownload(url)
        assert len(data) > 0

    def test_searchMovie(self):
        ygg = self.setUp()
        results = []
        media = {
            'identifier': 'tt0258463',
            'type': 'movie',
            'category': {'required': ''},
            'info': {'year': 2002}
        }
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
        ygg._searchOnTitle(u'zootopia', media, qualities[2], results)
        assert len(results) > 0

    def test_extraCheck(self):
        ygg = self.setUp()
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
        path_torrent = ygg.urls['torrent']
        nzb = {
            'detail_url': path_torrent + '/filmvid%C3%83%C2%A9o/film/84032'
                                         '-gremlins%201984%20multi%201080p'
                                         '%20hdlight%20x264%20ac3-mhdgz'
        }
        ygg.getMoreInfo(nzb)
        assert nzb['age'] is not None

    def test_noResult(self):
        ygg = self.setUp()
        results = []
        media = {
            'identifier': 'tt2948356',
            'type': 'movie',
            'category': {'required': ''},
            'info': {'year': 2016}
        }
        ygg._searchOnTitle(u'wxzxw', media, qualities[2], results)
        assert len(results) == 0

    def test_exception(self):
        ygg = self.setUp()
        media = {
            'identifier': 'tt0258463',
            'type': 'movie',
            'category': {'required': ''},
            'info': {'year': 2002}
        }
        ygg._searchOnTitle(u'the bourne identity', media, qualities[2], None)

    def test_url(self):
        ygg = self.setUp()
        assert ygg.urls['url'] is not None
        settings = Env.get('settings')
        settings.set('ygg', 'url', 'http://test.com/test')
        fireEvent('setting.save.ygg.url.after')
        assert ygg.urls['url'] is None
        settings.set('ygg', 'url', 'https://test.com/test')
        fireEvent('setting.save.ygg.url.after')
        assert ygg.urls['url'] is not None
        settings.set('ygg', 'url', 'https://test.com/test/test/')
        fireEvent('setting.save.ygg.url.after')
        assert ygg.urls['torrent'] == 'https://test.com/torrent'

    def test_login_url(self):
        ygg = self.setUp()
        assert ygg.urls['login'] is not None
        settings = Env.get('settings')
        settings.set('ygg', 'login_url', 'http://test.com/')
        fireEvent('setting.save.ygg.login_url.after')
        assert ygg.urls['login'] is None
        settings.set('ygg', 'login_url', 'https://test.com/')
        fireEvent('setting.save.ygg.login_url.after')
        assert ygg.urls['login'] is not None
        settings.set('ygg', 'login_url', 'https://test.com/test/test')
        fireEvent('setting.save.ygg.login_url.after')
        assert ygg.urls['login'] == 'https://test.com/user/login'
