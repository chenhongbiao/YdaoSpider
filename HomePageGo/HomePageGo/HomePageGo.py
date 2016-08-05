from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

#take the (nod - int) jump to that page
#up to six button at the list - left 3 and right 2
#next page = current page number + 1
def jumptopage(nod):
    driver = webdriver.PhantomJS(executable_path="D:/Internet-IE/phantomjs-2.1.1-windows/bin/phantomjs")
    driver.get("http://note.youdao.com/dushu/web/index.html") 
    
    wait = WebDriverWait(driver=driver,timeout=10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "currentPage")))
    
    driver.find_element_by_link_text(str(nod)).click()

    wait = WebDriverWait(driver=driver,timeout=10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "currentPage")))

    print(driver.find_element_by_class_name("note-item").text)
    #test whether the jump is successful
    driver.close()
    
jumptopage(2)
