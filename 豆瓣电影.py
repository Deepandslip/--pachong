#爬取前10部电影
import time,sys,codecs,urllib,csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def crawl(url):
    driver.get(url)
    print(u'豆瓣电影250: 序号 \t影片名\t 评分 \t评价人数')
    infofile.write(u"豆瓣电影250: 序号 \t影片名\t 评分 \t评价人数\r\n")
    print(u'爬取信息如下:\n')
    content=driver.find_elements_by_xpath('//div[@class="item"]')
    for tag in content:
        print(tag.text)
        infofile.write(tag.text+'\r\n')
        print('')




if __name__ == '__main__':
    driver=webdriver.Chrome('C:\\Users\DEEP\Desktop\chromedriver.exe')

    infofile=codecs.open('douban.movie.csv','a',encoding='utf-8')#获取源码
    url='http://movie.douban.com/top250?format=text'
    i=0
    while i<1:
        print(u'页码',i+1)
        num=i*25#每次显示25部 URL序号按25增加
        url='https://movie.douban.com/top250?start'+str(num)+'&filter='
        crawl(url)
        infofile.write('\r\n\r\n\r\n')
        i = i+1
    infofile.close()
