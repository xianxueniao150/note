## 基础API
```cpp
struct sigaction {
    void (*sa_handler)(int);
    void (*sa_sigaction)(int, siginfo_t *, void *);
    sigset_t sa_mask;
    int sa_flags;
    void (*sa_restorer)(void);
}
```


sa_handler是一个函数指针，指向信号处理函数

sa_sigaction同样是信号处理函数，有三个参数，可以获得关于信号更详细的信息

sa_mask用来指定在信号处理函数执行期间需要被屏蔽的信号

sa_flags用于指定信号处理的行为

SA_RESTART，使被信号打断的系统调用自动重新发起

SA_NOCLDSTOP，使父进程在它的子进程暂停或继续运行时不会收到 SIGCHLD 信号

SA_NOCLDWAIT，使父进程在它的子进程退出时不会收到 SIGCHLD 信号，这时子进程如果退出也不会成为僵尸进程

SA_NODEFER，使对信号的屏蔽无效，即在信号处理函数执行期间仍能发出这个信号

SA_RESETHAND，信号处理之后重新设置为默认的处理方式

SA_SIGINFO，使用 sa_sigaction 成员而不是 a_handler 作为信号处理函数

sa_restorer一般不使用

sigaction函数
1#include <signal.h>
2
3int sigaction(int signum, const struct sigaction *act, struct sigaction *oldact);


signum表示操作的信号。

act表示对信号设置新的处理方式。

oldact表示信号原来的处理方式。

返回值，0 表示成功，-1 表示有错误发生。

sigfillset函数
1#include <signal.h>
2
3int sigfillset(sigset_t *set);
用来将参数set信号集初始化，然后把所有的信号加入到此信号集里。

SIGALRM、SIGTERM信号
1#define SIGALRM  14     //由alarm系统调用产生timer时钟信号
2#define SIGTERM  15     //终端发送的终止信号
alarm函数
1#include <unistd.h>;
2
3unsigned int alarm(unsigned int seconds);
设置信号传送闹钟，即用来设置信号SIGALRM在经过参数seconds秒数后发送给目前的进程。如果未设置信号SIGALRM的处理函数，那么alarm()默认处理终止进程.

socketpair函数
在linux下，使用socketpair函数能够创建一对套接字进行通信，项目中使用管道通信。

1#include <sys/types.h>
2#include <sys/socket.h>
3
4int socketpair(int domain, int type, int protocol, int sv[2]);


domain表示协议族，PF_UNIX或者AF_UNIX

type表示协议，可以是SOCK_STREAM或者SOCK_DGRAM，SOCK_STREAM基于TCP，SOCK_DGRAM基于UDP

protocol表示类型，只能为0

sv[2]表示套节字柄对，该两个句柄作用相同，均能进行读写双向操作

返回结果， 0为创建成功，-1为创建失败

send函数
1#include <sys/types.h>
2#include <sys/socket.h>
3
4ssize_t send(int sockfd, const void *buf, size_t len, int flags);
当套接字发送缓冲区变满时，send通常会阻塞，除非套接字设置为非阻塞模式，当缓冲区变满时，返回EAGAIN或者EWOULDBLOCK错误，此时可以调用select函数来监视何时可以发送数据。

信号通知流程
Linux下的信号采用的异步处理机制，信号处理函数和当前进程是两条不同的执行路线。具体的，当进程收到信号时，操作系统会中断进程当前的正常流程，转而进入信号处理函数执行操作，完成后再返回中断的地方继续执行。

为避免信号竞态现象发生，信号处理期间系统不会再次触发它。所以，为确保该信号不被屏蔽太久，信号处理函数需要尽可能快地执行完毕。

一般的信号处理函数需要处理该信号对应的逻辑，当该逻辑比较复杂时，信号处理函数执行时间过长，会导致信号屏蔽太久。

这里的解决方案是，信号处理函数仅仅发送信号通知程序主循环，将信号对应的处理逻辑放在程序主循环中，由主循环执行信号对应的逻辑代码。

统一事件源
统一事件源，是指将信号事件与其他事件一样被处理。

具体的，信号处理函数使用管道将信号传递给主循环，信号处理函数往管道的写端写入信号值，主循环则从管道的读端读出信号值，使用I/O复用系统调用来监听管道读端的可读事件，这样信号事件与其他文件描述符都可以通过epoll来监测，从而实现统一处理。

信号处理机制
每个进程之中，都有存着一个表，里面存着每种信号所代表的含义，内核通过设置表项中每一个位来标识对应的信号类型。

图片

信号的接收

接收信号的任务是由内核代理的，当内核接收到信号后，会将其放到对应进程的信号队列中，同时向进程发送一个中断，使其陷入内核态。注意，此时信号还只是在队列中，对进程来说暂时是不知道有信号到来的。

信号的检测

进程从内核态返回到用户态前进行信号检测

进程在内核态中，从睡眠状态被唤醒的时候进行信号检测

进程陷入内核态后，有两种场景会对信号进行检测：

当发现有新信号时，便会进入下一步，信号的处理。

信号的处理

( 内核 )信号处理函数是运行在用户态的，调用处理函数前，内核会将当前内核栈的内容备份拷贝到用户栈上，并且修改指令寄存器（eip）将其指向信号处理函数。

( 用户 )接下来进程返回到用户态中，执行相应的信号处理函数。

( 内核 )信号处理函数执行完成后，还需要返回内核态，检查是否还有其它信号未处理。

( 用户 )如果所有信号都处理完成，就会将内核栈恢复（从用户栈的备份拷贝回来），同时恢复指令寄存器（eip）将其指向中断前的运行位置，最后回到用户态继续执行进程。

至此，一个完整的信号处理流程便结束了，如果同时有多个信号到达，上面的处理流程会在第2步和第3步骤间重复进行。

s
