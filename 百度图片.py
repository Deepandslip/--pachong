from urllib import parse
import requests,os,time
from uuid import uuid4
import threading
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor

headers={
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36',
    'Cookie': 'BIDUPSID=B780A4F2EDF21782883E40AD1FA469FD; PSTM=1583580666; BAIDUID=B780A4F2EDF21782FA163AB13E037500:FG=1; BDUSS=W5COVgzNUR4TTdkcXVwMG51bEZRSk03WnJYTm5rNWZ1WkhoN3FaT29za3k5OEJlSVFBQUFBJCQAAAAAAAAAAAEAAAA9Qg6SamlhbnpoaVJvY2sAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADJqmV4yapleS; IMG_BR_CLK=YES; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=31729_1428_31670_21078_31069_32046_31779_31715_30824_31845_26350; delPer=0; PSINO=6; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; userFrom=www.baidu.com; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; H_WISE_SIDS=148867_147681_146733_138426_145988_147527_147913_147443_149280_145608_148661_146785_148346_143646_148752_148762_110085; ysm=10259; IMG_WH=1318_94; BDRCVFR[5GQZCjFg8mf]=mk3SLVN4HKm; __bsi=7679250557499755193_00_10_R_R_6_0303_c02f_Y',
    'Referer': 'https://m.baidu.com/sf/vsearch?pd=image_content&word=%E7%99%BE%E5%BA%A6%E5%9B%BE%E7%89%87&tn=vsearch&atn=page'
}

def download(url):
    filename='img'
    try:
        if not os.path.exists(filename):
            os.mkdir(filename)
        img=requests.get(url,headers=headers)
        with open('img/{}.jpg'.format(uuid4()),'wb')as f:
            f.write(img.content)
    except:
        pass

def get_baidu(url):
    html=requests.get(url,headers=headers)
    # threadpools=ThreadPoolExecutor(max_workers=10)
    try:
        content=html.json()['linkData']
        for c in content[:-1]:
            print(c['hoverUrl'])
            # download(c['hoverUrl'])
            # threadpools.submit(download,url)#线程池
            t=threading.Thread(target=download,args=(c['hoverUrl'],))#多线程
            t.start()

    except:
        pass

def main(keyword,i):
    url='https://m.baidu.com/sf/vsearch/image/search/wisesearchresult?tn=wisejsonala&ie=utf-8&fromsf=1&word={}&pn={}&rn=30&gsm=&prefresh=undefined&searchtype=0&fromfilter=0&tpltype=0'.format(keyword,i)
    get_baidu(url)

if __name__ == '__main__':
    keyword=input('请输入<<')
    s=time.time()
    # with ProcessPoolExecutor(max_workers=5)as Pool:
    for i in range(30,500,30):
        main(keyword,i)
        # Pool.submit(main,keyword=keyword,i=i)
    print(time.time()-s)#打印的时间

