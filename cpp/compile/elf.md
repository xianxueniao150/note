## elf文件分类
- 可重定位目标文件 (.o)
	- 其代码和数据可和其他可重定位文件合并为可执行文件
	- 每个.o 文件由对应的.c文件生成
	- 每个.o文件代码和数据地址都从0开始
- 可执行目标文件 (默认为a.out)
	- 包含的代码和数据可以被直接复制到内存并被执行
	- 代码和数据地址为虚拟地址空间中的地址
- 共享的目标文件 (.so)
	- 特殊的可重定位目标文件

## 两种视图
– 链接视图（被链接）：可重定位目标文件 (Relocatable object files)
– 执行视图（被执行）：可执行目标文件（Executable object files）

链接视图—可重定位目标文件
• 可被链接（合并）生成可执行文件或共享目标文件
• 静态链接库文件由若干个可重定位目标文件组成
• 包含代码、数据（已初始化.data和未初始化.bss）
• 包含重定位信息（指出哪些符号引用处需要重定位）
• 文件扩展名为.o（相当于Windows中的 .obj文件）

执行视图—可执行目标文件
• 包含代码、数据（已初始化.data和未初始化.bss）
• 定义的所有变量和函数已有确定地址（虚拟地址空间中的地址）
• 符号引用处已被重定位，以指向所引用的定义符号
• 可被CPU直接执行，指令地址和指令给出的操作数地址都是虚拟地址

```sh
+-++-+-+-+-+-+-+-+-+-+-+-+-+
|     elf header           
+-++-+-+-+-+-+-+-+-+-+-+-+-+
|     .text          
+-++-+-+-+-+-+-+-+-+-+-+-+-+
|     other section ...         
+-++-+-+-+-+-+-+-+-+-+-+-+-+
|     Section header table（节头表）          
+-++-+-+-+-+-+-+-+-+-+-+-+-+
```

## elf头（ELF Header）
位于ELF文件开始，包含文件结构说明信息。分32位系统对应结构和64位系统对应结构（32位版本、64位版本）
```sh
$ readelf -h hello.o
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              REL (Relocatable file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x0 #程序执行的入口地址
  Start of program headers:          0 (bytes into file) #程序头表（段头表）的起始位置
  Start of section headers:          800 (bytes into file) #节头表相对于文件开始处的偏移量
  Flags:                             0x0
  Size of this header:               64 (bytes) #头部占64字节
  Size of program headers:           0 (bytes) #段头表每个表项占用字节
  Number of program headers:         0 #段头表表项数
  Size of section headers:           64 (bytes) #节头表每个表项占用字节
  Number of section headers:         14	#节头表表项数
  Section header string table index: 13
```

## 节头表
```sh
$ readelf -SW hello.o
There are 14 section headers, starting at offset 0x320:

Section Headers:
  [Nr] Name              Type            Address          Off    Size   ES Flg Lk Inf Al
  [ 0]                   NULL            0000000000000000 000000 000000 00      0   0  0
  [ 1] .text             PROGBITS        0000000000000000 000040 000020 00  AX  0   0  1
  [ 2] .rela.text        RELA            0000000000000000 000260 000030 18   I 11   1  8
  [ 3] .data             PROGBITS        0000000000000000 000060 000000 00  WA  0   0  1
  [ 4] .bss              NOBITS          0000000000000000 000060 000000 00  WA  0   0  1
  [ 5] .rodata           PROGBITS        0000000000000000 000060 00000e 00   A  0   0  1
  [ 6] .comment          PROGBITS        0000000000000000 00006e 00002c 01  MS  0   0  1
  [ 7] .note.GNU-stack   PROGBITS        0000000000000000 00009a 000000 00      0   0  1
  [ 8] .note.gnu.property NOTE            0000000000000000 0000a0 000020 00   A  0   0  8
  [ 9] .eh_frame         PROGBITS        0000000000000000 0000c0 000038 00   A  0   0  8
  [10] .rela.eh_frame    RELA            0000000000000000 000290 000018 18   I 11   9  8
  [11] .symtab           SYMTAB          0000000000000000 0000f8 000138 18     12  10  8
  [12] .strtab           STRTAB          0000000000000000 000230 00002b 00      0   0  1
  [13] .shstrtab         STRTAB          0000000000000000 0002a8 000074 00      0   0  1
```
.text 为首个表项,偏移量为0x40，为elf的结束位置
.shstrtab 为最后一个表项，结尾处为0x2a8+0x74=796

