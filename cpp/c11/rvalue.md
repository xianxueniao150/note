## 什么是左值和右值：
* lvalue 是 loactor value 的缩写，rvalue 是 read value 的缩写
* 左值是指存储在内存中、有明确存储地址（可取地址）的数据；
* 右值是指可以提供数据值的数据（不可取地址）；

通过描述可以看出，区分左值与右值的便捷方法是：可以对表达式取地址（&）就是左值，否则为右值 。所有有名字的变量或对象都是左值，而右值是匿名的。

C++11 中右值可以分为两种：一个是将亡值（ xvalue, expiring value），另一个则是纯右值（ prvalue, PureRvalue）：
* 纯右值：非引用返回的临时变量、运算表达式产生的临时变量、原始字面量和 lambda 表达式等
* 将亡值：与右值引用相关的表达式，比如，T&& 类型函数的返回值、 std::move 的返回值等。

```cpp
int&& value = 520; //520 是纯右值，value 是对字面量 520 这个右值的引用。
class Test
{
};

Test getObj()
{
    Test t;
    return t;
}

int main()
{
    Tet a;
    Test a1 = a; //这里又创建了一个a1对象，运行完毕后会有两个对象

    Test buffer = getTest(); //这里不考虑编译优化的话，如果想复用返回的对象，而不是重新生成一个对象，应该怎么做呢

    Test &buffer = getTest();       //error 非常量引用的初始值必须为左值
    const Test& t = getObj(); //常量左值引用是一个万能引用类型，它可以接受左值、右值、常量左值和常量右值。
    

    Test && t = getObj(); //getObj() 返回的临时对象被称之为将亡值，t 是这个将亡值的右值引用
    return 0;
}
```



## 移动构造函数
在 C++ 中在进行对象赋值操作的时候，很多情况下会发生对象之间的深拷贝，如果堆内存很大，这个拷贝的代价也就非常大，在某些情况下，如果想要避免对象的深拷贝，就可以使用右值引用进行性能的优化。
```cpp
#include <iostream>
using namespace std;

class Test
{
public:
    Test() : m_num(new int(100))
    {
        cout << "construct" << endl;
    }

    Test(const Test &a) : m_num(new int(*a.m_num))
    {
        cout << "copy construct" << endl;
    }

    // 添加移动构造函数
    // Test(Test &&a) : m_num(a.m_num)
    // {
    //     a.m_num = nullptr;
    //     cout << "move construct" << endl;
    // }

    ~Test()
    {
        delete m_num;
        cout << "destruct Test class ..." << endl;
    }

    int *m_num;
};

Test getObj()
{
    Test t;
    return t;
}

int main()
{
    Test t = getObj();
    return 0;
};
```


编译
g++ -std=c++11 -fno-elide-constructors main.cpp && ./a.out


测试代码执行的结果为:
```sh
construct
copy construct
destruct Test class ...
copy construct
destruct Test class ...
destruct Test class ...
```


通过输出的结果可以看到调用 Test t = getObj(); 的时候调用拷贝构造函数对返回的临时对象进行了深拷贝得到了对象 t，在 getObj() 函数中创建的对象虽然进行了内存的申请操作，但是没有使用就释放掉了。如果能够使用临时对象已经申请的资源，既能节省资源，还能节省资源申请和释放的时间，如果要执行这样的操作就需要使用右值引用了，右值引用具有移动语义，移动语义可以将资源（堆、系统对象等）通过浅拷贝从一个对象转移到另一个对象这样就能减少不必要的临时对象的创建、拷贝以及销毁，可以大幅提高 C++ 应用程序的性能。

取消上述程序的移动构造函数注释
测试代码执行的结果如下:
construct
move construct
destruct Test class ...
move construct
destruct Test class ...
destruct Test class ...

通过修改，在上面的代码给 Test 类添加了移动构造函数（参数为右值引用类型），这样在进行 Test t = getObj(); 操作的时候并没有调用拷贝构造函数进行深拷贝，而是调用了移动构造函数，在这个函数中只是进行了浅拷贝，没有对临时对象进行深拷贝，提高了性能。

对于需要动态申请大量资源的类，应该设计移动构造函数，以提高程序效率。需要注意的是，我们一般在提供移动构造函数的同时，也会提供常量左值引用的拷贝构造函数，以保证移动不成还可以使用拷贝构造函数。

上面右值引用减少了生成对象的数量，下面移动构造函数减少了每次生成对象的难度

## && 的特性
在 C++ 中，并不是所有情况下 && 都代表是一个右值引用，具体的场景体现在模板和自动类型推导中，如果是模板参数需要指定为 T&&，如果是自动类型推导需要指定为 auto &&，在这两种场景下 && 被称作未定的引用类型。另外还有一点需要额外注意 const T&& 表示一个右值引用，不是未定引用类型。

推导规则如下：
通过右值推导 T&& 或者 auto&& 得到的是一个右值引用类型
通过非右值（右值引用、左值、左值引用、常量右值引用、常量左值引用）推导 T&& 或者 auto&& 得到的是一个左值引用类型

先来看第一个例子，在函数模板中使用 &&:
```cpp
template<typename T>
void f(T&& param);
f(10); 	
int x = 10;
f(x); 
```

在上面的例子中函数模板进行了自动类型推导，需要通过传入的实参来确定参数 param 的实际类型。
第 4 行中，对于 f(10) 来说传入的实参 10 是右值，因此 T&& 表示右值引用
第 6 行中，对于 f(x) 来说传入的实参是 x 是左值，因此 T&& 表示左值引用

```cpp
int &&a1 = 5;
int &&a2 = a1; //error 无法将右值引用绑定到左值

int&& a1 = 5;
auto&& bb = a1; //a1 为右值引用，推导出的 bb 为左值引用类型
auto&& bb1 = 5; //5 为右值，推导出的 bb1 为右值引用类型

const int& s1 = 100;
const int&& s2 = 100;
auto&& dd = s1; //s1 为常量左值引用，推导出的 dd 为常量左值引用类型
auto&& ee = s2; //s2 为常量右值引用，推导出的 ee 为常量左值引用类型
```

## move
在 C++11 添加了右值引用，并且不能使用左值初始化右值引用，如果想要使用左值初始化一个右值引用需要借助 std::move () 函数，使用std::move方法可以将左值转换为右值。使用这个函数并不能移动任何东西，而是和移动构造函数一样都具有移动语义，将对象的状态或者所有权从一个对象转移到另一个对象，只是转移，没有内存拷贝。


作者: 苏丙榅
链接: https://subingwen.cn/cpp/move-forward/
来源: 爱编程的大丙
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。s
