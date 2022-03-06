我们知道 C++ 中本来就有引用的存在，为何 C++11 中还要引入一个 std::ref 了？主要是考虑函数式编程（如 std::bind）在使用时，是对参数直接拷贝，而不是引用。下面通过例子说明
示例1：
```cpp
#include <functional>
#include <iostream>

void f(int &n1, int &n2, const int &n3)
{
    std::cout << "In function: " << n1 << ' ' << n2 << ' ' << n3 << '\n';
    ++n1; // increments the copy of n1 stored in the function object
    ++n2; // increments the main()'s n2
    // ++n3; // compile error
}

int main()
{
    int n1 = 1, n2 = 2, n3 = 3;
    std::cout << "Before function: " << n1 << ' ' << n2 << ' ' << n3 << '\n';
    std::function<void()> bound_f = std::bind(f, n1, std::ref(n2), std::cref(n3));
    bound_f();
    std::cout << "After function: " << n1 << ' ' << n2 << ' ' << n3 << '\n';
}
```
Before function: 1 2 3
In function: 1 2 3
After function: 1 3 3

上述代码在执行 std::bind 后，在函数 f() 中 n1 的值仍然是 1，n2 改成了修改的值，说明 std::bind 使用的是参数的拷贝而不是引用，因此必须显示利用 std::ref 来进行引用绑定。

示例2：
```cpp
#include <functional>
#include <iostream>
#include <thread>

void threadFunc(std::string &str, int a)
{
    str = "change by threadFunc";
    a = 13;
}

int main()
{
    std::string str("main");
    int a = 9;
    std::thread th(threadFunc, std::ref(str), a);

    th.join();

    std::cout<<"str = " << str << std::endl;
    std::cout<<"a = " << a << std::endl;

    return 0;
}
```


输出：
str = change by threadFunc
a = 9

可以看到，和 std::bind 类似，多线程的 std::thread 也是必须显式通过 std::ref 来绑定引用进行传参，否则，形参的引用声明是无效的。n
