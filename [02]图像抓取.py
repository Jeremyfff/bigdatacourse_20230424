import math
import sys

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
from os import listdir
from PIL import Image
import pyperclip

import cv2 as cv
import os
from shutil import copy
import numpy as np


def PNG_JPG(PngPath,size = 1,quality = 100):
    img = cv.imread(PngPath, 0)
    w, h = img.shape[::-1]
    infile = PngPath
    outfile = os.path.splitext(infile)[0] + ".jpg"
    img = Image.open(infile)
    img = img.resize((int(w*size), int(h*size)), Image.ANTIALIAS)
    try:
        if len(img.split()) == 4:
            # prevent IOError: cannot write mode RGBA as BMP
            r, g, b, a = img.split()
            img = Image.merge("RGB", (r, g, b))
            img.convert('RGB').save(outfile, quality=quality)
            os.remove(PngPath)
        else:
            img.convert('RGB').save(outfile, quality=quality)
            os.remove(PngPath)
        return outfile
    except Exception as e:
        print("PNG转换JPG 错误", e)

def cal_density():
    png_file_name = 'temp.png'
    jpg_file_name = 'temp.jpg'
    square_file_name = 'temp2.jpg'

    # 获取原始截图
    driver.get_screenshot_as_file(png_file_name)
    # png转jpg
    PNG_JPG(png_file_name)
    # 取中间
    img = Image.open(jpg_file_name)
    w, h = img.size
    w2 = w - 250
    h2 = h - 90
    w3 = h2
    h3 = h2
    w_shift = int(((w2 - w3) / 2 + 250) * -1)
    h_shift = -89
    result = Image.new(img.mode, (w3, h3))
    result.paste(img, box=(w_shift, h_shift))
    # 缩小样本
    result = result.resize((512,512),Image.ANTIALIAS)
    result.save(square_file_name,quality=95,subsampling=0)

    # cv读图像
    img = cv.imread(square_file_name, 0)

    xy = np.where(img == 254, 1, 0)  # 检测白色部分

    new_xy = np.array(xy)
    new_xy = new_xy.flatten()
    sum = 0
    for k in range(len(new_xy)):
        sum = sum + new_xy[k]
    num = len(new_xy)

    density = sum / num
    return density
def cal_density2():
    png_file_name = 'temp.png'
    #jpg_file_name = 'temp.jpg'
    square_file_name = 'temp2.png'

    # 获取原始截图
    driver.get_screenshot_as_file(png_file_name)


    # 取中间
    img = Image.open(png_file_name)
    w, h = img.size
    w2 = w - 250
    h2 = h - 90
    w3 = h2
    h3 = h2
    w_shift = int(((w2 - w3) / 2 + 250) * -1)
    h_shift = -89
    result = Image.new(img.mode, (w3, h3))
    result.paste(img, box=(w_shift, h_shift))
    # 缩小样本
    result = result.resize((512,512),Image.ANTIALIAS)
    result.save(square_file_name,quality=100)

    # cv读图像
    img = cv.imread(square_file_name, 0)
    xy = np.where(img == 254, 1, 0)  # 检测白色部分
    new_xy = np.array(xy)
    new_xy = new_xy.flatten()
    sum = 0
    for k in range(len(new_xy)):
        sum = sum + new_xy[k]
    num = len(new_xy)

    density = sum / num
    return density




# 加启动配置

city = "南京"

option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
    )
#option.add_argument('user-agent=%s'%user_agent)
#p=r'C:\Users\jscss\AppData\Local\Google\Chrome\User Data\Default'
#option.add_argument('--user-data-dir='+p)  # 设置成用户自己的数据目录
#option.add_argument("user-data-dir=selenium")
#option.add_extension(r'C:\Users\jscss\Downloads\install\install.crx')  # 自己下载的crx路径
#return webdriver.Chrome(chrome_options = option,desired_capabilities = None)
option.add_experimental_option('excludeSwitches', ['enable-automation'])# 模拟真正浏览器

# 打开chrome浏览器
print("正在加载网页...")
driver = webdriver.Chrome(options=option)
driver.get("https://lbs.amap.com/dev/mapstyle/index")
driver.maximize_window()

#driver.find_element_by_class_name('sign_up').click()
wait = WebDriverWait(driver, 10)
first_result = wait.until(presence_of_element_located((By.NAME, "userName")))
print(first_result)
driver.find_element_by_name('userName').send_keys("yourUserName" )
driver.find_element_by_name('password').send_keys("yourPassword" )
print("请滑动滑块并点击登录")
wait = WebDriverWait(driver, 600)
xpath_map = '//*[@id="react-root"]/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]'
# wait.until(presence_of_element_located((By.XPATH, xpath_map)))i
time.sleep(1)
#time.sleep(1)
#driver.find_element_by_xpath(xpath_map).click()
print("请单击你要使用的地图")
flag = True

