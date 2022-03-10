## 静态成员变量的初始化

strngbad.h
```cpp
class StringBad{
private:
	static int num_strings;
}
```

strngbad.cpp
```cpp
int StringBad::num_strings = 0;
```
注意，不能在类声明中初始化静态成员变量，需要在类声明之外使用单独的语句来进行初始化。
注意，初始化语句指出了类型，并使用了作用域运算符，但没有使用关键字static
