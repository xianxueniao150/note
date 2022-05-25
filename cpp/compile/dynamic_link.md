## 动态链接可以按以下两种方式进行：
1. 在第一次加载并运行时进行 (load-time linking).
	– Linux通常由动态链接器(ld-linux.so)自动处理
	– 标准C库 (libc.so) 通常按这种方式动态被链接
2. 在已经开始运行后进行(run-time linking) 
	在Linux中，通过调用 dlopen()等接口来实现


## 动态共享库文件
```sh
gcc -c myproc1.c myproc2.c
gcc -shared -fPIC -o mylib.so myproc1.o myproc2.o # libc.so无需明显指出
```

## PIC：位置无关代码(Position Independent Code)
1）保证共享库代码的位置可以是不确定的
2）即使共享库代码的长度发生变化，也不会影响调用它的程序

## 加载时动态链接
加载目标程序时，如果加载器(execve)发现在其程序头表中有 .interp 段，其中包含了动态链接器路径名 ld-linux-x86-64.so，那么加载器就会根据指定路径加载并启动动
态链接器运行。动态链接器完成相应的重定位工作后，再把控制权交给目标程序，启动其第一条指令执行。

- 编译器将原始代码文件编译成为可重定位的目标文件。
- 链接器 ld 将可重定位目标文件与动态链接库进行部分链接生成部分链接的文件 m。注意这里 ld 并没有将 libc.so 中使用到的模块的代码段和数据段拷贝到 m 中，而是拷贝了一下符号表和可重定位信息。
- 在生成的部分链接文件 m 中，包含了一个 .interp 节 (Dynamic Linker)，其保存了动态链接器的路径名。加载器在加载 m 时首先加载和运行这个动态链接器（在 Linux 下典型是 ld-linux.so)。
 - 动态链接器重定位 libc.so 的文本和数据段到某个存储器段上，然后重定位 m 中所有对 libc.so 定义的符号的引用。
- 之后跳到应用程序起始地址开始执行，这时共享库的位置完全固定，在整个程序运行期间都不会发生变化。

## 使用共享库
链接器： 工作于链接阶段，工作时需要 -l 和 -L
动态链接器： 工作于程序运行阶段，工作时需要提供动态库所在目录位置

可以用ldd观察程序依赖的.so文件是否存在not found情况

### 编译链接时的动态库搜索路径的顺序
首先从gcc命令的参数-L指定的路径寻找；再从环境变量LIBRARY_PATH指定的路径寻址；再从默认路径/lib、/usr/lib、/usr/local/lib寻找。

### 执行二进制文件时的动态库搜索路径的顺序
首先搜索编译目标代码时指定的动态库搜索路径；再从环境变量LD_LIBRARY_PATH指定的路径寻址；再从配置文件/etc/ld.so.conf中指定的动态库搜索路径；再从默认路径/lib、/usr/lib寻找。


为了让程序运行时能够找到共享库，有以下几种方法
- 运行时用LD_LIBRARY_PATH指定共享库所在文件夹
- 链接时使用-Wl,-rpath指定共享库所在文件夹
- 运行时使用LD_PRELOAD指定要加载的共享库

动态库的加载顺序为LD_PRELOAD>LD_LIBRARY_PATH>/etc/ld.so.cache>/lib>/usr/lib。
LD_PRELOAD是Linux系统的一个环境变量，它可以影响程序的运行时的链接(Runtime linker),它允许你定义在程序运行前优先加载的动态链接库。

```cpp
//hello.c
#include <stdio.h>
void hello(void) {
    printf("hello\n");
}
```

```cpp
void hello(void);
void main(void) {
    hello();
}
```

```sh
# 创建共享库
ubuntu@VM-12-3-ubuntu:~/test/dltest$ gcc -c hello.c
ubuntu@VM-12-3-ubuntu:~/test/dltest$ gcc -shared -o libhello.so hello.o
# 生成可执行文件
ubuntu@VM-12-3-ubuntu:~/test/dltest$ gcc main.c -lhello -L .
ubuntu@VM-12-3-ubuntu:~/test/dltest$ ldd a.out
	linux-vdso.so.1 (0x00007ffc72dd5000)
	libhello.so => not found
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f07a6304000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f07a6508000)
ubuntu@VM-12-3-ubuntu:~/test/dltest$ ./a.out
./a.out: error while loading shared libraries: libhello.so: cannot open shared object file: No such file or directory
# 使用LD_LIBRARY_PATH
ubuntu@VM-12-3-ubuntu:~/test/dltest$ LD_LIBRARY_PATH=./ ./a.out
hello
ubuntu@VM-12-3-ubuntu:~/test/dltest$ LD_LIBRARY_PATH=./ ldd a.out
	linux-vdso.so.1 (0x00007ffd67ff3000)
	libhello.so => ./libhello.so (0x00007fcf980a0000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fcf97ea3000)
	/lib64/ld-linux-x86-64.so.2 (0x00007fcf980ac000)
# 使用-rpath
ubuntu@VM-12-3-ubuntu:~/test/dltest$ gcc main.c -lhello -L . -Wl,-rpath .
ubuntu@VM-12-3-ubuntu:~/test/dltest$ ldd a.out
	linux-vdso.so.1 (0x00007fff289ff000)
	libhello.so => ./libhello.so (0x00007fe236416000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fe236219000)
	/lib64/ld-linux-x86-64.so.2 (0x00007fe236422000)
ubuntu@VM-12-3-ubuntu:~/test/dltest$ ./a.out
hello
```











