值得一提的是，find_if() 和 find_if_not() 函数都定义在<algorithm>头文件中。因此在使用它们之前，程序中要先引入此头文件：
#include <algorithm>

C++ find_if()函数
和 find() 函数相同，find_if() 函数也用于在指定区域内执行查找操作。不同的是，前者需要明确指定要查找的元素的值，而后者则允许自定义查找规则。

所谓自定义查找规则，实际上指的是有一个形参且返回值类型为 bool 的函数。值得一提的是，该函数可以是一个普通函数（又称为一元谓词函数），比如：
```cpp
bool mycomp(int i) {
  return ((i%2)==1);
}
```
上面的 mycomp() 就是一个一元谓词函数，其可用来判断一个整数是奇数还是偶数。

也可以是一个函数对象，比如：
```cpp
//以函数对象的形式定义一个 find_if() 函数的查找规则
class mycomp2 {
public:
    bool operator()(const int& i) {
        return ((i % 2) == 1);
    }
};
```
此函数对象的功能和 mycomp() 函数一样。

确切地说，find_if() 函数会根据指定的查找规则，在指定区域内查找第一个符合该函数要求（使函数返回 true）的元素。

find_if() 函数的语法格式如下：
`InputIterator find_if (InputIterator first, InputIterator last, UnaryPredicate pred);`

其中，first 和 last 都为输入迭代器，其组合 [first, last) 用于指定要查找的区域；pred 用于自定义查找规则。
值得一提的是，由于 first 和 last 都为输入迭代器，意味着该函数适用于所有的序列式容器。甚至当采用适当的谓词函数时，该函数还适用于所有的关联式容器（包括哈希容器）。

同时，该函数会返回一个输入迭代器，当查找成功时，该迭代器指向的是第一个符合查找规则的元素；反之，如果 find_if() 函数查找失败，则该迭代器的指向和 last 迭代器相同。

举个例子：
```cpp
#include <iostream>     // std::cout
#include <algorithm>    // std::find_if
#include <vector>       // std::vector
using namespace std;
//以函数对象的形式定义一个 find_if() 函数的查找规则
class mycomp2 {
public:
    bool operator()(const int& i) {
        return ((i % 2) == 1);
    }
};
int main() {
    vector<int> myvector{ 4,2,3,1,5 };
    //调用 find_if() 函数，并以 IsOdd() 一元谓词函数作为查找规则
    vector<int>::iterator it = find_if(myvector.begin(), myvector.end(), mycomp2());
    cout << "*it = " << *it;
    return 0;
}
```
程序执行结果为：
*it = 3

值得一提的是，C++ STL find_if()官网给出了 find_if() 函数底层实现的参考代码（如下所示），感兴趣的读者可自行分析，这里不做过多描述：
```cpp
template<class InputIterator, class UnaryPredicate>
InputIterator find_if (InputIterator first, InputIterator last, UnaryPredicate pred)
{
    while (first!=last) {
        if (pred(*first)) return first;
        ++first;
    }
    return last;
}
```
