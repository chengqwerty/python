# _*_ coding: utf-8 _*_

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

browserPath = "D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe"
web_url = "https://unsplash.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

r_page = requests.get(web_url, headers = headers)
driver = webdriver.PhantomJS(executable_path=browserPath)
driver.get(web_url)
print(driver.page_source)
bsObj = BeautifulSoup(driver.page_source, 'lxml')
bsObj.find_all('a', class_='')