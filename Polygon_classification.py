# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 12:11:27 2018

@author: Admin
"""

import os
import pandas as pd 
import folium
from folium.plugins import HeatMap
import geopandas as gpd
import fiona
import shapely.geometry as geometry
import pylab as pl
import shapefile

Maha_state = gpd.read_file('zip://'+'jodhpur_roads_blocks_with_ward_ID.zip')


Maha_state['geometry'] ## gives geometry type and its coordinates

# Maha_state['geometry'][11] # it prints actual shape of polygon
#Maha_state.convex_hull
#Maha_state.exterior
#Maha_state.plot()
#Maha_state.iloc[10]



Maha = Maha_state[['OBJECTID_1','geometry']]

writer = pd.ExcelWriter('pandas_simple_new.xlsx', engine='xlsxwriter')
Maha.to_excel(writer, sheet_name='Sheet1')
writer.save()   
    
    
    
    
  
    


'''
input_shapefile = 'jodhpur_roads_blocks_with_ward_ID.shp'
shapefile = fiona.open(input_shapefile)
points = [geometry.shape(point['geometry'])
          for point in shapefile]

print points


x = [p.coords.xy[0] for p in points]
y = [p.coords.xy[1] for p in points]
pl.figure(figsize=(10,10))
_ = pl.plot(x,y,'o', color='#f16824')

for p in points:
    print p
  
## from shapefile

sf = shapefile.Reader("jodhpur_roads_blocks_with_ward_ID.shp")
shapes = sf.shapes()

for t in range(0,120):
    for point in shapes[t].points:
        print point
   

for point in shapes[1].points:
    print point
    
'''


    