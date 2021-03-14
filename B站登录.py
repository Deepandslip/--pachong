from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time,random
from io import StringIO
from common.base_service import BaseService
from common import chaojiying
from PIL import Image

class BliBliLogin(BaseService):
    name='bilibli'
    login_url = "https://passport.bilibili.com/login"
    def __init__(self):
        # self.user_name = settings.Accounts[self.name]["username"]
        # self.pass_word = settings.Accounts[self.name]["password"]
        chrome_options = Options()
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.browser = webdriver.Chrome('C:\\Users\DEEP\Desktop\chromedriver.exe',options=chrome_options)

    def check_login(self):
        try:
            self.browser.find_element_by_xpath("//span[contains(text(),'创作中心')]")
            return True
        except Exception as e:
            return False

    def compare_pixel(self, image1, image2, i, j):#判断像素是否相同
        pixel1=image1.load()[i,j]
        pixel2=image2.load()[i,j]
        threshold = 60
        if abs(pixel1[0]-pixel2[0])<threshold and abs(pixel1[1]-pixel2[1])<threshold and abs(pixel1[2]-pixel2[2])<threshold:
            return True
        return False

    def crop_image(self,image_file_name):
        #截取验证码图片
        time.sleep(2)
        img=self.browser.find_element_by_css_selector('.geetest_canvas_img.geetest_absolute')
        location=img.location
        print('图片位置:',location)

        size=img.size
        top,buttom,left,right=location['y'],location['y']+size['height'],location['x'],location['x']+size['width']
        print('验证码截图坐标',left,top,buttom,right)

        screen_shot=self.browser.get_screenshot_as_png()
        screen_shot=Image.open(BinaryIO(screen_shot))
        captcha = screen_shot.crop((int(left), int(top), int(right), int(buttom)))
        captcha.save(image_file_name)
        return captcha

    def login(self):
        try:
            self.browser.maximize_window()
        except Exception as e:
            pass
        while not self.check_login():
            self.browser.get(self.login_url)
            username_ele=self.browser.find_element_by_css_selector('#login-username')
            password_ele=self.browser.find_element_by_css_selector('#login-passwd')
            username_ele.send_keys('17620967734')
            password_ele.send_keys('676725.000')

            #点击登录调出验证码
            login_btn = self.browser.find_element_by_css_selector(".btn.btn-login")
            login_btn.click()

            time.sleep(5)
            #js改变js，显示没有缺口的图
            self.browser.execute_script('document.querySelectorAll("canvas")[3].style=""')
            #截取验证码
            image1=self.crop_image('captcha1.png')

            # 执行js改变css样式，显示有缺口的图
            self.browser.execute_script('document.querySelectorAll("canvas")[3].style="display: none;""')
            image2=self.crop_image('captcha2.png')

            left = 60
            has_find = False
            for i in range(60, image1.size[0]):  # 图片从左到有滑动
                if has_find:
                    break
                for j in range(image1.size[1]):
                    if not self.compare_pixel(image1, image2, i, j):
                        left = i
                        has_find = True
                        break
            left -= 6

            track=[]
            current=0
            # 减速阈值
            mid = left * 3 / 4
            t = 0.1
            v = 0
            while current < left:
                if current < mid:
                    a = random.randint(2, 3)
                else:
                    a = - random.randint(6, 7)
                v0 = v
                # 当前速度
                v = v0 + a * t
                # 移动距离
                move = v0 * t + 1 / 2 * a * t * t
                # 当前位移
                current += move
                track.append(round(move))
            slider=self.browser.find_element_by_css_selector('.geetest_slider_button')
            ActionChains(self.browser).click_and_hold(slider).perform()
            for x in track:
                ActionChains(self.browser).move_by_offset(xoffset=x,yoffset=0).perform()
            time.sleep(0,5)
            ActionChains(self.browser).release().perform()
            time.sleep(4)


    def check_cookie(self, cookie_dict):
        pass



if __name__ == '__main__':
    # bili=BliBliLogin()
    # bili.login()
    image1=Image.open('captcha1.png')
    image2=Image.open('captcha2.png')
    #获取缺口位置












