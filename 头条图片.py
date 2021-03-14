import requests
from urllib.parse import urlencode
import os,re
from hashlib import md5
from multiprocessing.pool import Pool
import threading

def get_page(offset):
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'cookie': 'csrftoken=3f75abdd42e29ce47423d5fd1d546297; tt_webid=6853781660141602317; ttcid=2fdba7ca6c59466f83d0839cdadf238261; SLARDAR_WEB_ID=265ddd7b-de68-41cb-8516-9347bd8cf698; __tasessionId=32nlm1zwk1596006515587; s_v_web_id=kd712lmo_KWX5kH4Q_3vC0_4epC_Bbxm_EyAVIBFmrRV4; tt_scid=-klz.yVYMmKXgPJObhfzzIPzMRFdNXdDi7fxXskSCdaGkqBTVQrtuNBHa1ONT2Eh8cb1',
        'x-requested-with': 'XMLHttpRequest'
    }
    params={
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '漫威',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    base_url='https://www.toutiao.com/api/search/content/?'
    url=base_url+urlencode(params)
    try:
        r = requests.get(url,headers=headers)
        if r.status_code==200:
            return r.json()
    except:
        return None

def get_image(json):
    if json.get('data'):
        data=json.get('data')
        for item in data:
            if item.get('title') is None:
                continue
            title=re.sub('[\t\\\|]','',item.get('title'))
            images=item.get('image_list')
            try:
                for image in images:
                    img=re.sub("list.*?pgc-image","large/pgc-image",image.get('url'))
                    yield {
                        'image':img,
                        'title':title
                    }
            except:
                pass

def save_image(item):
    img_path='img'+os.path.sep+item.get('title')#保存连接标题
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    r=requests.get(item.get('image'))
    file_path=img_path+os.path.sep+'{file_name}.{file_suffix}'.format(
        file_name=md5(r.content).hexdigest(),
        file_suffix='jpg'
    )
    if not os.path.exists(file_path):
        with open(file_path,'wb')as f:
            f.write(r.content)
        print('Downloading image path{}'.format(file_path))
    else:
        print('Already Downloaded')


def main(offset):
    json=get_page(offset)
    for item in get_image(json):
        try:
            save_image(item)
        except:
            print('下载图片失败...')


if __name__ == '__main__':
    groups=([x * 20 for x  in range(10)])
    """
    pool.map(main,groups)
    pool.close()
    pool.join()
    
    """


    tasks=[]

    for group in groups:
        task=threading.Thread(target=main,args=(group,))
        tasks.append(task)
        task.start()

    for i in tasks:
        i.join()
    print('完成图片爬取....')






