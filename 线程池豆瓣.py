import requests,time
from bs4 import BeautifulSoup
import multiprocessing
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
session=requests.session()
session.headers=headers
def get_link(html):
    print('获取书的父进程为：{}'.format(multiprocessing.current_process().pid))
    soup = BeautifulSoup(html.text,'lxml')
    title = soup.select_one('#wrapper h1 span').text
    print(title)


def get_html(url):
    print('html当前进程为{}'.format(multiprocessing.current_process().pid))
    html = requests.get(url, headers = headers)
    threadpools = ThreadPoolExecutor(max_workers=2)
    soup = BeautifulSoup(html.text, 'lxml')
    urls = soup.select('li.subject-item h2 a')
    for url in urls:
        link = url['href']
        html = requests.get(link, headers=headers)
        if html.status_code==200:
            threadpools.submit(get_link, html)
        else:
            print('Error')

if __name__ == '__main__':
    urls=[
        'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4',
        'https://book.douban.com/tag/%E5%8E%86%E5%8F%B2',
        'https://book.douban.com/tag/%E6%8E%A8%E7%90%86'
    ]
    s=time.time()
    with ProcessPoolExecutor(max_workers=3)as executor:
        futures=[executor.submit(get_html,url)for url in urls]
    print('花费时间:',time.time()-s)

