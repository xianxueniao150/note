# selenium基本操作
#导入selenium包
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#设置浏览器为无头模式并设置浏览器窗口大小
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--window-size=2000,1000")
driver = webdriver.Chrome(options=self.chrome_options)

#登录网页
driver.get('http://sso.hq.cpic.com/login')
#通过id寻找网页元素
userCode = self.driver.find_element_by_id('username')
#向文本框中输入内容
userCode.send_keys('xubeijie')
#通过css选择器寻找网页元素
submit = self.driver.find_elements_by_css_selector('.zw')[7]
#模拟鼠标单击动作
submit.click()
#通过链接文字寻找网页元素
senhe = self.driver.find_element_by_link_text('审核管理')
#模拟鼠标双击动作
ActionChains(driver).double_click(senhe).perform()
#找到并关闭警告框
driver.switch_to.alert.accept()
#进入子页面，子页面一般是通过D进行定位
driver.switch_to.frame('iframepage')

标签页切换
#新打开标签页后，切换标签页，此函数适合整个工作只涉及两个标签页，当标签页多于两个时，需要用下面一个函数。
def switch_window(self, now):
    all_handles = self.driver.window_handles    #得到当前开启的所有窗口的句柄
    for handle in all_handles:
        if handle != now:  # 获取到与当前窗口不一样的窗口
            self.driver.switch_to.window(handle)
# 此函数的意思是先关闭当前标签页，再转到下一个标签页
def switch_window2(self, now):
all_handles = self.driver.window_handles  
for handle in all_handles:
    if handle != now:  
        self.driver.close()
        self.driver.switch_to.window(handle)



import traceback
import logging
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import datetime
import re
import pandas as pd



#日志位置，记录失败及成功的单子，每次跑之前需要修改，修改为运行当天的日期
logfile='20200226.log'
#从第几单开始跑，正常就是2，如果中间断了，接着断着跑的话，就通过查看日志修改为紧接着断的那一单
num=217
#文件名
file_name='shangyexian0226.xlsx'

zhanghao="007667"
mima="A123456f"
chejia="LEFYEDG46HHN78459"


