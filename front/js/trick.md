## 获取数组对象中某一属性值的集合
```javascript
var user = [
     {
         id: 1,
         name: "李四"
     },
     {
         id: 2,
         name: "张三"
     },
     {
         id: 3,
         name: "李五"
     }
 ]
//map方法
var userName = user.map((item)=>{
    return item.name;
})
console.log(userName); // ["李四", "张三", "李五"]
```
