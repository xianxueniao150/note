## list类型：保存多个数据，底层使用双向链表存储结构实现

list 类型数据基本操作
```sh
# 添加/修改数据
lpush key value1 [value2] ……
rpush key value1 [value2] ……

# 获取数据
lrange key start stop 
lrange key 0 -1  #获取全部数据
lindex key index
llen key

# 获取并移除数据
lpop key
rpop key
```


list 类型数据扩展操作
```sh
# 规定时间内获取并移除数据，单位为s,阻塞式, 没有就等待，时间到了还没有就输出nil,可同时等待多个key
blpop key1 [key2] timeout
brpop key1 [key2] timeout

# 移除指定数据,count指定移除多少个指定的value，比如value为a,有5个,count为3,则移除3个a
lrem key count value
```


