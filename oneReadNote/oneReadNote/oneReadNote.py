from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver = webdriver.PhantomJS(executable_path="D:/Internet-IE/phantomjs-2.1.1-windows/bin/phantomjs")
driver.get("http://note.youdao.com/share/?id=9dea9c169bcfbd6a64d2db2fe67b295b&type=note") 

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
print(content.get_text())

driver.close()