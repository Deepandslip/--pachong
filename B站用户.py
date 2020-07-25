import requests,time,random
from queue import Queue#队列
from threading import Thread
from fake_useragent import UserAgent
import urllib3

class Bilibili(object):
    def __init__(self):
        self.space_url='https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'
        self.relation_url='https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp'
        self.upstat_url='https://api.bilibili.com/x/space/upstat?mid={}&jsonp=jsonp'
        self.navnum_url='https://api.bilibili.com/x/space/navnum?mid={}&jsonp=jsonp'
        self.queue=Queue()
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'cookie':'_zap=d3b85524-608a-40a0-a0c8-6cb65d433f06; d_c0="ACAhXCO-BRCPTl_RLKNCOS6yneaLpF29q4E=|1568043294"; tgw_l7_route=f2979fdd289e2265b2f12e4f4a478330; _xsrf=cbc8c703-c14e-4a2f-8e4d-3d80c4da82da; capsion_ticket="2|1:0|10:1568095339|14:capsion_ticket|44:Zjg4ZmRjMmY2ZTJjNDVkNTgwMWNiNjA1NjU5NTYzMzA=|506899d0030a455c56324b2bdf2592270dce960f4187dd6111662ee61824fb12"; l_n_c=1; r_cap_id="MmM4NjBkNTI0YTc4NGFmNGFiM2FjYzUwY2RkMmE0ZmQ=|1568095343|54d1cfb6dc5004e521366794171e1b01c584ef6b"; cap_id="MTI2MTIwNThhNWRlNGI1YzhjMzU5ZDEzZTQxZTJiMzg=|1568095343|2d87297fbb65212e7c20c6de9b35e64bce784945"; l_cap_id="ODI1N2Y0YjVhMDViNDI1Mjk2ZTkyNTY1M2RlMGYxZTQ=|1568095343|82490ce4fb492327ee04ba45315ec8906b136728"; n_c=1; z_c0=Mi4xQ09MUkNRQUFBQUFBSUNGY0k3NEZFQmNBQUFCaEFsVk5lb3BrWGdENlJUT1Vwc3BIdkgzSVhXN0pGUExPVlRvZU1R|1568095354|fc1d394d3725d0934fc9fd6b606932e1bb7ad659; tshl=; tst=h; unlock_ticket="AJBihgA5qw0XAAAAYQJVTYVDd10T-ZK-VwMEje_V-X8D4kfV2fn6TA=='

        }
        self.ip = [
            '117.191.11.110:8080',
            '39.137.69.6:80',
            '113.12.202.50:50327',
            '222.184.7.206:54832',
            '112.245.17.202:8080',
        ]
        self.proxies = {
            'http': random.choice(self.ip)
        }

    def put_url(self):
        for i in range(0,10):
            self.queue.put(i)

    def get_url(self):
        while not self.queue.empty():#如果队列为空，返回True,反之False
            uid=self.queue.get()
            item={}
            space_source=requests.get(self.space_url.format(uid),headers=self.headers,proxies=self.proxies,timeout=3)
            try:
                space_json=space_source.json()
                if space_json.get('code')==0:#以下用户信息
                    contents=space_json.get('data')
                    item['mid']=contents.get('mid',int(time.time()))
                    item['name']=contents.get('name','null')
                    item['sex']=contents.get('sex','null')
                    item['face']=contents.get('face','null')
                    item['sign']=contents.get('sign','null')
                    item['rank']=contents.get('rank',0)
                    item['level']=contents.get('level',0)
                    item['jointime']=contents.get('jointime',0)
                    item['birthday']=contents.get('birthday','null')
                    item.update(self.get_relation(uid))#定义下列函数
                    item.update(self.get_upstat(uid))
                    item.update(self.get_navnum(uid))

                    print(item)
                    with open('b.txt','a+',encoding='utf-8')as f:
                        f.write(str(item)+'\n')
            except Exception as e:
                print('一条数据出错{}'.format(e))

    def get_relation(self,uid):
        rel = {}
        try:
            relation_source = requests.get(self.relation_url.format(uid), headers={'User-Agent': UserAgent().random})
            relation_json = relation_source.json()
            rel['following'] = relation_json['data'].get('following', 0)
            rel['follower'] = relation_json['data'].get('follower', 0)
        except Exception as e:
            rel['following'] = 0
            # 粉丝数
            rel['follower'] = 0
        return rel

    def get_upstat(self,uid):
        upstat={}
        try:
            up_source=requests.get(self.upstat_url.format(uid),headers=self.headers,proxies=self.proxies)
            up_json=up_source.json()
            upstat['view']=up_json['data']['archive'].get('view',0)
            upstat['likes']=up_json['data'].get('likes',0)# 获赞数
        except Exception as e:
            upstat['view']=0
            upstat['likes']=0
        return upstat

    def get_navnum(self,uid):
        navnum={}
        try:
            nav_source=requests.get(self.navnum_url.format(uid),headers=self.headers,proxies=self.proxies)
            nav_json=nav_source.json()
            navnum['video']=nav_json['data'].get('video',0)
            navnum['bangumi']=nav_json['data'].get('bangumi',0)# 订阅番剧
            navnum['album']=nav_json['data'].get('album',0)
            navnum['channel_master'] = nav_json['data']['channel'].get('master', 0)
            navnum['favourite_master']=nav_json['data']['favourite'].get('master',0)
        except Exception as e:
            navnum['video']=0
            navnum['bangumi']=0
            navnum['album']=0
            navnum['channel_master']=0
            navnum['favourite_master']=0
        return navnum

    def main(self):
        put_th=Thread(target=self.put_url)
        get_th=Thread(target=self.get_url)

        put_th.start()
        time.sleep(1)
        get_th.start()


if __name__ == '__main__':
    urllib3.disable_warnings()
    bl=Bilibili()
    bl.main()










