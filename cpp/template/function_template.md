```cpp
#include<iostream>
using namespace std;

//这里把class换成typename也可以
//该模版只对接下来的第一个函数有用，如果函数模版重载的话对重载函数也有用
template<class  T> 
void mySwap(T& t1, T& t2) {
    T tmpT;
    tmpT = t1;
    t1 = t2;
    t2 = tmpT;
}


int main() {
    //模板方法 
    int num1 = 1, num2 = 2;
    mySwap(num1,num2);  //1.自动类型推导
    // mySwap<int>(num1, num2);  //2.显示指定类型
    printf("num1:%d, num2:%d\n", num1, num2);  
    return 0;
}
```

## 类型推断
普通函数可以进行自动类型转换（比如入参规定为int，实际传char）
函数模版不允许进行自动类型转换.
```cpp
template <typename T>
T max(T a, T b);

void A()
{
    max(3, 1.2); // error 没有与参数列表匹配的 函数模板 "max" 实例
}
```

有两种办法解决以上错误：
1. 对参数做类型转换
`max(static_cast<double>(4), 7.2); // OK`
2. 显式地指出类型参数 T 的类型， 这样编译器就不再会去做类型推导。
`max<double>(4, 7.2); // OK`
3. 指明调用参数可能有不同的类型（多个模板参数） 。
