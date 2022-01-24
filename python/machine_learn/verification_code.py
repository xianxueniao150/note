#爬取图片代码

from selenium import webdriver
from PIL import Image
from PIL import ImageDraw
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time,re
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--window-size=2000,1000")
def switch_window(driver, now):
    all_handles = driver.window_handles                #得到当前开启的所有窗口的句柄
    for handle in all_handles:
        if handle != now:                              #获取到与当前窗口不一样的窗口
            driver.switch_to.window(handle)
driver = webdriver.Chrome(options=chrome_options)
driver.get('htp://sso.hq.cpic.com/login')
#登录
userCode=driver.find_element_by_id('username')
userCode.send_keys('xubeijie')
password=driver.find_element_by_id('password')
password.send_keys('xxxxx')
num=1
for i in range(120,160):
    kanbuqing = driver.find_element_by_id('aaa')
    kanbuqing.click()
    time.sleep(2)
    driver.get_screenshot_as_file('ascreenshot.png')
    # location = driver.find_elements_by_tag_name('table')[6].find_element_by_css_selector('tr:nth-child(5)').location
    # size = driver.find_elements_by_tag_name('table')[6].find_element_by_css_selector('tr:nth-child(5)').size
    # left = location['x'] + size['width'] * 1.08
    # top = location['y'] + size['height'] * 1.9
    # right = location['x'] + size['width'] * 1.25
    # bottom = location['y'] + size['height'] * 3
    # print(left, top, right, bottom)
    im = Image.open('ascreenshot.png')
    im = im.crop((1084.5,273,1140,293))
    im.save('images\%s.png' % str(i))







#训练代码

from PIL import Image
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import joblib
# from sklearn.neural_network import MLPClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.svm import SVC
from os import listdir

x=[]
y=[]
mum=0
txt=pd.read_csv(r'C:\Users\Lenovo\Desktop\xunlian2.csv',
                header=None)
print(txt.iloc[1, 0]+1)
for i in range(160):
    for j in range(0, len(txt)):
        if (str(i+1))==str(txt.iloc[j, 0]) and str(txt.iloc[j, 1]) is not None and len(str(txt.iloc[j, 1]))==4:
            print(txt.iloc[j, 1])
            y.extend(str(txt.iloc[j, 1]))
            mum=mum+1
            print(mum)
            image = Image.open('images\\'+str(i+1)+ '.png')
            print(image.size)
            # image = image.resize((67, 23))
            source = image.split()  # 分隔RGB三通道颜色的副本
            image = source[1]
            # image = image.convert("L")
            threshold = 120
            table = []
            for k in range(256):
                if k < threshold:
                    table.append(0)
                else:
                    table.append(1)
            # #通过表格转换成二进制图片，1的作用是白色，不然就全部黑色了
            image = image.point(table, "1")
            im1 = image.crop((1, 0, 14, 20))
            im2 = image.crop((15, 0, 28, 20))
            im3 = image.crop((29, 0, 42, 20))
            im4 = image.crop((43, 0, 56, 20))
            pix1 = np.asarray(im1)
            pix2 = np.asarray(im2)
            pix3= np.asarray(im3)
            pix4 = np.asarray(im4)
            x.append(pix1.reshape(13 * 20))
            x.append(pix2.reshape(13 * 20))
            x.append(pix3.reshape(13 * 20))
            x.append(pix4.reshape(13 * 20))

x=np.asarray(x)
y=np.asarray(y)


# tree=DecisionTreeClassifier()
# tree.fit(x,y)
# joblib.dump(tree, './tree.pkl')
# svc=SVC()
# svc.fit(x,y)
# joblib.dump(svc, './svc.pkl')
knn=KNeighborsClassifier()
knn.fit(x,y)
joblib.dump(knn, './knn.pkl')



#识别代码

from PIL import Image
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import joblib
knn = joblib.load('knn.pkl')
    # pre_y_test = clf.predict(x)
    # print pre_y_test

z=[]
# co 4d41  co1 2kdk  co2   2a61
#  734  6; 322   4;  497 6; 907:6
for i in range(20):
    image = Image.open('images2\\'+'%s.png' % str(i))  # 将图片转成字符串
    # image = image.resize((67, 23))
    source=image.split()  #分隔RGB三通道颜色的副本
    image=source[1]
    # image = image.conv       ert("L")
    threshold = 120
    table = []

    for i in  range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # #通过表格转换成二进制图片，1的作用是白色，不然就全部黑色了
    image = image.point(table,"1")
    print(image.size)
    im1 = image.crop((1, 0, 14, 20))
    im2 = image.crop((15, 0, 28, 20))
    im3 = image.crop((29, 0, 42, 20))
    im4 = image.crop((43, 0, 56, 20))
    pix1 = np.asarray(im1)
    pix2 = np.asarray(im2)
    pix3= np.asarray(im3)
    pix4 = np.asarray(im4)
    # im1.save("im1.png")
    # im2.save("im2.png")
    # im3.save("im3.png")
    # im4.save("im4.png")
    z.append(pix1.reshape(13 * 20))
    z.append(pix2.reshape(13 * 20))
    z.append(pix3.reshape(13 * 20))
    z.append(pix4.reshape(13 * 20))
    z=np.asarray(z)
    output=knn.predict(z)
    print(output)
    z=[]
    im1.save("im1.png")
    im2.save("im2.png")
    im3.save("im3.png")
    im4.save("im4.png")t
