import requests
from bs4 import BeautifulSoup
import re,json,csv
import threadpool

from urllib import parse


# from getComm import get_comm
# keyword = parse.quote('python')
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'cookie': '__jdu=1872882353; shshshfpa=b2fee7ea-3f9e-10e8-1c04-bb1da53ae980-1596248581; shshshfpb=m0J%20gYN%202FzxkTITPsETSVw%3D%3D; unpl=V2_ZzNtbRdRRUEhWkZdfxxeV2JUEA1LV0dBdQ5BAXtOWQ03BRYJclRCFnQURlVnGV8UZwsZWUFcRxVFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsQWgZuChFfRlVzJXI4dmR%2bH1sEbgAiXHJWc1chVENcfh1UACoDG1tBXkoWdwxEZHopXw%3d%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_d77eec18543c4f3a815e176d1f49a75e|1602503573582; areaId=19; ipLoc-djd=19-1601-50284-0; PCSYCityID=CN_440000_440100_440118; __jda=122270672.1872882353.1596248578.1599017979.1602503574.4; __jdc=122270672; 3AB9D23F7A4B3C9B=WLCMJPXK2EGDJPHEZJPUM4GDW7V6ANSV2H4LTHONGJ7ZOPHZGKE6QAS6P5DOTXU6JINKOYGQLZETC6KL6QRVIVQD2Q; __jdb=122270672.4.1872882353|4.1602503574; shshshfp=634c1b2f2f93341bc3ada1d6b03dbc7c; shshshsID=639ffe341f190947b3002e425e4fb686_2_1602503596779; qrsc=3; rkv=1.0'
}
base='https://search.jd.com'

head=['shop_name','shop_data','shop_brand','book_name','price','comm_num','item_id','shop_evaluation','sale_server']
def write_csv(row):
    with open('shop.csv','a+',encoding='utf-8')as f:
        csv_writer=csv.DictWriter(f,head)
        csv_writer.writerow(row)

def get_id(url):
    id=re.compile('\d+')
    res=id.findall(url)
    return res[0]


def get_comm_num(url):
    item_id=get_id(url)
    comm_url='https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}&callback=jQuery3943560'.format(item_id)
    comment=requests.get(comm_url,headers=headers).text
    start = comm_url.find('{"CommentsCount":')
    end = comm_url.find('PoorRateStyle":0}]}') + len('PoorRateStyle":0}]}')
    try:
        comment = json.loads(comment[start:end])['CommentsCount']
    except:
        return 0
    comm_num=comment[0]['CommentsCount']
    return int(comm_num)


def get_shop_info(url):
    shop_data={}
    html=requests.get(url,headers=headers)
    soup=BeautifulSoup(html.text,'lxml')
    try:
        shop_name=soup.select('div.mt h3 a')[0].text
    except:
        shop_name='京东'
    shop_score=soup.select('.score-part span.score-detail em')
    try:
        shop_evaluation=shop_score[0].text
        sale_server=shop_score[1].text
    except:
        shop_evaluation=None
        logistics=None
        sale_server=None
    shop_info = soup.select('div.p-parameter ul')
    shop_brand = shop_info[0].select('ul li a')[0].text
    try:
        shop_other = shop_info[1].select('li')
        for s in shop_other:
            data=s.text.split(':')
            key=data[0]
            value=data[1]
            shop_data[key]=value
    except:
        pass
    shop_data['shop_name']=shop_name
    shop_data['shop_evaluation']=shop_evaluation
    shop_data['sale_server']=sale_server
    shop_data['shop_data']=shop_data
    shop_data['shop_brand']=shop_brand
    return shop_data



def get_comm(url,comm_num):
    good_comments=''#存放结果
    item_id=get_id(url)
    pages=comm_num//10
    if pages>90:
        pages=99
    for page in range(0,pages):
        comments_url='https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={}&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'.format(item_id,page)
    headers['Referer']=url
    json_decoder=requests.get(comments_url,headers=headers).text
    try:
        if json_decoder:
            start = json_decoder.find('{"productAttr"')
            end = json_decoder.find('}]}') + len('}]}')
            comment = json.loads(s=json_decoder[start:end])
            comments=comment['comments']
            for c in comments:
                comm=c['content']
                good_comments+='{}|'.format(comm)
    except Exception as e:
        pass
    return item_id,good_comments


id_comm_dict = {}
def get_index(url):
    session = requests.Session()
    session.headers = headers
    html=session.get(url)
    soup=BeautifulSoup(html.text,'lxml')
    items=soup.select('li.gl-item')
    for item in items:
        inner_url=item.select('.gl-i-wrap div.p-img a')[0].get('href')
        inner_url=parse.urljoin(base,inner_url)#https添加成完整URL
        item_id=get_id(inner_url)
        #评论数
        comm_num=get_comm_num(inner_url)
        #获取评论
        # if comm_num>0:#如果有评论就提交
        #     id_comm_dict[item_id]=get_comm.delay(inner_url,comm_num)

        shop_info_data=get_shop_info(inner_url)

        price=item.select("div.p-price strong i")[0].text
        book_name=item.select('div.p-name em')[0].text
        shop_info_data['book_name']=book_name
        shop_info_data['price']=price
        shop_info_data['comm_num']=comm_num
        shop_info_data['item_id']=item_id
        print(shop_info_data)
        write_csv(shop_info_data)



if __name__ == '__main__':
    keyword = input('请输入要搜索的书:')
    urls=[]
    for i in range(5,7,2):
        url='https://search.jd.com/Search?keyword={}&suggest=1.def.0.V05--38s0&wq={}&page={}&s=101&click=0'.format(keyword,keyword,i)

        urls.append(([url,],None))
    pool=threadpool.ThreadPool(3)
    reque=threadpool.makeRequests(get_index,urls)
    for c in reque:
        pool.putRequest(c)
    pool.wait()