class BigThingThread():
    def __init__(self):
        self.bianhao = pd.Series([11, 12, 13, 21, 22, 23, 31, 32, 33, 34, 41, 51, 52, 61, 62, 63,
                             71, 72, 73, 74, 75, 81, 82, 83, 84, 85, 86, 87, 91, 92, 93, 94])
        self.again = 0
        self.criti=0

    def run(self):
        dataframe = pd.read_excel(r'C:\Users\rpa3\Desktop\ludan\{}'.format(file_name))
        self.driver = webdriver.Ie()

        # self.zhanghao=dataframe.loc[0, "账号"][2:]
        self.zhanghao=zhanghao
        # self.mima=dataframe.loc[0, "密码"]
        self.mima=mima
        # self.need_to_copy=dataframe.loc[0, "第一单车牌号"]
        self.need_to_copy=chejia

        self.submit_copy()
        i=5

        print(i)
        self.yewulaiyuan=2
        self.jingbanren="ss"
        self.dailidian="dd";
        self.chudengdate = str(dataframe.loc[i, "初登时间"])
        self.qibaodate = str(dataframe.loc[i, "起保时间"])
        self.chepaihao = dataframe.loc[i, "车牌号"]
        print(self.chepaihao)
        self.fadongjihao = dataframe.loc[i, "发动机号"]
        self.chejiahao = dataframe.loc[i, "车架号"]
        self.shijijiazhi = str(dataframe.loc[i, "协商实际价值"])
        self.shiyongxingzhi = dataframe.loc[i, "使用性质代码"]
        self.zhekou = str(dataframe.loc[i, "折扣"])
        self.zhongzhiriqi = str(dataframe.loc[i, "终止时间"])
        if i == 0:
            self.again = 0
        print(datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
        self.fillIn_AutoComprenhensive(i)
        logging.error('第{0}条数据{1}录入成功' .format(i,self.chepaihao))
        if i != len(dataframe) - 1:
            if self.criti==0:
                self.copy()
            else:
                self.copy2()
        with open("test19.txt", "w") as f:
            f.write(self.driver.page_source.encode("gbk", 'ignore').decode("gbk", "ignore"))
        self.again = 1

    # 切换窗口
    def switch_window(self, now):
        all_handles = self.driver.window_handles  # 得到当前开启的所有窗口的句柄
        for handle in all_handles:
            if handle != now:  # 获取到与当前窗口不一样的窗口
                self.driver.switch_to.window(handle)

    def switch_window2(self, now):
        all_handles = self.driver.window_handles  # 得到当前开启的所有窗口的句柄
        for handle in all_handles:
            if handle != now:  # 获取到与当前窗口不一样的窗口
                self.driver.close()
                self.driver.switch_to.window(handle)

    def submit_copy(self):
        self.driver.get('http://10.190.48.197:8080/document-web/login;jsessionid=E327BDAAEB338F238FD03394CF679F6F')
        branchCode = self.driver.find_element_by_id("companycode")
        branchCode.send_keys('4020100')
        userCode = self.driver.find_element_by_id("userid")
        userCode.send_keys(self.zhanghao)
        password = self.driver.find_element_by_id("_password")
        password.send_keys(self.mima)
        submit = self.driver.find_element_by_id('login')
        submit.click()
        time.sleep(3)
        self.driver.switch_to.frame('iframepage')
        datagrid = self.driver.find_element_by_id("datagrid-row-r1-2-1")
        ActionChains(self.driver).double_click(datagrid).perform()
        time.sleep(3)
        skipId = self.driver.find_element_by_id("recorde")
        skipId.click()
        time.sleep(3)
        now = self.driver.current_window_handle
        self.switch_window2(now)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'SubButton')))
        time.sleep(3)
        # 找到录入按钮
        self.driver.maximize_window()
        luru = self.driver.find_elements_by_xpath('//*[@class="SubButton"]')[0]
        luru.click()
        # # 切换到页面子框架
        # time.sleep(2)
        self.driver.switch_to.frame("centerContentFrame")

        #交强险录入
        # content4 = self.driver.find_element_by_xpath('//*[@id="Image4"]')
        #综合险录入
        content4 = self.driver.find_element_by_xpath('//*[@id="Image6"]')
        content4.click()


        time.sleep(6)
        # 续保信息
        xubao = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[1]
        xubao.click()

        #是否同时续保交强险
        self.waitealert()

        # __frame___control_16186_1583227981380
        pattern = re.compile(r'__frame___control_[0-9]*_[0-9]*')  # re.I 表示忽略大小写
        try:
            time.sleep(1)
            m = pattern.findall(self.driver.page_source)[0]
        except:
            try:
                time.sleep(1)
                m = pattern.findall(self.driver.page_source)[0]
            except:
                time.sleep(1)
                m = pattern.findall(self.driver.page_source)[0]

        print(m)
        self.driver.switch_to.frame(m)

        # 录入车架号
        carVIN=self.driver.find_element_by_id("formVehicle_editor_carVIN")
        carVIN.send_keys(self.need_to_copy)

        search=self.driver.find_element_by_id("search")
        search.click()

        copy=self.driver.find_element_by_id("copy")
        copy.click()
        self.driver.switch_to.parent_frame()

        # self.waitealert()
        time.sleep(2)
        comfirm=self.driver.find_element_by_id("comfirm")
        comfirm.click()
        # time.sleep(5)


    def fillIn_basicInfo(self,i):
        ##基本信息
        if self.again != 0:
            try:
                time.sleep(1)
                basicinfo = self.driver.find_elements_by_xpath('//*[@class="Tab_top"]')[0]
                basicinfo.click()
            except:
                time.sleep(1)
                basicinfo = self.driver.find_elements_by_xpath('//*[@class="Tab_top"]')[0]
                basicinfo.click()

        # 业务来源
        SELLINGCHANNEL = self.driver.find_element_by_id('basicinfo$formAutoComprenhensive2007_editor_SELLINGCHANNEL')
        SELLINGCHANNEL.click()
        for i in range(self.yewulaiyuan):
            SELLINGCHANNEL.send_keys(Keys.DOWN)
        SELLINGCHANNEL.send_keys(Keys.ENTER)

        # 经办人
        agentName = self.driver.find_element_by_id('basicinfo$editorAgentName')
        agentName.send_keys(self.jingbanren)

        # 代理点
        editorAgency = self.driver.find_element_by_id('basicinfo$editorAgency')
        editorAgency.send_keys(self.dailidian)

        '''
           #统保代码
           t = time.time()
           print(int(round(t * 1000)))
           tongbaodaima=driver.find_element_by_id('basicinfo$formTrafficCompulsory2007_editor_UNIFORMINSURANCECODEFORVIEW')
           tongbaodaima.click()
           DropDownButton=driver.find_elements_by_class_name('DropDownButton')[1]
           DropDownButton.click()
           driver.switch_to.frame("dropdownTongbaoMultiSel$X3")
           yibanyewu=driver.find_element_by_id('__control_10005')
           yibanyewu.click()
           input=driver.find_element_by_id('inputFilterValue')
           input.send_keys('01248')
           filter=driver.find_element_by_id('filterButton')
           filter.click()
           filter2=driver.find_element_by_id('__control_10007')
           filter2.click()
           buttonOK=driver.find_element_by_id('buttonOK')
           buttonOK.click()
           driver.switch_to.parent_frame()
       '''

        # 商业险起保日期
        shangqibaoriqi = self.driver.find_element_by_id(
            'basicinfo$formAutoComprenhensive2007_editor_inceptionDate')
        shangqibaoriqi.click()
        shangqibaoriqi.clear()
        shangqibaoriqi.send_keys(self.qibaodate)

        # 商业险终止日期
        shangqibaoriqi = self.driver.find_element_by_id('basicinfo$formAutoComprenhensive2007_editor_terminationDate')
        shangqibaoriqi.click()
        shangqibaoriqi.clear()
        shangqibaoriqi.send_keys(self.zhongzhiriqi)

        # 支付方式
        payWay = self.driver.find_element_by_id('basicinfo$formAutoComprenhensive2007_editor_payWay')
        payWay.send_keys(Keys.UP)
        payWay.send_keys(Keys.ENTER)

    def fillIn_customerInfo(self):
        customerinfo = self.driver.find_elements_by_xpath('//*[@class="Tab_top"]')[0]
        customerinfo.click()

    #投保人
        #投保人代码
        editorApplicantCode=self.driver.find_element_by_id("customerinfo$editorApplicantCode")
        eac=editorApplicantCode.get_attribute("value")

        #投保人姓名
        editor_NAME1=self.driver.find_element_by_id("customerinfo$formAutoComprenhensive2007_editor_NAME1")
        editor_NAME1.get_attribute("value")

        #邮政编码
        POSTALCODE1=self.driver.find_element_by_id("customerinfo$formAutoComprenhensive2007_editor_POSTALCODE1")

        #地址
        ADDRESS1=self.driver.find_element_by_id("customerinfo$formAutoComprenhensive2007_editor_ADDRESS1")

        #移动电话
        TELEPHONE1=self.driver.find_element_by_id("customerinfo$formAutoComprenhensive2007_editor_TELEPHONE1")
        TELEPHONE1.send_keys()

        if True:
            #新增投保人
            # 投保人代码查询
            buttonApplicant = self.driver.find_element_by_id('customerinfo$buttonApplicant')
            buttonApplicant.click()
            pattern = re.compile(r'__frame___control_[0-9]*_[0-9]*')  # re.I 表示忽略大小写
            m = pattern.findall(self.driver.page_source)[0]
            print(m)
            self.driver.switch_to.frame(m)
            #客户类型
            customerType = self.driver.find_element_by_id('customerForm_editor_customerType')
            customerType.click()
            for i in range(self.tcustomerType):
                customerType.send_keys(Keys.DOWN)
            customerType.send_keys(Keys.ENTER)
            # 客户名称
            customerName = self.driver.find_element_by_id('customerForm_editor_customerName')
            customerName.send_keys(self.tcustomerName)
            # 证件类型
            certitfcateType = self.driver.find_element_by_id('customerForm_editor_certitfcateType')
            certitfcateType.click()
            for i in range(self.tcertitfcateType):
                certitfcateType.send_keys(Keys.DOWN)
            certitfcateType.send_keys(Keys.ENTER)
            # 证件号码
            certitfcateCode = self.driver.find_element_by_id('customerForm_editor_certitfcateCode')
            certitfcateCode.send_keys(self.tcertitfcateCode)
            # 电子邮箱
            emailAddress = self.driver.find_element_by_id('customerForm_editor_emailAddress')
            emailAddress.send_keys(self.temailAddress)
            # 移动电话
            phoneNumber = self.driver.find_element_by_id('customerForm_editor_phoneNumber')
            phoneNumber.send_keys(self.tphoneNumber)
            # 联系地址
            registAddress = self.driver.find_element_by_id('customerForm_editor_registAddress')
            registAddress.send_keys(self.tregistAddress)
            buttonQuery = self.driver.find_element_by_id('buttonQuery')
            buttonQuery.click()
            # 新增
            buttonSave = self.driver.find_element_by_id('buttonSave')
            buttonSave.click()
            # 双击确定
            ok = self.driver.find_element_by_xpath('//*[@id="customerTable$CT"]//*[@class="TextCell"]')
            # TextCell
            ActionChains(self.driver).double_click(ok).perform()
            self.driver.switch_to.parent_frame()
            time.sleep(2)

        # 车辆与投保人关系
        NATURETYPE = self.driver.find_element_by_id('customerinfo$formAutoComprenhensive2007_editor_NATURETYPE1')
        NATURETYPE.click()
        for i in range(self.cltbr):
            NATURETYPE.send_keys(Keys.DOWN)
        NATURETYPE.send_keys(Keys.ENTER)

        # 法人客户类型
        self.frkhlist = pd.Series([1, 2, 3, 4, 5, 6, 7])

        LEGALCUSTOMERTYPE = self.driver.find_element_by_id(
            'customerinfo$formAutoComprenhensive2007_editor_LEGALCUSTOMERTYPE')
        LEGALCUSTOMERTYPE.click()
        cursor_selected = self.driver.find_element_by_xpath(
            '//*[@id="dropdownLeaglCentificateType$E9$CT"]//tr[@class="CurrentRow"]/td/div').get_attribute(
            "title")
        self.choose_selectlist(cursor_selected, LEGALCUSTOMERTYPE, self.frkhlist, 1)

        # 是否勾选被保险人开票
        editor_ISSUEINVOICE = self.driver.find_element_by_id(
            "customerinfo$formAutoComprenhensive2007_editor_ISSUEINVOICE")
        print(editor_ISSUEINVOICE.is_selected())
        if editor_ISSUEINVOICE.is_selected() != self.gxkp:
            editor_ISSUEINVOICE.click()
        print("是否勾选被保险人开票")
        print(editor_ISSUEINVOICE.is_selected())

        # # 增值税发票
        IFSPECIALTICKET = self.driver.find_element_by_id(
            'customerinfo$formAutoComprenhensive2007_editor_IFSPECIALTICKET')
        IFSPECIALTICKET_value = IFSPECIALTICKET.get_attribute("value")
        if (self.zzsfp != IFSPECIALTICKET_value):
            IFSPECIALTICKET.click()
            if (IFSPECIALTICKET_value == "普票"):
                IFSPECIALTICKET.send_keys(Keys.DOWN)
            else:
                IFSPECIALTICKET.send_keys(Keys.UP)


     ##被保险人

        #被保险人代码
        editorInsuredCode=self.driver.find_element_by_id('customerinfo$editorInsuredCode')

        #被保险人名称
        editorNAME2=self.driver.find_element_by_id('customerinfo$editorNAME2')


        #邮箱
        EMAIL2=self.driver.find_element_by_id('customerinfo$formAutoComprenhensive2007_editor_EMAIL2')

        #移动电话
        TELEPHONE2=self.driver.find_element_by_id("customerinfo$formAutoComprenhensive2007_editor_TELEPHONE2")

        #地址
        editor_ADDRESS2=self.driver.find_element_by_id("customerinfo$formAutoComprenhensive2007_editor_ADDRESS2")

        #邮政编码
        POSTALCODE2=self.driver.find_element_by_id("customerinfo$formAutoComprenhensive2007_editor_POSTALCODE2")


        if True:
            #新增被保人
            # 被保险人代码
            buttonApplicant = self.driver.find_element_by_id('customerinfo$buttonApplicant')
            buttonApplicant.click()
            pattern = re.compile(r'__frame___control_[0-9]*_[0-9]*')  # re.I 表示忽略大小写
            m = pattern.findall(self.driver.page_source)[0]
            print(m)
            self.driver.switch_to.frame(m)
            # 客户类型
            customerType = self.driver.find_element_by_id('customerForm_editor_customerType')
            customerType.click()
            for i in range(self.bcustomerType):
                customerType.send_keys(Keys.DOWN)
            customerType.send_keys(Keys.ENTER)
            # 客户名称
            customerName = self.driver.find_element_by_id('customerForm_editor_customerName')
            customerName.send_keys(self.bcustomerName)
            # 证件类型
            certitfcateType = self.driver.find_element_by_id('customerForm_editor_certitfcateType')
            certitfcateType.click()
            for i in range(self.bcertitfcateType):
                certitfcateType.send_keys(Keys.DOWN)
            certitfcateType.send_keys(Keys.ENTER)
            # 证件号码
            certitfcateCode = self.driver.find_element_by_id('customerForm_editor_certitfcateCode')
            certitfcateCode.send_keys(self.bcertitfcateCode)
            # 电子邮箱
            emailAddress = self.driver.find_element_by_id('customerForm_editor_emailAddress')
            emailAddress.send_keys(self.bemailAddress)
            # 移动电话
            phoneNumber = self.driver.find_element_by_id('customerForm_editor_phoneNumber')
            phoneNumber.send_keys(self.bphoneNumber)
            # 联系地址
            registAddress = self.driver.find_element_by_id('customerForm_editor_registAddress')
            registAddress.send_keys(self.bregistAddress)
            buttonQuery = self.driver.find_element_by_id('buttonQuery')
            buttonQuery.click()
            # 新增
            buttonSave = self.driver.find_element_by_id('buttonSave')
            buttonSave.click()
            # 双击确定
            ok = self.driver.find_element_by_xpath('//*[@id="customerTable$CT"]//*[@class="TextCell"]')
            # TextCell
            ActionChains(self.driver).double_click(ok).perform()
            self.driver.switch_to.parent_frame()
            time.sleep(2)


        # 车辆与被保险人关系
        NATURETYPE2 = self.driver.find_element_by_id('customerinfo$formAutoComprenhensive2007_editor_NATURETYPE2')
        NATURETYPE2.click()
        for i in range(self.clbbr):
            NATURETYPE2.send_keys(Keys.DOWN)
        NATURETYPE2.send_keys(Keys.ENTER)

        # 法人客户类型
        LEGALCUSTOMERTYPE2 = self.driver.find_element_by_id(
            'customerinfo$formAutoComprenhensive2007_editor_LEGALCUSTOMERTYPE2')
        LEGALCUSTOMERTYPE2.click()
        cursor_selected = self.driver.find_element_by_xpath(
            '//*[@id="dropdownLeaglCentificateType$E9$CT"]//tr[@class="CurrentRow"]/td/div').get_attribute(
            "title")
        self.choose_selectlist(cursor_selected, LEGALCUSTOMERTYPE2, self.frkhlist, 1)

        #客户标识
        CUSTOMERLEVEL=self.driver.find_element_by_id("customerinfo$formAutoComprenhensive2007_editor_CUSTOMERLEVEL")
        CUSTOMERLEVEL.click()
        for i in range(self.khbs):
            CUSTOMERLEVEL.send_keys(Keys.DOWN)
        CUSTOMERLEVEL.send_keys(Keys.ENTER)

    #索赔权益人
        #索赔权益人代码
        editorCliamant=self.driver.find_element_by_id("customerinfo$editorCliamant")

        #索赔权益人名称
        editorNAME3=self.driver.find_element_by_id("customerinfo$editorNAME3")

        if True:
            #新增
            buttonCliamant=self.driver.find_element_by_id("customerinfo$buttonCliamant")
            buttonCliamant.click()
            pattern = re.compile(r'__frame___control_[0-9]*_[0-9]*')  # re.I 表示忽略大小写
            m = pattern.findall(self.driver.page_source)[0]
            print(m)
            self.driver.switch_to.frame(m)
            # 客户类型
            customerType = self.driver.find_element_by_id('customerForm_editor_customerType')
            customerType.click()
            for i in range(self.scustomerType):
                customerType.send_keys(Keys.DOWN)
            customerType.send_keys(Keys.ENTER)
            # 客户名称
            customerName = self.driver.find_element_by_id('customerForm_editor_customerName')
            customerName.send_keys(self.scustomerName)
            # 证件类型
            certitfcateType = self.driver.find_element_by_id('customerForm_editor_certitfcateType')
            certitfcateType.click()
            for i in range(self.scertitfcateType):
                certitfcateType.send_keys(Keys.DOWN)
            certitfcateType.send_keys(Keys.ENTER)
            # 证件号码
            certitfcateCode = self.driver.find_element_by_id('customerForm_editor_certitfcateCode')
            certitfcateCode.send_keys(self.scertitfcateCode)
            # 电子邮箱
            emailAddress = self.driver.find_element_by_id('customerForm_editor_emailAddress')
            emailAddress.send_keys(self.semailAddress)
            # 移动电话
            phoneNumber = self.driver.find_element_by_id('customerForm_editor_phoneNumber')
            phoneNumber.send_keys(self.sphoneNumber)
            # 联系地址
            registAddress = self.driver.find_element_by_id('customerForm_editor_registAddress')
            registAddress.send_keys(self.sregistAddress)
            buttonQuery = self.driver.find_element_by_id('buttonQuery')
            buttonQuery.click()
            # 新增
            buttonSave = self.driver.find_element_by_id('buttonSave')
            buttonSave.click()
            # 双击确定
            ok = self.driver.find_element_by_xpath('//*[@id="customerTable$CT"]//*[@class="TextCell"]')
            # TextCell
            ActionChains(self.driver).double_click(ok).perform()
            self.driver.switch_to.parent_frame()
            time.sleep(2)

    def choose_selectlist(self, cursor_selected, clickButton, list, fill_item):
        diff = (list[list[:].isin([int(cursor_selected)])].index)[0] - \
               (list[list[:].isin([int(fill_item)])].index)[0]
        if diff > 0:
            for i in range(diff):
                clickButton.send_keys(Keys.UP)
        elif diff < 0:
            for i in range(abs(diff)):
                clickButton.send_keys(Keys.DOWN)
        clickButton.send_keys(Keys.ENTER)


    def fillIn_vehicalInfo(self):
        ##车辆信息
        vehicalinfo = self.driver.find_elements_by_xpath('//*[@class="Tab_top"]')[1]
        vehicalinfo.click()

        #车主名称
        ICENSEOWNER=self.driver.find_element_by_id('vehicleinfo$editorLICENSEOWNER')

        # 性质
        NatureType=self.driver.find_element_by_id('vehicleinfo$editOwnerNatureType')


        self.zhengjian=pd.Series([1,6,10,11,12,13,14,15,16,17,2,3,4,8,9])
        #证件类型
        CERTIFICATETYPE=self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_OWNERCERTIFICATETYPE')
        CERTIFICATETYPE.click()
        cursor_selected = self.driver.find_element_by_xpath(
            '//*[@id="dropdownCentificateTypeAdd$E9$CT"]//tr[@class="CurrentRow"]/td/div').get_attribute(
            "title")
        self.choose_selectlist(cursor_selected,CERTIFICATETYPE,self.zhengjian,1)


        # 证件号码
        CERTIFICATECODE = self.driver.find_element_by_id(
            'vehicleinfo$formAutoComprenhensive2007_editor_OWNERCERTIFICATECODE')

        # 号牌号码
        licensenum = self.driver.find_element_by_id('vehicleinfo$editorVehiclelicense')
        licensenum.clear()
        licensenum.send_keys(self.chepaihao)

        # 发动机号
        ENGINENO = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_ENGINENO')
        ENGINENO.clear()
        ENGINENO.send_keys(self.fadongjihao)

        # 核定载客量
        SEATCOUNT = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_SEATCOUNT')
        SEATCOUNT_value=SEATCOUNT.get_attribute("value")

        # 核定载质量
        CARRYINGCAPACITY = self.driver.find_element_by_id(
            'vehicleinfo$formAutoComprenhensive2007_editor_CARRYINGCAPACITY')
        CARRYINGCAPACITY_value=CARRYINGCAPACITY.get_attribute("value")

        # 整备质量
        EMPTYWEIGHT = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_EMPTYWEIGHT')
        EMPTYWEIGHT_value=EMPTYWEIGHT.get_attribute("value")


        # 车辆定型
        # 车型库
        CodeBtn = self.driver.find_element_by_id('vehicleinfo$shortCutCodeBtn')
        CodeBtn.click()
        # time.sleep(2)
        now = self.driver.current_window_handle
        self.switch_window(now)
        # 综合查询
        time.sleep(1)
        zonghechaxun = self.driver.find_element_by_link_text('综合查询')
        zonghechaxun.click()

        # 查询
        chaxun2 = self.driver.find_element_by_xpath('//*[@name="msbut"]')
        chaxun2.click()
        # 点击确认
        clickok = self.driver.find_element_by_xpath('//*[@title="单击返回数据"]')
        clickok.click()
        self.driver.switch_to.window(now)
        self.driver.switch_to.frame("centerContentFrame")

        time.sleep(1)

        try:
            self.waitealert()
        except:
            # logging.error("无警告")
            print("无弹窗")

        # 使用性质细分
        USAGE = self.driver.find_element_by_id('vehicleinfo$VEHICLEUSAGEDETAIL')
        USAGE.click()
        try:
            cursor_selected = self.driver.find_element_by_xpath(
                '//*[@id="vehicleinfo$dropdownVehicleUsageDetail$E9$CT"]//tr[@class="CurrentRow"]/td/div').get_attribute(
                "title")
        except Exception as e:
            print(e)
            time.sleep(1)
            try:
                cursor_selected = self.driver.find_element_by_xpath(
                    '//*[@id="vehicleinfo$dropdownVehicleUsageDetail$E9$CT"]//tr[@class="CurrentRow"]/td/div').get_attribute(
                    "title")
            except Exception as e:
                print(e)
                time.sleep(1)
                cursor_selected = self.driver.find_element_by_xpath(
                    '//*[@id="vehicleinfo$dropdownVehicleUsageDetail$E9$CT"]//tr[@class="CurrentRow"]/td/div').get_attribute(
                    "title")
        diff = (self.bianhao[self.bianhao[:].isin([int(cursor_selected)])].index)[0] - \
               (self.bianhao[self.bianhao[:].isin([int(self.shiyongxingzhi)])].index)[0]
        if diff > 0:
            for i in range(diff):
                USAGE.send_keys(Keys.UP)
        elif diff < 0:
            for i in range(abs(diff)):
                USAGE.send_keys(Keys.DOWN)
        USAGE.send_keys(Keys.ENTER)

        # 初次登记日期
        time.sleep(1)
        REGISTERDATE = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_REGISTERDATE')
        REGISTERDATE.click()
        REGISTERDATE.clear()
        REGISTERDATE.send_keys(self.chudengdate)

        # # 核定载客量
        # SEATCOUNT = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_SEATCOUNT')
        # SEATCOUNT_value2 = SEATCOUNT.get_attribute("value")
        #
        # # 核定载质量
        # CARRYINGCAPACITY = self.driver.find_element_by_id(
        #     'vehicleinfo$formAutoComprenhensive2007_editor_CARRYINGCAPACITY')
        # CARRYINGCAPACITY_value2= CARRYINGCAPACITY.get_attribute("value")
        #
        # # 整备质量
        # EMPTYWEIGHT = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_EMPTYWEIGHT')
        # EMPTYWEIGHT_value2 = EMPTYWEIGHT.get_attribute("value")

        # 核定载客量
        SEATCOUNT = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_SEATCOUNT')
        SEATCOUNT.clear()
        SEATCOUNT.send_keys(SEATCOUNT_value)

        # 核定载质量
        CARRYINGCAPACITY = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_CARRYINGCAPACITY')
        CARRYINGCAPACITY.clear()
        CARRYINGCAPACITY.send_keys(CARRYINGCAPACITY_value)

        # 整备质量
        EMPTYWEIGHT = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_EMPTYWEIGHT')
        EMPTYWEIGHT.clear()
        EMPTYWEIGHT.send_keys(EMPTYWEIGHT_value)

    def calcu_fee(self):
        # 自主渠道系数
        CHANNELRATE=self.driver.find_element_by_id("policyFloatingItem_editor_CHANNELRATE")

        # 自主核保系数
        UNDERWRITINGRATE=self.driver.find_element_by_id("policyFloatingItem_editor_UNDERWRITINGRATE")

        ##保费计算
        baofeijisuan = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[2]
        baofeijisuan.click()
        # time.sleep(2)
        # self.driver.switch_to.alert.accept()
        self.waitealert()
        self.waitealert()
        try:
            self.waitealert()
            print("警告")
        except:
            # logging.error("无警告")
            print("无警告")
        try:
            self.waitealert()
            print("警告")
        except:
            # logging.error("无警告")
            print("无警告")
        try:
            self.waitealert()
            print("警告")
        except:
            # logging.error("无警告")
            print("无警告")

        time.sleep(1)

        ##费率信息
        vehicalinfo = self.driver.find_elements_by_xpath('//*[@class="Tab_top"]')[2]
        vehicalinfo.click()
        zhekkou = self.driver.find_element_by_id('policyFloatingItem_editor_ACTUALDISCUTERATE')
        zhekkou.clear()
        zhekkou.send_keys(self.zhekou)
        time.sleep(1)

        ##保费计算
        baofeijisuan = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[2]
        # baofeijisuan = self.driver.find_elements_by_xpath('//*[@class="HotButton"]')[0]
        baofeijisuan.click()
        # time.sleep(2)
        # self.driver.switch_to.alert.accept()
        self.waitealert()
        self.waitealert()
        try:
            self.waitealert()
            print("警告")
        except:
            # logging.error("无警告")
            print("无警告")
        try:
            self.waitealert()
            print("警告")
        except:
            # logging.error("无警告")
            print("无警告")
        try:
            self.waitealert()
            print("警告")
        except:
            # logging.error("无警告")
            print("无警告")
        print("录单完成1")

    def fillIn_AutoComprenhensive(self,i):
        # self.fillIn_basicInfo(i)

        # self.fillIn_customerInfo(i)
        self.fillIn_vehicalInfo()




        # ##特别约定
        # vehicalinfo = self.driver.find_elements_by_xpath('//*[@class="Tab_top"]')[5]
        # vehicalinfo.click()
        # time.sleep(1)
        # self.driver.switch_to.frame("tabsetmain_specialclause")
        # zheadd = self.driver.find_element_by_id('buttonAdd')
        # zheadd.click()
        # time.sleep(1)
        # teyue = self.driver.find_element_by_id("SpecialClauseList$CT").find_element_by_tag_name(
        #     "tbody").find_element_by_tag_name("tr"). \
        #     find_element_by_tag_name("td")
        # teyue.click()
        # # with open("test12.txt", "w") as f:
        # #     f.write(self.driver.page_source.encode("gbk", 'ignore').decode("gbk", "ignore"))
        # teyue2 = self.driver.find_elements_by_class_name("ActiveTextEditor")[0]
        # teyue2.send_keys("本保单投保人为宿迁智远科技咨询有限公司；本保单无其他特别约定。")
        # self.driver.switch_to.parent_frame()
        with open("test16.txt", "w") as f:
            f.write(self.driver.page_source.encode("gbk", 'ignore').decode("gbk", "ignore"))
        time.sleep(1)
        ##预核保
        # yuhebao = self.driver.find_element_by_css_selector("#menubarmain > TBODY:nth-of-type(2) > TR:nth-of-type(1) > TD:nth-of-type(6) > DIV:nth-of-type(1) > TABLE:nth-of-type(1) > TBODY:nth-of-type(1) > TR:nth-of-type(1) > TD:nth-of-type(1)")
        try:
            yuhebao = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[3]
            yuhebao.click()
            self.waitealert()
            time.sleep(3)
            pattern = re.compile(r'__frame___control_[0-9]*_[0-9]*')  # re.I 表示忽略大小写
            try:
                time.sleep(1)
                m = pattern.findall(self.driver.page_source)[0]
            except:
                try:
                    time.sleep(1)
                    m = pattern.findall(self.driver.page_source)[0]
                except:
                    time.sleep(1)
                    m = pattern.findall(self.driver.page_source)[0]

            print(m)
            self.driver.switch_to.frame(m)
            time.sleep(2)
            try:
                buttonclose = self.driver.find_element_by_id('closeAutoUWResultButton')
            except:
                try:
                    time.sleep(1)
                    buttonclose = self.driver.find_element_by_id('closeAutoUWResultButton')
                except:
                    time.sleep(1)
                    buttonclose = self.driver.find_element_by_id('closeAutoUWResultButton')
            buttonclose.click()
            self.driver.switch_to.parent_frame()

            print("录单完成2")
            self.criti=0
        except Exception as e:
            with open("test17.txt", "w") as f:
                f.write(self.driver.page_source.encode("gbk", 'ignore').decode("gbk", "ignore"))
            time.sleep(1)
            print("玉荷包")
            print(e)
            yuhebao = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[3]
            # yuhebao = self.driver.find_elements_by_xpath('//*[@class="HotButton"]')[0]
            yuhebao.click()
            self.waitealert()
            time.sleep(3)
            pattern = re.compile(r'__frame___control_[0-9]*_[0-9]*')  # re.I 表示忽略大小写
            try:
                time.sleep(1)
                m = pattern.findall(self.driver.page_source)[0]
            except:
                try:
                    time.sleep(1)
                    m = pattern.findall(self.driver.page_source)[0]
                except:
                    time.sleep(1)
                    m = pattern.findall(self.driver.page_source)[0]

            print(m)
            self.driver.switch_to.frame(m)
            time.sleep(2)
            try:
                buttonclose = self.driver.find_element_by_id('closeAutoUWResultButton')
            except:
                try:
                    time.sleep(1)
                    buttonclose = self.driver.find_element_by_id('closeAutoUWResultButton')
                except:
                    time.sleep(1)
                    buttonclose = self.driver.find_element_by_id('closeAutoUWResultButton')
            buttonclose.click()
            self.driver.switch_to.parent_frame()

            print("录单完成22")
            self.criti=1

        ##暂存
        submint = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[7]
        submint.click()
        self.waitealert()
        self.waitealert()
        self.waitealert()
        self.waitealert()
        try:
            self.waitealert()
        except Exception as e:
            print(e)

        try:
            self.waitealert()
        except Exception as e:
            print(e)

        time.sleep(3)
        pattern = re.compile(r'__frame___control_[0-9]*_[0-9]*')  # re.I 表示忽略大小写
        try:
            time.sleep(1)
            m = pattern.findall(self.driver.page_source)[0]
        except:
            try:
                time.sleep(1)
                m = pattern.findall(self.driver.page_source)[0]
            except:
                time.sleep(1)
                m = pattern.findall(self.driver.page_source)[0]

        print(m)
        self.driver.switch_to.frame(m)
        try:
            buttonclose = self.driver.find_element_by_id('continueSubmit')
        except:
            try:
                time.sleep(1)
                buttonclose = self.driver.find_element_by_id('continueSubmit')
            except:
                time.sleep(1)
                buttonclose = self.driver.find_element_by_id('continueSubmit')
        buttonclose.click()
        self.driver.switch_to.parent_frame()

        print("录单完成4")
        self.waitealert()

        time.sleep(1)
        with open("test18.txt", "w") as f:
            f.write(self.driver.page_source.encode("gbk", 'ignore').decode("gbk", "ignore"))

    def fillIn_detailProduct(self):

        #第三者责任险
        THIRDPARTYLIABILITYCOVERAGE=self.driver.find_element_by_id("formTHIRDPARTYLIABILITYCOVERAGE_editor_THIRDPARTYLIABILITYCOVERAGE_select")
        print("第三者责任险")
        print(THIRDPARTYLIABILITYCOVERAGE.is_selected())

        saEditor2=self.driver.find_element_by_id("saEditor2")
        saEditor2.send_keys()

        #司机
        INCARDRIVERLIABILITYCOVERAGE=self.driver.find_element_by_id("formINCARDRIVERLIABILITYCOVERAGE_editor_INCARDRIVERLIABILITYCOVERAGE_select")
        print(INCARDRIVERLIABILITYCOVERAGE.is_selected())

        INCARDRIVERLIABILITYCOVERAGE_SUMINSURED=self.driver.find_element_by_id("formINCARDRIVERLIABILITYCOVERAGE_editor_INCARDRIVERLIABILITYCOVERAGE_SUMINSURED")
        INCARDRIVERLIABILITYCOVERAGE_SUMINSURED.send_keys()

        #乘客
        INCARPASSENGERLIABILITYCOVERAGE=self.driver.find_element_by_id("formINCARPASSENGERLIABILITYCOVERAGE_editor_INCARPASSENGERLIABILITYCOVERAGE_select")
        print(INCARPASSENGERLIABILITYCOVERAGE.is_selected())

        editorSumInsured=self.driver.find_element_by_id("editorSumInsured")
        editorSumInsured.send_keys()

        #全车盗抢损失险
        THEFTCOVERAGE=self.driver.find_element_by_id("formTHEFTCOVERAGE_editor_THEFTCOVERAGE_select")
        print(THEFTCOVERAGE.is_selected())

        THEFTCOVERAGE_SUMINSURED=self.driver.find_element_by_id("formTHEFTCOVERAGE_editor_THEFTCOVERAGE_SUMINSURED")
        THEFTCOVERAGE_SUMINSURED.send_keys()

        #玻璃单独破碎险
        GLASSBROKENCOVERAGE=self.driver.find_element_by_id("formGLASSBROKENCOVERAGE_editor_GLASSBROKENCOVERAGE_select")
        print(GLASSBROKENCOVERAGE.is_selected())

        GLASSMANUFACTURER=self.driver.find_element_by_id("formGLASSBROKENCOVERAGE_editor_GLASSBROKENCOVERAGE_GLASSMANUFACTURER")
        GLASSMANUFACTURER.send_keys()








    # 复制
    def copy(self):
        time.sleep(1)
        try:
            time.sleep(1)
            submint = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[2]
        except:
            time.sleep(1)
            submint = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[2]
        # time.sleep(2)
        try:
            time.sleep(1)
            submint.click()
        except Exception as e:
            try:
                print(e)
                time.sleep(1)
                submint.click()
            except Exception as e:
                print(e)
                time.sleep(1)
                submint.click()
        self.waitealert()

    def waitealert(self):
        try:
            time.sleep(1)
            self.driver.switch_to.alert.accept()
        except:
            try:
                time.sleep(1)
                self.driver.switch_to.alert.accept()
            except:
                time.sleep(1)
                self.driver.switch_to.alert.accept()

    # 复制
    def copy2(self):
        time.sleep(1)
        try:
            time.sleep(1)
            submint = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[2]
        except:
            time.sleep(1)
            submint = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[2]
        # time.sleep(2)
        try:
            time.sleep(1)
            submint.click()
        except Exception as e:
            try:
                print(e)
                time.sleep(1)
                submint.click()
            except Exception as e:
                print(e)
                time.sleep(1)
                submint.click()
        self.waitealert()



if __name__ == '__main__':
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=logfile, format=LOG_FORMAT)
    app = BigThingThread()
    app.run()


