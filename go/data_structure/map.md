map上的大部分操作，包括查找、删除、len和range循环都可以安全工作在nil值的map上，它们的行为和一个空的map类似。但是向一个nil值的map存入元素将导致一个panic异常

其中K对应的key必须是支持==比较运算符的数据类型

```go
map[KeyType]ValueType

make(map[KeyType]ValueType, [cap])

```



## map基本使用
```go
func main() {
	scoreMap := make(map[string]int, 8)
	scoreMap["张三"] = 90
	scoreMap["小明"] = 100
	fmt.Println(scoreMap)
	fmt.Println(scoreMap["小明"])
	fmt.Printf("type of a:%T\n", scoreMap)
}
```

输出：
```sh
map[小明:100 张三:90]
100
type of a:map[string]int
```



所有这些操作是安全的，即使这些元素不在map中也没有关系；如果一个查找失败将返回value类型对应的零值，例如，即使map中不存在“bob”下面的代码也可以正常工作，因为ages["bob"]失败时将返回0。

```go
ages["bob"] = ages["bob"] + 1 // happy birthday!
```

我们不能对map元素进行取址操作：
```go
_ = &ages["bob"] // compile error: cannot take address of map element
```

禁止对map元素取址的原因是map可能随着元素数量的增长而重新分配更大的内存空间，从而可能导致之前的地址无效。


## 其他操作

```go
//在声明的时候填充元素
userInfo := map[string]string{
    "username": "沙河小王子",
    "password": "123456",
}

//判断某个键是否存在
// 如果key存在ok为true,v为对应的值；不存在ok为false,v为值类型的零值
value, ok := map[key]

//删除元素
delete(map, key)

```



## 遍历
Map的迭代顺序是不确定的，并且不同的哈希函数实现可能导致不同的遍历顺序。在实践中，遍历的顺序是随机的，每一次遍历的顺序都不相同。这是故意的，每次都使用随机的遍历顺序可以强制要求程序不会依赖具体的哈希函数实现。
```go
//map的遍历
for k, v := range scoreMap {
    fmt.Println(k, v)
}

//只想遍历key的时候
for k := range scoreMap {
    fmt.Println(k)
}
```

## 更新 map 字段的值

如果 map 一个字段的值是 struct 类型，则无法直接更新该 struct 的单个字段
```go
type data struct {
    name string
}

func main() {
    m := map[string]data{
        "x": {"Tom"},
    }
    m["x"].name = "Jerry" //Cannot assign to m["x"].name
}
```

因为 map 中的元素是不可寻址的。需区分开的是，slice 的元素可寻址，slice可以直接更新

更新 map 中 struct 元素的字段值，有 2 个方法：

1.使用局部变量
```go
func main() {
    m := map[string]data{
        "x": {"Tom"},
    }
    // 提取整个 struct 到局部变量中，修改字段值后再整个赋值
    r := m["x"]
    r.name = "Jerry"
    m["x"] = r
    fmt.Println(m)    // map[x:{Jerry}]
}

```

2.使用指向元素的 map 指针
```go
func main() {
    m := map[string]*data{
        "x": {"Tom"},
    }

    m["x"].name = "Jerry"    // 直接修改 m["x"] 中的字段
    fmt.Println(m["x"])    // &{Jerry}
}

```



但是要注意下边这种误用：
```go
func main() {
    m := map[string]*data{
       "x": {"Tom"},
    }
    m["z"].name = "what???"  //nil pointer dereference
}

```

## 自定义key

有时候我们需要一个map的key是slice类型，但是map的key必须是可比较的类型，但是slice并不满足这个条件。不过，我们可以通过两个步骤绕过这个限制。第一步，定义一个辅助函数k，将slice转为map对应的string类型的key，确保只有x和y相等时k(x) == k(y)才成立。然后创建一个key为string类型的map，在每次对map操作时先用k辅助函数将slice转化为string类型。
```go
var m = make(map[string]int)

func k(list []string) string { return fmt.Sprintf("%q", list) }

func Add(list []string)       { m[k(list)]++ }
func Count(list []string) int { return m[k(list)] }

```
