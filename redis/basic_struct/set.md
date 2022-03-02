set 类型数据的基本操作
 添加数据
sadd key member1 [member2]

 获取全部数据
smembers key

 删除数据
srem key member1 [member2]

获取集合数据总量
scard key

 判断集合中是否包含指定数据
sismember key member



set 类型数据的扩展操作
 随机获取集合中指定数量的数据
srandmember key [count]

随机获取集合中的某个数据并将该数据移出集合
spop key [count]


应用于随机推荐类信息检索，例如热点歌单推荐，热点新闻推荐等

QQ新用户入网年龄越来越低，这些用户的朋友圈交际圈非常小，往往集中在一所学校甚至一个班级中，如何
帮助用户快速积累好友用户带来更多的活跃度？
set 类型数据的扩展操作
 求两个集合的交、并、差集
sinter key1 [key2]
sunion key1 [key2]
sdiff key1 [key2]

 求两个集合的交、并、差集并存储到指定集合中
sinterstore destination key1 [key2]
sunionstore destination key1 [key2]
siffstore destination key1 [key2]



d
