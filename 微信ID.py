import requests,time
import urllib3
import re,csv
from lxml import etree
from threading import Thread
class WeChart(object):

    def __init__(self,key):
        self.key=key
        self.page=1
        self.req_url = 'https://weixin.sogou.com/weixin?query={}&page={}'
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        }

    @staticmethod
    def join_list(res):
        return ''.join(res)

    @staticmethod
    def realtime(res):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(res))

    def re_time(self,res):
        last=self.join_list(res)
        try:
            pulltime=int(re.findall(r'(\d+)',last)[0])
        except:
            pulltime=int(time.time())
        return self.realtime(pulltime)

    def get_html(self):
        for num in range(1,30):
            pagecontent=requests.get(self.req_url.format(self.key,num),headers=self.headers,verify=False)
            html=etree.HTML(pagecontent.text)
            contents=html.xpath('//div[@class="news-box"]/ul/li')
            for c in contents:
                item={}
                item['name'] = self.join_list(c.xpath(
                    './div[@class="gzh-box2"]/div[@class="txt-box"]/p[@class="tit"]/a/em/text()')) + self.join_list(
                    c.xpath('./div[@class="gzh-box2"]/div[@class="txt-box"]/p[@class="tit"]/a/text()'))
                item['image']='https:'+self.join_list(c.xpath('./div[@class="gzh-box2"]/div[@class="img-box"]/a/img/@src'))
                item['wechatid'] = self.join_list(c.xpath('./div[@class="gzh-box2"]/div[@class="txt-box"]/p[@class="info"]/label[@name="em_weixinhao"]/text()'))
                item['introduce'] = self.join_list(c.xpath('./dl[1]/dd/em/text()')) + self.join_list(c.xpath('./dl[1]/dd/text()'))
                item['renzheng'] = self.join_list(c.xpath('//div[@class="news-box"]/ul/li[1]/dl[2]/dd/text()')).replace('\n', '')
                item['title'] = self.join_list(c.xpath('./dl[3]/dd/a/text()'))
                item['date'] = self.re_time(c.xpath('./dl[3]/dd/span/script/text()'))
                print(item)
                # with open('wechart_id.csv','a+',encoding='utf-8')as f:
                #     f.write(str(item)+'\n')

                print('第{}页下载完成...'.format(self.page))
                time.sleep(1)
                self.page+=1

    def main(self):
        #self.get_html()
        t=Thread(target=self.get_html)
        t.start()


if __name__ == '__main__':
    urllib3.disable_warnings()

    key=input('请输入要搜索的公众号:')
    wc=WeChart(key)
    wc.main()







