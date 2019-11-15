from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import lxml
import sqlite3
import csv
import os
import glob
import os.path, ntpath

import re

inputWSS = r"C:\Users\Administrator\Desktop\UXO\Sulekha\Data_links\FMCG\Personal_care\Mumbai"

linkws = r"%s\links" % inputWSS 
outlinkws = r"%s\links_out" % inputWSS

#df=pd.DataFrame(columns=["Name","Address","Contact Details","Speciality"])
#df.to_csv(inputWSS+"\Personal_Care_Services_hyderabad_2_out.csv",index=False)                                     #Output file:Just change the keyword Input_name

cpath=r"C:\Users\Administrator\Downloads\chromedriver_win32 (2)\chromedriver.exe"

def initDriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('disable-infobars')
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=cpath)
    driver.implicitly_wait(10)
    return driver

driver = initDriver()






def goJustDial(infile,outfile):
    #provideCsv name

        
    #inputCsv = linkws+"\%s"  % dfile
    inputCsv = infile
    outff = outfile                                      #Name of Input csv goes here
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

    

def getShopDetails(pageLink,outff):   
    global driver

    print(pageLink)
    try:
        driver.get("https://"+str(pageLink))
    except Exception as e:
        print(e)
    sleep(5)
    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    html=driver.page_source
    soup= BeautifulSoup(html,"lxml")


    name=soup.find('title').text
    name=name.replace("| Sulekha Mumbai","")                                #Change the Name of the city only according to respected city you are scraping
    print(name)
    name=name.encode('utf-8')
    try:
        numb= soup.find('span',class_="number").text
        print(numb)
        numb=numb
    except:
        numb="None"
        numb=numb
    addr=soup.find('address')
    jam=addr.text
    jam=jam.replace("GET DIRECTIONS","")
    jam=jam.replace("Address","")
    addr=jam.encode('utf-8')
    spec=soup.find('p',class_="ic-tag")

    
    try:
        spec2=spec.find_all("span")
        print(spec2.a.text)
        spec2=spec2.a.text.encode('utf-8')
    except:
        try:
            spec2=spec.a.text
        except:
        #spec=spec.span.text
            spec2="Personal_care"                                              #Change according to the Entity you are scraping
    print(spec2)
    print("---------------------------------")


    row = [name,addr,numb,spec2]
    
    
    
    #with open(inputCsv+"_out.csv", 'ab') as csvFile:
    with open(outff, 'ab') as csvFile:             #Output file:Just change the keyword Input_name
                                                                            #Note: Name of output file should be same as above
        writer = csv.writer(csvFile)
        writer.writerow(row)

    csvFile.close()
    
   
    
if __name__ == "__main__":
    
    dataf= glob.glob(r"%s\Sulekha_*_Personal_Care_Services_Mumbai.*" % (linkws))
    
    for dfiles in dataf:
        #print (dfile)
        dfile = ntpath.basename(dfiles)[:-4]
        print (dfile)
        infile = r'%s\%s' %(linkws,dfile)
        outfile = outlinkws+"\%s_out.csv" %(dfile)
        df=pd.DataFrame(columns=["Name","Address","Contact Details","Speciality"])
        #df.to_csv(linkws+"\%s_out.csv",index=False) 
        #outf = df.to_csv(outfile,index=False)
        df.to_csv(outfile,index=False) 
        goJustDial(infile, outfile)
        
     
