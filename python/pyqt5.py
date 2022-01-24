class TabDemo(QTabWidget):
    def __init__(self, parent=None):
        super(TabDemo, self).__init__(parent)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, "Tab 3")
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.setWindowTitle("Tab 例子")

    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow("姓名", QLineEdit())
        layout.addRow("地址", QLineEdit())
        self.setTabText(0, "联系方式")
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("男"))
       sex.addWidget(QRadioButton("女"))
        layout.addRow(QLabel("性别"), sex)
        layout.addRow("生日", QLineEdit())
        self.setTabText(1, "个人详细信息")
        self.tab2.setLayout(layout)

    def tab3UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("科目"))
        layout.addWidget(QCheckBox("物理"))
        layout.addWidget(QCheckBox("高数"))
        self.setTabText(2, "教育程度")
        self.tab3.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = TabDemo()
    demo.show()
    sys.exit(app.exec_())


import sys
import time
import datetime
import re
import logging
import sqlite3
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PyQt5.QtCore import QThread,Qt,pyqtSignal
from PyQt5.QtWidgets import QTabWidget,QWidget,QListWidget,QFormLayout,QLabel,QPushButton,QMessageBox,QFileDialog,QApplication


class BigThingThread(QThread):
    data_signal=pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.bianhao = pd.Series([11, 12, 13, 21, 22, 23, 31, 32, 33, 34, 41, 51, 52, 61, 62, 63,
                             71, 72, 73, 74, 75, 81, 82, 83, 84, 85, 86, 87, 91, 92, 93, 94])
        self.again = 0
        self.selection=1
    def run(self):
        self.driver = webdriver.Ie()
        conn = sqlite3.connect('ludan.db')
        c = conn.cursor()
        cursor2 = c.execute('''SELECT * from register_info order by id desc limit 0,1 ''')
        for row in cursor2:
            self.zhanghao = row[2]
            print(self.zhanghao)
            self.mima = row[3]
            self.need_to_copy = row[1]
        cursor3 = c.execute('''SELECT count(1)  from auto_info where zhuangtai=0''')
        self.submit_copy2()
        for row in cursor3:
            num=row[0]
        self.data_signal.emit('当前共有%s条数据需要录入' % (num))
        cursor = c.execute('''SELECT chepaihao,chejiahao,fadongjihao,zaikeliang,
                                 zaizhiliang,zhengbeizhiliang,cheliangzhonglei,shiyongxingzhi,chudengriqi,
                                 qibaodate,chechuangshui,yewulaiyuan,shijijiazhi  from auto_info where zhuangtai=0''')
        i=-1
        for row in cursor:
            i=i+1
            self.qibaodate = row[9]
            self.chepaihao = row[0]
            self.fadongjihao = row[2]
            self.chejiahao = row[1]
            self.zaikeliang = row[3]
            self.zaizhiliang = row[4]
            self.zhengbeizhiliang = row[5]
            self.chudengriqi = row[8]
            self.shiyongxingzhi = row[7]
            self.chechuangshui = row[10]
            self.cheliangzhonglei = row[6]
            self.yewulaiyuan = row[11]
            self.shijijiazhi = row[12]

            if i == 0:
                self.again = 0
            try:
                print(datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
                if self.selection == 1:
                    self.fillIn_TrafficCompulsory(i)
                elif self.selection == 2:
                    self.fillIn_AutoComprenhensive(i)
                self.data_signal.emit('第%s条数据录入成功' % (i + 1))
                sql2 = '''update auto_info set zhuangtai=1 where chepaihao=?'''
                pare2 = (self.chepaihao)
                c.execute(sql2, pare2)
                conn.commit()
                logging.error('第%s条数据录入成功' % (i + 1))
                if i != num - 1:
                    self.copy()
                    self.again = 1
            except Exception as e:
                print(e)
                logging.error(e)
                self.data_signal.emit("第%s条录入失败" % (i + 1))
                logging.error('第%s条数据录入失败' % (i + 1))
                self.again = 0
                self.submit_copy()

                print(datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
        conn.close()
        self.data_signal.emit('完成')
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

    def submit_copy2(self):
        self.driver.get('http://10.190.48.28/CPIC09Auto/pages/loginView.jsp')
        # 登录
        branchCode = self.driver.find_element_by_xpath('//input[@name="branchCode"]')
        branchCode.send_keys('4020100')
        userCode = self.driver.find_element_by_xpath('//input[@name="userCode"]')
        userCode.send_keys(self.zhanghao)
        password = self.driver.find_element_by_xpath('//input[@name="password"]')
        password.send_keys(self.mima)
        # submit = self.driver.find_element_by_id('submitBtn')
        password.send_keys(Keys.ENTER)

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'SubButton')))

        # 找到查询按钮
        chaxun = self.driver.find_elements_by_xpath('//*[@class="SubButton"]')[1]
        chaxun.click()
        # 切换到页面子框架
        self.driver.switch_to.frame("centerContentFrame")
        # 车牌号码
        plateNo = self.driver.find_element_by_id('queryCondition_editor_plateNo')
        plateNo.send_keys(self.need_to_copy)
        # 录入员
        inputorName = self.driver.find_element_by_id('queryCondition_editor_inputorName')
        inputorName.click()
        inputorName.send_keys(Keys.DELETE)
        # 查询起始日期
        queryStartDate = self.driver.find_element_by_id('queryCondition_editor_queryStartDate')
        queryStartDate.click()
        queryStartDate.send_keys(Keys.DELETE)
        # 查询
        query = self.driver.find_element_by_id("query")
        query.click()
        #
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'CurrentRow')))
        # query_result=self.driver.find_element_by_xpath('//*[@title="机动车综合险2014版"]')
        query_result = self.driver.find_element_by_xpath('//*[@class="CurrentRow"]')
        ActionChains(self.driver).double_click(query_result).perform()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'MenuBar_Button')))

        # 复制
        copy = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[0]
        time.sleep(2)
        copy.click()
        # time.sleep(2)
        # self.driver.switch_to.alert.accept()
        self.waitealert()
        time.sleep(3)

    def fillIn_AutoComprenhensive(self,i):
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
        # 起保日期
        qibaoriqi = self.driver.find_element_by_id('basicinfo$formAutoComprenhensive2007_editor_inceptionDate2')
        qibaoriqi.click()
        qibaoriqi.clear()
        qibaoriqi.send_keys(self.qibaodate)

        ##车辆信息
        vehicalinfo = self.driver.find_elements_by_xpath('//*[@class="Tab_top"]')[1]
        vehicalinfo.click()

        # 号牌号码
        licensenum = self.driver.find_element_by_id('vehicleinfo$editorVehiclelicense')
        licensenum.clear()
        licensenum.send_keys(self.chepaihao)

        # 发动机号
        ENGINENO = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_ENGINENO')
        ENGINENO.clear()
        ENGINENO.send_keys(self.fadongjihao)

        # 车架号
        CodeTF = self.driver.find_element_by_id('vehicleinfo$shortCutCodeTF')
        CodeTF.clear()
        CodeTF.send_keys(self.chejiahao)

        # 车辆定型
        # 车型库
        CodeBtn = self.driver.find_element_by_id('vehicleinfo$shortCutCodeBtn')
        CodeBtn.click()
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

        # 核定载客量
        SEATCOUNT = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_SEATCOUNT')
        SEATCOUNT.clear()
        SEATCOUNT.send_keys(self.zaikeliang)
        # 核定载质量
        CARRYINGCAPACITY = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_CARRYINGCAPACITY')
        CARRYINGCAPACITY.clear()
        CARRYINGCAPACITY.send_keys(self.zaizhiliang)

        # 车辆种类
        if self.cheliangzhonglei != 0:
            VEHICLEVARIETY1 = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_VEHICLEVARIETY1')
            VEHICLEVARIETY1.click()
            self.waitealert()
            for i in range(self.cheliangzhonglei):
                VEHICLEVARIETY1.send_keys(Keys.DOWN)
            VEHICLEVARIETY1.send_keys(Keys.ENTER)
        # 整备质量
        EMPTYWEIGHT = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_EMPTYWEIGHT')
        EMPTYWEIGHT.clear()
        EMPTYWEIGHT.send_keys(self.zhengbeizhiliang)

        # 初次登记日期
        time.sleep(1)
        REGISTERDATE = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_REGISTERDATE')
        REGISTERDATE.click()
        REGISTERDATE.clear()
        REGISTERDATE.send_keys(self.chudengriqi)

        # 协商实际价值
        CURRENTVALUE = self.driver.find_element_by_id('vehicleinfo$formAutoComprenhensive2007_editor_CURRENTVALUE')
        CURRENTVALUE.click()
        CURRENTVALUE.send_keys(Keys.DELETE)
        CURRENTVALUE.send_keys(self.shijijiazhi)

        ##车船税
        if self.chechuangshui != 0:
            tax = self.driver.find_elements_by_xpath('//*[@class="Tab_top"]')[2]
            tax.click()
            # 减免税方案代码
            time.sleep(1)
            self.driver.switch_to.frame("tabsetmain_vehicletax")
            taxType = self.driver.find_element_by_id('formTax_editor_deductionDueType')
            taxType.click()
            # time.sleep(1)
            DropDownButton = self.driver.find_element_by_xpath('//button[@class="DropDownButton"]')
            DropDownButton.click()
            DropDownButton.send_keys(Keys.ENTER)
            self.driver.switch_to.parent_frame()
        ##保费计算
        baofeijisuan = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[2]
        baofeijisuan.click()
        # time.sleep(2)
        # self.driver.switch_to.alert.accept()
        self.waitealert()
        self.waitealert()

        ##预核保
        yuhebao = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[2]
        yuhebao.click()
        self.driver.switch_to.alert.accept()
        # time.sleep(3)
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
        buttonclose = self.driver.find_element_by_id('closeAutoUWResultButton')
        buttonclose.click()
        self.driver.switch_to.parent_frame()
        ##提交
        submint = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[5]
        submint.click()
        # time.sleep(3)
        # self.driver.switch_to.alert.accept()
        # time.sleep(2)
        # self.driver.switch_to.alert.accept()
        self.waitealert()
        self.waitealert()

    # 复制
    def copy(self):
        time.sleep(3)
        try:
            time.sleep(1)
            submint = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[0]
        except:
            time.sleep(1)
            submint = self.driver.find_elements_by_xpath('//*[@class="MenuBar_Button"]')[0]
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

