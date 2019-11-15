# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 15:02:32 2019

@author: Admin
"""

import geopandas

import contextily as ctx
#

df = geopandas.read_file(geopandas.datasets.get_path('nybb'))
ax = df.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')

df = df.to_crs(epsg=3857)