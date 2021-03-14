from selenium import webdriver
import pandas as pd
import re
import multiprocessing
from selenium.webdriver.chrome import options
def provinceMap(province_name):
    # 省份对应的code，但是深圳是单独的数据
    code_dict = {"北京": "010000", "上海": "020000", "广东省": "030000", "深圳": "040000", "天津": "050000", "重庆": "060000",
                 "江苏省": "070000", "浙江省": "080000", "四川省": "090000", "海南省": "100000", "福建省": "110000", "山东省": "120000",
                 "江西省": "130000", "广西省": "140000", "安徽省": "150000", "河北省": "160000", "河南省": "170000", "湖北省": "180000",
                 "湖南省": "190000", "陕西省": "200000", "山西省": "210000", "黑龙江省": "220000", "辽宁省": "230000",
                 "吉林省": "240000", "云南省": "250000", "贵州省": "260000", "甘肃省": "270000", "内蒙古": "280000", "宁夏": "290000",
                 "西藏": "300000", "新疆": "310000", "青海省": "320000", "香港": "330000", "澳门": "340000", "台湾": "350000"}
    province_code=code_dict[province_name]
    return province_name

def fileMap(field):
    if field=='后端开发':
        field_code='0100'
    elif field=='数据分析师':
        field_code='7700'
    elif field=='机器学习':
        field_code='7301'
    else:
        field_code='0000'
    return field_code

