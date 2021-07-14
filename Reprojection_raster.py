##############################################################################################
#  This Script is devloped for city growth projections

###################################################################################################


import sys, time, os, win32com.client, glob, arcpy, numpy, random
import ghalton, shapefile, matplotlib.pyplot as plt, numpy as np, arcpy, os.path, ntpath, shutil, glob, os, sys, time
import win32com.client, random
import os.path, ntpath, shutil, glob
import pandas as pd

import arcpy.cartography as CA
import arceditor

from shapely.geometry import Point
from shapely.geometry import asShape
from shapely.geometry import Polygon
import math

import googlemaps
from itertools import tee



##
#WS = r"I:\#UK_pack_project\GHSL_procssing" # workspace
input_shapes = r"I:\#UK_pack_project\GHSL_procssing\GHSL_WS"
input_shapes = ['San_Vicente_del_Caguan']

#GHSL_data= r"G:\#GHSL_Data_26_march_2018\GHS_CR2018\V1\GHS_BUILT_LDSMT_GLOBE_R2018A_3857_30_V1_0-ESRI.vrt"

tempWS = r"I:\Temp_rasters"

arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension('spatial')

arcpy.env.scratchWorkspace = tempWS
arcpy.env.workspace = tempWS
cs = 54052

#basepath = os.path.basename

Data = r"D:\Urban_Landscape_Analysis_Data_fourtime\UXO_download\batch2"
outWS= r"I:\#UK_pack_project\GHSL_procssing"
#for city in os.listdir(input_shapes):
for city in input_shapes:
#for shape in glob.glob(r"%s\*.shp" %(input_shapes)):
    print city
    s = time.clock()
    #cityname = ntpath.basename(shape)[:-4]
    cityname =city

    print cityname
    

    dataWS = r"%s\GHSL_WS_projection_correction\%s" % (outWS,city)
    if not os.path.exists(dataWS):
        os.makedirs(dataWS)


    t1_ws = r"%s\T1" % (dataWS)
    if not os.path.exists(t1_ws):
        os.makedirs(t1_ws)

    t2_ws = r"%s\T2" % (dataWS)
    if not os.path.exists(t2_ws):
        os.makedirs(t2_ws)

    t3_ws = r"%s\T3" % (dataWS)
    if not os.path.exists(t3_ws):
        os.makedirs(t3_ws)




        


        
    fc = glob.glob(r"%s\%s\T4\%s*.img" % (Data,city,city))
    print fc

    desc = arcpy.Describe(fc[0])

    # Get the spatial reference 
    #
    sr = desc.spatialReference

    for n in range (1,4):
        print n
        input_raster = glob.glob(r"%s\%s\T%s\%s*.img" % (Data,city,n,city))
        print input_raster
        fname = ntpath.basename(input_raster[0])
        print fname
        output_raster=r"%s\T%s\%s" %(dataWS,n,fname)

        arcpy.ProjectRaster_management(input_raster[0], output_raster,sr)
    
    
    
    
    # time
    e = time.clock()
    print 'completed in time %s'  % ((e-s)/60)
    
  
        
        
        
        


   


    
    
    

    
    
    
    
    
    
    

 

   
    
        
            
            


  

        

   



    

    

   

   

   

    
    
    

    

    

    

    

    

    

    

    

    
    
    

    
    

    
    



    

    
    

