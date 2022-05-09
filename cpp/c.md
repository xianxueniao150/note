## free空指针
如果free一个空指针，是没有任何事情发生的。
但是如果两次free一个已经分配内存的指针(即double free)一个指针是有问题的。
所以在申明一个指针的时候，最好赋初值NULL，例如char* str = NULL,后面不小心free了也没有问题发生。
free一块malloc的指针后，需要将指针置为NULL，可以避免double free。


## __thread 关键字
 __thread是GCC内置的线程局部存储设施。_thread变量每一个线程有一份独立实体，各个线程的值互不干扰。可以用来修饰那些带有全局性且值可能变，但是又不值得用全局变量保护的变量。

```cpp
__thread int count = 0;
int main()
{
    //创建线程A
    //创建线程B
    //此时A和B线程都有一个实体 count，二者并不相同
}
```
