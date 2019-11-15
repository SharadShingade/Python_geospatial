import sys, time, os, win32com.client, glob, arcpy, numpy, random, shapefile
import os.path, ntpath, shutil, glob
import pandas as pd


arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension('spatial')
tempWS = r"D:\#Landscan_pop_share\Temp"   # provide temporary workspace
arcpy.env.scratchWorkspace = tempWS
arcpy.env.extent =""

#landscan_dataf = r"\\desktop-q4d4det\E\200 City Pop_Data" # \\192.168.20.150\e
landscan_dataf = r"\\192.168.20.150\e\200 City Pop_Data"
raw_data = r"G:\#InclusionProject\Completed_City_t"
#raw_data = r"D:\#Landscan_pop_share_Nov_2019\Cities"
df = pd.read_excel('D:\#Landscan_pop_share_Nov_2019\city_year.xlsx', sheet_name='T2')

basepath = os.path.basename

for cityd in os.listdir(raw_data):
    city = ntpath.basename(cityd)
    print city
    output = r"%s\Worldpop_data_processed_revised\%s" % (landscan_dataf,city)
    output_old = r"%s\Worldpop_data_processed\%s" % (landscan_dataf,city)
    if not os.path.exists(output):
        os.makedirs(output)

    out_folder_path = r"%s" % output
    out_name = "fGDB.gdb"
    outgdb= r"%s\\fGDB.gdb" % output
    if not arcpy.Exists(outgdb):
        arcpy.CreateFileGDB_management(out_folder_path, out_name)
    
    for t in range(2,4):
        print t
        
        k = r"T%s_datte" % t 
        kk = df.set_index('City Name')[k].to_dict()
        #print kk
        year = kk[city]
        #print year
 
                
        l = r"Country" 
        ll = df.set_index('City Name')[l].to_dict()
        if city in ll:
            country = ll[city]
            #print country

        #try:
            

        landscan_data = r"%s\T%s_Landscan" % (landscan_dataf,t)

        worldpopdata = glob.glob(r"%s\%s\%s\*.tif" % (landscan_data,year,country))
        #print worldpopdata
        
        for land_f in worldpopdata:
            print land_f
            urban_edge = r"%s\%s\urban_edge_t3.shp" % (raw_data,city)
            urban_edge_t = r"%s\%s\urban_edge_t%s.shp" % (raw_data,city,t)

            # Mask
            #mask_pop = r"%s\%s_T%s_%s.img" %(output,city,t,year)
            mask_pop = r"%s\%s_T%s_%s.img" %(output_old,city,t,year)
            if not arcpy.Exists(mask_pop):
                
                outExtractByMask = arcpy.sa.ExtractByMask(land_f, urban_edge)
                outExtractByMask.save(r"%s\%s_T%s_%s.img" %(output,city,t,year))
                mask_pop = r"%s\%s_T%s_%s.img" %(output,city,t,year)

            
            #point = r"%s\\fGDB.gdb\\%s_point_T%s_%s" %(output,city,t,year)
            point = r"%s\\fGDB.gdb\\%s_point_T%s_%s" %(output_old,city,t,year)
            if not arcpy.Exists(point):
                print r"point file not exists for %s" % city
                point_raster = arcpy.RasterToPoint_conversion(mask_pop,point,"VALUE")

            #fishnet_out_gdb = r"%s\\fGDB.gdb\\%s_fishnet_T%s_%s" %(output,city,t,year)
            fishnet_out_gdb = r"%s\\fGDB.gdb\\%s_fishnet_T%s_%s" %(output_old,city,t,year)

            #if not arcpy.Exists(fishnet_out):
            if not arcpy.Exists(fishnet_out_gdb):
                print "%s No file" % city
                

                fishnet_out = r"%s\\fGDB.gdb\\%s_fishnet_T%s_%s" %(output,city,t,year)
                #cellSizeWidth = 0.0083333333
                #cellSizeHeight = 0.0083333333
                geometryType = 'POLYGON'
                templateExtent = mask_pop
                numRows =  '#'
                numColumns = '#'
                        
                labels = 'NO_LABELS'
                desc = arcpy.Describe(mask_pop)
                        
                cellSizeWidth = desc.children[0].meanCellWidth
                cellSizeHeight = desc.children[0].meanCellHeight
                        
                originCoordinate = str(desc.extent.lowerLeft)
                yAxisCoordinate = str(desc.extent.XMin) + " " + str(desc.extent.YMax + 10)
                oppositeCoorner = str(desc.extent.upperRight)
                        

                fishnet =arcpy.CreateFishnet_management(fishnet_out,originCoordinate,yAxisCoordinate,cellSizeWidth,\
                                                        cellSizeHeight,numRows, numColumns, oppositeCoorner, labels,templateExtent, geometryType)

                    #print r"fishnet created"


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

            
            ###

            inFeatures = [urban_edge_t,out_feature_class]
            intersect_out = r"%s\%s_pop_T%s_%s.shp" %(output,city,t,year)
            arcpy.Intersect_analysis(inFeatures, intersect_out, "ALL", "", "INPUT")
            arcpy.AddField_management(intersect_out, "AreaHH", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.CalculateField_management(intersect_out, "AreaHH", "!Shape.Area@hectares!", "PYTHON", "")

            
            arcpy.AddField_management(intersect_out, "Pop_ls", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            calculation = "([AreaHH]/%s)*[grid_code]" % factor
            #arcpy.CalculateField_management(intersect_out, "Pop_ls", "[GRID_CODE]", "VB", "")
            arcpy.CalculateField_management(intersect_out, "Pop_ls", calculation, "VB", "")
            arcpy.DeleteField_management(intersect_out, "AreaH")
            arcpy.DeleteField_management(intersect_out, "AreaHH")

            print r"Succes %s" % city
         
                            
        #except:
            #print "city not worked %s" % city
        
           

                                
                                
                                
                                
                            
                            
                    

                    

        
        
        
        
        
    
