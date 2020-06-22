import requests,time
from bs4 import  BeautifulSoup
from urllib import parse
from lxml import etree
import os
import asyncio,aiohttp#异步包
from douban11 import Book,sess
headers={
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36',
    'Cookie': 'll="108306"; bid=W3FrQRk6gJI; __gads=ID=8d048bd16d4dded7:T=1584347241:S=ALNI_MbW7jbpkqCjAt5j9boZ2RggGx309A; _vwo_uuid_v2=D3D44C30141731E2F234E4DA48D679E43|5a207e1a5493e1c1a1a527f18d07bd76; douban-fav-remind=1; gr_user_id=711974e2-7a43-4c9d-959e-a868253e3918; __yadk_uid=ZR2BsRNdbRjvLgEMWPRsy2al89j9ZAsY; __utmz=30149280.1590151689.11.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=30149280; __utma=30149280.1277304803.1584347234.1590123791.1590151689.11; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=46e6d361-c7e1-4904-b5f3-f41caf89248e; gr_cs1_46e6d361-c7e1-4904-b5f3-f41caf89248e=user_id%3A0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1590151696%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; __utmc=81379588; ap_v=0,6.0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_46e6d361-c7e1-4904-b5f3-f41caf89248e=true; __utma=81379588.698459084.1589337065.1590151696.1590152100.7; __utmz=81379588.1590152100.7.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; viewed="1858513_10549733_10546125_26880667_19986936_5952531_26708119_25711796_2161249"; _pk_id.100001.3ac3=763adcae36c7a7bb.1589337065.6.1590152181.1590123797.; __utmb=30149280.23.9.1590152060192; __utmb=81379588.8.10.1590152100'
}

async def get_books(url):
    async with aiohttp.ClientSession(headers=headers)as session:
        async with session.get(url)as resp:
            if resp.status==200:
                text=await resp.text()
            else:
                print('获取失败')
                return None
    soup=BeautifulSoup(text,'lxml')
    books=soup.select('li.subject-item')
    for r in books:
        try:
            title=r.select_one('.info h2 a').text.strip().replace('\n','')
            info=r.select_one('.info  div.pub').text.strip().replace('\n','')
            star=r.select_one('.rating_nums').text.strip().replace('\n','')
            pl = r.select_one('.pl').text.strip().replace('\n', '')
            introduce=r.select_one('.info p').text.strip().replace('\n', '')
            href=r.select_one('.info h2 a')['href']
            print(title,info,star,pl,href)
            print(introduce)
            print('_'*40)

            book_data=Book(
                title=title,
                info=info,
                star=star,
                pl=pl,
                introduce=introduce,
            )
            sess.add(book_data)
            sess.commit()
        except Exception as e:
            print(e)
            sess.rollback()
if __name__ == '__main__':
    keyword=parse.quote(input('请输入要爬取的类型:'))
    num=eval(input('请输入要爬取的页数：'))
    s=time.time()
    for i in range(0,num):
        url=f'https://book.douban.com/tag/{keyword}?start={i*20}&type=T'
    loop=asyncio.get_event_loop()
    loop.run_until_complete(get_books(url))
    print('花费时间：',time.time()-s)


