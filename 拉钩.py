import requests,re
import time,json
import multiprocessing
from handle_insert_data import lagou_mysql
class LaGou(object):
    def __init__(self):
        self.lagou_session=requests.session()
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        self.city_list=''


    def handle_city(self):
        city_search=re.compile(r'zhaopin/">(.*?)</a>')

        city_search = re.compile(r'www\.lagou\.com\/.*/">(.*?)</a>')#匹配全国城市
        city_url='https://www.lagou.com/jobs/allCity.html'
        city_result=self.html_request(method='Get',url=city_url)
        self.city_list=city_search.findall(city_result)
        self.lagou_session.cookies.clear()

    def handle_city_job(self,city):
        first_request_url='https://www.lagou.com/jobs/list_python/p-city_%s?px=default'%city
        first_response=self.html_request(method='Get',url=first_request_url)
        total_page1=re.compile(r'class="span\stotalNum">(\d+)</span>')
        try:
            total_page=total_page1.search(first_response).group(1)
        except:
            return
        else:
            for i in range(1,int(total_page)+1):
                data={
                    'pn':i,
                    'kd':'python'
                }
                page_url='https://www.lagou.com/jobs/positionAjax.json?px=default&city=%s&needAddtionalResult=false'%city
                referer_url='https://www.lagou.com/jobs/list_python/p-city_%s?px=default'%city
                self.headers['Referer']=referer_url.encode()
                response=self.html_request(method='post',url=page_url,data=data,info=city)
                lagou_data=json.loads(response)
                job_list=lagou_data['content']['positionResult']['result']
                for job in job_list:
                    lagou_mysql.insert_item(job)

    def html_request(self,method,url,data=None,info=None):
        while True:
            try:
                proxy={
                    'http':'163.204.240.95:9999',
                    'http':'175.43.32.38:9999',
                    'http':'1.198.73.5:9999'
                }
                if method =='Get':
                    response=self.lagou_session.get(url=url,headers=self.headers,proxies=proxy,timeout=6)
                elif method =='post':
                    response=self.lagou_session.post(url=url,headers=self.headers,data=data,proxies=proxy,timeout=6)
            except:
                self.lagou_session.cookies.clear()
                first_request_url = 'https://www.lagou.com/jobs/list_python/p-city_%s?px=default' % info
                self.html_request(method='Get', url=first_request_url)
                time.sleep(10)
                continue
            response.encoding='utf-8'
            if '频繁' in response.text:
                print(response.text)
                #需要先清除cookies
                self.lagou_session.cookies.clear()
                first_request_url = 'https://www.lagou.com/jobs/list_python/p-city_%s?px=default' %info
                self.html_request(method='Get', url=first_request_url)
                time.sleep(10)
                continue
            return response.text

if __name__ == '__main__':
    lagou=LaGou()
    lagou.handle_city()
    pool=multiprocessing.Pool(2)
    for city in lagou.city_list:
        pool.apply_async(lagou.handle_city_job,args=(city,))
        pool.close()
        pool.join()



