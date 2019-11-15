##
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

#raw_data = r"G:\#InclusionProject\Completed_City"
raw_data = r"G:\#InclusionProject\Completed_city_extra_cities\#Completed_cities"
reclassWS =r"G:\#InclusionProject\Reclass"
landscan = r"D:\#Land_Worldpop_share_Nov_2019\World_pop_data"
output = r"D:\#Land_Worldpop_share_Nov_2019\#Densification_output"
output_d = r"D:\#Densification\Output"
csv = r"D:\#Land_Worldpop_share_Nov_2019\#Densificationout_csv"

pop_den = r"D:\#Land_Worldpop_share_Nov_2019\World_pop_data"

df = pd.read_excel('D:\#Landscan_pop_share_Nov_2019\city_year.xlsx', sheet_name='T2')

basepath = os.path.basename
'''
for current_data_dir in os.listdir(raw_data):

    dirname = ntpath.basename(current_data_dir)
    print dirname
    output_f =r"%s\%s" %(output,dirname)
    if not os.path.exists(output_f ):
            os.makedirs(output_f )

    for t in range(2,4):
        print t
        urban_edge = r"%s\%s\urban_edge_t%s.shp" % (raw_data,dirname,t)
        print urban_edge
        k = r"T%s_datte" % t
        kk = df.set_index('City Name')[k].to_dict()
        #print kk
        year = kk[dirname]
        print year

        time_f = t-1

        #Dev = r"%s\%s_t%s_mosiac.img" % (reclassWS,dirname,time_f)
        
        #ext_leapfrog_SQL = "\"Value\" = 3 OR \"Value\" = 4"
        #incl_SQL = "VALUE = 5"

        #new_Dev_attExtract = arcpy.sa.ExtractByAttributes(Dev, ext_leapfrog_SQL)
        #incl_attExtract = arcpy.sa.ExtractByAttributes(Dev, incl_SQL)

        new_Dev_outpoly=r"%s\%s\%s_t%s_new_dev.shp" %(output_d,dirname,dirname,t)
     
        #new_Dev_poly = arcpy.RasterToPolygon_conversion(new_Dev_attExtract, new_Dev_outpoly, "NO_SIMPLIFY")

        incl_outpoly=r"%s\%s\%s_t%s_incl.shp" %(output_d,dirname,dirname,t)
     
        #incl_poly = arcpy.RasterToPolygon_conversion(incl_attExtract, incl_outpoly, "NO_SIMPLIFY")

        # clip
        #clip_new_dev = r"%s\%s_t%s_new_dev_clip" %(output_f,dirname,t)

        #arcpy.Clip_analysis(new_Dev_outpoly, urban_edge,clip_new_dev, "")

        #

        #clip_incl = r"%s\%s_t%s_incl_clip" %(output_f,dirname,t)

        #arcpy.Clip_analysis(incl_outpoly, urban_edge,clip_incl, "")


        #
        pop_d = r"%s\%s\%s_pop_bua_t%s.shp" % (pop_den,dirname,dirname,t)

        inFeatures = [new_Dev_outpoly,pop_d]
        intersect_out = r"%s\%s_t%s_new_dev_intersect_pop.shp" %(output_f,dirname,t)
        arcpy.Intersect_analysis(inFeatures, intersect_out, "ALL", "", "INPUT")

        arcpy.AddField_management(intersect_out, "AreaH", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

        arcpy.CalculateField_management(intersect_out, "AreaH", "!Shape.Area@hectares!", "PYTHON", "")

        arcpy.AddField_management(intersect_out, "Pop_new", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

        arcpy.CalculateField_management(intersect_out, "Pop_new", "[BUA_den] * [AreaH]", "VB", "")


        #
        inFeatures_i = [incl_outpoly,pop_d]
        intersect_out_i = r"%s\%s_t%s_incl_intersect_pop.shp" %(output_f,dirname,t)
        arcpy.Intersect_analysis(inFeatures_i, intersect_out_i, "ALL", "", "INPUT")

        arcpy.AddField_management(intersect_out_i, "AreaH", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

        arcpy.CalculateField_management(intersect_out_i, "AreaH", "!Shape.Area@hectares!", "PYTHON", "")

        arcpy.AddField_management(intersect_out_i, "Pop_new", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

        arcpy.CalculateField_management(intersect_out_i, "Pop_new", "[BUA_den] * [AreaH]", "VB", "")

        #dissolve_summ = r"%s\%s_t2pop_t%s_sum.shp" %(output,dirname,y)
        #arcpy.Dissolve_management(intersect_outtt, dissolve_summ, "#", "Pop SUM", "MULTI_PART", "DISSOLVE_LINES")


        #
        new_dev_csv = r"%s_T%s_dev.csv" %(dirname,t)
        incl_csv = r"%s_T%s_incl.csv" %(dirname,t)

        arcpy.TableToTable_conversion(intersect_out,csv,new_dev_csv)
        arcpy.TableToTable_conversion(intersect_out_i,csv,incl_csv)

'''
###################################################################
# Script for calculating population share inclusion vs extension+leapfrog using worldpop data        