def JobMining(province_name,field):
    for pro in province_name:
        opt=options.Options()
        opt.add_argument('--disable-infobars')
        opt.add_argument('--headless')
        opt.add_argument('--incognito')
        chrome_options=webdriver.Chrome('C:\\Users\DEEP\Desktop\chromedriver.exe')
        driver=chrome_options
        province_code=provinceMap(pro)
        field_code=fileMap(field)
        url_pre = 'https://search.51job.com/list/'
        url_before_field = ',000000,'
        url_before_num = ',00,9,99,+,2,'
        url_end = '.html'
        url = url_pre + str(province_code) + url_before_field + str(field_code) + url_before_num + str(1) + url_end
        driver.get(url)
        page=driver.find_element_by_xpath("//div[@class='rt rt_page']")
        pattern = re.compile(r'(?<=/ )(.+?)((?<![^a-zA-Z0-9_\u4e00-\u9fa5])(?=[^a-zA-Z0-9_\u4e00-\u9fa5])|(?<=['
                             r'^a-zA-Z0-9_\u4e00-\u9fa5])(?![^a-zA-Z0-9_\u4e00-\u9fa5])|$)', re.S)
        result=re.search(pattern,page.text)
        page_num=int(result.group(1))
        driver.quit()

        for page in range(1,page_num+1):
            opt = options.Options()
            opt.add_argument('--disable-infobars')
            opt.add_argument('--headless')
            opt.add_argument('--incognito')
            chrome_options = webdriver.Chrome('C:\\Users\DEEP\Desktop\chromedriver.exe')
            driver = chrome_options
            print("省/市：" + str(pro) + "；领域：" + str(field) + "；正在爬取第" + str(page) + "页的数据，共" + str(page_num) + "页")
            url_pre = 'https://search.51job.com/list/'
            url_before_field = ',000000,'
            url_before_num = ',00,9,99,+,2,'
            url_end = '.html'
            url = url_pre + str(province_code) + url_before_field + str(field_code) + url_before_num + str(
                page) + url_end
            driver.get(url)

            job_name=driver.find_elements_by_xpath("//div[@class='j_joblist']/div[@class='e']/a/p[@class='t']/span[@class='jname at']")
            job_list=[]
            for i in job_name:
                job_list.append(i.text)

            company_name = driver.find_elements_by_xpath(
                "//div[@class='j_joblist']/div[@class='e']/div[@class='er']/a[@class='cname at']")
            company_list = []
            for i in company_name:
                company_list.append(i.text)

            info = driver.find_elements_by_xpath(
                "//div[@class='j_joblist']/div[@class='e']/a/p[@class='info']/span[@class='d at']")
            education_list=[]
            city_list=[]
            district_list=[]
            experience_list=[]
            for i in info:
                if '初中及以下' in i.text:
                    education_list.append('初中及以下')
                elif '高中' in i.text:
                    education_list.append('高中')
                elif '中专' in i.text:
                    education_list.append('中专')
                elif '中技' in i.text:
                    education_list.append('中技')
                elif '大专' in i.text:
                    education_list.append('大专')
                elif '本科' in i.text:
                    education_list.append('本科')
                elif '硕士' in i.text:
                    education_list.append('硕士')
                elif '博士' in i.text:
                    education_list.append('博士')
                else:
                    education_list.append('')
            pattern = re.compile(r'(.+?)(?=\|)', re.S)
            city_short = re.search(pattern, i.text)
            # 检测到-时把城市和地区拆分开
            if '-' in city_short.group(1):
                pattern = re.compile(r'(.+?)(?=-)', re.S)
                city1 = re.search(pattern, city_short.group(1))
                city_list.append(city1.group(1))
                pattern = re.compile(
                    r'(?<=-)(.+?)((?<![^a-zA-Z0-9_\u4e00-\u9fa5])(?=[^a-zA-Z0-9_\u4e00-\u9fa5])|(?<=['
                    r'^a-zA-Z0-9_\u4e00-\u9fa5])(?![^a-zA-Z0-9_\u4e00-\u9fa5])|$)', re.S)
                district = re.search(pattern, city_short.group(1))
                district_list.append(district.group(1))
            else:
                city_list.append(city_short.group(1))
                district_list.append('')

            if '年经验' in i.text:
                pattern = re.compile(r'(?<=\|)(.+?)(?=经)', re.S)
                experience = re.search(pattern, i.text)
                # 去除多余空格
                experience_list.append(experience.group(1).replace(' ', ''))
            else:
                experience_list.append('')
                # 发布时间
            date = driver.find_elements_by_xpath(
                "//div[@class='j_joblist']/div[@class='e']/a/p[@class='t']/span[@class='time']")
            date_list = []
            for i in date:
                # 获取到的是 “12-14发布” 这样的数据，用 replace 把“发布”去掉。
                date_list.append(i.text.replace('发布', ''))
            # 获取二级url
            url = driver.find_elements_by_xpath("//div[@class='j_joblist']/div[@class='e']/a")
            url_list = []
            for i in url:
                # <a href=".get_attribute('href')获取的是这里的文本">.text是获得这里的文本</a>
                url_list.append(i.get_attribute('href'))
            salary_list = []
            company_benefit_list = []
            company_type_list = []
            company_scale_list = []
            company_industry_list = []
            job_describe_list = []
            for job in url_list:
                url = str(job)
                driver.get(url)
                # 薪水
                try:
                    salary = driver.find_element_by_xpath("//div[@class='cn']/strong").text
                    salary_list.append(salary)
                except:
                    salary_list.append('')
                # 福利
                try:
                    company_benefit = driver.find_elements_by_xpath("//div[@class='t1']/span")
                    # 福利是写在多个 span 里，因此循环遍历每一个 span，将其添加到列表里
                    sub_list = []
                    for i in company_benefit:
                        sub_list.append(i.text)
                    # 之后获得['五险一金', '带薪假']这样的列表，通过转换为字符串再 replace 修改成:五险一金, 带薪假，然后再写进 dataframe 里
                    company_benefit_list.append(str(sub_list).replace('[', '').replace(']', '').replace("'", ''))
                except:
                    company_benefit_list.append('')
                # 公司类型
                try:
                    company_type = driver.find_element_by_xpath("//div[@class='com_tag']/p[1]").text
                    company_type_list.append(company_type)
                except:
                    company_type_list.append('')
                # 公司规模
                try:
                    # <p class="at" title=".get_attribute('title')获取的是这里的文本"></p>
                    company_scale = driver.find_element_by_xpath("//div[@class='com_tag']/p[2]").get_attribute('title')
                    company_scale_list.append(company_scale)
                except:
                    company_scale_list.append('')
                # 所属行业
                try:
                    company_industry = driver.find_element_by_xpath("//div[@class='com_tag']/p[3]").get_attribute(
                        'title')
                    company_industry_list.append(company_industry)
                except:
                    company_industry_list.append('')
                # 职位描述
                try:
                    job_describe = driver.find_element_by_xpath("//div[@class='bmsg job_msg inbox']").text
                    # 去除多余空格与“微信分享”
                    job_describe = job_describe.replace(' ', '').replace('微信分享', '')
                    job_describe_list.append(job_describe)
                except:
                    job_describe_list.append('')
            # 下面将所有列表的内容写进 dataframe
            df = pd.DataFrame()
            df["岗位名称"] = job_list
            df["公司名称"] = company_list
            df["城市"] = city_list
            df["地区"] = district_list
            df["学历"] = education_list
            df["经验"] = experience_list
            df["薪水"] = salary_list
            df["时间"] = date_list
            df["公司类型"] = company_type_list
            df["公司规模"] = company_scale_list
            df["所属行业"] = company_industry_list
            df["福利"] = company_benefit_list
            df["职位描述"] = job_describe_list
            df["链接"] = url_list
            # 使用a+模式追加数据，每一页存储一次，防止数据丢失，因而需要取消header（列名），在数据清理过程再加上
            file_path = "raw/" + str(pro) + '_' + str(field) + '.csv'
            df.to_csv(path_or_buf=file_path, mode="a+", header=False, index=False, encoding="utf_8_sig")
            # 退出webdriver，防止过多进程影响计算机性能
            driver.quit()


if __name__ == '__main__':
    list1 = ["北京", "重庆", "海南省", "广西省", "湖北省", "贵州省"]
    list3 = ["广东省", "浙江省","澳门", "陕西省", "吉林省", "深圳", "上海"]
    list4 = [ "天津", "四川省", "江西省", "山西省", "宁夏", "香港"]
    p1 = multiprocessing.Process(target=JobMining, args=(list1, '数据分析师'))
    p3 = multiprocessing.Process(target=JobMining, args=(list3, '数据分析师'))
    p4 = multiprocessing.Process(target=JobMining, args=(list4, '数据分析师'))
    p1.start()
    p3.start()
    p4.start()
    p1.join()
    p3.join()
    p4.join()


