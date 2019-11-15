# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 15:02:32 2019

@author: Admin
"""

import pandas as pd
import json
import time
import requests
#

address = r"TungLok Signatures,6 Eu Tong Sen St,02-88,Singapore 059817"

response = requests.get('https://developers.onemap.sg/commonapi/search?searchVal=%s&returnGeom=Y&getAddrDetails=Y' % (address), auth=('user', 'password'))

location = response.json()
