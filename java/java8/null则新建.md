## 为null则新建
```java
this.globalConfig = Optional.ofNullable(globalConfig).orElseGet(GlobalConfig::new);
```


## 为null则用指定的值
```java
Optional.ofNullable(columnNaming).orElse(naming);
```


## 取出列表中实体的某一个字段组成一个列表
```java
needUpdateGoods.stream().map(GoodsThird::getGoodsCode).collect(Collectors.toList())
```



## 取出列表中符合某个条件的唯一元素
```java
supplier.getTenantCreditQuotaList().stream().filter(t -> t.getTenantId().equals(tenantId)).findFirst().get()
```


## 取出列表中实体的某一个字段的最大值
```java
voItem.getScoreItems().stream().map(ScoreItem::getScore).max(Integer::compareTo).get()
```


## 将列表根据某一个字段的值从小到大排序
```java
ruleVo.getFileQualities().sort(Comparator.comparingInt(FileQuality::getSort));
```


## 取出列表中实体的某一个字段的和
```java
ruleVo.getFileQualities().stream().mapToInt(FileQuality::getScore).sum()
```


## 取出列表中实体的某一个字段用","连接为字符串
```java
String pids = existGoods.stream().map(GoodsThrd::getThirdGoodsCode).collect(Collectors.joining(","));
```


## 将列表变成以","分割的字符串
```java
String.join(",", userIds)
```


## 对于Map，若指定key存在，则直接返回value，否则利用传入的lambda表达式算出value并存入Map并返回value
```java
private final Map<Method, MapperMethod> methodCache;

private MapperMethod cachedMapperMethod(Method method) {
  return methodCache.computeIfAbsent(method, k -> new MapperMethod(mapperInterface, method, sqlSession.getConfiguration()));
}
```


## 上面等同于下面
```java
private MapperMethod cachedMapperMethod(Method method) {
        MapperMethod mapperMethod = (MapperMethod)this.methodCache.get(method);
        if (mapperMethod == null) {
            //创建一个MapperMethod，参数为mapperInterface和method还有Configuration
            mapperMethod = new MapperMethod(this.mapperInterface, method, this.sqlSession.getConfiguration());
            this.methodCache.put(method, mapperMethod);
        }

        return mapperMethod;
    }
```


## 将列表分组
```java
import com.google.common.collect.Lists;

List<List<CouponSerialMysql>> subLists = Lists.partition(couponSerialMysqls, BATCH_INSERT_SIZE);
```


## 列表转map
```java
Map<String, DTMember> memberMap = memberList.stream().collect(Collectors.toMap(DTMember::getId, a -> a));
```


## 将中间得到的list最终合成一个list
```java
List<HospitalCityListVo> vos = jsonObject.getJSONObject("datas").values().stream()
        .map(a-> JSON.parseArray(String.valueOf(a),HospitalCityListVo.class))
        .flatMap(Collection::stream)
        .collect(Collectors.toList());
```


## 从集合中删除最大值(或最小值)
```java
recentCityDetailList=recentCityDetailList.stream().sorted((a,b)-> BooleanUtils.toInteger(a.getUpdateTime().after(b.getUpdateTime())))
        .skip(1)
        .collect(Collectors.toList());
```


## 利用Stream聚合函数对BigDecimal求和
```java
billDetailList.stream().map(BillDetail::getPayoutAmount).reduce(BigDecimal.ZERO,BigDecimal::add);
```

