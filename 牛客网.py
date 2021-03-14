import requests
from lxml import etree
import re
from bs4 import BeautifulSoup
import random
import time,os
import threading
from retry import retry


class NiuKe(object):
    def __init__(self):
        self.url='https://www.nowcoder.com/discuss/tag/{}?type=2&page={}'
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
        self.prefix='https://www.nowcoder.com'
        self.origin_url='https://www.nowcoder.com/discuss/tags?type=2'


    def get_enterprise(self):
        r=requests.get(self.origin_url,headers=self.headers)
        tree=etree.HTML(r.text)
        enterprise=tree.xpath('//div[@data-nav="企业"]/ul[@class="discuss-tags-mod"]/li[6]/a/@data-href')
        enterprise_name=tree.xpath('//div[@data-nav="企业"]/ul[@class="discuss-tags-mod"]/li[6]/a/span/text()')
        enterprise_num=tree.xpath('//div[@data-nav="企业"]/ul[@class="discuss-tags-mod"]/li[6]/span[@class="discuss-tag-num"]/text()')
        enterprise=[i[13:-7]for i in enterprise]
        num=[int(i[:-1])for i in enterprise_num]
        return enterprise,enterprise_name,num


    def get_href(self,enterprise,page):
        title_new=[]
        r=requests.get(self.url.format(enterprise,page),headers=self.headers)
        tree=etree.HTML(r.text)
        hrefs=tree.xpath('//div[@class="discuss-main clearfix"]/a[1]/@href')
        titles=tree.xpath('//div[@class="discuss-main clearfix"]/a[1]/text()')
        hrefs=[self.prefix+href for href in hrefs]
        for title in titles:
            if title !='\n':
                title_new.append(title.replace('\n','').replace("[","").replace("]","").replace("/","").replace("|"," ").replace("*","").replace("?","").replace("\\",",").replace(":",",").replace("<","").replace(">",""))

        return hrefs,title_new


    def get_article(self,enterprise_name,hrefs,titles):
        for i in range(len(hrefs)):
            if os.path.exists('{}/{}.txt'.format(enterprise_name,titles[i])):
                pass
            else:
                r=requests.get(hrefs[i],headers=self.headers)
                tree=etree.HTML(r.text)
                text=tree.xpath('string(//div[@class="post-topic-des nc-post-content"])')
                with open('{}/{}.txt'.format(enterprise_name,titles[i]),'w',encoding='utf-8')as f:
                    f.write(text.replace("  ",'\n'))


    @retry(tries=5,delay=0.5)
    def main(self,enterprise,page,enterprise_name):
        hrefs,titles=self.get_href(enterprise,page)
        self.get_article(enterprise_name,hrefs,titles)




if __name__ == '__main__':
    crwal=NiuKe()
    enterprise,enterprise_name,num=crwal.get_enterprise()
    for j in range(100):
        pages=int(num[j]/30)+2 if int(num[j]/30)<45 else 46
        if os.path.exists(enterprise_name[j]):
            pass
        else:
            os.mkdir(enterprise_name[j])
        tasks=[]
        for page in range(1,pages):
            print('开始抓取{}第{}页面试...'.format(enterprise_name[j],page))
            task=threading.Thread(target=crwal.main,args=(enterprise[j],page,enterprise_name[j],))
            tasks.append(task)
            task.start()

        for _ in tasks:
            _.join()
        print('成功抓取{}所以面试...'.format(enterprise_name[j]))
        print('-'*30)