xlFile = r"D:\#Land_Worldpop_share_Nov_2019\Densification_Sample_table.xlsx"

xlApp = win32com.client.Dispatch("Excel.Application")

workbook = xlApp.Workbooks.Open(xlFile)

worksheet = workbook.Worksheets("Sheet1")

fdd = csv

#for xlrow in xrange(3,50):
#for xlrow in xrange(3,50):
xlrow = 4
for x in glob.glob("%s/*_T2_dev.csv" % (fdd)):
#for f in glob.glob("%s/*_T1_T2_shares.csv" % (dd)):
    #print f
    dirname = ntpath.basename(x).split('_T')[0]
    print dirname
    #T = ntpath.basename(f).split('_')[-2]

    
    
    for a in glob.glob("%s\%s_T2_dev.csv" % (fdd,dirname)):
        print a

    for b in glob.glob("%s\%s_T3_dev.csv" % (fdd,dirname)):
        print b

    for c in glob.glob("%s\%s_T2_incl.csv" % (fdd,dirname)):
        print c

    for d in glob.glob("%s\%s_T3_incl.csv" % (fdd,dirname)):
        print d


   
  

    
    #a = r"%s/%s_T2_T2_shares.csv" % (dd,dirname)
    #print a
    #b = r"%s/%s_T1_T3_shares.csv" % (dd,dirname)
    #print b
    #c = r"%s/%s_T2_T3_shares.csv" % (dd,dirname)
    #print c
    #d = r"%s/%s_T3_T3_shares.csv" % (dd,dirname)
    #print d
    
      
    worksheet.Range("A%s" % xlrow).Value = dirname
    #worksheet.Range("C%s" % xlrow).Value = dirname
        
    #xx = pd.read_csv(x)
    aa = pd.read_csv(a)
    bb = pd.read_csv(b)
    cc = pd.read_csv(c)
    dd = pd.read_csv(d)
    
    

    
    #print sur_df
    #T2data = sur_df[sur_df.Per == 'T1']
    #Total = ff['Area'].sum()
    
    BU1= aa['Pop_new'].sum()
    worksheet.Range("D%s" % xlrow).Value = BU1
    
    BU2= bb['Pop_new'].sum()
    worksheet.Range("H%s" % xlrow).Value = BU2

    BU3= aa['AreaH'].sum()
    worksheet.Range("E%s" % xlrow).Value = BU3

    BU4= bb['AreaH'].sum()
    worksheet.Range("I%s" % xlrow).Value = BU4

    BU5= cc['Pop_new'].sum()
    worksheet.Range("B%s" % xlrow).Value = BU5
    
    BU6= dd['Pop_new'].sum()
    worksheet.Range("F%s" % xlrow).Value = BU6

    BU7= cc['AreaH'].sum()
    worksheet.Range("C%s" % xlrow).Value = BU7

    BU8= dd['AreaH'].sum()
    worksheet.Range("G%s" % xlrow).Value = BU8

    
    
    ## Population
    
    
    
    xlrow = xlrow +1
workbook.Save()

