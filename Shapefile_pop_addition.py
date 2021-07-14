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
#input_shapes = r"I:\#UK_pack_project\#Cities_Boundary\#Final_boundaries_all_cities_24June\Municipio_Boundaries\T1_T2"
input_shapes = r"I:\#UK_pack_project\#Cities_Boundary\8_cities_13thJuly\City_boundaries\T1_T2"

#GHSL_data= r"G:\#GHSL_Data_26_march_2018\GHS_CR2018\V1\GHS_BUILT_LDSMT_GLOBE_R2018A_3857_30_V1_0-ESRI.vrt"

tempWS = r"I:\Temp_rasters"

arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension('spatial')

arcpy.env.scratchWorkspace = tempWS
arcpy.env.workspace = tempWS
cs = 54052

#basepath = os.path.basename


#for current_U_edge in os.listdir(raw_data):
for shape in glob.glob(r"%s\*.shp" %(input_shapes)):
    print shape
    s = time.clock()
    cityname = ntpath.basename(shape)[:-4]

    print cityname
    
    ###
    #extract classfication dates
    with arcpy.da.SearchCursor(shape, ["Year_T1","Year_T2"]) as cursor:
        for row in cursor:
            P1_year = row[0]
            P2_year= row[1]

            print P1_year
            print P2_year

    ## calculate field
    field_p1 = r"P1_%s" % P1_year
    field_p2 = r"P2_%s" % P2_year

    print field_p1
    print field_p2
    
    
    #field_p1 = r"P1_%s" % P1_year
    arcpy.AddField_management(shape, field_p1, "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(shape, field_p1, "[P1]", "VB", "")

    #field_p2 = r"P2_%s" % P2_year
    arcpy.AddField_management(shape, field_p2, "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(shape, field_p2, "[P2]", "VB", "")


    print "field added"
    
    
    
    # time
    e = time.clock()
    print 'completed in time %s'  % ((e-s)/60)
    
  
        
        
        
        


   


    
    
    

    
    
    
    
    
    
    

 

   
    
        
            
            


  

        

   



    

    

   

   

   

    
    
    

    

    

    

    

    

    

    

    

    
    
    

    
    

    
    



    

    
    

