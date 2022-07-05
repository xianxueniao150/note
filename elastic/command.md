## 查看基本信息(版本等)
```sh
curl -XGET localhost:9200
```

## indice
```sh
# List All Indices
curl -X GET "localhost:9200/_cat/indices?v&pretty"

health status index                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   video                           Vc25C1alQlWPMZGBOuqwEw   1   1      19216         6663      4.6mb          4.6mb


# 查询具体某个indice字段类型
curl -X GET "localhost:9200/user/_mapping?pretty&pretty"
GET user/_mapping
```

## search
search的查询条件既可以放在请求路径上也可以放在请求体里，为了可读性一般放在请求体里
- took – time in milliseconds for Elasticsearch to execute the search
- hits.total – total number of documents matching our search criteria
- hits.hits – actual array of search results (defaults to first 10 documents)

```sh
# 查询所有
curl -X GET "localhost:9200/user/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} }
}
'

# from默认为0，size默认为10，sort默认按score排序
# _source 指定最终返回的字段，默认返回所有
GET /user/_search
{
  "query": { "match_all": {} },
  "from": 10,
  "size": 10,
  "sort": { "phone": { "order": "desc" } },
  "_source": ["phone", "email"] 
}


# 匹配查询
# 对于keyword要完全匹配
GET /user/_search
{
  "query": { "match": { "phone": "+8615927610275" } }
}

# 查询非空
curl -X GET "localhost:9200/video/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "exists" : { "field" : "pattern_labels" }
    }
}
'
```

## bool query
```sh
# must:且 containing "mill" and "lane" in the address
# must_not:且	contain neither "mill" nor "lane" in the address 
GET /bank/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "address": "mill" } },
        { "match": { "address": "lane" } }
      ]
    }
  }
}

# should:或	containing "mill" or "lane" in the address
GET /bank/_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { "address": "mill" } },
        { "match": { "address": "lane" } }
      ]
    }
  }
}


#组合 40 years old but doesn’t live in ID
GET /bank/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "age": "40" } }
      ],
      "must_not": [
        { "match": { "state": "ID" } }
      ]
    }
  }
}
```

