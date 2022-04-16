## exit 
```cpp
void exit(int status);
```

exit是fork的逆操作，进程通过调用exit来停止运行。
exit刷新所有的流，调用由atexit和on_exit注册的函数，执行当前系统定义的其他与exit相关的操作。然后调用_exit。

系统函数_exit是一个内核操作，这个操作处理所有分配给这个进程的内存，关闭所有这个进程打开的文件，释放所有内核用来管理和维护这个进程的数据结构。
系统调用_exit终止当前进程并执行所有必须的清理工作。这些工作在各个不同版本的Unix中有些不同，但都包括以下一些操作：
(1)关闭所有文件描述符和目录描述符。
(2)将该进程的PID置为init进程的PID。
(3)如果父进程调用wait或waitpid来等待子进程结束，则通知父进程。
(4)向父进程发送SIGCHLD。

这样，如果父进程在子进程之前退出，那么子进程将能继续运行，而不会成为“孤儿”，它们将是init进程的“子女”。
注意，就算父进程没有调用wait,内核 也会向它发送SIGCHLD消息。尽管对SIGCHLD消息的默认处理方法是忽略的。如果想响应这个消息，可以设置一个处理函数。




## 钩子函数
```cpp
int atexit(void (*function)(void));
```
The  atexit() function registers the given function to be called at normal process termination

示例
```cpp
#include <stdio.h>
#include <stdlib.h>

void f1(){
    puts("f1 is working");
}

void f2(){
    puts("f2 is working");
}

int main(){
    
    puts("Begin");

    atexit(f1);
    atexit(f2);

    puts("end");
    exit(0);
}

Begin
end
f2 is working
f1 is working
```



