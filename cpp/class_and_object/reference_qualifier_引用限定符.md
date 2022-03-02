```cpp
class Test{
public:
    void foo(int)&;
    void foo(int)&&;
    void foo(int)const;
};

// 用obj去调用成员函数时
Test obj;
obj.foo(1); 

//实际上
foo(*this, 1);
}
```
在成员函数形参列表后的&，&&, const 实际上是对类对象的类型签名：Test的三个foo函数，完整的声明应该是：
```cpp
void foo(Test&, int);
void foo(Test&&, int);
void foo(const Test&, int);
```
这样就可以清晰分辨出，foo针对Test对象的属性，有三个重载版本。

```cpp
struct Arg
{
    int i = 1;
    int  aget() &&
    {
        std::cout<<"in aget &&\n";
        return i;
        
    }
        
    int& aget() &
    {
        std::cout<<"in aget &\n";
        return i;
    }
};


int main(int argc, const char * argv[])
{
    Arg g1 { 5 };
    g1.aget();
    std::move(g1).aget();
    return 0;
}
```
有人问这个重载有啥用。我重新举个更贴切的例子，看了就明白了。下面这个例子中，get_text()的实现无论对于左值还是右值，都很高效。注意调用的时候用auto&& text = xxx.get_text()，这样调用的语法也能统一起来。
```cpp
#include <iostream>

struct P {
    std::string text;

    std::string& get_text() &
    {
        return text; // *this是左值，直接返回引用
    }
    
    std::string get_text() &&
    {
        return std::move(text); // *this是右值，直接move过去
    }
};

P func()
{
    return P{"this is some text"};
}

int main() {
    // 右值演示
    auto&& s = func().get_text();
    std::cout<<s<<"\n";
    
    // 左值演示
    P p {"another text"};
    auto&& s2 = p.get_text();
    std::cout<<s2<<"\n";
    return 0;
}
```
