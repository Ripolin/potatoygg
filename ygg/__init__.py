# coding: utf8
from .ygg import YGG


def autoload():
    return YGG()

config = [{
    'name': 'ygg',
    'groups': [
        {
            'tab': 'searcher',
            'list': 'torrent_providers',
            'name': 'Yggtorrent',
            'description': '<a href="https://yggtorrent.com" target="_blank">Y'
                           'ggtorrent</a>',
            'icon': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAAXNSR0IAr'
                    's4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAA'
                    'H/SURBVDhPtZLNS9RBGMeH6MW2oIiCiKhLeys6dQqjRTxUBLkHpUNEEhE'
                    'JSZcW25JOkiJRsKYg5UtEi+iWUZDLkhjUIXojyE2SysMqVOb+fjO/efnN'
                    'zDM903+wh555GJ5n5vk834FniKvFLEBtAFptAIAjNlyWxWOWVjGP3/XoT'
                    'wPm+2tVSsviUf0+56yLP9zBWJWazHzJoIKpzIqx9bYyh4CcSsvJE/JJUk'
                    '61qJkOMblTPm3FXc1kVPGkLGz/U1kgZmmOj2ywi1898KxZTDSI/G67/Nu'
                    'nhUYxvk+OpzC2K1SObqqWX3ggyq22Sx4QhTR/cJgP7rCBB0S+gY/uFQ9T'
                    'gEAY8r5EtTyNwBfWRczPhX8VTeLuwejWNksDTPlIKupP8qFDXoGL6Maq6'
                    'uw0sb9+0AzRHx9hm+j2ft5fz66vNfOvQKqod090Mxl17wIZm29vWJZQfJ'
                    'LvNHCEthN6dQu9khBDzbwvRS8Rmt1MsxvFvRbWuZVeXsc6EjSzRn8uegB'
                    '0gApy4iJtrxP5NjzRb4fl2Hl6gfDn3TE4+XKQDbeGZ0i8WCYOcCl+/1xw'
                    'irCuAyCof1vueHCaRL31sQHtXNhWF54l4vE15SeNgAqdjUGuOGccWIiZM'
                    'xoU81J4BA5FLDpO1uJfwnFr6awvxQofa+Ws9g5grHe8wBn74L9/PufcX1'
                    '/7jCFM7Z74AAAAAElFTkSuQmCC',
            'wizard': True,
            'options': [
                {
                    'name': 'enabled',
                    'type': 'enabler',
                    'default': False,
                },
                {
                    'name': 'username',
                    'default': '',
                },
                {
                    'name': 'password',
                    'default': '',
                    'type': 'password',
                },
                {
                    'name': 'seed_ratio',
                    'label': 'Seed ratio',
                    'type': 'float',
                    'default': 1,
                    'description': 'Will not be (re)moved until this seed'
                                   ' ratio is met.',
                },
                {
                    'name': 'seed_time',
                    'label': 'Seed time',
                    'type': 'int',
                    'default': 40,
                    'description': 'Will not be (re)moved until this seed time'
                                   ' (in hours) is met.',
                },
                {
                    'name': 'extra_score',
                    'advanced': True,
                    'label': 'Extra Score',
                    'type': 'int',
                    'default': 20,
                    'description': 'Starting score for each release found via'
                                   ' this provider.',
                }
            ]
        }
    ]
}]
