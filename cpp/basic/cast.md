## static_cast
在C++语言中static_cast用于数据类型的强制转换，强制将一种数据类型转换为另一种数据类型。例如将整型数据转换为浮点型数据。
```cpp
int a = 10;
int b = 3;
double result = static_cast<double>(a) / static_cast<double>(b);
double result = (double)a / (double)b;  //这样也可以
```

## const_cast
在C语言中，const限定符通常被用来限定变量，用于表示该变量的值不能被修改。而const_cast则正是用于强制去掉这种不能被修改的常数特性，但需要特别注意的是const_cast不是用于去除变量的常量性，而是去除指向常数对象的指针或引用的常量性
```cpp
#include<iostream>
using namespace std;
int main()
{
    const int a = 10;
    const int * p = &a;
    // *p=20;  //compile error
    int *q = const_cast<int *>(p);
    *q = 20;    //fine
    cout <<a<<" "<<*p<<" "<<*q<<endl;
        cout <<&a<<" "<<p<<" "<<q<<endl;
    return 0;
}


10 20 20
0x7fffeeb3c1d4 0x7fffeeb3c1d4 0x7fffeeb3c1d4
```

我们可以看到三者的地址相同，值却不同

## reinterpret_cast
在C++语言中，reinterpret_cast主要有三种强制转换用途：改变指针或引用的类型、将指针或引用转换为一个足够长度的整形、将整型转换为指针或引用类型。在使用reinterpret_cast强制转换过程仅仅只是比特位的拷贝，因此在使用过程中需要特别谨慎！
```cpp
int *a = new int;
double *d = reinterpret_cast<double *>(a);
```
将整型指针通过reinterpret_cast强制转换成了双精度浮点型指针。

## dynamic_cast
dynamic_cast用于类的继承层次之间的强制类型转换

## 继承关系的转换
对于从子类到基类的指针转换，static_cast和dynamic_cast都是成功并且正确的（所谓成功是说转换没有编译错误或者运行异常；所谓正确是指方法的调用和数据的访问输出是期望的结果），这是面向对象多态性的完美体现。

而从基类到子类的转换，static_cast和dynamic_cast都是成功的，但是正确性方面，我对两者的结果都先进行了是否非空的判别：dynamic_cast的结果显示是空指针，而static_cast则是非空指针。但很显然，static_cast的结果应该算是错误的，子类指针实际所指的是基类的对象，而基类对象并不具有子类的Study()方法(除非妈妈又想去接受个"继续教育")。

对于没有关系的两个类之间的转换，输出结果表明，dynamic_cast依然是返回一个空指针以表示转换是不成立的；static_cast直接在编译期就拒绝了这种转换。
