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
'''
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
'''
out_csvt =r"D:\#Land_Worldpop_share_Nov_2019\CSV_T_wise_Nov2019"
'''
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
'''
#############################################################
# 7_landscan_pop_share_in_excel
xlFile = r"D:\#Land_Worldpop_share_Nov_2019\Template_format_21_feb_corrections.xlsx"  ## for revised version


xlApp = win32com.client.Dispatch("Excel.Application")

workbook = xlApp.Workbooks.Open(xlFile)

worksheet = workbook.Worksheets("Sheet1")

    
    
fdd = out_csvt

#for xlrow in xrange(3,50):
xlrow = 3
for f in glob.glob("%s/*_T1_T2_shares.csv" % (fdd)):
#for f in glob.glob("%s/*_T1_T2_shares.csv" % (dd)):
    #print f
    dirname = ntpath.basename(f).split('_T')[0]
    print dirname
    #T = ntpath.basename(f).split('_')[-2]

    
    
    for a in glob.glob("%s\%s_T2_T2*.csv" % (fdd,dirname)):
        print a

    for b in glob.glob("%s\%s_T1_T3*.csv" % (fdd,dirname)):
        print b

    for c in glob.glob("%s\%s_T2_T3*.csv" % (fdd,dirname)):
        print c

    for d in glob.glob("%s\%s_T3_T3*.csv" % (fdd,dirname)):
        print d
    

    worksheet.Range("A%s" % xlrow).Value = dirname
    #worksheet.Range("C%s" % xlrow).Value = dirname
        
    ff = pd.read_csv(f,low_memory=False)
    aa = pd.read_csv(a,low_memory=False)
    bb = pd.read_csv(b,low_memory=False)
    cc = pd.read_csv(c,low_memory=False)
    dd = pd.read_csv(d,low_memory=False)

    

    
    #print sur_df
    #T2data = sur_df[sur_df.Per == 'T1']
    #Total = ff['Area'].sum()
    
    BU1= ff['Area'].sum()
    worksheet.Range("L%s" % xlrow).Value = BU1
    
    BU2= aa['Area'].sum()
    worksheet.Range("M%s" % xlrow).Value = BU2
    
    PO1= ff['Pop'].sum()
    worksheet.Range("Q%s" % xlrow).Value = PO1
    
    PO2= aa['Pop'].sum()
    worksheet.Range("R%s" % xlrow).Value = PO2
    
    ##
    #sur_dff = pd.read_csv(k)
    BU1= bb['Area'].sum()
    worksheet.Range("N%s" % xlrow).Value = BU1
    
    BU2= cc['Area'].sum()
    worksheet.Range("O%s" % xlrow).Value = BU2
    
    BU3= dd['Area'].sum()
    worksheet.Range("P%s" % xlrow).Value = BU3
    
    PO1= bb['Pop'].sum()
    worksheet.Range("U%s" % xlrow).Value = PO1
    
    PO2= cc['Pop'].sum()
    worksheet.Range("V%s" % xlrow).Value = PO2
    
    PO3= dd['Pop'].sum()
    worksheet.Range("W%s" % xlrow).Value = PO3
    
    
    xlrow = xlrow +1
   

workbook.Save()

'''
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

xlFilee = r"D:\#Land_Worldpop_share\Template_format_11_March_BUA_corrections.xlsx"                 

xlApp = win32com.client.Dispatch("Excel.Application")

workbook = xlApp.Workbooks.Open(xlFilee)

worksheet = workbook.Worksheets("Sheet1")

fdd = out_csvb


#for xlrow in xrange(3,50):
xlrow = 3
for f in glob.glob("%s/*_T1_T2_BUAshares.csv" % (fdd)):
#for f in glob.glob("%s/*_T1_T2_shares.csv" % (dd)):
    #print f
    dirname = ntpath.basename(f).split('_T')[0]
    print dirname
    #T = ntpath.basename(f).split('_')[-2]

    
    
    for a in glob.glob("%s\%s_T2_T2*.csv" % (fdd,dirname)):
        print a

    for b in glob.glob("%s\%s_T1_T3*.csv" % (fdd,dirname)):
        print b

    for c in glob.glob("%s\%s_T2_T3*.csv" % (fdd,dirname)):
        print c

    for d in glob.glob("%s\%s_T3_T3*.csv" % (fdd,dirname)):
        print d

      
    worksheet.Range("A%s" % xlrow).Value = dirname
    #worksheet.Range("C%s" % xlrow).Value = dirname
        
    ff = pd.read_csv(f)
    aa = pd.read_csv(a)
    bb = pd.read_csv(b)
    cc = pd.read_csv(c)
    dd = pd.read_csv(d)

    

    
    #print sur_df
    #T2data = sur_df[sur_df.Per == 'T1']
    #Total = ff['Area'].sum()
    
    BU1= ff['Area'].sum()
    worksheet.Range("L%s" % xlrow).Value = BU1
    
    BU2= aa['Area'].sum()
    worksheet.Range("M%s" % xlrow).Value = BU2
    
    
    ##
    #sur_dff = pd.read_csv(k)
    BU1= bb['Area'].sum()
    worksheet.Range("N%s" % xlrow).Value = BU1
    
    BU2= cc['Area'].sum()
    worksheet.Range("O%s" % xlrow).Value = BU2
    
    BU3= dd['Area'].sum()
    worksheet.Range("P%s" % xlrow).Value = BU3
    
    
    
    xlrow = xlrow +1
   

workbook.Save()

#### Complete
'''              

   
       
   
