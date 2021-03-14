import requests,time,random

from queue import Queue
from fake_useragent import UserAgent
from threading import Thread,Lock

class HouLangComments(object):
    def __init__(self):
        self.url='''https://api.bilibili.com/x/v2/reply?&pn={}&type=1&oid=412935552&sort=2&_={}'''
        self.rep_comment_url='''https://api.bilibili.com/x/v2/reply/reply?&pn={}&type=1&oid=412935552&ps=10&root={}&_={}'''
        self.queue=Queue()
        self.replies_queue=Queue()
        self.flag=True
        self.replies_flag=True
        self.comment_num=1
        self.lock=Lock()
        self.lock_rep=Lock()

    def put_url(self):#评论的页数
        i=1
        while True:
            try:
                source=requests.get(self.url.format(i,int(time.time()*1000)),headers={'UserAgent':UserAgent().random})
                json_source=source.json()
                replies=json_source['data']['replies']
                if isinstance(replies,list):
                    self.queue.put(replies)
                    print('第{}页评论添加成功..'.format(i))
                    i+=1
                else:
                    self.flag=False
                    break
            except Exception as e:
                print('一页数据添加失败。。')
            time.sleep(random.uniform(0.8,1.5))

    def write_data(self,row):
        with open('dates.txt','a+',encoding='utf-8')as f:
            f.write(row)

    def get_url(self):
        while True:
            if not self.queue.empty():  # 如果队列不为空就获取
                contents = self.queue.get()
                for content in contents:
                    item=dict()
                    item['rpid'] = content.get('rpid', 0)
                    item['mid'] = content.get('mid', 0)
                    item['comment_date'] = self.time2date(content.get('ctime', 0))
                    item['likes'] = content.get('like', 0)
                    item['content'] = content['content'].get('message', 'Null')
                    item['rcount'] = content.get('rcount', 0)
                    user = content.get('member', 'Null')
                    if user != 'Null':
                        item['uname'] = user.get('uname', 'Null')
                        item['sex'] = user.get('sex', 'Null')
                        item['sign'] = user.get('sign', 'Null')
                    else:
                        item['uname'],item['sex'],item['sign']='','',''
                    print(item)
                    #self.write_data(item['content']+'\n')
                    print('第{}条评论获取成功！'.format(self.comment_num))
                    self.comment_num += 1
                    if item['rcount'] > 0:
                        self.replies_queue.put(item['rpid'])
            elif self.flag:
                print('等待中..........')
                time.sleep(random.uniform(3, 6))
            else:
                self.replies_flag = False
                break



    def get_rep_comment(self):
        while True:
            if not self.replies_queue.empty():
                num = 1
                root_id = self.replies_queue.get()
                while True:
                    try:
                        source = requests.get(self.rep_comment_url.format(num, root_id, int(time.time() * 1000)),
                                              headers={'User-Agent': UserAgent().random})
                        json_source = source.json()
                        replies = json_source['data']['replies']
                        if isinstance(replies, list):
                            for content in replies:
                                item_com = dict()
                                # 评论id
                                item_com['rpid'] = content.get('rpid', 0)
                                # 回复评论的id
                                item_com['root_id'] = content.get('root', 0)
                                # 返回时间戳
                                item_com['comment_date'] = self.time2date(content.get('ctime', 0))
                                # 评论内容
                                item_com['content'] = content['content'].get('message', 'Null')
                                print(item_com)
                                if user != 'Null':
                                    item_com['uname'] = user.get('uname', 'Null')
                                    item_com['sex'] = user.get('sex', 'Null')
                                else:
                                    item_com['uname'],item_com['sex']='',''

                            num+=1
                        else:
                            break
                    except Exception as e:
                        print('一条回复信息失败，，')
                    time.sleep(random.uniform(0.5, 1.2))
            elif self.replies_flag:
                print('等待中...')
                time.sleep(random.uniform(3,5))
            else:
                break


    @staticmethod
    def time2date(ctime):
        if len(str(ctime))==10:
            return time.strftime('%y-%m-%d %H:%M:%A',time.localtime(ctime))
        elif len(str(ctime))==13:
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctime / 1000))
        else:
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def main(self):
        put_th = Thread(target=self.put_url)
        get_th = Thread(target=self.get_url)
        rep_th = Thread(target=self.get_rep_comment)

        put_th.start()
        time.sleep(1.3)
        get_th.start()
        time.sleep(4)
        rep_th.start()

        put_th.join()
        get_th.join()
        rep_th.join()


if __name__ == '__main__':
    h1=HouLangComments()
    h1.main()








