```javascript
统计查询
db.comment.count({userid:"1003"})

分页查询
//第一页
db.comment.find().skip(0).limit(2)
//第二页
db.comment.find().skip(2).limit(2)
//第三页
db.comment.find().skip(4).limit(2)

排序查询，1 为升序排列，-1 降序排列
db.comment.find().sort({userid:-1,likenum:1})

模糊查询
查询评论内容包含“开水”的所有文档，代码如下：
db.comment.find({content:/开水/})

查询非null的
find({"goodsThirdSalesList":{$ne:null}})

比较查询
db.集合名称.find({ "field" : { $gt: value }}) // 大于: field > value
db.集合名称.find({ "field" : { $lt: value }}) // 小于: field < value
db.集合名称.find({ "field" : { $gte: value }}) // 大于等于: field >= value
db.集合名称.find({ "field" : { $lte: value }}) // 小于等于: field <= value
db.集合名称.find({ "field" : { $ne: value }}) // 不等于: field != value

包含查询
包含使用$in操作符。不包含使用$nin操作符。
db.comment.find({userid:{$in:["1003","1004"]}})
db.comment.find({userid:{$nin:["1003","1004"]}})

条件连接查询
我们如果需要查询同时满足两个以上条件，需要使用$and操作符将条件进行关联格式为：
$and:[ { },{ },{ } ]
示例：查询评论集合中likenum大于等于700 并且小于2000的文档：
db.comment.find({$and:[{likenum:{$gte:NumberInt(700)}},{likenum:{$lt:NumberInt(2000)}}]})
如果两个以上条件之间是或者的关系，格式为：
$or:[ { },{ },{ } ]
示例：查询评论集合中userid为1003，或者点赞数小于1000的文档记录
db.comment.find({$or:[ {userid:"1003"} ,{likenum:{$lt:1000} }]})
```


## 数组tenantIdList包含tenantId
```javascript
query.addCriteria(Criteria.where("tenantIdList").is(tenantId));
```


模糊查询
//模糊查询通过name查询
```javascript
Pattern pattern = BusinessUtil.getMongoPattern(name);
criteria.and("name").regex(pattern);
```


```javascript
public static Pattern getMongoPattern(String param) {
    return Pattern.compile(MessageFormat.format("^.*{0}.*$", escapeExprSpecialWord(param)), Pattern.CASE_INSENSITIVE);
}

private static String escapeExprSpecialWord(String keyword) {
    String[] fbsArr = { "\\", "$", "(", ")", "*", "+", ".", "[", "]", "?", "^", "{", "}", "|" };
    for (String key : fbsArr) {
        if (keyword.contains(key)) {
            keyword = keyword.replace(key, "\\" + key);
        }
    }
    return keyword;
}
```


## 分页查询
```javascript
Pagination<GoodsThirdSupplier> pagination = new Pagination<>(goodsThirdPageRequest.getPageNum(), goodsThirdPageRequest.getPageSize());
pagination.setSort("updateTime desc");
return super.page(query, pagination);
```


## 空格替换为“”（？不能替换，为森么会写这个？）
```javascript
goodsThirdSupplierId=goodsThirdSupplierId.replace(" ","\\t");
```


## 或
```javascript
criteria.and("_id").is(pmListParam.getId());
criteria.and("status").is(pmListParam.getStatus());
criteria.orOperator(Criteria.where("createName").regex(pattern),Criteria.where("createId").regex(pattern));

find using query: {"isDelete": 0, "_id": "1331443708540747777", "status": 0, "$or": [{"createName": {"$regex": "^.*小.*$", "$options": "i"}}, {"createId": {"$regex": "^.*小.*$", "$options": "i"}}]} 
```


## 两个字段的和作为查询条件
```javascript
db.getCollection('PointLog_T0001').find({"$where":"this.jobName+'|'+this.moduleName=='积分发放|积分发放'"})
```


## 排序如果想按中文字母排序的话，
```javascript
//实测不准确，解决方案数据库增加一个首字母字段
query.collation(Collation.of(Collation.CollationLocale.of("zh"))),pagination);
```


