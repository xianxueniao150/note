hash 类型数据的基本操作
添加/修改数据
hset key field value

获取数据
hget key field
hgetall key

删除数据
hdel key field1 [field2]

 添加/修改多个数据
hmset key field1 value1 field2 value2 …

 获取多个数据
hmget key field1 field2 …

 获取哈希表中字段的数量
hlen key

 获取哈希表中是否存在指定的字段
hexists key field

获取哈希表中所有的字段名或字段值
hkeys key
hvals key

 设置指定字段的数值数据增加指定范围的值
hincrby key field increment
hincrbyfloat key field increment


HSETNX key field value
只有在字段 field 不存在时，设置哈希表字段的值。

