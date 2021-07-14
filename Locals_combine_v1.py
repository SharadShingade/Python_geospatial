# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 14:53:42 2021

@author: Admin
"""

from osgeo import gdal, osr
import os
import geopandas as gpd
from shapely.geometry import Point,Polygon,mapping
from fiona.crs import from_epsg  
from osgeo import gdal, ogr, osr
import pandas as pd
import glob, ntpath,shutil

##


def linestring_to_polygon(fili_shps):
    gdf = gpd.read_file(fili_shps) #LINESTRING
    geom = [x for x in gdf.geometry]
    all_coords = mapping(geom[0])['coordinates']
    lats = [x[1] for x in all_coords]
    lons = [x[0] for x in all_coords]
    polyg = Polygon(zip(lons, lats))
    return gpd.GeoDataFrame(index=[0], crs=gdf.crs, geometry=[polyg])




localsws = r"I:\#UK_pack_project\PHASE_II\Download_data\Locales"

merge_locals = r"I:\#UK_pack_project\PHASE_II\Download_data\Locals_merge"
timeframe = 'T0'# "T1_T3"





dataf = [f for f in os.listdir(r"%s\%s" % (localsws,timeframe))]

for city in dataf:
    print city 
    newdata_master = gpd.GeoDataFrame()
    newdata_master['geometry']=None
    
    newdata_master_index = 0
    for xx in glob.glob(r"%s\%s\%s\*0.shp" % (localsws,timeframe,city)):
        print xx
        locale_id = ntpath.basename(xx)[:-5]
        print locale_id
        gdf = gpd.read_file(xx) #LINESTRING
        geom = [x for x in gdf.geometry]
        all_coords = mapping(geom[0])['coordinates']
        lats = [x[1] for x in all_coords]
        lons = [x[0] for x in all_coords]
        polyg = Polygon(zip(lons, lats))
        
        newdata_master.loc[newdata_master_index,'geometry']=polyg
            
        newdata_master.loc[newdata_master_index,'ID_string']=locale_id
            
            
        newdata_master_index= newdata_master_index+1

    newdata_master.crs = from_epsg(4326)

    outchip_shp_merge = r"%s/%s" % (merge_locals,timeframe)
    if not os.path.exists(outchip_shp_merge):
        os.makedirs(outchip_shp_merge)
    merge_shape_name = r"%s/%s_%s_locals_merge.shp" %(outchip_shp_merge,city,timeframe)
    newdata_master.to_file(merge_shape_name)




