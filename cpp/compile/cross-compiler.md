## C运行时库
C语言标准主要由两部分组成：一部分描述C的语法，另一部分描述C标准库。
C标准库定义了一组标准头文件，每个头文件中包含一些相关的函数、变量、类型声明和宏定义，譬如常见的printf函数便是一个C标准库函数，其原型定义在stdio头文件中。

C语言标准仅仅定义了C标准库函数原型，并没有提供实现。因此，C语言编译器通常需要一个C运行时库（C Run Time Libray，CRT）的支持。C运行时库又常简称为C运行库。

如上所述，要在一个平台上支持C语言，不仅要实现C编译器，还要实现C标准库，这样的实现才能完全支持C标准。

## glibc
glibc（GNU C Library）是Linux下面C标准库的实现，其要点如下：
glibc本身是GNU旗下的C标准库，后来逐渐成为了Linux的标准C库。glibc 的主体分布在Linux系统的/lib与/usr/lib目录中，包括 libc 标准 C 函式库、libm数学函式库等等，都以.so做结尾。

注意：Linux系统下面的标准C库不仅有这一个，如uclibc、klibc、以及Linux libc，但是glibc使用最为广泛。而在嵌入式系统中使用较多的C运行库为Newlib。

Linux系统通常将libc库作为操作系统的一部分，它被视为操作系统与用户程序的接口。譬如：glibc不仅实现标准C语言中的函数，还封装了操作系统提供的系统服务，即系统调用的封装。

通常情况，每个特定的系统调用对应了至少一个glibc 封装的库函数，如系统提供的打开文件系统调用sys_open对应的是glibc中的open函数；其次，glibc 一个单独的API可能调用多个系统调用，如glibc提供的 printf 函数就会调用如 sys_open、sys_mmap、sys_write、sys_close等系统调用；另外，多个 glibc API也可能对应同一个系统调用，如glibc下实现的malloc、free 等函数用来分配和释放内存，都利用了内核的sys_brk的系统调用。

与C语言类似，C++也定义了自己的标准，同时提供相关支持库，称为C++运行时库。
对于C++语言，常用的C++标准库为libstdc++。注意：通常libstdc++与GCC捆绑在一起的，即安装gcc的时候会把libstdc++装上。而glibc并没有和GCC捆绑于一起，这是因为glibc需要与操作系统内核打交道，因此其与具体的操作系统平台紧密耦合。而libstdc++虽然提供了c++程序的标准库，但其并不与内核打交道。对于系统级别的事件，libstdc++会与glibc交互，从而和内核通信。
