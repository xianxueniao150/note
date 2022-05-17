## 链接操作的步骤
Step 1
	1）确定符号引用关系（符号解析）
Step 2. 重定位
	2）合并相关.o文件(将多个代码段与数据段分别合并为一个单独的代码段和数据段)
	3）计算每个定义的符号在虚拟地址空间中的绝对地址
	4）将可执行文件中符号引用处的地址修改为重定位后的地址信息



## 链接符号的类型
每个可重定位目标模块m都有一个符号表，它包含了在m中定义和引用的符号。有三种链接器符号：
- Global symbols（模块内部定义的全局符号） 由模块m定义并能被其他模块引用的符号。例如，非static C函数和非static的C全局变量
- External symbols（外部定义的全局符号） 由其他模块定义并被模块m引用的全局符号
- Local symbols（本模块的局部符号） 仅由模块m定义和引用的本地符号。例如，在模块m中定义的带static的C函数和全局变量

链接器不关心局部变量

## 目标文件中的符号表
.symtab 节记录符号表信息

## 符号解析（Symbol Resolution）
目的：将每个模块中引用的符号与某个目标模块中的定义符号建立关联。
符号解析也称符号绑定
```asm
add B
jmp L0
……
L0：sub 23
……
B： ……

确定L0的地址，
再在jmp指令中
填入L0的地址
所有定义符号的值就是其目标所在的首地址
```

将引用符号与定义符号建立关联后，就可在重定位时将引用符号的地址重定位为相关联的定义符号的地址。

“符号的定义”其实质是什么？
指被分配了存储空间。为函数名即指其代码所在区；为变量名即指其所占的静态数据区。

## 多重定义符号
### 全局符号的强/弱特性
– 函数名和已初始化的全局变量名是强符号
– 未初始化的全局变量名是弱符号

### 多重定义符号的处理规则
Rule 1: 强符号不能多次定义
– 强符号只能被定义一次，否则链接错误
Rule 2: 若一个符号被定义为一次强符号和多次弱符号，则按强定义为准
– 对弱符号的引用被解析为其强定义符号
Rule 3: 若有多个弱符号定义，则任选其中一个
– 使用命令 gcc –fno-common链接时，会告诉链接器在遇到多个弱定义的全局符号时输出一条警告信息。

符号解析的结果就是每个符号最终只能有一个确定的定义（即每个符号仅占一处存储空间）

### 符号定义建议
– 尽量使用本地变量（static）
– 全局变量要赋初值
– 外部全局变量要使用extern

```cpp
//main.c
# include <stdio.h>
int y=100;
int z;
void p1(void);
int main()
{
    z=1000;
    p1( );
    printf("y=%d, z=%d\n", y, z);
    return 0;
}
```

```cpp
//p1.c
int y;
int z;
void p1( )
{
    y=200;
    z=2000;
}
```

```sh
$ gcc main.c p1.c
# 意想不到的结果
$ ./a.out
y=200, z=2000

# 加上 -fno-common 直接报错
$ gcc -fno-common  main.c p1.c
/usr/bin/ld: /tmp/cc2bUI6s.o:(.bss+0x0): multiple definition of `y'; /tmp/ccP9wwyr.o:(.data+0x0): first defined here
/usr/bin/ld: /tmp/cc2bUI6s.o:(.bss+0x4): multiple definition of `z'; /tmp/ccP9wwyr.o:(.bss+0x0): first defined here
collect2: error: ld returned 1 exit status

#如果把p1.c的y定义为double的话,最终能编译成功，但是打印的结果是不可知的
$ gcc main.c p1.c
/usr/bin/ld: warning: alignment 4 of symbol `y' in /tmp/cc5OiJtR.o is smaller than 8 in /tmp/cc5L9t2N.o
```

## 重定位信息
• 汇编器遇到引用时，生成一个重定位条目
• 数据引用的重定位条目在.rel_data节中
• 指令中引用的重定位条目在.rel_text节中
• IA-32有两种最基本的重定位类型
	– R_386_32: 绝对地址
	– R_386_PC32: PC相对地址
