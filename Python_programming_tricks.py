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
    

###
WS = r"G:\ULA_Phase_I_UXO_scripts"

data = [x for x in os.listdir(r"%s\Cities" % WS) if not x.startswith('#')] # list comprensation
for currentcity in data:
    dirname = ntpath.basename(currentcity)
    print dirname
    
    dataWS = r"%s\Data\%s" % (WS,dirname)
    if not os.path.exists(dataWS):
        os.makedirs(dataWS)
        
Halton_data = r"D:\#Halton_Residential_share\Haltoncsv_data"
        
files = [f for f in os.listdir('.') if os.path.isfile(f)]


### Arcpy combined logics
# 
##############################################################################################
#  This Script is devloped for city growth projections


import googlemaps
from itertools import tee


apiKey = 'AIzaSyC-TZ28cjlc9AI5eQpv1MWT7t0BWT0LjGU'
gmaps = googlemaps.Client(key=apiKey)


##
raw_data = r"D:\#City_Growth_Projection_March_2020\test"

output = r"D:\#City_Growth_Projection_March_2020\test_output"

BUA_data = r"G:\#InclusionProject\Completed_City"

CBD = r"D:\Urban_Landscape_Analysis_Data_CAFcities\CBDs\CBDs_200_cities.shp"

tempWS = r"D:\Temp"

arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension('spatial')
arcpy.env.scratchWorkspace = tempWS
arcpy.env.workspace = tempWS
cs = 54052

#basepath = os.path.basename



## Halton Generation ##



