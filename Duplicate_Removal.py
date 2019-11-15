import pandas as pd
import glob, os, os.path, ntpath
import numpy as np


Data_f = r"D:\#WebScraping_project\FMCG\Beverage_Suppliers"
#Data_f=r"D:\#WebScraping_project\FMCG\hyderabad"

FMCG_class =r"Beverage_Suppliers"  #
data_out = r"D:\#WebScraping_project\FMCG\Master_output_files\Beverage_Suppliers"

#datafile = glob.glob("%s\*.csv" % (Data_f))



for folder in os.listdir(Data_f):
    print folder
    outfile=r"%s\%s_%s.csv" % (data_out,folder,FMCG_class)
    for cat in glob.glob(r"%s\%s\*.csv" % (Data_f,folder)):
        print cat
        links = pd.read_csv(cat)
        kk = folder.lower()
        ddd = links['link'].astype(str).str.replace("https://www.sulekha.com/", '')
        fff = ddd.astype(str).str.replace("/"+kk, '')
        subcat = fff.astype(str).str.replace('-',' ')
        print subcat
        
        i = 0
        dfm = pd.DataFrame()
        for num in range(1,len(subcat)+1):
            print num
            #bb=str(num)+"hyderabad"
            #i = 0
            for dff in glob.glob(r"%s\%s\links_out\*_%s_*.csv" % (Data_f,folder,num)):
            #for dff in glob.glob(r"%s\%s\links_out\*_%s_*.csv" % (Data_f,folder,bb)):
                print dff
                #subcat[i]
                df=pd.read_csv(dff)
                df['Category']=FMCG_class
                #df["Speciality"]= df["Speciality"].str.replace("Retail_Shopping", "Personal_care", case = False) 
                df['sub_category']=subcat[i]
                i = i+1
                df['Address_upper'] =df['Address'].astype(str).str.upper()
                df2=df.drop_duplicates(subset=['Address_upper'],keep="last")
                df2.drop(['Address_upper'],axis=1,inplace=True)
                #dfm.append(df2)
                dfm = pd.concat([dfm,df2])
            #dfm
        dfm.to_csv(outfile,index=False) 
        
###
        
## Overall duplicate removal based on Name and Address coloumn and split file in to parts         
masterf= pd.DataFrame(columns=['Name','Address','Contact Details','Speciality','Category','sub_category'])
for files in glob.glob(r"%s\*.csv" % (data_out)):
    print files
    x=pd.read_csv(files)
    print x 
    masterf = pd.concat([masterf,x])
    
masterf["Address_upper"]=masterf['Address'].astype(str).str.upper()
masterf["NAME_upper"]=masterf['Name'].astype(str).str.upper()
    
    
df3=masterf.drop_duplicates(subset=['NAME_upper','Address_upper'],keep="last")
    #df4=masterf.drop_duplicates(subset=['Address_upper'],keep="last")
df3.drop(['NAME_upper','Address_upper'],axis=1,inplace=True)
    
new = df3["Name"].str.split(" in ", n = 1, expand = True)
new1 = df3["Address"].str.split(" Landmark: ", n = 1, expand = True) 
    
df3["Correct Name"]= new[0] 
df3["Locality"]= new[1] 
    
df3["Correct Address"]= new1[0] 
df3["Landmark"]= new1[1] 
                
df3['Full Address'] = df3['Correct Name'].str.cat(df3['Correct Address'], sep =",")        
            
df3["Name"] = df3["Correct Name"]
    
df3["Address"]= df3["Correct Address"]
    
df3.drop(['Correct Name','Correct Address'],axis=1,inplace=True)
    
    
    #masterf["combine"]=masterf['NAME_upper'].str.cat(masterf['Address_upper'], sep =",")
    #df5=masterf.drop_duplicates(subset=['combine'],keep="last")
i=1
for g, dk in df3.groupby(np.arange(len(df3)) // 25000):
    print(dk.shape)
    outfile = r"D:\#WebScraping_project\FMCG\#Master_combined_output_files\Beverage_Suppliers_part_%s.csv" %(i)
    dk.to_csv(outfile,index=False)
    i=i+1
        


        
####
    
    
'''    
sample = r"D:\#WebScraping_project\FMCG\#Master_combined_output_files\Retail_shoping_part_4.csv"
            
df = pd.read_csv(sample)

new = df["Name"].str.split(" in ", n = 1, expand = True)
 
new1 = df["Address"].str.split(" Landmark: ", n = 1, expand = True) 

df["Correct Name"]= new[0] 
df["Locality"]= new[1] 

df["Correct Address"]= new1[0] 
df["Landmark"]= new1[1] 
            
df['Full Address'] = df['Correct Name'].str.cat(df['Correct Address'], sep =",")        
        
df["Name"] = df["Correct Name"]

df["Address"]= df["Correct Address"]

df.drop(['Correct Name','Correct Address'],axis=1,inplace=True)
    
'''








'''
for x in datafile:
    print x
    zone = ntpath.basename(x)[:-4]
    df=pd.read_csv(x)
    #print df
    df['Address_upper'] =df['Address'].astype(str).str.upper()
    df2=df.drop_duplicates(subset=['Address_upper'],keep="last")
    df2.drop(['Address_upper'],axis=1,inplace=True)
    #df2=df.drop_duplicates(subset=["Address"],keep="last")
    out_f = r"%s\%s_duplicate_removed.csv" % (data_out,zone)
    df2.to_csv(out_f,index=False)
    print("done")
'''

'''
df=pd.read_excel(x)#Name of input csv goes here<<---

df2=df.drop_duplicates(subset=["Name","Address"],keep="last")#duplicate removal on basis of subset i.e columns in csv

df2.to_csv("rh.csv",index=False)#Name of output csv goes here

print("done")
listf = glob.glob(r"D:\#WebScraping_project\FMCG\Retail_Shopping\Ahmedabad\*.csv")
for x in listf:
    print x 
links = pd.read_csv(x)
i=1
for y in links['link']:
    print i
    print y
    i=i+1
    q = r"https://www.sulekha.com/"
    W= r"/ahmedabad"
    banned =[q,W] 
    
    #ff = lambda x: ' '.join([item for item in x.split() if item not in banned])
    #trial = links['link'].apply(ff)
    
    #fff=[' '.join([item for item in bb.split()if item not in banned])for bb in links['link']]
    

ddd['link'] = links['link'].astype(str).str.replace("https://www.sulekha.com/", '')

fff = ddd['link'].astype(str).str.replace("/ahmedabad", '')

op = fff.astype(str).str.replace('-',' ')



  data = pd.read_csv(inputCsv+".csv",sep=',',names=["link"],skiprows=1)
    i=1
    for x in data["link"]:
        print(i)
        try:
            getShopDetails(x,outff)
        except Exception as e:
            print(e)
        i=i+1
        sleep(2)
'''