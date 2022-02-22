## key基本操作
 获取key的类型
type key

 获取key是否存在
exists key

删除指定key
del key


### key 扩展操作（时效性控制）
 为指定key设置有效期
expire key seconds
pexpire key milliseconds
expireat key timestamp
pexpireat key milliseconds-tim

 获取key的有效时间
ttl key      返回值为-2表示key不存在，为-1表示永久有效
pttl key

 切换key从时效性转换为永久性
persist key


### key 扩展操作（查询模式）
 查询key
keys pattern


查询模式规则
* 匹配任意数量的任意符号 ? 配合一个任意符号 [] 匹配一个指定符号

keys * 查询所有
keys it* 查询所有以it开头
keys *heima 查询所有以heima结尾
keys ??heima 查询所有前面两个字符任意，后面以heima结尾
keys user:? 查询所有以user:开头，最后一个字符任意
keys u[st]er:1 查询所有以u开头，以er:1结尾，中间包含一个字母， s或t


## key 其他操作
 对所有value排序
sort key

 为key改名
rename key newkey
renamenx key newkey   如果newkey已经存在，则会失败

 其他key通用操作
help @generic



## 数据库通用操作
 redis为每个服务提供有16个数据库，编号从0到15
 每个数据库之间的数据相互独立
 切换数据库
select indx

 数据移动
move key db

 数据清除
dbsize   返回有多少个key
flushdb   清空该数据库
flushall


 其他操作
quit
ping
echo message

e
