## 静态持续变量
1. C++为静态存储持续性变量提供了3种链接性：
* 外部链接性（可在其他文件中访问）
* 内部链接性（只能在当前文件中访问）
* 无链接性（只能在当前函数或代码块中访问）
	
由于静态变量的数量在程序运行期间是不变的，因此程序不需要使用特殊的装置（如栈）来管理它们, 编译器将分配固定的内存块来存储所有的静态变量，这些变量在整个程序执行期间一直存在

2. 如何创建这3中静态持续变量？
要想创建链接性为外部的静态持续变量，必须在代码块的外面声明它； 
要想创建链接性为内部的静态持续变量，必须在代码块的外面声明它，并且使用static限定符； 
要想创建链接性为外部的静态持续变量，必须在代码块内声明它，并且使用static限定符；

3. 程序举例： 
```cpp
int global = 100;         // static duration, external linkage
static int one_file = 50; // static duration, internal linkage

void fun1()
{
    static int count = 0; // static duration, no linkage
}
```
global、one_file与count为静态持续变量，在整个程序执行期间都存在。 

在fun1()中定义的count的作用域为局部，没有链接性，这意味着只能在fun1()函数中使用它。然而，即使在funct1()函数没有被执行时，count也留在内存中。 

由于one_file的链接性为内部，因此只能在包含上述代码的文件中使用它；
由于global的链接性为外部，因此可以在程序的其他文件中使用它。 


## 在类中，有时候为了避免误操作而修改了一些人们不希望被修改的数据，此时就必须借助const关键字加以限定了。

### const成员变量
const成员变量其用法和普通的const变量用法相似，在定义时只需在前面加上const关键字即可。const成员变量的初始化只有唯一的一条途径：参数初始化表。

### const成员函数
const成员函数可以使用类中的所有成员变量，但是不能修改变量的值，这种措施主要还是为了保护数据而设置的。
```cpp
class book
{
public:
    void setprice(double a) const
    {
        price = a; // error 表示式必须是可修改的左值
    }

    void display() const
    {
        cout << "The price is $ " << price << endl;
    }

private:
    double price;
};
```

## const对象
const对象定义的基本语法如下：
    const 类名 对象名(实参名);
    类名 const 对象名(实参名);

这两种定义方式都是可以的，我们一旦将对象定义为常对象之后，该对象就只能调用类中的常成员函数了。

```cpp
#include<iostream>
using namespace std;
class book
{
public:
    void setprice(double a);
    void display() const;
private:
    double price;
};

void book::display()const
{
    cout<<"The price of "<<title<<" is $"<<price<<endl;
}

void book::setprice(double a)
{
    price = a;
}

int main()
{
    const book Alice();
    Alice.display();
    Alice.setprice(51.0);//compile error
    return 0;
}
```


有些时候我们在程序设计过程中要求修改常对象中的某个成员变量，这个时候如果是普通的成员变量是不能被修改的。为了满足这一需求，C++提供了mutable关键字。
```cpp
mutable int var;
```
通过这样的声明将变量var声明为可变的成员变量，此时如果要修改常对象的该变量时，只需要通过常对象调用const成员函数修改该变量即可。

