import os
import threading
import re
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver

browserPath = "D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe"
homepage = "https://mm.taobao.com/search_tstar_model.htm?"
outputDir = "D:\\photo\\"

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        print("创建文件夹", path)
        os.makedirs(path)
    else:
        print("文件夹", path, "已经存在")

def getImgs(url, path):
    driver = webdriver.PhantomJS(executable_path=browserPath)
    driver.get(url)
    print("Opening...")
    bsObj = BeautifulSoup(driver.page_source, 'lxml')
    #获得个人页面上的艺术照
    imgs = bsObj.find_all("img", {"src": re.compile(".*\.jpg")})
    for i, img in enumerate(imgs[1:]):
        try:
            html = urlopen("https:" + img["src"])
            data = html.read()
            fileName = "{}/{}.jpg".format(path, i + 1)
            print("Loading...", fileName)
            with open(fileName, 'wb') as f:
                f.write(data)
        except Exception:
            print(" Address Error!")
    driver.close()

def main():
    driver = webdriver.PhantomJS(executable_path=browserPath)
    driver.get(homepage)
    bsObj = BeautifulSoup(driver.page_source, 'lxml')
    girlsList = driver.find_element_by_id("J_GirlsList").text.split('\n')
    print(girlsList)
    girlsUrl = bsObj.find_all("a", {"href": re.compile("\/\/.*\.htm\?(userId=)\d*")})
    print(girlsUrl)
    imagesUrl = re.findall('\/\/gtd\.alicdn\.com\/sns_logo.*\.jpg', driver.page_source)
    print(imagesUrl)

    #所有妹子的名字和地点
    girlsNL = girlsList[::3]
    #所有妹子的身高体重
    girlsHW = girlsList[1::3]
    #所有妹子的个人主页地址
    girlsHURL = [('https:' + i['href']) for i in girlsUrl]
    #所有妹子的封面图片地址
    girlsPhotoURL = [('https:' + i) for i in imagesUrl]

    girlsInfo = zip(girlsNL, girlsHW, girlsHURL, girlsPhotoURL)

    for girlNL, girlHW, girlHURL, girlCover in girlsInfo:
        print("Girl :", girlNL, girlHW)
        mkdir(outputDir + girlNL)
        print("saving...")
        data = urlopen(girlCover).read()
        with open(outputDir + girlNL + '/cover.jpg', 'wb') as f:
            f.write(data)
        print("Loading Cover... ")
        getImgs(girlHURL, outputDir + girlNL)

if __name__ == '__main__':
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    main()