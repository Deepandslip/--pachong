import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class YunSpider(object):
    def __init__(self,url):
        self.url=url
        self.driver=webdriver.Chrome('C:\\Users\DEEP\Desktop\chromedriver.exe')

    def getContent(self):
        self.driver.get(self.url)
        self.driver.switch_to.frame(0)

        for n in range(5):
            js='window.scrollBy(0,8000)'
            self.driver.execute_script(js)
            time.sleep(1)

            elememts = self.driver.find_elements_by_xpath('//div[contains(@class,"cmmts")]/div')
            # 循环遍历
            try:
                for text in elememts:
                    result = text.find_element_by_xpath('.//div[contains(@class,"cnt f-brk")]').text
                    print(result)
                    self.saveFile(result)

                self.driver.find_element_by_partial_link_text('下一页').click()
                time.sleep(1)
            except:
                pass


    @staticmethod
    def saveFile(data):
        with open('music_com.txt','a+',encoding='utf-8')as f:
            f.write(data+'\n')

if __name__ == '__main__':
    url='https://music.163.com/#/song?id=1463165983'
    MComments=YunSpider(url)
    MComments.getContent()