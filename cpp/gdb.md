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

### 产看函数调用栈
```sh
bt

bt full #显示各个函数的局部变量值
bt full n #意思是从内向外显示n个栈桢，及其局部变量
```


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
