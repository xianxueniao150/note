## 头文件、库文件的查找路径
使用尖括号首先检索标准路径，看看这些文件夹下是否有该头文件；如果没有，也不会检索当前文件所在路径，并将报错。
使用双引号首先检索文件的当前路径；如果没有，再检索标准路径。

## free空指针
如果free一个空指针，是没有任何事情发生的。
但是如果两次free一个已经分配内存的指针(即double free)一个指针是有问题的。
所以在申明一个指针的时候，最好赋初值NULL，例如char* str = NULL,后面不小心free了也没有问题发生。
free一块malloc的指针后，需要将指针置为NULL，可以避免double free。


## 变量
定义：[存储类型]  数据类型  标识符 = 值

存储类型：
- auto: 默认，自动分配空间，自动回收空间
- register: （建议型）寄存器类型，使用有限制
- static: 静态性，自动初始化为0值或空值；static修饰的变量或者函数只能在当前.c文件中执行（有点private的意思）
- extern: 说明型，引用工程中其他文件定义的全局变量

### static 定义的变量只会在第一次被调用的时候执行，后面会被忽略
如下函数在main中执行三次，最终会输出2
```cpp
void func(){
    static int x=0;
    printf("%d\n",x++);
}
```

### 全局变量：
相同的全局变量在整个工程中只能定义一次
main.c
```cpp
#include <stdio.h>
#include <stdlib.h>
#include "a.h"

int age=10;

int main(){

    func();
    exit(0);
}
```


```cpp
a.c
#include "a.h"

//这里如果显式赋值的话，编译直接报错重复申明，但是不赋值的话可以正常运行，下面输出10
//这里前面加不加extern的执行结果都是一样的
//这里如果不声明这个变量的话，编译都过不去
int age;

void func(){

    printf("%d\n",age);
}
```


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
