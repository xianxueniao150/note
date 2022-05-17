https://mp.weixin.qq.com/s/5ILY-kF01URNRSlOZ3mzag
https://github.com/xianxueniao150/c_hook

## 什么是插桩？
在稍微具有一点规模的代码中(C 语言)，调用**第三方动态库**中的函数来完成一些功能，是很常见的工作场景。

假设现在有一项任务：需要在调用某个动态库中的某个函数的之前和之后，做一些额外的处理工作。
这样的需求一般称作：插桩，也就是对于一个指定的目标函数，新建一个包装函数，来完成一些额外的功能。
在包装函数中去调用真正的目标函数，但是在调用之前或者之后，可以做一些额外的事情。
比如：统计函数的调用次数、验证函数的输入参数是否合法等等。

## 插桩示例代码分析
示例代码很简单：
├── app.c
└── lib
    ├── rd3.h
    └── librd3.so

假设动态库librd3.so是由第三方提供的，里面有一个函数：int rd3_func(int, int);。
```cpp
// lib/rd3.h
#ifndef _RD3_H_
#define _RD3_H_
extern int rd3_func(int, int);
#endif
```

```cpp
// lib/rd3.c
#include <stdlib.h>
#include "rd3.h"

int rd3_func(int a, int b)
{
    int c = a + b;
    return c;
}
```

```cpp
//app.c
#include <stdio.h>
#include <stdlib.h>
#include "rd3.h"

int main(int argc, char *argv[])
{
    int result = rd3_func(1, 1);
    printf("result = %d \n", result);
    return 0;
}
```
```sh
# -L./lib: 指定编译时，在 lib 目录下搜寻库文件。
# -Wl,--rpath=./lib: 指定执行时，在 lib 目录下搜寻库文件。
$ gcc -o app app.c -I./lib -L./lib -lrd3 -Wl,--rpath=./lib
$ ./app
result = 3
```


## 在预处理阶段插桩
对函数进行插桩，基本要求是：不应该对原来的文件(app.c)进行额外的修改。
由于app.c文件中，已经include "rd3.h"了，并且调用了其中的rd3_func(int, int)函数。
所以我们需要新建一个假的 "rd3.h" 提供给app.c，并且要把函数rd3_func(int, int)"重导向"到一个包装函数，然后在包装函数中去调用真正的目标函数
"重导向"函数：可以使用宏来实现。
包装函数：新建一个C文件，在这个文件中，需要 #include "lib/rd3.h"，然后调用真正的目标文件。

完整的文件结构如下：
├── app.c
├── lib
│   ├── librd3.so
│   └── rd3.h
├── rd3.h
└── rd3_wrap.c

```cpp
// rd3.h

#ifndef _LIB_WRAP_H_
#define _LIB_WRAP_H_

// 函数“重导向”，这样的话 app.c 中才能调用 wrap_rd3_func
#define rd3_func(a, b)   wrap_rd3_func(a, b)

// 函数声明
extern int wrap_rd3_func(int, int);

#endif
```

```cpp
// rd3_wrap.c

#include <stdio.h>
#include <stdlib.h>

// 真正的目标函数
#include "lib/rd3.h"

// 包装函数，被 app.c 调用
int wrap_rd3_func(int a, int b)
{
    // 在调用目标函数之前，做一些处理
    printf("before call rd3_func. do something... \n");
    
    // 调用目标函数
	return rd3_func(a, b);
}
```

头文件的搜索路径不能错：必须在当前目录下搜索rd3.h，这样的话，app.c中的#include "rd3.h" 找到的才是我们新增的那个头文件 rd3.h。
所以在编译指令中，第一个选项就是 -I./(此处可以省略不写)，表示在当前目录下搜寻头文件。
另外，由于在rd3_wrap.c文件中，使用#include "lib/rd3.h"来包含库中的头文件，因此在编译指令中，就不需要指定到lib 目录下去查找头文件了。
```sh
$ gcc -o app app.c rd3_wrap.c -L./lib -lrd3 -Wl,--rpath=./lib
$ ./app 
before call rd3_func. do something... 
result = 3 
```

总结：在目标文件编译时要指定替换后的头文件所在的目录，对于标准库来说就不太可能


## 链接阶段插桩
Linux 系统中的链接器功能是非常强大的，它提供了一个选项：--wrap f
这个选项的作用是：告诉链接器，遇到f符号时解析成__wrap_f，在遇到__real_f符号时解析成f，正好是一对！

只要在编译选项中加上-Wl,--wrap,rd3_func, 编译器就会：
- 把 app.c 中的 rd3_func 符号，解析成 __wrap_rd3_func，从而调用包装函数;
- 把 rd3_wrap.c 中的 __real_rd3_func 符号，解析成 rd3_func，从而调用真正的函数。

这几个符号的转换，是由链接器自动完成的！

文件目录结构如下：
.
├── app.c
├── lib
│   ├── librd3.so
│   └── rd3.h
├── rd3_wrap.c
└── rd3_wrap.h

