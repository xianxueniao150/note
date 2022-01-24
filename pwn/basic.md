程序在内存中的结构
```sh
stack

shared libararies

heap
bss    存放未初始化的全局变量
data   存放已初始化的全局变量
text   存放代码,字符串常量,只读数据
```

大端序与小端序
```sh
0a0b0c0d

小端序:低地址存放数据低位、高地址存放数据高位
memery
|0a| a+3
|0b| a+2
|0c| a+1
|0d| a

大端序:低地址存放数据高位
memery
|0d|
|0c|
|0b|
|0a|
```

32位程序通过stack传参，64位通过register
x86 通过 int 0x80 指令进行系统调用、amd64 通过 syscall 指令进行系统调用