for current_U_edge in os.listdir(raw_data):
    print current_U_edge

    cityname = ntpath.basename(current_U_edge)

    print cityname

    input_file = r"%s\%s\urban_edge_t3.shp" % (raw_data,cityname)

    
    output_WS= r"%s\%s" %(output,cityname)
    if not os.path.exists(output_WS):
            os.makedirs(output_WS)
    
   
    buffer_radius = r"%s\%s_buffer_radius_new.shp" % (output_WS,cityname)
    # fishnet
    fishnet_out = r"%s\%s_fishnet_1km_grid.shp" % (output_WS,cityname)
    
    geometryType = 'POLYGON'
    templateExtent = buffer_radius
    numRows =  '#'
    numColumns = '#'
                        
    labels = 'LABELS'
    desc = arcpy.Describe(buffer_radius)
                        
    #cellSizeWidth = desc.children[0].meanCellWidth
    #cellSizeHeight = desc.children[0].meanCellHeight
    cellSizeWidth = 1000
    cellSizeHeight = 1000
                        
    originCoordinate = str(desc.extent.lowerLeft)
    yAxisCoordinate = str(desc.extent.XMin) + " " + str(desc.extent.YMax + 10)
    oppositeCoorner = str(desc.extent.upperRight)
                        

    fishnet =arcpy.CreateFishnet_management(fishnet_out,originCoordinate,yAxisCoordinate,cellSizeWidth,\
                                            cellSizeHeight,numRows, numColumns, oppositeCoorner, labels,\
                                            templateExtent, geometryType)

    print "fishnet created"

    

    sr = arcpy.SpatialReference(4326)
    fishnet_out_WGS = r"%s\%s_fishnet_1km_grid_WGS.shp" % (output_WS,cityname)
    arcpy.Project_management(fishnet_out,fishnet_out_WGS,sr)

    # Fishnet_points
    fishnet_points = r"%s\%s_fishnet_1km_grid_label.shp" % (output_WS,cityname)

    fishnet_points_WGS = r"%s\%s_fishnet_1km_grid_label_WGS.shp" % (output_WS,cityname)
    arcpy.Project_management(fishnet_points,fishnet_points_WGS,sr)

    arcpy.AddField_management(fishnet_points_WGS, "UID", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(fishnet_points_WGS, "UID", "[FID]+1", "VB", "")

    arcpy.AddField_management(fishnet_points_WGS, "T_CBD", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    arcpy.AddField_management(fishnet_out_WGS, "UID", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(fishnet_out_WGS, "UID", "[FID]+1", "VB", "")

    ##Built Area as points
    for b in range(1,4):
        print b
        
    
        Bu_area = r"%s\%s\city_urbfootprint_clp_t%s.img" %(BUA_data,cityname,b)
        Query = "\"VALUE\" = 1 OR \"VALUE\" = 2 OR \"VALUE\" = 3"
        Bu_extrac = arcpy.sa.ExtractByAttributes(Bu_area, Query)
        Bu_extract = r"%s\city_BUExtract_clp_t%s.img" % (output_WS,b)
    
        arcpy.gp.Int_sa(Bu_extrac,Bu_extract)
        BU_points = r"%s\%s_BU_points_t%s.shp"  % (output_WS, cityname,b)
        arcpy.RasterToPoint_conversion(Bu_extract, BU_points, "VALUE")

    

        # reprojection
        sr = arcpy.SpatialReference(4326)
    
        BU_points_WGS = r"%s\%s_BU_points_t%s_WGS.shp"  % (output_WS, cityname,b)
        arcpy.Project_management(BU_points,BU_points_WGS,sr)

        
        Bu_field = r"T_BU_t%s" % b
        arcpy.AddField_management(fishnet_points_WGS,Bu_field, "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        #arcpy.AddField_management(fishnet_points_WGS, "T_CBD", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    

        # near analysis
    
        arcpy.Near_analysis(fishnet_points_WGS, BU_points_WGS, "", "LOCATION", "NO_ANGLE", "PLANAR")
    
        # Calculate field

    
        infc = arcpy.GetParameterAsText(0)
    

        # Enter for loop for each feature
        #expression = r"'NAME'='%s'" % (cityname)

        if b==1:
            
            
            name_field ='NAME'
            expression = arcpy.AddFieldDelimiters(CBD, name_field) + " = '%s'" % cityname

            # CBD
            with arcpy.da.SearchCursor(CBD, ["SHAPE@XY","NAME"],where_clause=expression) as cursor:
                for row in cursor:
                    #print row(1)
                    x,y = row[0]
                    cbd_point = (y,x)
                    print cbd_point
            

           
            with arcpy.da.UpdateCursor(fishnet_points_WGS, ["SHAPE@XY","NEAR_X","NEAR_Y","T_CBD",Bu_field ]) as cursor:
                for row in cursor:
            
                    x,y = row[0]
                    #print x,y
                    origin = (y,x)
                    destination = (row[2],row[1])
                    print origin
                    print destination
        
                    result_driving = gmaps.distance_matrix(origin, destination, mode='driving')
                    try:
                        duration_drive = result_driving["rows"][0]["elements"][0]["duration"]["value"]
                        print duration_drive
                        print"Pass"
                    except:
                        duration_drive =-9999
                        print duration_drive


                    result_driving_CBD = gmaps.distance_matrix(origin, cbd_point, mode='driving')
                    try:
                        duration_drive_CBD = result_driving_CBD["rows"][0]["elements"][0]["duration"]["value"]
                        print duration_drive_CBD
                        print"Pass"
                    except:
                        duration_drive_CBD =-9999
                        print duration_drive_CBD
            
                    row[4] = duration_drive
                    row[3] = duration_drive_CBD
                    cursor.updateRow(row)

                    print "Time updated"
        else:
            
            with arcpy.da.UpdateCursor(fishnet_points_WGS, ["SHAPE@XY","NEAR_X","NEAR_Y",Bu_field]) as cursor:
                for row in cursor:
            
                    x,y = row[0]
                    #print x,y
                    origin = (y,x)
                    destination = (row[2],row[1])
                    print origin
                    print destination
        
                    result_driving = gmaps.distance_matrix(origin, destination, mode='driving')
                    try:
                        duration_drive = result_driving["rows"][0]["elements"][0]["duration"]["value"]
                        print duration_drive
                        print"Pass"
                    except:
                        duration_drive =-9999
                        print duration_drive
            
                    row[3] = duration_drive
                    cursor.updateRow(row)

                    print "Time updated"
        
        

            
    join_fields = ["T_CBD","T_BU_t1","T_BU_t2","T_BU_t3"]
    arcpy.JoinField_management(fishnet_out_WGS, "UID", fishnet_points_WGS, "UID", join_fields)
    print "Join Success"
    
        
#################################################
        
    # Script for calculating population share using landscan data
##


import sys, time, os, win32com.client, glob, arcpy, numpy, random, shapefile
import os.path, ntpath, shutil, glob
import pandas as pd


arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension('spatial')
tempWS = r"D:\#Landscan_pop_share\Temp"   # provide temporary workspace
arcpy.env.scratchWorkspace = tempWS
arcpy.env.extent =""

BUA_data =r"D:\#Landscan_pop_share\BUA_data" ##
#BUA_data =r"D:\#Landscan_pop_share\BUA_data_error_cities"
raw_data = r"G:\#InclusionProject\Completed_City"
out_folder = r"D:\#Land_Worldpop_share_Nov_2019\World_pop_data"  ###
out_csv =r"D:\#Land_Worldpop_share_Nov_2019\Final_Output_CSV"

#
landscan_dataf = r"\\192.168.20.150\e\200 City Pop_Data"

basepath = os.path.basename


# Year and city
df = pd.read_excel('D:\#Landscan_pop_share_Nov_2019\city_year.xlsx', sheet_name='T2')
#kk = df.set_index('City Name')['T2_datte'].to_dict()

# city and pop

pf = pd.read_excel('D:\#Landscan_pop_share\city_pop_t2_t3.xlsx', sheet_name='Sheet1')
#pk = pf.set_index('City')['T2_pop'].to_dict()

for current_data_dir in os.listdir(BUA_data):
    dirname = ntpath.basename(current_data_dir)
    print dirname
    output= r"%s/%s" %(out_folder, dirname)
    if not os.path.exists(output):
        os.makedirs(output)
    try:
        for y in range(2,4):
            BU_t2 = r"%s\%s\%s_BUA_dd_t%s.shp" % (BUA_data,dirname,dirname,y)
        
            urban_edge_t1 = r"%s\%s\urban_edge_t1.shp" % (raw_data,dirname)
            urban_edge_t2 = r"%s\%s\urban_edge_t2.shp" % (raw_data,dirname)
            urban_edge_t3 = r"%s\%s\urban_edge_t3.shp" % (raw_data,dirname)

            urban_edge = r"%s\%s\urban_edge_t%s.shp" % (raw_data,dirname,y)

            k = r"T%s_datte" % y
            kk = df.set_index('City Name')[k].to_dict()
            #if dirname in kk:
            year = kk[dirname]

            p = r"T%s_pop" %y
            pk = pf.set_index('City')[p].to_dict()
            if dirname in pk:
                atlas_pop = pk[dirname]
        

            #out_feature_class = r"%s\%s_pop_t%s.shp" %(output,dirname,year)
            output_fu = r"%s\Worldpop_data_processed_revised\%s" % (landscan_dataf,dirname)
            out_feature_class = r"%s\%s_pop_T%s_%s.shp" %(output_fu,dirname,y,year)
            if not arcpy.Exists(out_feature_class):
                out_feature_class = r"%s\\fGDB.gdb\\%s_pop_T%s_%s" %(output_fu,dirname,y,year)
            
            
        
        
        
            ## intersect 1
            inFeatures = [BU_t2,out_feature_class]
            intersect_out = r"%s\%s_pop_t%s_intersect_BU%s.shp" %(output,dirname,y,y)
            arcpy.Intersect_analysis(inFeatures, intersect_out, "ALL", "", "INPUT")

            ## project
            out_coordinate_system = arcpy.Describe(BU_t2).spatialReference
            project_out =r"%s\%s_pop_bua_t%s.shp" %(output,dirname,y)
            arcpy.Project_management(intersect_out, project_out, out_coordinate_system)

            # Area calculation
            arcpy.AddField_management(project_out, "Area", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

            arcpy.CalculateField_management(project_out, "Area", "!Shape.Area@hectares!", "PYTHON", "")

            # BUA Density

            arcpy.AddField_management(project_out, "BUA_den", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

            arcpy.CalculateField_management(project_out, "BUA_den", "[Pop_ls] / [Area]", "VB", "")

            ## intersect 2

            inFeaturess = [project_out,urban_edge_t1]
            intersect_outt = r"%s\%s_t1pop_t%s.shp" %(output,dirname,y)

        
            arcpy.Intersect_analysis(inFeaturess, intersect_outt, "ALL", "", "INPUT")

            ###
            arcpy.CalculateField_management(intersect_outt, "Area", "!Shape.Area@hectares!", "PYTHON", "")

            arcpy.AddField_management(intersect_outt, "Pop", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.CalculateField_management(intersect_outt, "Pop", "[Area] * [BUA_den]", "VB", "")

            ## dissolve and stats sum
            dissolve_sum = r"%s\%s_t1pop_t%s_sum.shp" %(output,dirname,y)
            arcpy.Dissolve_management(intersect_outt, dissolve_sum, "#", "Pop SUM", "MULTI_PART", "DISSOLVE_LINES")

            ### erase
            urban_edge_t2_t1 = r"%s\%s_urban_edge_t2_t1.shp" %(output,dirname)  ## need to save in seperate output folder
            arcpy.Erase_analysis(urban_edge_t2, urban_edge_t1,urban_edge_t2_t1, "")

            ##
            inFeaturesss = [project_out,urban_edge_t2_t1]
            intersect_outtt = r"%s\%s_t2pop_t%s.shp" %(output,dirname,y)

        
            arcpy.Intersect_analysis(inFeaturesss, intersect_outtt, "ALL", "", "INPUT")

            arcpy.CalculateField_management(intersect_outtt, "Area", "!Shape.Area@hectares!", "PYTHON", "")

            arcpy.AddField_management(intersect_outtt, "Pop", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.CalculateField_management(intersect_outtt, "Pop", "[Area] * [BUA_den]", "VB", "")

            dissolve_summ = r"%s\%s_t2pop_t%s_sum.shp" %(output,dirname,y)
            arcpy.Dissolve_management(intersect_outtt, dissolve_summ, "#", "Pop SUM", "MULTI_PART", "DISSOLVE_LINES")

            ## for t3
            if y == 3:
                urban_edge_t3_t2 = r"%s\%s_urban_edge_t3_t2.shp" %(output,dirname)  ## need to save in seperate output folde
                arcpy.Erase_analysis(urban_edge_t3, urban_edge_t2,urban_edge_t3_t2, "")
                inFeaturessss = [project_out,urban_edge_t3_t2]
                intersect_outttt = r"%s\%s_t3pop_t%s.shp" %(output,dirname,y)
                arcpy.Intersect_analysis(inFeaturessss, intersect_outttt, "ALL", "", "INPUT")
                arcpy.CalculateField_management(intersect_outttt, "Area", "!Shape.Area@hectares!", "PYTHON", "")
                arcpy.AddField_management(intersect_outttt, "Pop", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
                arcpy.CalculateField_management(intersect_outttt, "Pop", "[Area] * [BUA_den]", "VB", "")
                dissolve_summm = r"%s\%s_t3pop_t%s_sum.shp" %(output,dirname,y)
                arcpy.Dissolve_management(intersect_outttt, dissolve_summm, "#", "Pop SUM", "MULTI_PART", "DISSOLVE_LINES")
            
                arcpy.AddField_management(dissolve_summm, "Per", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
                arcpy.CalculateField_management(dissolve_summm, "Per", "\"T3\"", "VB", "")
            else:
                print "Pass"


            ###

            arcpy.AddField_management(dissolve_sum, "Per", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.CalculateField_management(dissolve_sum, "Per", "\"T1\"", "VB", "")

            arcpy.AddField_management(dissolve_summ, "Per", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.CalculateField_management(dissolve_summ, "Per", "\"T2\"", "VB", "")

        ##
            merge_file = r"%s\%s_T%s_shares.shp" %(output,dirname,y)
        
            if y == 3:
                arcpy.Merge_management([dissolve_sum, dissolve_summ,dissolve_summm], merge_file, "")
            else:
                arcpy.Merge_management([dissolve_sum, dissolve_summ], merge_file, "")

            #arcpy.Merge_management([dissolve_sum, dissolve_summ], merge_file, "")

            SC = arcpy.SearchCursor(merge_file)
            yy = 0
            for x in SC:
                yy = yy + x.getValue('SUM_Pop')

            arcpy.AddField_management(merge_file, "Share", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        
            expression = "!SUM_Pop!"+"/"+"%s" % yy
            arcpy.CalculateField_management(merge_file, "Share", expression, "PYTHON_9.3", "" ) #% yy

        

            ## Atlas pop
            arcpy.AddField_management(merge_file, "Atlas_Pop", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            expressionn = "!Share!"+"*"+"%s" % atlas_pop
            arcpy.CalculateField_management(merge_file, "Atlas_Pop", expressionn, "PYTHON_9.3", "" )


            ## Area and Share area

            arcpy.AddField_management(merge_file, "Area", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.CalculateField_management(merge_file, "Area", "!Shape.Area@hectares!", "PYTHON", "")

            SCC = arcpy.SearchCursor(merge_file)
            yyy = 0
            for xx in SCC:
                yyy = yyy + xx.getValue('Area')

            arcpy.AddField_management(merge_file, "Share_Area", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

            expressionnn = "!Area!"+"/"+"%s" % yyy
            arcpy.CalculateField_management(merge_file, "Share_Area", expressionnn, "PYTHON_9.3", "" )

            ## Density

            arcpy.AddField_management(merge_file, "Density", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.CalculateField_management(merge_file, "Density", "[Atlas_Pop] / [Area]", "VB", "")

            print '\n Succees in city %s for T%s' %(dirname, y)

            ## share file as csv
            out_table = r"%s_T%s_shares.csv" %(dirname,y)
            arcpy.TableToTable_conversion(merge_file,out_csv,out_table)
        

        
 

    except:
        print "\n error in %s city" % dirname
    
##################################################
#### 6 share wise excel export

out_csvt =r"D:\#Land_Worldpop_share_Nov_2019\CSV_T_wise_Nov2019"
=
for current_data_dir in os.listdir(BUA_data):
    dirname = ntpath.basename(current_data_dir)
    print dirname
    output= r"%s/%s" %(out_folder, dirname)
    if not os.path.exists(output):
        os.makedirs(output)
    #try:

    T1_in_T2 = r"%s\%s_t1pop_t2.shp" %(output,dirname)
    T2_in_T2 = r"%s\%s_t2pop_t2.shp" %(output,dirname)
    T1_in_T3 = r"%s\%s_t1pop_t3.shp" %(output,dirname)
    T2_in_T3 = r"%s\%s_t2pop_t3.shp" %(output,dirname)
    T3_in_T3 = r"%s\%s_t3pop_t3.shp" %(output,dirname)


        
   # print '\n Succees in city %s for T%s' %(dirname, y)

    ## share file as csv
    A = r"%s_T1_T2_shares.csv" %(dirname)
    B = r"%s_T2_T2_shares.csv" %(dirname)
    C = r"%s_T1_T3_shares.csv" %(dirname)
    D = r"%s_T2_T3_shares.csv" %(dirname)
    E = r"%s_T3_T3_shares.csv" %(dirname)
    #
    #out_table = r"%s_T%s_shares.csv" %(dirname)

    arcpy.TableToTable_conversion(T1_in_T2,out_csvt,A)
    arcpy.TableToTable_conversion(T2_in_T2,out_csvt,B)
    arcpy.TableToTable_conversion(T1_in_T3,out_csvt,C)
    arcpy.TableToTable_conversion(T2_in_T3,out_csvt,D)
    arcpy.TableToTable_conversion(T3_in_T3,out_csvt,E)

    print '\n Succees in city %s' % dirname

#############################################################
# 7_landscan_pop_share_in_excel
# this part deleted
###########
## 8_landscan_pop_share_BuArea_calculation

out_csvb =r"D:\#Land_Worldpop_share\Final_BUA_CSV_Oct_2019"

for current_data_dir in os.listdir(BUA_data):
    dirname = ntpath.basename(current_data_dir)
    print dirname
    output= r"%s/%s" %(out_folder, dirname)
    if not os.path.exists(output):
        os.makedirs(output)
    #try:
    for y in range(2,4):
        BU_t2 = r"%s\%s\%s_BUA_dd_t%s.shp" % (BUA_data,dirname,dirname,y)
        
        urban_edge_t1 = r"%s\%s\urban_edge_t1.shp" % (raw_data,dirname)
        urban_edge_t2 = r"%s\%s\urban_edge_t2.shp" % (raw_data,dirname)
        urban_edge_t3 = r"%s\%s\urban_edge_t3.shp" % (raw_data,dirname)

        #urban_edge = r"%s\%s\urban_edge_t%s.shp" % (raw_data,dirname,y)

        urban_edge_t2_t1 = r"%s\%s_urban_edge_t2_t1.shp" %(output,dirname)  ## need to save in seperate output folder
        #arcpy.Erase_analysis(urban_edge_t2, urban_edge_t1,urban_edge_t2_t1, "")

        urban_edge_t3_t2 = r"%s\%s_urban_edge_t3_t2.shp" %(output,dirname)  ## need to save in seperate output folder
        #arcpy.Erase_analysis(urban_edge_t3, urban_edge_t2,urban_edge_t3_t2, "")



        #Clip analysis
        
        Input_feature = BU_t2
        clip_features = urban_edge_t1
        out_clip = r"%s\%s_BUA_t1_t%s.shp" %(output,dirname,y)

        arcpy.Clip_analysis(Input_feature, clip_features,out_clip, "")
        
        arcpy.AddField_management(out_clip, "Area", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

        arcpy.CalculateField_management(out_clip, "Area", "!Shape.Area@hectares!", "PYTHON", "")

        #dissolve_sum = r"%s\%s_t1_BUA_t%s_sum.shp" %(output,dirname,y)
        #arcpy.Dissolve_management(out_clip, dissolve_sum, "#", "Area SUM", "MULTI_PART", "DISSOLVE_LINES")

        arcpy.AddField_management(out_clip, "Per", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(out_clip, "Per", "\"T1\"", "VB", "")


        T1_CSV = r"%s_T1_T%s_BUAshares.csv" %(dirname,y)
        arcpy.TableToTable_conversion(out_clip,out_csvb,T1_CSV)
        

        ##


        Input_feature_1 = BU_t2
        clip_features_1 = urban_edge_t2_t1
        out_clip_1 = r"%s\%s_BUA_t2_t%s.shp" %(output,dirname,y)

        arcpy.Clip_analysis(Input_feature_1, clip_features_1,out_clip_1, "")

        arcpy.AddField_management(out_clip_1, "Area", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

        arcpy.CalculateField_management(out_clip_1, "Area", "!Shape.Area@hectares!", "PYTHON", "")

        #dissolve_summ = r"%s\%s_t2_BUA_t%s_sum.shp" %(output,dirname,y)
        #arcpy.Dissolve_management(out_clip_1, dissolve_summ, "#", "Area SUM", "MULTI_PART", "DISSOLVE_LINES")

        arcpy.AddField_management(out_clip_1, "Per", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(out_clip_1, "Per", "\"T2\"", "VB", "")

        T2_CSV = r"%s_T2_T%s_BUAshares.csv" %(dirname,y)
        arcpy.TableToTable_conversion(out_clip_1,out_csvb,T2_CSV)


        if y == 3:
            urban_edge_t3_t2 = r"%s\%s_urban_edge_t3_t2.shp" %(output,dirname)  ## need to save in seperate output folde

            Input_feature_2 = BU_t2
            clip_features_2 = urban_edge_t3_t2
            out_clip_2 =r"%s\%s_BUA_t3_t%s.shp" %(output,dirname,y)
            arcpy.Clip_analysis(Input_feature_2, clip_features_2,out_clip_2, "")

            arcpy.AddField_management(out_clip_2, "Area", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.CalculateField_management(out_clip_2, "Area", "!Shape.Area@hectares!", "PYTHON", "")

            #dissolve_summm = r"%s\%s_t3_BUA_t%s_sum.shp" %(output,dirname,y)
            #arcpy.Dissolve_management(out_clip_2, dissolve_summm, "#", "Area SUM", "MULTI_PART", "DISSOLVE_LINES")

            arcpy.AddField_management(out_clip_2, "Per", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.CalculateField_management(out_clip_2, "Per", "\"T3\"", "VB", "")

            T3_CSV = r"%s_T3_T%s_BUAshares.csv" %(dirname,y)
            arcpy.TableToTable_conversion(out_clip_2,out_csvb,T3_CSV)

        else:
            print "Pass"
        

        merge_file = r"%s\%s_T%s_BUAshares.shp" %(output,dirname,y)
        
        if y == 3:
            arcpy.Merge_management([out_clip, out_clip_1,out_clip_2], merge_file, "")
        else:
            arcpy.Merge_management([out_clip, out_clip_1], merge_file, "")


        print '\n Succees in city %s for T%s' %(dirname, y)

        ## share file as csv
        out_table = r"%s_T%s_BUAshares.csv" %(dirname,y)
        arcpy.TableToTable_conversion(merge_file,out_csvb,out_table)

        print '\n Succees in city %s for T%s' %(dirname, y)
        


###################################################################
# 9 landscan_BUA_Area_in_excel
# deleted part
        
##########################################
# Data join 
    outTable = r"%s\centriod.gdb\%s_slope_table" % (output_WS,cityname)
   
    arcpy.sa.ZonalStatisticsAsTable(fishnet_out_UTM,"ID", out_slope_file,outTable, "DATA", "MEAN")

    join_fields = ["MEAN"]

    arcpy.JoinField_management(fishnet_out_WGS, "ID", outTable, "ID", join_fields)
    print "Join Success"

   
######
 name_field ='NAME'
    expression = arcpy.AddFieldDelimiters(CBD, name_field) + " = '%s'" % cityname

    # CBD
    with arcpy.da.SearchCursor(CBD, ["SHAPE@XY","NAME"],where_clause=expression) as cursor:
        for row in cursor:
            #print row(1)
            x,y = row[0]
            cbd_point = (y,x)
            print cbd_point
            

           
    with arcpy.da.UpdateCursor(fishnet_points_WGS, ["SHAPE@XY","NEAR_DIST","NEAR_X","NEAR_Y","T_BUA","T_CBD"]) as cursor:
        
    #for row in arcpy.da.UpdateCursor(fishnet_out_WGS, ["SHAPE@XY","NEAR_DIST","NEAR_X","NEAR_Y","Time"]):
        for row in cursor:
            
            x,y = row[0]
            #print x,y
            origin = (y,x)
            destination = (row[3],row[2])
            print origin
            print destination
        
            result_driving = gmaps.distance_matrix(origin, destination, mode='driving')
            try:
                duration_drive = result_driving["rows"][0]["elements"][0]["duration"]["value"]
                print duration_drive
                print"Pass"
            except:
                duration_drive =-9999
                print duration_drive


            result_driving_CBD = gmaps.distance_matrix(origin, cbd_point, mode='driving')
            try:
                duration_drive_CBD = result_driving_CBD["rows"][0]["elements"][0]["duration"]["value"]
                print duration_drive_CBD
                print"Pass"
            except:
                duration_drive_CBD =-9999
                print duration_drive_CBD
            
            row[4] = duration_drive
            row[5] = duration_drive_CBD
            cursor.updateRow(row)

            print "Time updated"

            
    join_fields = ["NEAR_DIST", "NEAR_X","NEAR_Y","T_BUA","T_CBD"]
    arcpy.JoinField_management(fishnet_out_WGS, "UID", fishnet_points_WGS, "UID", join_fields)
    print "Join Success"

    
#######################################################################################
 ## create centriod
    arcpy.AddGeometryAttributes_management(Dissolve_urban_edge,"AREA;CENTROID", "", "SQUARE_METERS","")
    Event_layer = "Event_layer"

    dsc = arcpy.Describe(Dissolve_urban_edge)
    coord_sys = dsc.spatialReference
    #wkt 
    #arcpy.MakeXYEventLayer_management(Dissolve_urban_edge,"CENTROID_X", "CENTROID_Y", Event_layer,wkt)
    arcpy.MakeXYEventLayer_management(Dissolve_urban_edge,"CENTROID_X", "CENTROID_Y", Event_layer,coord_sys)

    print "Event Done"

    out_gdb_path = output_WS
    out_gdb_name = "centriod.gdb"

    # Execute CreateFileGDB
    gdb_path = r"%s\%s" % (out_gdb_path,out_gdb_name)
    if not os.path.exists(gdb_path):
        arcpy.CreateFileGDB_management(out_gdb_path,out_gdb_name)
    gdb = r"%s\%s" % (out_gdb_path,out_gdb_name)
    #name_centriod = cityname
    arcpy.env.overwriteOutput=True
    #fileInQuestion = r"%s\%s\%s" % (out_gdb_path,out_gdb_name,cityname)
    #if arcpy.Exists(fileInQuestion):
        #arcpy.Delete_management(fileInQuestion)
    
    arcpy.FeatureClassToFeatureClass_conversion(Event_layer,gdb,cityname, "","")
    print "Centriod done"
    centriod = r"%s\%s\%s" % (out_gdb_path,out_gdb_name,cityname)

    #
    urban_edge_points = r"%s\%s_vertics_points.shp" % (output_WS,cityname)
    arcpy.FeatureVerticesToPoints_management(input_file, urban_edge_points, "ALL")

    # Point Distance
    distance_table = r"%s\%s\%s_distance_table" % (out_gdb_path,out_gdb_name,cityname)
    arcpy.PointDistance_analysis(centriod, urban_edge_points, distance_table, "")

    distance_table_max = r"%s\%s\%s_distance_table_max" % (out_gdb_path,out_gdb_name,cityname)
    arcpy.Statistics_analysis(distance_table, distance_table_max, "DISTANCE MAX", "")

    print "point distance done"

    # Join field ID

    arcpy.AddField_management(Dissolve_urban_edge, "UID", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(Dissolve_urban_edge, "UID", "[FID]+1", "VB", "")
    
    arcpy.JoinField_management(Dissolve_urban_edge, "UID", distance_table_max, "OBJECTID", "MAX_DISTANCE")

    print "join done"

    # add Buffer field
    arcpy.AddField_management(Dissolve_urban_edge, "Buffer", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(Dissolve_urban_edge, "Buffer", "[MAX_DISTAN]*5", "VB", "")

    print "max_distance done"

    # Buffer
    buffer_file = r"%s\%s_buffer.shp" % (output_WS,cityname)
    arcpy.Buffer_analysis(Dissolve_urban_edge, buffer_file, "Buffer", "FULL", "ROUND", "NONE", "", "PLANAR")

    print "buffer done"

    arcpy.AddField_management(Dissolve_urban_edge, "Radius", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    
    arcpy.CalculateField_management(Dissolve_urban_edge, "Radius", "math.sqrt((!POLY_AREA!*5)/math.pi)", "PYTHON", "")

    buffer_file_radius = r"%s\%s_buffer_radius_new.shp" % (output_WS,cityname)
    arcpy.Buffer_analysis(Dissolve_urban_edge, buffer_file_radius, "Radius", "FULL", "ROUND", "NONE", "", "PLANAR")

    
    
###############################################################################################################
# Halton layer
    for halton in os.listdir(Halton_files):
    print halton[:-16]
    

    #cityname = ntpath.basename(current_U_edge)

    cityname = halton[:-16]

    print cityname

    #input_file = r"%s\%s\urban_edge_t3.shp" % (raw_data,cityname)
    
    out_WS= r"%s\%s" %(out_folder,cityname)
    if not os.path.exists(out_WS):
            os.makedirs(out_WS)
            
    #reproject_file = r"%s\%s.shp" %(reproj_WS,cityname)
    
    wkt = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
            PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];\
            -400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;\
            0.001;0.001;IsHighPrecision"

    #sr = arcpy.SpatialReference(4326)

    #sr.loadFromString(wkt)

    #arcpy.Project_management(input_file,reproject_file,sr)

    # Make XY Event layer

    halton_csv = r"%s\%s_Halton_250D.csv" % (Halton_files, cityname)
    halton_layer = "Halton_250_layer"

    arcpy.MakeXYEventLayer_management(halton_csv, "Longitude", "Latitude",halton_layer,wkt,"")

    print "Halton Event generated"
    del halton_csv
    
    out_gdb_path = out_WS
    out_gdb_name = "halton_250.gdb"

    gdb_path = r"%s\%s" % (out_gdb_path,out_gdb_name)
    if not os.path.exists(gdb_path):
        arcpy.CreateFileGDB_management(out_gdb_path,out_gdb_name)
        
    gdb = r"%s\%s" % (out_gdb_path,out_gdb_name)

      
    arcpy.env.overwriteOutput = True

    halton_gdb = r"%s\halton_250.gdb\%s" % (out_WS,cityname)
    arcpy.CopyFeatures_management(halton_layer,halton_gdb,"","0","0","0")

    print "Halton generated"
    
    
###
out_coordinate_system = arcpy.Describe(urban_edge).spatialReference
            project_out =r"%s\\fGDB.gdb\\%s_fishnet_T%s_%s_project" %(output,city,t,year)
            arcpy.Project_management(fishnet_out_gdb, project_out, out_coordinate_system)
            arcpy.AddField_management(project_out, "AreaH", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.CalculateField_management(project_out, "AreaH", "!Shape.Area@hectares!", "PYTHON", "")
            ###
            #with arcpy.da.SearchCursor(project_out,'AreaH') as cursor:
            #   print max(cursor)

            max_total = max((r[0] for r in arcpy.da.SearchCursor(project_out, ['AreaH'])))
            min_total = min((r[0] for r in arcpy.da.SearchCursor(project_out, ['AreaH'])))
            factor = (max_total+min_total)/2
            #print "summed total %s " % factor

            #stupid = r"D:\#Landscan_pop_share_Nov_2019\trial\Algiers_fishnet_T2_2001_project.shp"

            arcpy.MakeFeatureLayer_management(project_out, 'cities_lyrr') 

            selected = arcpy.SelectLayerByLocation_management('cities_lyrr', "INTERSECT", urban_edge, "", "NEW_SELECTION", "NOT_INVERT")

            #out_feature_class = r"%s\%s_pop_T%s_%s.shp" %(output,city,t,year)
            out_feature_class = r"%s\\fGDB.gdb\\%s_fishnet_T%s_intersect" %(output,city,t)
            join_type = 'KEEP_COMMON'
            join_operation = 'JOIN_ONE_TO_ONE'
            spatial_join = arcpy.SpatialJoin_analysis(selected, point , out_feature_class, 'JOIN_ONE_TO_ONE', join_type)
            
            


    
    
    
a = 3

if a >=4 AND a <=2:
    print "yes"
else:
    print "No"    

 

   
    
        
            
            


  

        

   



    

    

   

   

   