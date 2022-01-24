## 我们来看看没有Optional会遇到哪些问题。
假设在我们的程序中具有以下方法。此方法使用员工的ID从数据库中检索员工的详细信息：
```java
Employee findEmployee(String id) {
 ...
};
```


假设在使用上述方法时所提供的ID在数据库中不存在。然后，该方法将返回null值。现在，如果我们已经编写了下面的代码：
```java
Employee employee = findEmployee("1234");
System.out.println("Employee's Name = " + employee.getName());
```

上面的代码将在运行时抛出NullPointerException异常，因为程序员在使用该值之前没有对它进行空指针检测。

## Java 8的Optional提供了怎样的解决方案？
```java
Optional<Employee> findEmployee(String id) {
 ...
};
```


在上面的代码中，我们将返回类型修改为Optional<Employee>来向调用者表明与给定ID的对应的员工可能不存在。
现在，需要在调用方中明确表达这一事实。
调用者应该编写如下代码：
```java
Optional <Employee> optional = findEmployee("134");
optional.ifPresent(employee -> {
 System.out.println("Employee name is " + employee.getName());
})
```


## Optional类的方法
```java
//创建一个Optional对象
public static <T> Optional<T> ofNullable(T value)

//传递一个Customer函数过去。仅当Optional对象中存在非空值时，才会执行该Consumer函数。
//如果Optional对象中存放的是空值，则不执行任何操作：
public void ifPresent(Consumer<? super T> consumer) 
```

