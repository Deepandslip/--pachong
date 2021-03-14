import requests
from bs4 import BeautifulSoup
import time
from urllib import parse
import threading
import multiprocessing
headers={
    'Request': 'https://www.kuaidaili.com/free/inha/1/',
    'Cookie': '_ga=GA1.2.1916395203.1584794209; channelid=0; sid=1587881416997937; _gid=GA1.2.950360447.1587881420; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1587881420; _gat=1; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1587881489',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Mobile Safari/537.36'
}

def get_ip(url):
    html=requests.get(url,headers=headers)
    if html.status_code==200:
        print('正在爬取...')
        time.sleep(5)
        parse_html(html.text)


    else:
        print('Error',url)

def parse_html(text):
    soup=BeautifulSoup(text,'lxml')
    ips=soup.select('div tbody tr')
    for line in ips:
        ip=line.select_one('td').text
        port=line.select('td')[1].text
        print(f'IP:{ip},Port:{port}')
        address=f'http://{ip}:{port}'
        proxies={
            'http':address,
            'http':address

        }
        #verify_ip(proxies)
        t=multiprocessing.Process(target=verify_ip,args=(proxies,))
        t.start()

def verify_ip(proxies):
    try:
        html=requests.get('http://www.baidu.com',proxies=proxies,timeout=3)
        print(f'[SUCCESS]可用代理:{proxies}')
        save_ip(proxies)
    except:
        print(f'[ERROR]代理不可用:{proxies}')

def save_ip(proxies):
    with open('C:\\Users\DEEP\Desktop\ip_text.txt','a+') as f:
        f.write(str(proxies)+'\n')
        print('\n[SUCCESS]代理已经写入文本！！！')

def read_text():
    with open('C:\\Users\DEEP\Desktop\ip_text.txt','r',encoding='utf-8') as f:
        contents=f.readlines()
        for content in contents:
            try:
                html=requests.get('http://www.baidu.com',proxies=eval(content),timeout=3)
                print('[SUCCESS]有效代理',content)
            except:
                print('[ERROR]失败代理',content)

if __name__ == '__main__':
    num=eval(input('请输入爬取页数:'))
    for i in range(1,num+1):
        url=f'https://www.kuaidaili.com/free/inha/{i}/'
        read_text()
        get_ip(url)


