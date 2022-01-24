checksec 可以单独安装也可以使用peda内置的

### ASLR (Address Space Layout Randomization)
系统的防护措施，程序装载时生效
```sh
/proc/sys/kernel/randomize_va_space = 0：没有随机化。即关闭 ASLR
/proc/sys/kernel/randomize_va_space = 1：保留的随机化。共享库、栈、mmap() 以及 VDSO 将被随机化
/proc/sys/kernel/randomize_va_space = 2：完全的随机化。在randomize_va_space = 1的基础上，通过 brk() 分配的内存空间也将被随机化
```

### Stack-canary
栈溢出保护是一种缓冲区溢出攻击缓解手段，编译时生效
在刚进入函数时，在栈上放置一个标志canary，在函数返回时检测其是否被改变。以达到防护栈溢出的目的
```sh
gcc -fno-stack-protector -o hello test.c   //禁用栈保护
gcc -fstack-protector -o hello test.c    //启用堆栈保护，不过只为局部变量中含有 char 数组的函数插入保护代码
gcc -fstack-protector-all -o hello test.c  //启用堆栈保护，为所有函数插入保护代码
```

### NX(No-eXecute)
编译时决定是否生效，由操作系统实现
通过在内存页的标识中增加“执行”位, 可以表示该内存页是否可以执行, 若程序代码的 EIP 执行至不可运行的内存页, 则 CPU 将直接拒绝执行“指令”造成程序崩溃
```sh
gcc -o  hello test.c // 默认情况下，开启NX保护
gcc -z execstack -o  hello test.c // 禁用NX保护
gcc -z noexecstack -o  hello test.c // 开启NX保护
```

### PIE
PIE(Position-Independent Executable, 位置无关可执行文件)技术与 ASLR 技术类似,ASLR 将程序运行时的堆栈以及共享库的加载地址随机化, 而 PIE 技术则在编译时将程序编译为位置无关, 即程序运行时各个段（如代码段等）加载的虚拟地址也是在装载时才确定。这就意味着, 在 PIE 和 ASLR 同时开启的情况下, 攻击者将对程序的内存布局一无所知, 传统的改写
GOT 表项的方法也难以进行, 因为攻击者不能获得程序的.got 段的虚地址。
若开启一般需在攻击时泄露地址信息

gcc -o hello test.c  // 默认情况下，不开启PIE
gcc -fpie -pie -o hello test.c  // 开启PIE，此时强度为1
gcc -fPIE -pie -o hello test.c  // 开启PIE，此时为最高强度2
(还与运行时系统ALSR设置有关）

### RELRO
Relocation Read-Only (RELRO) 此项技术主要针对 GOT 改写的攻击方式。它分为两种，Partial RELRO 和 Full RELRO。
部分RELRO 易受到攻击，例如攻击者可以atoi.got为system.plt，进而输入/bin/sh\x00获得shell
完全RELRO 使整个 GOT 只读，从而无法被覆盖，但这样会大大增加程序的启动时间，因为程序在启动之前需要解析所有的符号。


gcc -o hello test.c // 默认情况下，是Partial RELRO
gcc -z norelro -o hello test.c // 关闭，即No RELRO
gcc -z lazy -o hello test.c // 部分开启，即Partial RELRO
gcc -z now -o hello test.c // 全部开启，即Full RELRO

