import requests
import time
from bs4 import BeautifulSoup

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
	'Referer': 'https://github.com/login',
	#'Host': 'github.com',
	'Cookie': '_octo=GH1.1.263989782.1569344881; _ga=GA1.2.259279496.1569344916; _device_id=497f8bc5de7714a282b363912445cbe2; has_recent_activity=1; tz=Asia%2FShanghai; experiment:homepage_signup_flow=eyJ2ZXJzaW9uIjoiMSIsInJvbGxPdXRQbGFjZW1lbnQiOjYuOTUyMDExNDIzODcyNzg2LCJzdWJncm91cCI6ImNvbnRyb2wiLCJjcmVhdGVkQXQiOiIyMDIwLTA0LTE1VDAwOjIwOjMyLjYyM1oiLCJ1cGRhdGVkQXQiOiIyMDIwLTA0LTE1VDAwOjIwOjMyLjYyM1oifQ==; _gat=1; logged_in=no; _gh_sess=3u7Rr3weOwMDK51PRATzAAunBZ6iaiIId51K4dKUPfDuiYqCuiJ%2FWNRtS%2B3Cmii7XwhbLRCGWkWA69enfTAtIcQLPnEJlAujNSRw7VAeuiOTVx0pmWOFQaf9zzWIO80e%2FmCpoI%2BLV%2FOR5shTzdLNTsUOA7Od02Vu4ijZkGIfqi0n3iHWFVYWg1zEeNNS%2FemkvyHCDirZDM1dM5QR6Gsr4egMrErmfYHN9XFRJFNB%2BOo%2FRI0vjjSYtjrywIrRfdBVjqBwDFq18J6frFdpfbnSig%3D%3D--JpDybCWe8xNbSsHb--Z%2FH1E8%2F1u2hwwXQu5UL7yA%3D%3D'
}
def save_html(html):
    with open('login.html','w',encoding='utf-8')as f:
        f.write(html)

session=requests.session()
session.headers=headers
def post_html():
    url='https://github.com/session'
    data={
        'authenticity_token': 'DjWfw+dn9H52qV7j1FEHYzrvV4ltxs//Z7QtC0AfJua25GJKLgCkO61yOMysDEjTXQQBmKte3DRmBz9ukz8YGw==',
        'login': 'Deepandslip',
        'password': '676725.abc',
        'webauthn - support': 'unknown',
        'webauthn - iuvpaa - support': 'unknown',
        'timestamp': '{}'.format(time.time()),
        'timestamp_secret': '0c2ec8d6a7d25a3a2fc8de43afa85fd904377066f3c4202aae4941b01e3cda73',
        'commit': 'Sign in'
    }
    html=session.post(url,headers=headers,data=data,timeout=2)
    if html.status_code==200:
        # print('正在登录页面...')
        # save_html(html.text)
        print('feeding...')
        get_feed(session)
    else:
        print(html.status_code)


def get_feed(sess):
    html=sess.get('https://github.com/dashboard-feed')
    soup=BeautifulSoup(html.text,'lxml')
    content=soup.select('div.watch_started')
    for c in content:
        try:
            from_people=c.select('.d-flex.flex-items-baseline div div div div a')[0].text
            to_people=c.select('.d-flex.flex-items-baseline div div div div a')[1].text
            code=c.select('.d-flex.flex-items-baseline span .ml-0 span')[1].text
            print(from_people,to_people,code)
            save_data('from:{} to:{} code:{}\n'.format(from_people,to_people,code))
        except:
            pass

def save_data(row):
    with open('githun_data.txt','a+',encoding='utf-8')as f:
        f.write(row)
if __name__ == '__main__':
    post_html()

