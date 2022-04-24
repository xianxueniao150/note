## fork 复制自己
init进程，1号，所有进程的祖先进程

当一个进程调用fork之后，就有两个二进制代码相同的进程。而且它们都运行到相同的地方。但是每个进程都将可以开始它们自己的旅程
注意子进程会接着往下执行，但上面父进程已经执行过得就不再执行了
```cpp
#include <stdio.h>
void main()
{
    int ret_from_fork, mypid;
    mypid = getpid();
    printf("Before:my pid is %d\n", mypid);
    ret_from_fork = fork();
    sleep(1);
    printf("After:my pid is %d, fork() said %d\n", getpid(), ret_from_fork);
}

Before:my pid is 51335
After:my pid is 51335, fork() said 51336
After:my pid is 51336, fork() said 0
```

### 分辨父进程和子进程
不同的进程，fork的返回值是不同的

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{

    int fork_rv;

    printf("Before:my pid is %d\n", getpid());

    fork_rv = fork();
    if (fork_rv < 0)
    {
        perror("fork error");
        exit(1);
    }
    if (fork_rv == 0) // child
    {
        printf("I am the child. my pid=%d\n", getpid());
    }
    else // parent
    {
        printf("I am the parent. my child is %d\n", fork_rv);
    }
}


Before:my pid is 52577
I am the parent. my child is 52578
I am the child. my pid=52578
```


## 终端发送的信号会发给连接到该终端的所有程序


## 缓冲区刷新
如果把运行结果输出到文件，或者去掉begin打印后面的"\n"，都会发现before输出两次
终端是输出设备，输出设备默认为行缓冲模式，输出语句如果有"\n"的话，就表示刷新了缓冲区
文件默认是全缓冲模式
```fflush(NULL);   //fork前面一定要加这一句，刷新缓冲区，重要！！```


## 写时拷贝
fork之后父子进程共用同样的物理空间，假设对其中一块数据空间两个进程都是只读的话，那就什么都不用做。
如果其中一个进程要修改这块数据的话（不管是父进程还是子进程），都会先拷贝一份，然后修改拷贝后的