```cpp
//rd3_wrap.h
#ifndef _RD3_WRAP_H_
#define _RD3_WRAP_H_
extern int __wrap_rd3_func(int, int);
#endif
```

```cpp
//rd3_wrap.c
#include <stdio.h>
#include <stdlib.h>

#include "rd3_wrap.h"

extern int __real_rd3_func(int, int);

int __wrap_rd3_func(int a, int b)
{
    printf("before call rd3_func. do something... \n");
    return __real_rd3_func(a, b);
}
```
rd3_wrap.c中，不能直接去 include "rd3.h"，因为lib/rd3.h中的函数声明是int rd3_func(int, int);，没有__real前缀。

```sh
$ gcc -I./lib -L./lib -Wl,--rpath=./lib -Wl,--wrap,rd3_func -o app app.c rd3_wrap.c -lrd3
$ ./app 
before call rd3_func. do something... 
result = 3 
```


## 执行阶段插桩
文件目录结构如下：
├── app.c
├── lib
│   ├── librd3.so
│   └── rd3.h
└── rd3_wrap.c

```cpp
//rd3_wrap.c
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>

#include "rd3.h"

// 与目标函数签名一致的函数类型
typedef int (*pFunc)(int, int);

int rd3_func(int a, int b)
{
    printf("before call rd3_func. do something... \n");
    //打开动态链接库
    void *handle = dlopen("./lib/librd3.so", RTLD_NOW);
    // 查找库中的目标函数
    pFunc pf = dlsym(handle, "rd3_func");
    // 调用目标函数
    int c = pf(a, b);
    // 关闭动态库句柄
    dlclose(handle);
    return c;
}
```

```sh
# 1.整体编译
$ gcc app.c rd3_wrap.c -I ./lib -ldl
$ ./a.out
before call rd3_func. do something...
result = 3


# 这里-ldl 不管写在下面这条语句或者下下面这条语句都行
# 编译包装的动态库：得到librd3_wrap.so
$ gcc -shared -fPIC -I./lib -o librd3_wrap.so rd3_wrap.c
# 编译可执行程序，需要链接包装库 librd3_wrap.so：
$ gcc -I./lib -L./ -o app app.c -lrd3_wrap -ldl -Wl,--rpath=./
# 得到可执行程序app，执行：
$ ./app 
before call rd3_func. do something... 
result = 3
```

### 替换方式
#### 第一种方法是使用LD_PRELOAD环境变量。

我们来看一个小小的例子(摘自libco)：
```cpp
//hookread.cpp
#include <dlfcn.h>
#include <unistd.h>

#include <iostream>

typedef ssize_t (*read_pfn_t)(int fildes, void *buf, size_t nbyte);

static read_pfn_t g_sys_read_func = (read_pfn_t)dlsym(RTLD_NEXT,"read");

ssize_t read( int fd, void *buf, size_t nbyte ){
    std::cout << "进入 hook read\n";
    return g_sys_read_func(fd, buf, nbyte);
}
```

```cpp
//main.cpp
#include <bits/stdc++.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

using namespace std;

int main(){
    int fd = socket(PF_INET, SOCK_STREAM, 0);
    char buffer[10000];
    
    int res = read(fd, buffer ,10000);
    return 0;
}
```

然后执行以下命令：
```sh
$ g++ -o hookread.so -fPIC -shared -D_GNU_SOURCE hookread.cpp -ldl
$ g++ -o main main.cpp
$ LD_PRELOAD=./hookread.so ./main
进入 hook read
```
hook成功！


#### libco如何做
但是libco并不是这样做的，整个libco中你都看不到LD_PRELOAD，libco使用了一种特殊的方法，秘密都在于co_enable_hook_sys函数，通过在用户代码中包含这个函数，可以把整个hookread.cpp中的符号表导入我们的项目中，这样也可以做到使用我们自己的库去替换系统的库。我们来看看如何做到吧：

```cpp
//hookread.cpp
#include <dlfcn.h>
#include <unistd.h>

#include <iostream>

#include "hookread.h"

typedef ssize_t (*read_pfn_t)(int fildes, void *buf, size_t nbyte);

static read_pfn_t g_sys_read_func = (read_pfn_t)dlsym(RTLD_NEXT,"read");

ssize_t read( int fd, void *buf, size_t nbyte ){
    std::cout << "进入 hook read\n";
    return g_sys_read_func(fd, buf, nbyte);
}

void co_enable_hook_sys(){
    std::cout << "可 hook\n";
}
```

```cpp
// hookread.h
void co_enable_hook_sys();
```

```cpp
// main.cpp
#include <bits/stdc++.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "hookread.h"
#include <unistd.h>

using namespace std;

int main(){
    co_enable_hook_sys();
    int fd = socket(PF_INET, SOCK_STREAM, 0);
    char buffer[10000];
    
    int res = read(fd, buffer ,10000);
    return 0;
}
```

```cpp
$ g++ -c  hookread.cpp -o hookread.o -ldl
$ g++ main.cpp  hookread.o -ldl
$ ./a.out
可 hook
进入 hook read
```
