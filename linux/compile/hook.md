### 替换方式
#### 第一种方法是使用LD_PRELOAD环境变量。
LD_PRELOAD是Linux系统的一个环境变量，它可以影响程序的运行时的链接(Runtime linker),它允许你定义在程序运行前优先加载的动态链接库。
系统一般会去LD_LIBRARY_PATH下寻找，但如果使用了这个变量，系统会优先去这个路径下寻找，如果找到了就返回，不在往下找了，
顺便提下，动态库的加载顺序为LD_PRELOAD>LD_LIBRARY_PATH>/etc/ld.so.cache>/lib>/usr/lib。

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
g++ -o hookread.so -fPIC -shared -D_GNU_SOURCE hookread.cpp -ldl
g++ -o main main.cpp
LD_PRELOAD=./hookread.so ./main
./main
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