class filedialogdemo(QTabWidget):
    def __init__(self):
        super().__init__()
        self.tab1 = QWidget()
        self.addTab(self.tab1, "Tab 1")
        self.tab1UI()
        self.setGeometry(600,400,600,400)
        # self.setFixedSize(600,400)
        self.setWindowTitle("车险录单工具")
        self.contents = QListWidget()

    def tab1UI(self):
        layout = QFormLayout()
        edit=QLabel("请选择相应险种")
        edit.setAlignment(Qt.AlignCenter)
        self.btn1=QPushButton("交强险")
        self.btn1.clicked.connect(self.select_jiaoqiang)
        self.btn2=QPushButton("机动车综合险")
        self.btn2.clicked.connect(self.select_zonghe)
        layout.addRow(edit)
        layout.addRow(self.btn1)
        layout.addRow(self.btn2)
        self.setTabText(0, "险种选择")
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout = QFormLayout()
        btn1 = QPushButton("导入excel文件")
        btn1.clicked.connect(self.getfile)
        btn2 = QPushButton("开始录入")
        btn2.clicked.connect(lambda :self.fill_in(1))
        layout.addRow(btn1)
        layout.addRow(btn2)
        layout.addRow(self.contents)
        self.setTabText(1, "交强险")
        self.tab2.setLayout(layout)

    def tab3UI(self):
        layout = QFormLayout()
        btn1 = QPushButton("导入excel文件")
        btn1.clicked.connect(self.getfile)
        btn2 = QPushButton("开始录入")
        btn2.clicked.connect(lambda :self.fill_in(2))
        layout.addRow(btn1)
        layout.addRow(btn2)
        # contents = QListWidget()
        layout.addRow(self.contents)
        self.setTabText(1, "机动车综合险")
        self.tab3.setLayout(layout)

    def select_jiaoqiang(self):
        self.tab2 = QWidget()
        self.addTab(self.tab2, "Tab 2")
        self.tab2UI()
        self.setCurrentIndex(1)
        self.btn1.setEnabled(False)
        self.btn2.setEnabled(False)
    def select_zonghe(self):
        self.tab3 = QWidget()
        self.addTab(self.tab3, "Tab 3")
        self.tab3UI()
        self.setCurrentIndex(1)
        self.btn1.setEnabled(False)
        self.btn2.setEnabled(False)

    def getfile(self):
        fail = 0
        try:
            filename, _ = QFileDialog.getOpenFileName(self, '选择文件', 'c:\\', 'Excel files(*.xlsx , *.xls)')
            dataframe = pd.read_excel(filename)

            need_to_copy = dataframe.loc[0, "第一单车牌号"]
            zhanghao = dataframe.loc[0, "账号"][2:]
            mima = dataframe.loc[0, "密码"]
            conn = sqlite3.connect('ludan.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE if not exists register_info
                           (id integer primary key AUTOINCREMENT,
                           need_to_copy   CHAR(5),
                          zhanghao          Char(5)  ,
                          mima          CHAR(5)
                           );''')
            sql = '''INSERT INTO register_info (need_to_copy,zhanghao,mima)
                    VALUES (?,?,?)'''
            pare = (need_to_copy,zhanghao,mima)
            c.execute(sql, pare)
            c.execute('''CREATE TABLE if not exists auto_info
                   (chepaihao          Char(5)  primary key ,
                  chejiahao          CHAR(5),
                  fadongjihao        CHAR(5),
                  zaikeliang      CHAR (5),
                  zaizhiliang     CHAR (5),
                  zhengbeizhiliang  CHAR (5),
                  cheliangzhonglei  int,
                  shiyongxingzhi    int ,
                  chudengriqi           TIME ,
                  qibaodate             TIME ,
                  chechuangshui     int,
                  yewulaiyuan       INT,
                  shijijiazhi       CHAR (5),
                  zhuangtai  int default 0
                   );''')
            try:
                for i in range(len(dataframe)):
                    qibaodate = str(dataframe.loc[i, "起保日期"])
                    chepaihao = dataframe.loc[i, "车牌号"]
                    fadongjihao = dataframe.loc[i, "发动机号"]
                    chejiahao = dataframe.loc[i, "车架号"]
                    zaikeliang = str(dataframe.loc[i, "核定载客量"])
                    zaizhiliang = str(dataframe.loc[i, "核定载质量"])
                    zhengbeizhiliang = str(dataframe.loc[i, "整备质量"])
                    chudengriqi = str(dataframe.loc[i, "初登日期"])
                    shiyongxingzhi = int(dataframe.loc[i, "使用性质代码"])
                    chechuangshui = int(dataframe.loc[i, "车船税逻辑值"])
                    cheliangzhonglei = int(dataframe.loc[i, "车辆种类"])
                    yewulaiyuan = int(dataframe.loc[i, "业务来源代码"])
                    shijijiazhi = str(dataframe.loc[i, "协商实际价值"])
                    sql = '''INSERT INTO auto_info (chepaihao,chejiahao,fadongjihao,zaikeliang,
                             zaizhiliang,zhengbeizhiliang,cheliangzhonglei,shiyongxingzhi,chudengriqi,
                             qibaodate,chechuangshui,yewulaiyuan,shijijiazhi)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'''
                    pare = (chepaihao, chejiahao, fadongjihao, zaikeliang,
                            zaizhiliang, zhengbeizhiliang, cheliangzhonglei, shiyongxingzhi, chudengriqi,
                            qibaodate, chechuangshui,yewulaiyuan,shijijiazhi)
                    c.execute(sql, pare)
            except:
                c.execute("Rollback")
                fail = 1
                QMessageBox.about(self, "excel文件导入", "excel文件中存在与之前导入的数据相同的车牌号")
            conn.commit()
            if fail == 0:
                cursor = c.execute('''SELECT count(1)  from auto_info''')
                for row in cursor:
                    QMessageBox.about(self, "excel文件导入", "excel文件成功导入,当前数据库共有%s条数据" % row[0])
            conn.close()
        except Exception as e:
            print(e)

    def fill_in(self,i):
        self.big_thread=BigThingThread()
        self.big_thread.selection=i
        self.big_thread.data_signal.connect(self.handleDisplay)
        self.big_thread.start()

    def handleDisplay(self,data):
        self.contents.addItem(data)

if __name__ == '__main__':
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='my.log', format=LOG_FORMAT)
    app = QApplication(sys.argv)
    ex = filedialogdemo()
    ex.show()
    sys.exit(app.exec_())

 
