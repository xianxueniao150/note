ABI (Application Binray interface) : 应用程序二进制接口，描述了应用程序和操作系统之间，一个应用和它的库之间，或应用的组成部分之间的底层接口。

ELF文件类型
- 可重定位文件 (Relocatable File)包含了代码和数据,如Linux的.o、.a  windows的.obj、.lib
- 可执行文件（Executable File)包含了可以直接执行的程序,如/bin/ls 文件  windows的.exe
- 共享目标文件 (Shared Object File)包含了代码和数据,Linux 的.so  windows的dll


## 影响ABI兼容性的因素
### 硬件 - 如处理器

### 操作系统 
一是elf格式不同，二是系统库不同

###  编译器
```cpp
int Function(int i);
```
上面的代码在gcc和vc编译器生成之后的符号：
gcc : _Z8Functioni
vc++: ?Function@@YAHH@Z

你会发现gcc和vc++的函数签名规则都不一样，那gcc编译的库vc++能够找到它的符号吗，答案肯定是不行的，就算是相同版本的gcc也一样可能出现二进制不兼容，如gcc4.9版本C++ string,list符号命名和gcc5.1之后的符号命名都是不同的gcc5.1上会增加__cxx11，所以一样会产生在gcc4.9编译的库，再gcc5.1上使用不了（符号未定义，如果使用了string，list）

