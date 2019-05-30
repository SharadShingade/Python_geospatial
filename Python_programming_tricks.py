# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:57:48 2019

@author: Admin
"""
##Libraries



import os , sys,win32com.client, glob
import os.path, ntpath, shutil, glob
import pandas as pd
import os

## For loops
InputWS = r"D:\#US_india_grant\Population_zonal_stat\pop_data_india\UTM"
for f in glob.glob("%s/*.shp" %InputWS):
    print f
    zone = ntpath.basename(f)
    
    for y in glob.glob("%s/*.tif" %InputWS):
        print y
files = [f for f in os.listdir('.') if os.path.isfile(f)]
files_xlsx = [f for f in files if f[-3:] == 'csv']


## commend line code: 
 os.system('gdalwarp %s %s -cutline %s -crop_to_cutline -cwhere OBJECTID_2=%s' %(inraster,outraster,inshape,country_name))
 os.system('gdal_translate -of JPEG -scale -co worldfile=yes %s %s' %(outraster,outJPG))
 
    output_f = r"%s\%s.shp" % (uncorrect_points,pin)
    arcpy.Select_analysis(out_feature_class, output_f, "\"Pincode\" <> %s" % pin) # not equal to

    output_ff = r"%s\%s.shp" % (correct_points,pin)
    arcpy.Select_analysis(out_feature_class, output_ff, "\"Pincode\" = %s" % pin) # equal to