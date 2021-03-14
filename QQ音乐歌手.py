import requests
import json
from urllib import parse
import math
import execjs
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
    'referer': 'https://y.qq.com/portal/singer_list.html',
}

# with open('./sign.js', 'r', encoding='utf8')as f:
#     content = f.read()
#     jsData = execjs.compile(content)
#     sign = jsData.call('getSign')

def write_text(row):
    with open('singer.text','a+',encoding='utf-8')as f:
        f.write(row+'\n')

def get_singer_data(mid,singer_name):
    params = '{"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList",' \
             '"param":{"order":1,"singerMid":"%s","begin":0,"num":10},' \
             '"module":"musichall.song_list_server"}}' % str(mid)

    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getSingerSong9513357793133783&' \
          'g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8' \
          '&notice=0&platform=yqq.json&needNewCode=0&data={}'.format(parse.quote(params))
    html=requests.session()
    content=html.get(url,headers=headers).json()['data']
    songs_num=content['singerSongList']['data']['totalNum']


    # datas=dict()
    # datas['singer_name']=singer_name
    # datas['singer_country']=singer_country
    # datas['sing_num']=songs_num

    if int(songs_num)<=80:
        params = '{"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList",' \
                 '"param":{"order":1,"singerMid":"%s","begin":0,"num":%s},' \
                 '"module":"musichall.song_list_server"}}' % (str(mid), int(songs_num))

        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getSingerSong9513357793133783&' \
              'g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8' \
              '&notice=0&platform=yqq.json&needNewCode=0&data={}'.format(parse.quote(params))
        html=requests.session()
        content=html.get(url,headers=headers).json()
        datas = content['singerSongList']['data']['songList']
        for song in datas:
            sing_name = d['songInfo']['title']
            songmid = d['songInfo']['mid']
            print(sing_name, songmid, singer_name)

        # song_list=[]
        # for song in content['singerSongList']['data']['songList']:
        #     inner_song={}
        #     inner_song['songname']=song['name']
        #     inner_song['albumname']=song['album']['name']
        #     inner_song['singer_name']=song['singer'][0]['name']
        #     song_list.append(inner_song)
        #     datas['song_mid']=song['mid']
        # datas['sings']=song_list
        # write_text(str(datas))
        # print(datas)
    else:
        # song_list=[]
        for a in range(0,songs_num,80):
            params = '{"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList",' \
                     '"param":{"order":1,"singerMid":"%s","begin":%s,"num":%s},' \
                     '"module":"musichall.song_list_server"}}' % (str(mid), int(a), int(songs_num))

            url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getSingerSong9513357793133783&' \
                  'g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8' \
                  '&notice=0&platform=yqq.json&needNewCode=0&data={}'.format(parse.quote(params))
            content=html.get(url,headers=headers).json()
            datas = content['singerSongList']['data']['songList']

            for d in datas:
                sing_name = d['songInfo']['title']
                songmid = d['songInfo']['mid']
                print(sing_name, songmid, singer_name)

            # for song in content['singerSongList']['data']['songList']:
            #     inner_song = {}
            #     inner_song['songname'] = song['name']
            #     inner_song['albumname'] = song['album']['name']
            #     inner_song['singer_name'] = song['singer'][0]['name']
            #     song_list.append(inner_song)
            #     datas['song_mid'] = song['mid']
            # datas['sings'] = song_list
            # write_text(str(datas))
            # print(datas)


def get_singer_mid(index):#歌手id
    data = '{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer"' \
           ',"method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,' \
           '"index":%s,"sin":0,"cur_page":1}}}' % (str(index))

    # Python3.7
    # encoding = utf-8

    import requests, os, json, math
    from urllib import parse
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
    from db import SQLsession, Song

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        'referer': 'https://y.qq.com/portal/singer_list.html',
        # 参考链接 https://y.qq.com/portal/singer_list.html#page=1&index=1&
    }

    session = SQLsession()

    def myProcess():
        # 把歌手按照首字母分为27类
        with ProcessPoolExecutor(max_workers=2) as p:  # 创建27个进程
            for i in range(2, 3):  # 28
                p.submit(get_singer_mid, i)

    def get_singer_mid(index):
        # index =  1-----27
        # 打开歌手列表页面，找出singerList,找出所有歌手的数目,除于80,构造后续页面获取page歌手
        # 找出mid, 用于歌手详情页

        data = '{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer"' \
               ',"method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,' \
               '"index":%s,"sin":0,"cur_page":1}}}' % (str(index))

        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI0432880619182503' \
              '&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&out' \
              'Charset=utf-8&notice=0&platform=yqq.json&needNewCode=0' \
              '&data={}'.format(parse.quote(data))
    html=requests.get(url).json()
    total=html['singerList']['data']['total']
    pages=int(math.floor(int(total)/80))#向下取整数
    thread_number=pages
    ThreadPoolExecutor(max_workers=thread_number)
    sin = 0
    for page in range(1, pages):
        data = '{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer",' \
               '"method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,"' \
               'index":%s,"sin":%d,"cur_page":%s}}}' % (str(index), sin, str(page))

        # Python3.7
        # encoding = utf-8

        import requests, os, json, math
        from urllib import parse
        from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
        from db import SQLsession, Song

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
            'referer': 'https://y.qq.com/portal/singer_list.html',
            # 参考链接 https://y.qq.com/portal/singer_list.html#page=1&index=1&
        }

        session = SQLsession()

        def myProcess():
            # 把歌手按照首字母分为27类
            with ProcessPoolExecutor(max_workers=2) as p:  # 创建27个进程
                for i in range(2, 3):  # 28
                    p.submit(get_singer_mid, i)

        def get_singer_mid(index):
            # index =  1-----27
            # 打开歌手列表页面，找出singerList,找出所有歌手的数目,除于80,构造后续页面获取page歌手
            # 找出mid, 用于歌手详情页

            data = '{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer"' \
                   ',"method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,' \
                   '"index":%s,"sin":0,"cur_page":1}}}' % (str(index))

            url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI0432880619182503' \
                  '&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&out' \
                  'Charset=utf-8&notice=0&platform=yqq.json&needNewCode=0' \
                  '&data={}'.format(parse.quote(data))
        html = requests.get(url, headers=headers).json()
        sings = html['singerList']['data']['singerlist']
        for sing in sings:
            singer_name = sing['singer_name']
            mid = sing['singer_mid']
            Thread.submit(get_singer_data, mid=mid,
                          singer_name=singer_name, )
        sin += 80

def myprocess():
    with ProcessPoolExecutor(max_workers=10)as p:
        for i in range(2,3):
            p.submit(get_singer_mid,i)

if __name__ == '__main__':
    myprocess()

