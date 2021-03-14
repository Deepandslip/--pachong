import requests
from bs4 import BeautifulSoup
from copy import copy
import time,threading
from openpyxl import Workbook
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

weibo_hot_list=[]

def get_weibo_hot(index):
    global weibo_hot_list
    index+=1
    if not weibo_hot_list:
        base_url='https://s.weibo.com/top/summary'
        html=requests.get(base_url,headers=headers)
        soup=BeautifulSoup(html.text,'lxml')
        today_hot=soup.select('#pl_top_realtimehot tr')[1:]
        weibo_hot_list=copy(today_hot)
    item=weibo_hot_list[index]
    title=item.select('.td-02 a')[0].text.strip()
    hot_count=int(item.select('.td-02 span')[0].text.strip())
    url=item.select('.td-02 a')[0].get('href')
    #with ThreadPoolExecutor(max_workers=2)as t:
    if 'c' in url:
        url=item.select('.td-02 a')[0].get('href_to')#定位href
    url=f'https://s.weibo.com{url}'#附上href

    html=requests.get(url,headers=headers)
    soup=BeautifulSoup(html.text,'lxml')
    author=soup.select('.card-wrap .content .info .name')[0].text.strip()
    content=soup.select('.card-wrap .content .txt')[0].text.strip()
    return [hot_count,title,author,content,url]
    t=threading.Thread(target=get_weibo_hot)
    t.start()
    #t.submit(get_weibo_hot,index)

we=Workbook()
sheet=we.active

for i in range(20):
    row=get_weibo_hot(i)
    sheet.append(row)
    print(row)
    time.sleep(0.5)


we.save(filename='微博.xlsx')



