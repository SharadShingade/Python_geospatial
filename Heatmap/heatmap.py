# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 15:38:48 2018

@author: Admin
"""
import pandas as pd 
import folium
from folium.plugins import HeatMap
for_map = pd.read_csv('final_point_data.csv',header=0)

#print for_map.head()
#print for_map.columns

max_amount = float(for_map['Bank_count'].max())

#hmap = folium.Map(location=[73.237613, 19.154564], zoom_start=7, )
hmap = folium.Map(location=[19.154564,73.237613], zoom_start=7, )

hm_wide = HeatMap( zip(for_map.Y.values, for_map.X.values, for_map.Bank_count.values), 
                   min_opacity=0.2,
                   max_val=max_amount,
                   radius=17, blur=15, 
                   max_zoom=1, 
                 )

#folium.GeoJson(district23).add_to(hmap)
hmap.add_child(hm_wide)
hmap.save(os.path.join('results', 'heatmap.html'))

print 'heatmap html exported congrats'