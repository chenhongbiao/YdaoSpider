from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pymysql
import time
import getsets
import book

def jumptopage(currentpage, driver):
    #do something collect the two sets in the current page, then ready to go to the next page
    pagenoteset = set()
    pagebookset = set()
    global noteset
    global notebookset
    pageSource = driver.page_source
    bsObj = BeautifulSoup(pageSource,"html.parser")
    pagenoteset, pagebookset = getsets.getBnoteLinks(bsObj)
    noteset = noteset | pagenoteset
    notebookset = notebookset | pagebookset
    
    if (currentpage == totalpages):
        return  #(two global sets okay)
    else:
        #find the next page button in the current page
        driver.find_element_by_link_text(str(currentpage+1)).click()
        #jump to the new current page and wait it loaded
        wait = WebDriverWait(driver=driver,timeout=10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "currentPage")))
        
        jumptopage(currentpage+1, driver)

noteset = set()
notebookset = set()
totalpages = 0
currentpage = 1
homepage = "http://note.youdao.com/dushu/web/index.html"

driver = webdriver.PhantomJS(executable_path="D:/Internet-IE/phantomjs-2.1.1-windows/bin/phantomjs")
driver.get(homepage) 
wait = WebDriverWait(driver=driver,timeout=10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "currentPage")))

pageSource = driver.page_source
bsObj = BeautifulSoup(pageSource,"html.parser")
totalpages = int ( bsObj.find("span",{"id":"total-pages"}).get_text() )

##(two global sets okay)
jumptopage(currentpage, driver)
driver.close()

for notebook in notebookset:
    noteset = noteset | book.getNoteLinks(notebook)

for note in noteset:
    readnote(note)
print("All note in the database note~")

##################################################
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='faustmeow',
                       db='mysql',
                       charset='utf8mb4')
cur = conn.cursor()
cur.execute("USE readnote")
##################################################
def storeShr(name, photo):
    "insert sharer if not existed"
    cur.execute("SELECT * FROM sharers WHERE name = %s", (name))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO sharers (name, photo) VALUES (%s, %s)", (name, photo))
        conn.commit()
        return cur.lastrowid #get the 'id' attr
    else:
        return cur.fetchone()[0] #get the 'first' attr - 'id' attr
        
def storeNote(title, content, readtimes, praises, updatetime):
    "insert note if not existed"
    cur.execute("SELECT * FROM notes WHERE title = %s AND updatetime = %s", 
                (title, updatetime) )
    if cur.rowcount == 0:
        cur.execute("INSERT INTO notes (title, content, readtimes, praises, updatetime) VALUES (%s, %s, %s, %s, %s)", 
                    (title, content, int(readtimes), int(praises), updatetime))
        conn.commit()
        return cur.lastrowid
    else:
        return cur.fetchone()[0]

def storeLink(shr_Id, note_Id):
    #insert link if not existed shr_Id and note_Id  - int
    cur.execute("SELECT * FROM links WHERE shr_Id = %s AND note_Id = %s", 
                (int(shr_Id), int(note_Id)) )
    if cur.rowcount == 0:
        cur.execute("INSERT INTO links (shr_Id, note_Id) VALUES (%s, %s)", 
                    (int(shr_Id), int(note_Id)) )
        conn.commit()
        return cur.lastrowid
    else:
        return cur.fetchone()[0]
##################################################
def readnote(noteurl):
    driver = webdriver.PhantomJS(executable_path="D:/Internet-IE/phantomjs-2.1.1-windows/bin/phantomjs")
    driver.get(noteurl)
    wait = WebDriverWait(driver=driver,timeout=10)
    wait.until(EC.presence_of_element_located((By.ID, "main-container")))
    
    pageSource = driver.page_source
    bsObj = BeautifulSoup(pageSource,"html.parser")
    
    title = bsObj.find("div",{"class":"note-name-container"}).attrs["title"]
    
    sharer = bsObj.find("div",{"class":"sharer"})
    shr_photo = sharer.find("img",{"class":"user-portrait"}).attrs["src"]
    shr_name = sharer.find("p",{"class":"user-name"}).attrs["title"]
    shrId = storeShr(shr_name, shr_photo)
    
    readtimes = bsObj.find("div",{"class":"read-times-container"}).find("span",{"class":"read-text"}).find("span").get_text()
    praisetimes = bsObj.find("div",{"class":"praise"}).find("span",{"class":"praise-text"}).find("span").get_text()
    updatetime = bsObj.find("div",{"class":"modify-time-container"}).find("span").get_text()
    
    #wait until the iframe is loaded
    iwait = WebDriverWait(driver=driver,timeout=10)
    iwait.until(EC.presence_of_element_located((By.ID, "content-body")))
    driver.switch_to.frame("content-body")
    #if it switch successfully, you can think your 'driver' are in a new html now.
    ipageSource = driver.page_source
    ibsObj = BeautifulSoup(ipageSource,"html.parser")
    content = ibsObj.find("div",{"id":"noteIFrameContent"})
    
    noteId = storeNote(title, content, readtimes, praisetimes, updatetime)
    storeLink(shrId, noteId)
    driver.close()