#argv = sys.argv[1]
#argv = str(argv)
#argv = argv.split(",")
#argv_count = 0
while flag:

    city = input("您搜索的城市名称为:\n")
    #city = argv[argv_count]
    #argv_count += 1


    df = pd.read_csv(fr"data/metro/{city}/data_{city}地铁.csv")
    lon_list = df['lon'].tolist()
    lat_list = df['lat'].tolist()
    start = input("从第几个开始？\n")
    end = input("第几个结束?(不包含)\n")
    #start = argv[argv_count]
    #argv_count += 1
    #end = argv[argv_count]
    #argv_count += 1

    if start == "":
        start = 0
    else:
        start = int(start)
    if end == "":
        end = len(lon_list)
    else:
        end = int(end)
    # 读取文件 data_city.csv  地铁站信息


    img_type = input("作为训练集[A]还是[B]？\n")
    #img_type = argv[argv_count]
    #argv_count += 1

    img_type = img_type.upper()


    folder_path = os.path.abspath('.')
    folder_path = f"./output/img/{img_type}/"
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path,exist_ok=True)
    if img_type == "A":
        with open(folder_path + "density.txt", 'w', encoding='utf-8') as f:
            f.write("density\n")

        cal_den = True
    else:

        cal_den = False
    print("文件将保存在", folder_path)
    sleep_time = 2.6
    #sleep_time = float(argv[argv_count])
    #argv_count += 1
    #sleep_time =  float(input("sleeptime"))
    # print("sleep_time=",sleep_time)


    # xpath_level = "//*[@id=\"main-map\"]/div[3]/div/div[2]/input"
    #xpath_level = '<canvas class ="amap-layer"'
    #wait.until(presence_of_element_located((By.XPATH, xpath_level)))
    #print("30s后开始爬取")
    print("您有30s的时间将道路节点的文字透明度设为0")
    for i in range(30):
        print(30-i)
        time.sleep(1)

    ifrun = input("开始运行?y/n\n")
    #ifrun = argv[argv_count]
    #argv_count += 1
    if ifrun == "y":
        #driver.find_element_by_class_name('user_item console_enter').click()

        xpath_level = "//*[@id=\"main-map\"]/div[3]/div/div[2]/input"
        xpath_lon = "//*[@id=\"react-root\"]/div/div[1]/div[4]/input[1]"
        xpath_lat = "//*[@id=\"react-root\"]/div/div[1]/div[4]/input[2]"
        driver.find_element_by_xpath(xpath_level).send_keys(Keys.CONTROL + "a")
        pyperclip.copy('16.8')
        driver.find_element_by_xpath(xpath_level).send_keys(Keys.CONTROL + "v")
        driver.find_element_by_xpath(xpath_level).send_keys(Keys.RETURN)
        time.sleep(1)



        for i in range(start,end):
            print(i)
            #driver.find_element_by_xpath(xpath_level).send_keys(Keys.CONTROL + "a")
            #pyperclip.copy('13')
            #driver.find_element_by_xpath(xpath_level).send_keys(Keys.CONTROL + "v")
            #driver.find_element_by_xpath(xpath_level).send_keys(Keys.RETURN)
            #time.sleep(1)

            driver.find_element_by_xpath(xpath_lon).send_keys(Keys.CONTROL + "a")
            pyperclip.copy(str(lon_list[i]))
            driver.find_element_by_xpath(xpath_lon).send_keys(Keys.CONTROL + "v")

            driver.find_element_by_xpath(xpath_lat).send_keys(Keys.CONTROL + "a")
            pyperclip.copy(str(lat_list[i]))
            driver.find_element_by_xpath(xpath_lat).send_keys(Keys.CONTROL + "v")



            #driver.find_element_by_xpath(xpath_level).send_keys(Keys.CONTROL + "a")
            #driver.find_element_by_xpath(xpath_level).send_keys("16.8" + Keys.RETURN)
            STR_READY_STATE = ''
            if i == 0:
                dis = 9999
                time.sleep(2)#第一次额外多暂停2s
            else:
                dis = math.sqrt((lon_list[i]-lon_list[i-1])**2+(lat_list[i]-lat_list[i-1])**2)
            print(dis)

            if dis > 0.02:
                time.sleep(sleep_time)
            else:
                time.sleep(sleep_time/1.5)
            try:
                if cal_den == True:
                    density = 0
                    for k in range(2):#定义重复次数
                        density = cal_density2()
                        print("density: ",density)
                        if density != 0:
                            break
                        else:
                            time.sleep(0.5)#定义重复间隔
                else:
                    cal_density2()

                from_path = 'temp2.png'
                to_path = folder_path + str(i)+".png"
                copy(from_path, to_path)#将临时文件复制到保存文件夹
                print("文件已保存到",to_path)
                if cal_den == True:
                    with open(folder_path+"density.txt", 'a', encoding='utf-8') as f:
                        f.write(str(density) + "\n")


            except BaseException as msg:
                print(msg)

    #if argv[argv_count] != "y":
    if input("继续？y/n\n") != "y":
        flag = False
        driver.quit()

driver.quit()