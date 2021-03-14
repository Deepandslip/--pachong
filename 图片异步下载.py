import asyncio
import hashlib
import logging,os,re,shutil,time
from urllib.parse import quote
import aiofiles
import aiohttp


IMAGE_DIR='image_data'
logging.basicConfig(level=logging.INFO)#打印日志配置文件
event=asyncio.Event()


def check_image_dir_exist():
    #检查目录是否存在，存在则删除， 不存在则新建
    if os.path.exists(IMAGE_DIR):
        shutil.rmtree(IMAGE_DIR)# 表示递归删除存在文件夹。
    os.mkdir(IMAGE_DIR)



async def download_url(q):
    async with aiohttp.ClientSession()as session:
        while 1:
            try:
                url=q.get_nowait()#从队列头获取元素，非阻塞方式，当队列为空时，不等待，而是直接抛出empty异常
            except asyncio.QueueEmpty as e:
                await asyncio.sleep(1)
                if event.is_set():
                    break
                continue
            async with session.get(url)as resp:
                content=await resp.read()
                md5=hashlib.md5(content).hexdigest()
                file_path=os.path.join(IMAGE_DIR,md5 + '.jpg')
                async with aiofiles.open(file_path,'wb')as f:
                    await f.write(content)
                    now=time.time()
                    logging.info(f'ok...{file_path}..{now}')
                    q.task_done()



async def get_json_result(q,key_word):
    async with aiohttp.ClientSession()as session:
      for num in range(0,1000,20):
          try:
              baidu_url='https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={key_word}&pn={num}'
              request_url=baidu_url.format(num=num,key_word=key_word)
              async with session.get(request_url,timeout=5)as resp:
                  content=await resp.read()#返回html字符串
                  content=content.decode('utf-8')
                  reg=re.compile(r'"middleURL":"(.*?)"')#网页源码匹配
                  image_data_list=re.findall(reg,content)

                  for image_url in image_data_list:
                      if image_url.endswith('jpg'):
                          await q.put(image_url)#阻塞写入队列
              logging.info(f'done...{request_url}')
          except UnicodeDecodeError:
              logging.error('UnicodeDecodeError')
          except aiohttp.client_exceptions.ClientConnectorError:
              logging.error('ClientConnectorError')
    event.set()


async def run(q,loop):
    key_word=input('请输入要搜索的图片:')
    tasks=[loop.create_task(get_json_result(q,key_word))]
    tasks_download=[loop.create_task(download_url(q))for _ in range(5)]
    await asyncio.wait(tasks+tasks_download)


if __name__ == '__main__':
    check_image_dir_exist()
    queue=asyncio.Queue()
    event_loop=asyncio.get_event_loop()
    event_loop.run_until_complete(run(queue,event_loop))




