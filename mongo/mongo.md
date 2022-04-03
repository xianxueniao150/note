## 启动命令
mongod --dbpath=..\data\db

## 基本命令

## 数据库操作
```sh
# 查看当前所在数据库
db

# 查看所有数据库, 如果数据库不存在则自动创建
show dbs

# 切换数据库
use test
```

### 集合操作
```sh
# 查看所有集合
show tables

# 查看集合内的所有记录
db.msgindex97.find()


隐式创建集合并插入文档
db.comment.insert({"articleid":"100000","content":"今天天气真好，阳光明媚",
	"userid":"1001","nickname":"Rose","createdatetime":new Date(),
	"likenum":NumberInt(10),"state":null})
 
批量插入
 db.comment.insertMany([
{"_id":"1","articleid":"100001","content":"我们不应该把清晨浪费在手机上，健康很重要，一杯温水幸福你我他。",
"userid":"1002","nickname":"相忘于江湖","createdatetime":new Date("2019-08-05T22:08:15.522Z"),"likenum":NumberInt(1000),"state":"1"},
{"_id":"2","articleid":"100001","content":"我夏天空腹喝凉开水，冬天喝温开水",
"userid":"1005","nickname":"伊人憔悴","createdatetime":new Date("2019-08-05T23:58:51.485Z"),"likenum":NumberInt(888),"state":"1"}
]);

 show collections
 
基本查询
db.comment.find({userid:'1003'})
只显示部分字段，为1显示，为0强制不显示
db.comment.find({userid:"1003"},{userid:1,nickname:1,_id:0})

更新
db.comment.update({_id:"2"},{$set:{likenum:NumberInt(889)}})
批量的修改更新所有用户为 1003 的用户的昵称为凯撒大帝。
db.comment.update({userid:"1003"},{$set:{nickname:"凯撒大帝"}},{multi:true})
列值增长的修改
db.comment.update({_id:"3"},{$inc:{likenum:NumberInt(1)}})

删除文档
db.comment.remove({_id:"1"})
```