按4字节对齐的话，elf头开始处就是800,结尾处为800+64*14=1696
```cpp
$ ll hello.o
-rw-rw-r-- 1 ubuntu ubuntu 1696 May 10 22:12 hello.o
```
可见整个可重定位目标文件由elf头、各个section,节头表三部分组成，通过elf头可以定位到节头表，通过节头表可以找到各个section


```sh
readelf -a hello.o    #readelf --all 输出所有ELF包含的信息
```
总共输出了以下部分：ELF Header、Section Table和各个Section。

## Section
- .text 保存的是程序的指令
- .rela.text 保存的是需要重定位的指令（某些函数在该目标文件中找不到，需要在链接的时候重定位指令中的地址部分）
- .data 保存的是已初始化的全局变量和已初始化局部静态变量
- .bss 保存的是未初始化的全局变量和未初始化局部静态变量，而且.bss段只预留位置没有内容，在文件中不占空间
- .rodata 保存的是只读数据段，顾名思义该段存放的数据只允许读操作，例如C语言中用const修饰的数据和字符串常量会放到该段中
- .strtab String Table 字符串表，用于存储ELF文件中用到的各种字符串
- .comment 存放的是编译器的版本信息
- .symtab 保存符号表
- .rel.text 节 .text节的重定位信息，用于重新修改代码段的指令中的地址信息
- .rel.data 节 .data节的重定位信息，用于对被模块使用或定义的全局变量进行重定位的信息
- .debug 节 调试用符号表 (gcc -g)
	
有4个节将会分配存储空间
.text：可执行
.data和.bss：可读可写
.rodata：可读

### .bss节
C语言规定：未初始化的全局变量和局部静态变量的默认初始值为0

将未初始化变量（.bss节）与已初始化变量（.data节）分开的好处
– .data节中存放具体的初始值，需要占磁盘空间
– .bss节中无需存放初始值，只要说明.bss中的每个变量将来在执行时占用几个字节即可，因此，.bss节实际上不占用磁盘空间，提高了磁盘空间利用率

所有未初始化的全局变量和局部静态变量都被汇总到.bss节中，通过专门的“节头表（Section header table）”来说明应该为.bss节预留多大的空间

### .text段
```sh
objdump -s -d hello.o    #-s参数可以将所有段的内容以十六进制的方式打印出来 -d参数可以将包含指令的段反汇编

hello.o:     file format elf64-x86-64

Contents of section .text:
 0000 f30f1efa 554889e5 488d3d00 000000b8  ....UH..H.=.....
 0010 00000000 e8000000 00b80000 00005dc3  ..............].
Contents of section .rodata:
 0000 68656c6c 6f20776f 726c642e 0a00      hello world...
Contents of section .comment:
 0000 00474343 3a202855 62756e74 7520392e  .GCC: (Ubuntu 9.
 0010 342e302d 31756275 6e747531 7e32302e  4.0-1ubuntu1~20.
 0020 30342e31 2920392e 342e3000           04.1) 9.4.0.
Contents of section .note.gnu.property:
 0000 04000000 10000000 05000000 474e5500  ............GNU.
 0010 020000c0 04000000 03000000 00000000  ................
Contents of section .eh_frame:
 0000 14000000 00000000 017a5200 01781001  .........zR..x..
 0010 1b0c0708 90010000 1c000000 1c000000  ................
 0020 00000000 20000000 00450e10 8602430d  .... ....E....C.
 0030 06570c07 08000000                    .W......

Disassembly of section .text:

0000000000000000 <main>:
   0:	f3 0f 1e fa          	endbr64
   4:	55                   	push   %rbp
   5:	48 89 e5             	mov    %rsp,%rbp
   8:	48 8d 3d 00 00 00 00 	lea    0x0(%rip),%rdi        # f <main+0xf>
   f:	b8 00 00 00 00       	mov    $0x0,%eax
  14:	e8 00 00 00 00       	callq  19 <main+0x19>
  19:	b8 00 00 00 00       	mov    $0x0,%eax
  1e:	5d                   	pop    %rbp
  1f:	c3                   	retq
```
我们关注offset=0x14的那一条指令，前面的操作码是0xE8，这是一条近址相对位移调用指令，后面的4个字节是被调用函数的相对于调用指令的下一条指令的偏移量。此时我们可以看到地址是全0，编译器把这条指令的地址部分暂时用地址0x00000000代替，把真正的地址计算工作留给了链接器。


## 可执行目标文件格式
### 与可重定位文件的不同
- ELF头中字段e_entry给出执行程序时第一条指令的地址，而在可重定位文件中，此字段为0
- 多一个程序头表，也称段头表（segment header table）
- 多一个.init节，用于定义_init函数，该函数用来进行可执行目标文件开始执行时的初始化工作
- 少两个.rel节（无需重定位）
