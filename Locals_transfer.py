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





localsws = r"I:\#UK_pack_project\PHASE_II\Download_data\Locales"

#merge_locals = r"I:\#UK_pack_project\PHASE_II\Download_data\Locals_merge"
timeframe = 'T0_extra'# "T1_T3"

halton_data = r"I:\#UK_pack_project\PHASE_II\Halton_majority\Halton_files"



#dataf = [f for f in os.listdir(r"%s\%s" % (localsws,timeframe))]
dataf = ['Facatativa']

for city in dataf:
    print city
    
    # create folder
    city_ws= r"%s\Locals_combined\%s" %(localsws,city)
    if not os.path.exists(city_ws):
        os.makedirs(city_ws)
        
    t0_ws = r"%s\%s\Locals_T0" % (halton_data,city)
    if not os.path.exists(t0_ws):
        os.makedirs(t0_ws)
    
    t1_ws = r"%s\%s\Locals_T1_T2_T3_corrected" % (halton_data,city)
    if not os.path.exists(t1_ws):
        os.makedirs(t1_ws)
        
    '''    
    for ff in glob.glob(r"%s\%s\%s\*.*" % (localsws,timeframe,city)):
        print ff
        dest = shutil.copy(ff,city_ws)
        
    for f in glob.glob(r"%s\T1_T3\%s\*.*" % (localsws,city)):
        print f
        destt = shutil.copy(f,city_ws)
    '''  

    df_T0 = pd.read_excel(r"%s\%s\halton_excel\%s_circles_t0.xls" % (halton_data,city,city))
    
    df_T1 = pd.read_excel(r"%s\%s\halton_excel\%s_circles_t1_t2_t3.xls" % (halton_data,city,city))
    
    
    for locale in df_T0['ID_string']:
        print locale
        for locale_file in glob.glob(r"%s\%s*.*" % (city_ws,locale)):
            print locale_file
            
            dest = shutil.copy(locale_file,t0_ws)
    
            
    for localee in df_T1['ID_string']:
        print localee
        for locale_filee in glob.glob(r"%s\%s*.*" % (city_ws,localee)):
            print locale_filee
            
            destt = shutil.copy(locale_filee,t1_ws)
            
            
            

        
   
