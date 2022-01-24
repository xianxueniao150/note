## 字符串拼接
```java
String.format("产品名称 : %s , 价格 : %s , 生产地 : %s", productName, 
            productPrice, productAddress);
```


## 字符串转驼峰
```java
//PRODUCT_DATA -> productData
System.out.println(CaseFormat.LOWER_UNDERSCORE.to(CaseFormat.LOWER_CAMEL, x));
//PRODUCT_DATA -> ProductData
System.out.println(CaseFormat.UPPER_UNDERSCORE.to(CaseFormat.UPPER_CAMEL,x));
```


## 字符串截取
```java
str.substring(4) // [4:]
str.substring(0,4)  //[0:4)
```


## 保留两位小数
```java
DecimalFormat df = new DecimalFormat( "0.00");
df.format(receipt.getAmount())
```


## map转json
```java
JSONObject jsonObject = new JSONObject(map);
```


## 简单日期格式转换
```java
SimpleDateFormat myFmt = new SimpleDateFormat("yyyy-MM-dd");
Calendar calendar = Calendar.getInstance();
System.out.println(myFmt.format(calendar.getTime()));
//求昨天日期
calendar.add(Calendar.DATE,-1);
System.ou.println(myFmt.format(calendar.getTime()));
//求当前时间时间戳
long now1 = System.currentTimeMillis();
System.out.println("当前时间戳:" +now1);
```


## 获取键盘输入
```java
Scanner sc = new Scanner(System.in);
System.out.println("ScannerTest, Please Enter lnvc:");
String lnvc = sc.nextLine();  //读取字符串型输入
```


## Object 转 Double
```java
Object number=10;
double douNumber1=Double.parseDouble(number.toString());
```



## 比较（避免null判断)
```java
Objects.equals(value, that.getValue());
```


## 字符串转驼峰
```java
public static String toCamel(String word){
    while (true){
        int i = word.indexOf("_");
        if(i==-1){
            break;
        }
        word=word.substring(0,i)+StrUtil.upperFirst(word.substring(i+1));
    }
    return StrUtil.lowerFirst(word);
}
```


## 打印数组
```java
int[] array = {1,2,3,4,5};
System.out.println(Arrays.toString(array));
```


## 判断是否是数组
```java
String[] ids ={"a"};
//第一种方法
System.out.println(ids.getClass().isArray());
//第二种方法
ids instanceof String[]
```


## 使用@link在注释中关联代码
```java
/**
 * 课程类型,{@link com.boot.entity.User}
 */
```

