from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

driver = webdriver.PhantomJS(executable_path="D:/Internet-IE/phantomjs-2.1.1-windows/bin/phantomjs")
driver.get("http://note.youdao.com/dushu/web/index.html") 

#time.sleep(2) #wait to make sure the page has entirely loaded
wait = WebDriverWait(driver=driver,timeout=10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "note-item")))

pageSource = driver.page_source
bsObj = BeautifulSoup(pageSource,"html.parser")
#<span id="total-pages">84</span>
totalpags = int ( bsObj.find("span",{"id":"total-pages"}).get_text() )
#Collects all internal notebook or note links in home page - the rank hot part
allbookLinks = set()
allnoteLinks = set()

#ul id=main-list  li class="note-item"
for noteItem in bsObj.find("ul",{"id":"main-list"}).findAll("li",{"class":"note-item"}):
    noteItemLink = noteItem.find("a").attrs["href"]
    Linkparts = urlparse(noteItemLink).query.replace("id=", "").split("&")
    if(Linkparts[1] == "type=note"):
        allnoteLinks.add("http://note.youdao.com/share/?id="+Linkparts[0]+"&type=note")
    elif(Linkparts[1]=="type=notebook"):
        allbookLinks.add("http://note.youdao.com/share/?id="+Linkparts[0]+"&type=notebook")

for booklink in allbookLinks:
    print(booklink)
for notelink in allnoteLinks:
    print(notelink)

driver.close()