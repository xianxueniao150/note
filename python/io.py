导入数据库
import pymysql

# 建立mysql连接
conn = pymysql.connect(
        host = '127.0.0.1',
        user='root',
        passwd='',
        db='ezdbyl1227' ,
        port=3306,
        charset='utf8'
    )

# 获得游标
cur = conn.cursor()

sql = 'insert into medicals (medical_name, medical_category) values (%s, %s, %s)'

for i in range(0, len(data3)):
    values = (data3.loc[i,"medical"], data3.loc[i,"category"],data3.loc[i,"dosage"])
    cur.execute(sql, values)
    print ('youxi'+str(i)+' sucess')
conn.commit()
cur.close()
conn.close()


日志
with open("test11.txt", "w") as f:
    f.write(driver.page_source.encode("gbk", 'ignore').decode("gbk", "ignore"))





