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
            'description': 'La communauté bittorrent francophone',
            'icon': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAA'
                    'LGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mA'
                    'AAF3CculE8AAABj1BMVEUAAADP/v/P///L///K/v985Oc20NUAo7B95ed'
                    'm29hk2th5/+iS//9RpIpSp406bV09c2Kp+f6h9/6g9/2f9v2h9/2m+P1r'
                    '3uFn3+Ni2t5i299k3uJj3eFk3eJk3uJn3+Nr3uFp39xdz85e0dBp3dvt7'
                    'u1z1c9c0clh2c9+w77g3t674txf18RYx7aZ3NPs6eqnr65u175bx62b3c'
                    '3Z3dxdyqte2rNd1a9dzKxNloFbxKBTtZJVvpdc16lZyZ9LpINOq4layqF'
                    'NqohayKBbxaFOmoMyWk5PpIZTr41QqolRrItVtJFUs5BRrIpVtJFNn4I0'
                    'XlFDlJRUwMBNsLA9h4g5fX49iIlCkpM8hIVElpcpWlYqV1QfQD4BAQEkS'
                    '0ckSkYCAwMbODYrWVQWLSxWyL9PtaUQIB0ZMi4bNTEuY1wuYVsAAAAjSk'
                    'U3dm4XLyxb2bpWxqsXLyo/jHpKoo0oT0YbNS8WKSUqU0khQDkXMCs+inM'
                    'hRTpZz6k/jHQiRDsbNy8lSz8jRz0dOjMtY1L////0lPd2AAAAUXRSTlMA'
                    'AAAAAAAAAAAAAAAAAAAAAAICAgICAimBp6mpqamnhCsy09c2DZP6oANPu'
                    'Ov5ujIPr+umNW76+3MNguL09fX19fX144cPBSdBQ0NDQ0NBKAUzAVOdAA'
                    'AAb0lEQVQoz53PMQ4BURhF4f97oRCRic4GNBMJiUKmUVmyRkWhobYGKok'
                    'FkKcweUIlTndObnPFF34JVMgpp6t76BpCBLjQG5l6EY7OxswV9tQ0xbeY'
                    'Wb4HG/RrqxLWTgaToo8OB1EtWs+J3c1fXz55Ats0Ecm4zZNfAAAAAElFT'
                    'kSuQmCC',
            'wizard': True,
            'options': [
                {
                    'name': 'enabled',
                    'type': 'enabler',
                    'default': False
                },
                {
                    'name': 'url',
                    'default': 'https://ygg.to',
                    'description': 'Only an https url will be accepted'
                },
                {
                    'name': 'username',
                    'default': ''
                },
                {
                    'name': 'password',
                    'default': '',
                    'type': 'password'
                },
                {
                    'name': 'seed_ratio',
                    'label': 'Seed ratio',
                    'type': 'float',
                    'default': 1,
                    'description': 'Will not be (re)moved until this seed'
                                   ' ratio is met.'
                },
                {
                    'name': 'seed_time',
                    'label': 'Seed time',
                    'type': 'int',
                    'default': 40,
                    'description': 'Will not be (re)moved until this seed time'
                                   ' (in hours) is met.'
                },
                {
                    'name': 'extra_score',
                    'advanced': True,
                    'label': 'Extra Score',
                    'type': 'int',
                    'default': 20,
                    'description': 'Starting score for each release found via'
                                   ' this provider.'
                }]
        }
    ]
}]
