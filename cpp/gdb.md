GDB可以分析崩溃程序产生的core文件


## 常用调试命令参数
调试开始：执行gdb [exefilename] ，进入gdb调试程序，其中exefilename为要调试的可执行文件名

```sh
## 以下命令后括号内为命令的简化使用，比如run（r），直接输入命令 r 就代表命令run

help(h)        # 查看命令帮助，具体命令查询在gdb中输入help + 命令 
run(r)         # 重新开始运行文件（run-text：加载文本文件，run-bin：加载二进制文件）
start          # 单步执行，运行程序，停在第一行执行语句
list(l)        # 查看原代码（list-n,从第n行开始查看代码。list+ 函数名：查看具体函数）
where          # 打印从开始到现在的堆栈
set            # 设置变量的
next(n)        # 单步调试（逐过程，函数直接执行,后面可以加上num，表示执行后面的num条指令，然后再停住。
step(s)        # 单步调试（逐语句：跳入自定义函数内部执行
backtrace(bt)  # 查看函数的调用的栈帧和层级关
frame(f)       # 切换函数的栈
info(i)        # 查看函数内部局部变量的数
finish         # 结束当前函数，返回到函数调用
continue(c)    # 继续运
print(p)       # 打印
quit(q)        # 退出gd
display                      # 追踪查看具体变量
undisplay                    # 取消追踪观察变
watch                        # 被设置观察点的变量发生修改时，打印显
i watch                      # 显示观察
x                            # 查看内存x/20xw 显示20个单元，16进制，4字节每单
run argv[1] argv[2]          # 调试时命令行传
et follow-fork-mode child   # Makefile项目管理：选择跟踪父子进程（fork()）
```

Tips:
- 编译程序时需要加上-g，之后才能用gdb进行调试：gcc -g main.c -o main
- 回车键：重复上一命令

## 产看函数调用栈
### 查看栈回溯信息
```sh
backtrace(bt)

bt full #显示各个函数的局部变量值
bt full n #意思是从内向外显示n个栈桢，及其局部变量
bt n # 只显示最近的两个栈帧
bt -n # 只显示最远的两个栈帧
```
### 切换栈帧
为什么要切换栈帧呢？因为每一个栈帧所对应的程序的运行上下文都不同(比如想看局部变量，或者想看对应代码)
```sh
# 切换栈帧,其中n 是bt命令输出中的编号
frame(f) n
```
还可以使用命令up和down来切换帧。up和down都是基于当前帧来计数的。比如，当前帧号为1，up 1则切换到2号帧，down 1则切换到0号帧
还可以使用以下命令来切换帧：f 帧地址

### 查看帧信息
```sh
info(i) frame(f) n
```
帧的详细信息包括帧地址、rip地址、函数名、函数参数等信息

## 线程管理
```sh
# 查看当前进程所有的线程信息,前面带*号的表示当前线程
info threads

# 切换线程
thread(t) 线程ID

# 为线程设置断点
break(b) 断点 thread 线程ID

# 为指定线程执行命令
# 可以同时指定多个，或者用all（表示所有)
thread apply 线程ID 命令
```
当前线程很重要，因为很多命令都是针对当前线程有效。比如，查看栈回溯的bt命令、查看栈帧的f命令等都是针对当前线程。如果想要查看某个线程堆栈的相关信息，必须要先切换到该线程。

死锁调试时先按ctrl+c,然后就可以执行gdb命令了

## 断点
```sh
c #去下一个断点
info b(reakpoints) #查看所有断点
delete breakpoints num    # 删除第num个断点
enable breakpoints           # 启用断点
disable breakpoints          # 禁用断点
```

### 打断点
break命令设置永久断点，而tbreak命令设置临时断点

如果要在当前文件中的某一行打断点，直接b linenum即可
也可以显式指定文件，b file:linenum
gdb会对所有匹配的文件设置断点。你可以通过指定（部分）路径，来区分相同的文件名：
(gdb) b a/file.c:6


## 打印

### gdb中使用“x”命令来打印内存的值，格式为“x/nfu addr”。含义为以f格式打印从addr开始的n个长度单元为u的内存值。参数具体含义如下：
a）n：输出单元的个数。
b）f：是输出格式。比如x是以16进制形式输出
c）u：标明一个单元的长度。b是一个byte，h是两个byte（halfword），w是四个byte（word），g是八个byte（giant word）。

f和u的位置可以互换
### 打印源代码行
```
接着打印上次list命令打印出代码后面的代码。如果是第一次执行list命令则会显示当前正在执行代码位置附近的代码。
(gdb) l 

list命令可以指定行号，函数：
(gdb) l 24
(gdb) l main

还可以指定向前或向后打印：
(gdb) l -

还可以指定范围：
(gdb) l 1,10

```
### 打印变量的类型
```
(gdb) ptype var
```

### “set print pretty on”命令，这样每行只会显示结构体的一名成员，而且还会根据成员的定义层次进行缩进
```
(gdb) set print pretty on
(gdb) p st
```
### 打印函数所有局部变量
```
(gdb) info locals
```

## 汇编
si命令类似于s命令，但针对汇编指令。
ni命令类似于n命令，但针对汇编指令。

## 动态库调试
Linux系统动态库的链接方式也分为静态链接和动态链接(调用dlopen等函数)。
静态链接动态库的程序需要在程序启动时加载动态库。
动态链接则是在调用动态库函数时才会真正载入动态库，而不是在程序启动时。


在程序启动前，由于动态库还没加载，所以调试符号也没有被加载,当我们为动态库中的文件设置断点时，gdb会询问是否为动态库设置一个断点，如下所示。输入y为动态库设置断点，但是该断点的状态是挂起的，gdb并不了解将来是否会命中。
实际是即使在gdb的命令窗口中为一个不存在的文件或者函数设置断点也是允许的，只不过同样是挂起的状态，而且永远不会命中。
```sh
(gdb) b test.cpp:calc_pi
No source file named test.cpp.
Make breakpoint pending on future shared library load? (y or [n]) y
Breakpoint 2 (test.cpp:calc_pi) pending.
(gdb) info b
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x0000000000400a1e in main() at testexe.cpp:6
2       breakpoint     keep y   <PENDING>          test.cpp:calc_pi
```
对于静态链接而言，当程序启动后，比如运行到main断点时,动态库中的断点就不再是挂起的状态,而是有了确切的地址。
对于动态链接而言，只有执行过dlopen之后,动态库中的断点才有了确切的地址。

对于附加到进程调试动态库,如果运行时指定了LD_LIBRARY_PATH，并且使用的是相对路径，那么也必须在程序运行的目录下面执行gdb，否则就找不到动态库
warning: Could not load shared library symbols for ../testso/libtest.so.

如果使用ldconfig的方式或者将动态库复制到/usr/lib中的方式来成功加载动态库，使用gdb附加程序的方式会更加方便，这样在任意位置都可以启动附加进程，而不用到特定的目录中去启动gdb。

## Linux系统中的转储文件
```cpp
gdb 可执行文件名 转储文件名
```
指定可执行文件的目的是为了获得调试符号信息

### 转储文件生成
1. gdb attach 正在运行的进程，然后执行 gcore 转储文件名
