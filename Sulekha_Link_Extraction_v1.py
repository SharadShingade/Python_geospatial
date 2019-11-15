from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import random
import sqlite3
import csv
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

cpath="C:\Users\Administrator\Downloads\chromedriver_win32 (2)\chromedriver.exe"    #Path for Chromedriver varies for each PC
def initDriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('disable-infobars')
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=cpath)
    driver.implicitly_wait(10)
    return driver

r=0
#main=[]
driver = initDriver()
inputWSS = r"C:\Users\Administrator\Desktop\UXO\Sulekha\Data_links\FMCG\Personal_care\Mumbai"
inputCsv = "%s\Personal_Care_Services_Mumbai"  % inputWSS 
#inputCsv = "Accommodation_Services_Bangalore"                                   #Task file in which you have given a set of links to scrape
data = pd.read_csv(inputCsv+".csv",sep=',')
for p in data["link"]:
    main=[]
    driver.get(p)
    m=0
    i=0
    j=0

    for i in range(5000):                                       
        try:
             
            element = driver.find_element_by_css_selector('#morebusinesslist > a')                                          
            element.click()
            j=0
            m=m+1                                              
            print(m)  
            sleep(7)
            
        except:
            j=j+1
            print("not loaded")
            sleep(15)
            if j==8:
                break
    sleep(4)
    html=driver.page_source
    soup = BeautifulSoup(html,"lxml")
    boxes=soup.find_all("div",class_="wraper")
    print(len(boxes))
    print("-----------------------------")
    for box in boxes:
        linko=box.find("div",class_="head")
        linky=linko.find("a",href=True)
        extract=linky["href"]
        link=str("www.sulekha.com"+extract)
        main.append(link)
        print(link)
    print(len(main)) 
    df=pd.DataFrame()
    df["Links"]=main
    r=r+1
    df.to_csv(inputWSS+"\links"+"\Sulekha_"+str(r)+"_Personal_Care_Services_Mumbai.csv",index=False)            #Change the Output file name according to the Entity
    df=df.iloc[0:0]
    