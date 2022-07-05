## 数组
在ES中，没有专门的数组数据类型，但是默认情况下，任意一个字段都可以包含0或多个值，这意味着每个字段默认都是数组类型。不过ES要求数组类型的各个元素值的数据类型必须相同。

```sh
# 查询pattern_labels字段包含2或3的
curl -X GET "localhost:9200/video/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
		"bool": {
		  "should": [
			{ "match": { "pattern_labels": 2 } },
			{ "match": { "pattern_labels": 3 } }
		  ]
		}
    }
}
'

# 查询pattern_labels字段不为空的
{
    "query": {
        "exists" : { "field" : "pattern_labels" }
    }
}
```

## date类型
日期类型表示格式可以是以下几种：
（1）日期格式的字符串，比如 “2018-01-13” 或 “2018-01-13 12:10:30”
（2）long类型的毫秒数( milliseconds-since-the-epoch，epoch就是指UNIX诞生的UTC
时间1970年1月1日0时0分0秒)


## 数字类型 - 8种
数字类型有如下分类:
- byte	有符号的8位整数, 范围: [-128 ~ 127]
- short	有符号的16位整数, 范围: [-32768 ~ 32767]
- integer	有符号的32位整数, 范围: [−2^31 ~ 2^31-1]
- long	有符号的64位整数
- float	32位单精度浮点数
- double	64位双精度浮点数
