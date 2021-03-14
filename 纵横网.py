import asyncio
import aiohttp
import time,json
import re
import random
from lxml import etree
from fake_useragent import UserAgent
import pymysql


class ZongHeng(object):
    def __init__(self,page):
        self.url='http://book.zongheng.com/store/c6/c0/b0/u0/p{}/v9/s9/t0/u0/i1/ALL.html'
        self.num=1
        self.page=page
        self.useragent=UserAgent()
        self.connect=pymysql.connect(host='localhost',port=3306,user='root',password='676725',db='test')
        self.cur=self.connect.cursor()
        self.queue=asyncio.Queue()
        self.sem=asyncio.Semaphore(2)# 控制并发量

    async def geturl(self,url):
        headers={
            'User-Agent':self.useragent.random
        }
        async with self.sem:
            async with aiohttp.ClientSession() as session:
                async with await session.get(url,headers=headers)as req:
                    res= await req.read()
                    html=etree.HTML(res)
                    urls=html.xpath('//div[@class="store_collist"]//div[@class="bookimg"]/a/@href')
                    title=html.xpath('//div[@class="bookinfo"]/div[@class="bookname"]/a/text()')
                    authors=html.xpath('//div[@class="bookinfo"]/div[@class="bookilnk"]/a[1]/text()')
                    author_url=html.xpath('//div[@class="bookinfo"]/div[@class="bookilnk"]/a[1]/text()')
                    categories=html.xpath('//div[@class="bookinfo"]/div[@class="bookilnk"]/a[2]/text()')
                    category_urls=html.xpath('//div[@class="bookinfo"]/div[@class="bookilnk"]/a[2]/@href')
                    status=html.xpath('//div[@class="bookinfo"]/div[@class="bookilnk"]/span[1]/text()')
                    update_times=html.xpath('//div[@class="bookinfo"]/div[@class="bookilnk"]/span[1]/text()')
                    intros=html.xpath('//div[@class="bookinfo"]/div[@class="bookintro"]/text()')
                    book_update=html.xpath('//div[@class="bookinfo"]/div[@class="bookupdate"]/a/text()')
                    update_url=html.xpath('//div[@class="bookinfo"]/div[@class="bookupdate"]/a/@href')
                    all_contents=zip(urls,title,authors,author_url,categories,category_urls,status,update_times,intros,book_update,update_url)
                    for url,title,author,author_url,category,category_url,status,update_times,intros,book_update,update_url in all_contents:
                        item=dict()
                        item['url']=url
                        item['title']=title
                        item['author']=author
                        item['authors_url']=author_url
                        item['category']=category
                        item['category_url']=category_url
                        item['status']=self.status_strip(status)
                        item['update_times']=self.update_time_re(update_times)
                        item['intros']=intros
                        item['book_update']=book_update
                        item['update_url']=update_url
                        print(item)
                        await self.get_detail(item)
                        #await self.save_mysql(item)


    async def get_detail(self,contents):#进一步获取
        async with self.sem:
            async with aiohttp.ClientSession() as session1:
                async with await session1.get(contents['url'],headers={'User-Agent':self.useragent.random})as rep:
                    res = await rep.read()
                    html_com=etree.HTML(res)
                    number=html_com.xpath('//div[@class="book-info"]/div[@class="nums"]/span[1]/i/text()')
                    all_recommend=html_com.xpath('//div[@class="book-info"]/div[@class="nums"]/span[2]/i/text()')
                    click_num=html_com.xpath('//div[@class="book-info"]/div[@class="nums"]/span[3]/i/text()')
                    week_recommend=html_com.xpath('//div[@class="book-info"]/div[@class="nums"]/span[4]/i/text()')

                    contents['number']=self.join_str(number)
                    contents['all_recommend']=self.join_str(all_recommend)
                    contents['click_num']=self.join_str(click_num)
                    contents['week_recommend']=self.join_str(week_recommend)
                    contents['Spider_time']=time.strftime('%Y-%m-%d %H:%M:S',time.localtime(time.time()))
                    print(contents)

                    await self.save_json(contents)

    @staticmethod
    async def save_json(item):
        with open('zongheng.json','a',encoding='utf-8') as file:
            file.write(json.dumps(item,ensure_ascii=False)+'\n')

    # async def save_mysql(self,item):
    #     self.cur.execute(
    #         """insert into zongheng(title,url,author,category) values (%s,%s,%s,%s)""",
    #         (
    #             item['title'],
    #             item['url'],
    #             item['author'],
    #             item['category']
    #         )
    #     )
    #     self.connect.commit()


    @staticmethod
    def status_strip(in_content):
        return in_content.strip()

    @staticmethod
    def update_time_re(in_content):
        de_strip = in_content.strip()
        try:
            res=re.findall(r'(\d+\-\d+\s+\d+\:\d+)',de_strip)[0]
        except Exception as e:
            return de_strip
        else:
            return res

    @staticmethod
    def join_str(in_join):
        """提取书籍中详细的字数等，将'万'转化位10000"""
        join_res = ''.join(in_join)
        if join_res:
            try:
                # 匹配字符中是否有万
                num_re = re.findall(r'(.*?)万', join_res)[0]
            except:
                # 没有万则直接转化原数字
                num = eval(join_res)
            else:
                # 有万的话转化位10000
                num = eval(num_re) * 10000
        else:
            num = 0
        return int(num)

    async def put_url(self):
        #将url地址添加到队列当中
        for i in range(1,self.page+1):
            await self.queue.put(self.url.format(i))

    async def get_url(self):
        while not self.queue.empty():
            await self.geturl(await self.queue.get())

    def main(self):
        loop=asyncio.get_event_loop()

        tasks=[
            loop.create_task(self.put_url()),
            loop.create_task(self.get_url())
        ]
        loop.run_until_complete(asyncio.wait(tasks))

if __name__ == '__main__':
    zh=ZongHeng(2)
    zh.main()









