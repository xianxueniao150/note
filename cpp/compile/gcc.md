```sh
-E   只做预处理（替换所有以#开头的东西）,这个不生成文件,结果直接输出
-c  只做预处理，编译，汇编。得到二进制文件
-o 指定输出的文件名
-g  编译时添加调试语句，用于gdb调试
-Wall  显示所有警告信息（比如某个变量定义了但是未使用）
-w    关闭警告信息
-std=c++11    设置编译标准
```

-I    指定头文件搜索目录
当头文件和源码不在一个目录下时，需要指定头文件所在位置， /usr/include目录一般是不用指定的

### -static 采用静态链接
默认情况下，gcc是使用动态链接的。
查看文件大小，会发现静态链接生成的文件会比动态链接大很多，这是因为静态链接把glibc库相关的代码全部复制过来了

### -D   向程序中“动态”注册宏定义
-D与具体宏之间无空格
 gcc flushtest.c -o flushtest -D_FILE_OFFSET_BITS=64

或者makefile里面开头加上
CFLAGS+=-D_FILE_OFFSET_BITS=64

### -O[n]    优化源代码
-O 同时减小代码的长度和执行时间，其效果等价于-O1
-O0 表示不做优化
-O1 为默认优化
-O2 除了完成-O1的优化之外，还进行一些额外的调整工作，如令调整等。
-O3 则包括循环展开和其他一些与处理特性相关的优化工作。

### -l  和  -L     指定库文件  |  指定库文件路径
```sh
# -l参数(小写)就是用来指定程序要链接的库，-l参数紧接着就是库名
# 在/lib和/usr/lib和/usr/local/lib里的库直接用-l参数就能链接

# 链接glog库
g++ -lglog test.cpp

# 如果库文件没放在上面三个目录里，需要使用-L参数(大写)指定库文件所在目录
# -L参数跟着的是库文件所在的目录名

# 链接mytest库，libmytest.so在/home/bing/mytestlibfolder目录下
g++ -L/home/bing/mytestlibfolder -lmytest test.cpp
```
