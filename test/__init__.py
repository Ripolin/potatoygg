# coding: utf8
from os.path import dirname
import os
import sys

# Root path
base_path = dirname(os.path.abspath(__file__))

# Insert local directories into path
sys.path.insert(0, os.path.join(base_path, '../couchpotato/libs'))
sys.path.insert(1, os.path.join(base_path, '../couchpotato'))
sys.path.insert(2, os.path.join(base_path, '..'))

import requests

# Disable HTTPS InsecureRequestWarning
requests.packages.urllib3.disable_warnings()
