import requests,re,csv
from lxml import etree
from urllib import parse
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
# from db import sess,House

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'cookie': 'global_cookie=575l3uxu1hoxgn2rbo2sckg5k1tk9v3itfu; Integrateactivity=notincludemc; lastscanpage=0; integratecover=1; global_wapandm_cookie=jobvj46nn0gk3uyuv49uoxop24skbt3s7m6; keyWord_recenthousegz=%5b%7b%22name%22%3a%22%e5%a2%9e%e5%9f%8e%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a080%2f%22%2c%22sort%22%3a1%7d%2c%7b%22name%22%3a%22%e5%a4%a9%e6%b2%b3%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a073%2f%22%2c%22sort%22%3a1%7d%2c%7b%22name%22%3a%22%e6%b5%b7%e7%8f%a0%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a074%2f%22%2c%22sort%22%3a1%7d%5d; city=gz; __utma=147393320.1505781782.1588754777.1593008641.1593014523.6; __utmc=147393320; __utmz=147393320.1593014523.6.6.utmcsr=gz.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmt_t3=1; __utmt_t4=1; new_search_uid=4b5ac99de52a161ccba018e1a6abd8fb; ASP.NET_SessionId=crp23ujlhlbbptbzmpwiv4jk; g_sourcepage=zf_fy%5Elb_pc; Captcha=7937313975624942325361465251562F38476B6F6C69707A6276302F38554E7267626A4B51416B34637A4A5771337854464C4C6A724B434F476B3548695A62695344396946666973414F453D; unique_cookie=U_vof7idjgqdb25cb4fo5hc8ywk10kbtjpdzg*6; __utmb=147393320.18.10.1593014523',
    'referer': 'https://gz.zu.fang.com/house-a074/',
    'Host': 'gz.zu.fang.com'
}
session=requests.session()
session.headers=headers

def get_number(text):
    number=re.compile('\d+')
    return number.findall(text)[0]

def get_page(html):
    soup=etree.HTML(html.text)
    pages=soup.xpath('//div[@class="fanye"]/'
                     'span[@class="txt"]/text()')
    number=get_number(pages[0])
    if number:
        return int(number)
    return None

def get_house_data(url,*args):#二次跳转链接获取
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Cookie': 'global_cookie=575l3uxu1hoxgn2rbo2sckg5k1tk9v3itfu; Integrateactivity=notincludemc; lastscanpage=0; integratecover=1; global_wapandm_cookie=jobvj46nn0gk3uyuv49uoxop24skbt3s7m6; keyWord_recenthousegz=%5b%7b%22name%22%3a%22%e5%a2%9e%e5%9f%8e%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a080%2f%22%2c%22sort%22%3a1%7d%2c%7b%22name%22%3a%22%e5%a4%a9%e6%b2%b3%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a073%2f%22%2c%22sort%22%3a1%7d%2c%7b%22name%22%3a%22%e6%b5%b7%e7%8f%a0%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a074%2f%22%2c%22sort%22%3a1%7d%5d; city=gz; new_search_uid=4b5ac99de52a161ccba018e1a6abd8fb; __utma=147393320.1505781782.1588754777.1593061034.1593148076.9; __utmz=147393320.1593148076.9.9.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-14bf8046a68f9c4b39/redirect; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmc=147393320; ASP.NET_SessionId=trwrckjq5qql3cckpbdmwc2f; Rent_StatLog=8d1324af-1745-4da3-b60a-6690d9e6be4e; Captcha=5548624D4F534',
        # 'referer': 'https://zu.fang.com/house=ao80',
        'Connection': 'keep-alive'
    }
    local_url = re.compile('location.href="(.*?)"')
    session = requests.session()
    session.headers = headers

    url = 'http://search.fang.com/captcha-8c163b072c0f9c4e02/redirect?h='+url
    html = session.get(url)
    next_url = local_url.findall(html.text)[-1]

    html = session.get(next_url)
    second_url = local_url.findall(html.text)[-1]
    html = session.get(second_url)
    soup = etree.HTML(html.text)
    result = soup.xpath('//div[contains(@class,"fyms_con")]/text()')
    if result:
        result = '|'.join(result)
    else:
        result = '暂无房源'
    print('详细页数据:', result)


    # s=sess()
    # try:
    #     house=House(block=args[0],
    #                 title=args[2],
    #             rent=args[1],
    #                 data=result)
    #     s.add(house)
    #     s.commit()
    #     print('commit')
    # except Exception as e:
    #     print('rollback',e)
    #     s.rollback()

def get_data_next(url):
    html=session.get(url,headers=headers)
    soup=etree.HTML(html.text)
    dls=soup.xpath('//div[@class="houseList"]/dl')
    block=soup.xpath('//span[@class="selestfinds"]/a/text()')#当前找房条件
    rfss=soup.xpath('//input[@id="baidid"]/@value')[0]
    for dl in dls:
        try:
            title=dl.xpath('dd/p/a/text()')[0]
            rent=dl.xpath('dd/div/p/span[@class="price"]/text()')[0]
            href=parse.urljoin('https://gz.zu.fang.com',dl.xpath('dd/p/a/@href')[0])
            print('列表页数据:',title,rent,href,rfss)
            get_house_data(href,block,rent,title,rfss)
        except IndexError as e:
            print('dl error',e)

def get_data(html):#翻页
    pages=get_page(html)
    if not pages:
        pages=1
    urls=['https://gz.zu.fang.com/house-a074/i3%d/'%i
          for i in range(1,pages+1)]
    with ThreadPoolExecutor(max_workers=2)as t:
        for url in urls:
            print('爬取页 %s'%url)
            t.submit(get_data_next,url)

def get_index(url):
    html=session.get(url,headers=headers)
    if html.status_code==200:
        get_data(html)
    else:
        print('请求页面{}出错',format(url))

def main():
    urls=['https://gz.zu.fang.com/house-a0{}/'.format(i)for i in range(70,85)]
    with ThreadPoolExecutor(max_workers=2)as p:
        for url in urls:
            p.submit(get_index,url)

if __name__ == '__main__':
    main()
    session.close()

