############################################
# 将不同Excel中相同部门组的内容抽取出来，组成新的多个Excel
a=['鄂州中心支公司','恩施中心支公司','黄冈中心支公司','黄石中心支公司','荆门中心支公司','荆州中心支公司',
    '潜江支公司','十堰中心支公司','随州中心支公司','天门支公司','武汉中心支公司','仙桃支公司','咸宁中心支公司',
    '襄阳中心支公司','孝感中心支公司','宜昌中心支公司']

import pandas as pd

df1=pd.read_excel(r'D:\杂\谢心怡\12月\1-15日统筹额度.xlsx')
df1=df1.iloc[:]
df2=pd.read_excel(r'D:\杂\谢心怡\12月\16-31跟单业务费.xlsx')
df2=df2.iloc[:]

bb=[]   
cc=[]
for j in a:
    writer = pd.ExcelWriter(r'D:\杂\谢心怡\12月\统筹\%s.xlsx'% j)
    for i in range(0,df1.shape[0]):
        if df1.loc[i,'部门组']==j:
            bb.append(i)
    for i in range(0,df2.shape[0]):
        if df2.loc[i,'部门组']==j:
            cc.append(i)
    jigou1=df1.iloc[bb,:]
    jigou2=df2.iloc[cc,:]
    jigou.to_excel(writer,sheet_name='1-15日统筹额度',index=False)
    jigou2.to_excel(writer,sheet_name='16-31跟单业务费',index=False)
    bb=[]
    cc=[]
    writer.save()
    writer.close()

############################################
# 时间格式调整
wuhan_policy=pd.read_csv(r'C:\Users\Administrator\Desktop\5month_change.csv',encoding="gbk")
shiwai_policy=pd.read_csv(r'C:\Users\Administrator\Desktop\5month_change2.csv',encoding="gbk")
sms=pd.read_excel(r'C:\Users\Administrator\Desktop\sms.xlsx')

sms['签发日期']=pd.to_datetime(sms['签发日期'].dt.date)
wuhan_policy['date']=pd.to_datetime(wuhan_policy['date'])
shiwai_policy['date']=pd.to_datetime(shiwai_policy['date'])
sms=sms.reset_index()
wuhan_policy=wuhan_policy.reset_index()
shiwai_policy=shiwai_policy.reset_index()

############################################
# Excel追加写入数据
# 目前还存在问题，写入的Excel打不开
import xlrd
from xlutils.copy import copy

file=r'C:\Users\bowen\Documents\Tencent Files\1360414539\FileRecv\shangyexian2.xlsx'
workbook = xlrd.open_workbook(file)
sheets = workbook.sheet_names()
worksheet = workbook.sheet_by_name(sheets[0])
rows_old = worksheet.nrows

new_workbook = copy(workbook)
new_worksheet = new_workbook.get_sheet(0) 
new_worksheet.write(4, 2, "book")
new_workbook.save(file) ()


############################################
# 向Excel中写入数据
data2.to_excel('testbbbbaaa.xlsx',index=False,float_format="%.2f")


# 读取Excel数据
data=pd.read_excel(r"C:\Users\ezyb\xiyao.xlsx",header=0)
data2=data.iloc[3:,[6,8]]
data2.columns=["category","medical"]
# 只保留指定长度
data2["category"]=data2["category"].str.slice(0,1)
# 替换指定列指定值
data2["category"]=data2["category"].replace({'是':'甲'})
data3=data2.dropna(subset=["medical"])
# 去除重复项
data3.drop_duplicates(inplace=True)
data3=data3.reset_index(drop=True)
# 将nan替换为none,否则插入数据库会报错
data3 = data3.astype(object).where(pd.notnull(data3), None)


