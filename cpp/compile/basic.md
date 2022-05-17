所谓的文本文件，就是以ASCII字符方式存储的文件。举个例子，如果我们新建一个文件，并输入一串字符hello,那么，这个文件在计算机中保存形式是将h、e、l、l和o根据ASCII表转化成二进制，即0110 1000、0110 0101、0110 1100、0110 1100和0110 1111，然后将这串二进制数字保存成一个文件，放在了对应的位置。

所谓的二进制文件，就是这个文件里保存的是一系列的二进制数字，这些数字人们无法直接理解其意义，但是计算机是可以以一定的规则去理解它。例如，可执行文件是一个二进制文件，当我们使用某些工具查看其内部保存的数据是，只能看到一些二进制数字，但是对应的计算机却能够执行它，并生成相应的结果。

示例程序
```cpp
#include<stdio.h>
int main(void)
{
    printf("hello world.\n");
    return 0;
}
```

## 1.预编译
```sh
gcc -E hello.c -o hello.i
```
执行完成后，我们可以发现生成了一个共732行的文件hello.i，以下是hello.i的文件节选：
```cpp
711 # 840 "/usr/include/stdio.h" 3 4
712 extern void flockfile (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__));
713
714
715
716 extern int ftrylockfile (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) ;
717
718
719 extern void funlockfile (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__));
720 # 858 "/usr/include/stdio.h" 3 4
721 extern int __uflow (FILE *);
722 extern int __overflow (FILE *, int);
723 # 873 "/usr/include/stdio.h" 3 4
724
725 # 2 "hello.c" 2
726
727 # 2 "hello.c"
728 int main(void)
729 {
730     printf("hello world.\n");
731     return 0;
732 }
```

预编译过程主要是处理那些以#号开头的预编译指令如#include、#define、#ifdef、#ifndef等，主要处理的规则如下：
- 将所有的#define删除，并展开所有的宏定义
- 处理条件预编译指令，如#if、#ifdef、#elif、#else、#endif。
- 处理#include预编译指令，将被包含的文件插入到预编译指令（#include）的位置，注意这个过程是递归进行的，意味着被包含的文件中也含有#include指令会递归执行。
- 删除所有的注释符号如//和/**/。
- 添加行号和文件名标识，比如上图中第725行中的#2 hello.c 2，以便于编译时编译器产生调试用的行号信息
- 保留所有的#progma编译指令，因为编译器在后面需要使用它们。

```cpp
//stdio.h
839 /* Acquire ownership of STREAM.  */
840 extern void flockfile (FILE *__stream) __THROW;
841
842 /* Try to acquire ownership of STREAM but do not block if it is not
843    possible.  */
844 extern int ftrylockfile (FILE *__stream) __THROW __wur;
845
846 /* Relinquish the ownership granted for STREAM.  */
847 extern void funlockfile (FILE *__stream) __THROW;
848 #endif /* POSIX */
849
850 #if defined __USE_XOPEN && !defined __USE_XOPEN2K && !defined __USE_GNU
851 /*  X/Open Issues 1-5 required getopt to be declared in this
852    header.  It was removed in Issue 6.  GNU follows Issue 6.  */
853 # include <bits/getopt_posix.h>
854 #endif
855
856 /* Slow-path routines used by the optimized inline functions in
857    bits/stdio.h.  */
858 extern int __uflow (FILE *);
859 extern int __overflow (FILE *, int);
860
861 /* If we are compiling with optimizing read this file.  It contains
862    several optimizing inline functions and macros.  */
863 #ifdef __USE_EXTERN_INLINES
864 # include <bits/stdio.h>
865 #endif
866 #if __USE_FORTIFY_LEVEL > 0 && defined __fortify_function
867 # include <bits/stdio2.h>
868 #endif
869 #ifdef __LDBL_COMPAT
870 # include <bits/stdio-ldbl.h>
871 #endif
872
873 __END_DECLS
874
875 #endif /* <stdio.h> included.  */
```

## 2.编译
```sh
$ gcc -fno-builtin -S hello.i -o hello.s    #-fno-builtin 不使用优化函数
$ gcc -S hello.i -o hello2.s    
$ diff hello*.s
5c5
< 	.string	"hello world."
---
> 	.string	"hello world.\n"
19c19,20
< 	call	puts@PLT
---
> 	movl	$0, %eax
> 	call	printf@PLT
```
我们通过diff工具比较优化和不优化分别生成的.s文件。可以看出只有两处不同，为什么产生不同的.s文件呢？
答案是：gcc在编译的过程中会将一些常用的函数代替成<built-in>库中被优化的函数，不难看出<built-in>库使用puts来优化了printf，这也能解释为什么第5行的换行符会被删掉，因为puts会自动将换行符追加到输出中。为了更好的分析执行过程，我们关闭编译器的常用函数优化，即我们使用不优化的hello.s进行分析和后续操作。

查看.s文件，可知编译后生成了x86_64的汇编代码，代码中指明了一些信息如.string "hello world."，.main的section还指明了一些汇编指令用来输出hello world，我们需要重点关注的是printf函数后面有一个@PLT，这意味着什么呢？我们在后面揭晓。

编译过程主要是将预处理过后的文件经过一系列的词法分析、语法分析、语义分析以及优化后，生成相应的汇编代码文件。这个过程是程序构建的核心部分，也是最复杂的部分。让我们重新审视编译器的职责，编译过程一般可以分成6步：扫描、语法分析、语义分析、源代码优化、代码生成和目标代码优化。

## 汇编
汇编器是将汇编代码转换成机器可以执行的指令，每一个汇编语句几乎对应一条机器指令。所以汇编过程相比于编译过程来讲比较简单，没有复杂的语法和语义，不需要做指令优化，只用根据汇编指令和机器指令的对照表一一翻译就可以了。
```sh
# 只汇编不进行链接
as hello.s -o hello.o
# 或者使用
gcc -c hello.s -o hello.o    
```
汇编后的文件不再是文本格式，而是一种名为ELF的文件格式。

