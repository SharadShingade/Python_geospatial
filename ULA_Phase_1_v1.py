# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 11:08:39 2019

@author: Admin
"""
# Script for ULA Phase-I analysis using opensourcre e.g GDAL etc.

# references https://pysal.readthedocs.io/en/1.5/library/esda/mapclassify.html

import os, win32com.client, glob,sys
import os.path, ntpath, shutil, glob
import pandas as pd
import os
from shapely.geometry import Point, Polygon

import operator
from osgeo import gdal, gdalnumeric, ogr, osr

import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

WS = r"G:\ULA_Phase_I_UXO_scripts"

data = [x for x in os.listdir(r"%s\Cities" % WS) if not x.startswith('#')] # list comprensation
for currentcity in data:
    dirname = ntpath.basename(currentcity)
    print dirname
    
    dataWS = r"%s\Data\%s" % (WS,dirname)
    if not os.path.exists(dataWS):
        os.makedirs(dataWS)
        
    
    lcT1 = glob.glob(r'%s\Cities\%s\T1\%s*t1*.img' % (WS,dirname,dirname))
    lcT2 = glob.glob(r'%s\Cities\%s\T2\%s*t2*.img' % (WS,dirname,dirname))
    lcT3 = glob.glob(r'%s\Cities\%s\T3\%s*t3*.img' % (WS,dirname,dirname))
    lcT4 = glob.glob(r'%s\Cities\%s\T4\%s*t4*.img' % (WS,dirname,dirname))
    
    t1_bndy = glob.glob(r'%s\Cities\%s\T1\%s*.shp' % (WS,dirname,dirname))
    t2_bndy = glob.glob(r'%s\Cities\%s\T2\%s*.shp' % (WS,dirname,dirname))
    t3_bndy = glob.glob(r'%s\Cities\%s\T3\%s*.shp' % (WS,dirname,dirname))
    t4_bndy = glob.glob(r'%s\Cities\%s\T4\%s*.shp' % (WS,dirname,dirname))
    
    
    t1_bndy = t1_bndy[0]
    t2_bndy = t2_bndy[0]
    t3_bndy = t3_bndy[0]
    t4_bndy = t4_bndy[0]
    rlcT1 = lcT1[0]
    rlcT2 = lcT2[0]
    rlcT3 = lcT3[0]
    rlcT4 = lcT4[0]
    
    # reprojecting vector using geopandas
    
    boundary = gpd.read_file(t1_bndy)
    
    inp_crs = boundary.crs
    
    
    
 
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataset = driver.Open('%s' % (t1_bndy))
    
    # from Layer
    layer = dataset.GetLayer()
    spatialRef = layer.GetSpatialRef()
    
    # output SpatialReference
    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(4326)
    
    # create the CoordinateTransformation
    coordTrans = osr.CoordinateTransformation(spatialRef, outSpatialRef)
    
    
    
    ## raster reprojection
    R_t1 = gdal.Open(rlcT1)
    R_t2 = gdal.Open(rlcT2)
    R_t3 = gdal.Open(rlcT3)
    R_t4 = gdal.Open(rlcT4)
    
    lcT1_output = r"%s\%s" % (dataWS,os.path.basename(rlcT1))
    
    os.system('gdalmanage copy %s %s' %(rlcT1,lcT1_output))
    
    # gdal.Warp(lcT1_output,R_t1,dstSRS='EPSG:4326') raster reprojection


    
    
    