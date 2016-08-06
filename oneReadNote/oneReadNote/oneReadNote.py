from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pymysql

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
        return cur.lastrowid
        #get the 'id' attr
    else:
        return cur.fetchone()[0]
        #get the 'first' attr - 'id' attr

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
#################################################

#pageurl = "http://note.youdao.com/share/?id=793e201fcd098517ddba2d0af9b2eeb9&type=notebook#/5C00F9977C754A19BCBD8EFE088CE416"
pageurl = "http://note.youdao.com/share/?id=f0328c20102b73dad0a1d7c36c839b66&type=notebook#/c6a2c2136c28c88cf06bbfedc94efbbf"
driver = webdriver.PhantomJS(executable_path="D:/Internet-IE/phantomjs-2.1.1-windows/bin/phantomjs")
driver.get(pageurl) 

#time.sleep(2) #wait to make sure the page has entirely loaded
wait = WebDriverWait(driver=driver,timeout=10)
wait.until(EC.presence_of_element_located((By.ID, "main-container")))

pageSource = driver.page_source
bsObj = BeautifulSoup(pageSource,"html.parser")

title = bsObj.find("div",{"class":"note-name-container"}).attrs["title"]

sharer = bsObj.find("div",{"class":"sharer"})
shr_photo = sharer.find("img",{"class":"user-portrait"}).attrs["src"]
#src="/yws/api/image/normal/1458615342535?userId=weixinobU7VjgVJUk9NlDKmI3LbSU2uAg4"
#http://note.youdao.com/yws/api/image/normal/1458615342535?userId=weixinobU7VjgVJUk9NlDKmI3LbSU2uAg4
shr_name = sharer.find("p",{"class":"user-name"}).attrs["title"]
shrId = storeShr(shr_name, shr_photo)

#readtimes = bsObj.find("div",{"class":"read-times-container"}).find("span").find("span").get_text()
readtimes = bsObj.find("div",{"class":"read-times-container"}).find("span",{"class":"read-text"}).find("span").get_text()
praisetimes = bsObj.find("div",{"class":"praise"}).find("span",{"class":"praise-text"}).find("span").get_text()
updatetime = bsObj.find("div",{"class":"modify-time-container"}).find("span").get_text()

#content = bsObj.find("iframe",{"id":"content-body"}) #print(content) #there would be nothing to present

#wait until the iframe is loaded
iwait = WebDriverWait(driver=driver,timeout=10)
iwait.until(EC.presence_of_element_located((By.ID, "content-body")))
driver.switch_to.frame("content-body")
#if it switch successfully, you can think your 'driver' are in a new html now.
ipageSource = driver.page_source
ibsObj = BeautifulSoup(ipageSource,"html.parser")
content = ibsObj.find("div",{"id":"noteIFrameContent"})

#Non-pretty printing - bsObj to html string - raw
noteId = storeNote(title, str(content), readtimes, praisetimes, updatetime)
storeLink(shrId, noteId)

driver.close()