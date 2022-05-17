```sh
# 创建静态库
$ gcc -c myproc1.c myproc2.c
$ ar rcs mylib.a myproc1.o myproc2.o

# 使用静态库
$ gcc –c main.c
$ gcc -static -o myproc main.o libmy.a #libc.a无需明显指出
# or
$ gcc -static -o myproc main.o -L. -lmy

# 列出静态库包含的所有模块(所有.o文件) 
ar -t /usr/lib32/libc.a
```

## 静态共享库
静态库 (.a)
– 将所有相关的目标模块（.o）打包为一个单独的库文件（.a），称为静态库文件 ，也称存档文件（archive）
– 在构建可执行文件时，只需指定库文件名，链接器会自动到库中寻找那些应用程序用到的目标模块，并且只把用到的模块从库中拷贝出来
– 在gcc命令行中无需明显指定C标准库libc.a(默认库)


### 静态库创建
1. 将各个目标模块由.c文件编译成.o文件
2. 用ar命令整合所有.o文件
```sh
ar rs libc.a \
atoi.o printf.o … random.o
```
Archiver（归档器）允许增量更新，只要重新编译需修改的源码并将其.o文件替换到静态库中

### 常用静态库
libc.a ( C标准库 )
– 1392个目标文件（大约8 MB）
– 包含I/O、存储分配、信号处理、字符串处理、时间和日期、随机数生成、定点整数算术运算
libm.a (the C math library)
– 401 个目标文件（大约 1 MB）
– 浮点数算术运算(如sin, cos, tan, log, exp, sqrt, …)

## 符号解析的全过程
E 将被合并以组成可执行文件的所有目标文件集合
U 当前所有未解析的引用符号的集合
D 当前所有定义符号的集合

链接器对外部引用的解析算法要点如下:
– 按照命令行给出的顺序扫描.o 和.a 文件
– 扫描期间将当前未解析的引用记录到一个列表U中
– 每遇到一个新的.o 或 .a 中的模块，都试图用其来解析U中的符号
– 如果扫描到最后，U中还有未被解析的符号，则发生错误

```cpp
//myproc1.c
# include <stdio.h>
void myfunc1() {
    printf("This is myfunc1!\n");
}
```

```cpp
//myproc2.c
# include <stdio.h>
void myfunc2() {
    printf("This is myfunc1!\n");
}
```

```cpp
//main.c
void myfunc1(void);
int main()
{
    myfunc1();
    return 0;
}
```

开始E、U、D为空，首先扫描main.o，把它加入E， 同时把myfun1加入U，main加入D。
接着扫描到mylib.a，将U中所有符号（本例中为myfunc1）与 mylib.a中所有目标模块（myproc1.o和myproc2.o ）依次匹配，发现在myproc1.o中定义了myfunc1 ，故myproc1.o加入E，myfunc1从U转移到D。
在 myproc1.o中发现还有未解析符号printf，将其加到U。不断在mylib.a的各模块上进行迭代以匹配U中的符号，直到U、D都不再变化。此时U中只有一个未解析符号printf，而D中有main和myfunc1。因为模块
myproc2.o没有被加入E中，因而它被丢弃。
接着，扫描默认的库文件libc.a，发现其目标模块printf.o定义了printf，于是printf也从U移到D，并将printf.o加入E，同时把它定义的所有符号加入D，而所有未解析符号加入U。处理完libc.a时，U一定是空的

解析结果：
E中有main.o、myproc1.o、printf.o及其调用的模块(注意：E中无myproc2.o)
D中有main、myproc1、printf及其引用的符号

### 链接顺序
```sh
$ gcc -static -o myproc ./mylib.a main.o
/usr/bin/ld: main.o: in function `main':
main.c:(.text+0x9): undefined reference to `myfunc1'
collect2: error: ld returned 1 exit status
```
首先，扫描mylib，因是静态库，应根据其中是否存在U中未解析符号对应的定义符号来确定哪个.o被加入E。因为开始U为空，故其中两个.o模块都不
被加入E中而被丢弃。 然后，扫描main.o，将myfunc1加入U，直到最后它都不能被解析。 因此，出现链接错误！

好的做法：将静态库放在命令行的最后


假设调用关系如下：
func.o → libx.a 和 liby.a 中的函数
libx.a → liby.a 同时 liby.a → libx.a
则以下命令行可行：
```sh
gcc -static –o myfunc func.o libx.a liby.a libx.a
```
