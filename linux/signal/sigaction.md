## sigaction
可以添加信号处理过程中的信号阻塞集。
比如我的程序接收到SIGQUIT或者SIGTERM信号，就执行资源清理操作。如果收到SIGQUIT信号清理到一半，又收到SIGTERM信号，就又重复去清理了，就可能导致异常。
sigaction就可以保证我不会被打断。
```cpp
// act参数指定新的信号处理方式， oact参数则输出先前的处理方式（如果不为 NULL）
// 成功时返回 0，失败返回 -1并设置 errno
int sigaction(int sig,const struct sigacion* act, struct sigaction* oact)

struct sigaction
  {
    /* Signal handler.  */
    union
      {
		/* Used if SA_SIGINFO is not set.  */
		__sighandler_t sa_handler;
		/* Used if SA_SIGINFO is set.  */
		void (*sa_sigaction) (int, siginfo_t *, void *);
      }

	//* Additional set of signals to be blocked.  */
    __sigset_t sa_mask;

	//设置程序收到信号时的行为
    int sa_flags;

  };

siginfo_t: 可以拿到信号的许多信息，包括信号是不是来自内核
```

### 示例
```cpp
//信号处理函数
void sig_handler(int sig)
{
    //为保证函数的可重入性，保留原来的errno
    //可重入性表示中断后再次进入该函数，环境变量与之前相同，不会丢失数据
    int save_errno = errno;
    int msg = sig;

    //将信号值从管道写端写入，传输字符类型，而非整型
    send(pipefd[1], (char *)&msg, 1, 0);

    //将原来的errno赋值为当前的errno
    errno = save_errno;
}
void addsig( int sig )
{
    struct sigaction sa;
    memset( &sa, '\0', sizeof( sa ) );
    sa.sa_handler = sig_handler;
    sa.sa_flags |= SA_RESTART;
    sigfillset( &sa.sa_mask );
    assert( sigaction( sig, &sa, NULL ) != -1 );
}
```

### sa_flags
#### SA_RESTART
一些特定的系统调用在信号处理函数结束后restartable
https://man7.org/linux/man-pages/man7/signal.7.html
从上面的man手册里可以看到,restart分两种情况
1. Interruption of system calls and library functions by signal handlers
2. Interruption of system calls and library functions by stop signals

我们这里符合第一种情况，就只看第一种
  If a signal handler is invoked while a system call or library function call is blocked, then either:

       * the call is automatically restarted after the signal handler
         returns; or

       * the call fails with the error EINTR.

       If a blocked call to one of the following interfaces is
       interrupted by a signal handler, then the call is automatically
       restarted after the signal handler returns if the SA_RESTART flag
       was used; otherwise the call fails wit the error EINTR:

       * read(2), readv(2), write(2), writev(2), and ioctl(2) calls on
         "slow" devices.  

       * wait(2), wait3(2), wait4(2), waitid(2), and waitpid(2).

       * Socket interfaces: accept(2), connect(2), recv(2), recvfrom(2),
         recvmmsg(2), recvmsg(2), send(2), sendto(2), and sendmsg(2),
         unless a timeout has been set on the socket (see below).

       * pthread_mutex_lock(3), pthread_cond_wait(3), and related APIs.

       The following interfaces are never restarted after being
       interrupted by a signal handler, regardless of the use of
       SA_RESTART; they always fail with the error EINTR when
       interrupted by a signal handler:

       * "Input" socket interfaces, when a timeout (SO_RCVTIMEO) has
         been set on the socket using setsockopt(2): accept(2), recv(2),
         recvfrom(2), recvmmsg(2) (also with a non-NULL timeout
         argument), and recvmsg(2).

       * "Output" socket interfaces, when a timeout (SO_RCVTIMEO) has
         been set on the socket using setsockopt(2): connect(2),
         send(2), sendto(2), and sendmsg(2).

       * File descriptor multiplexing interfaces: epoll_wait(2),
         epoll_pwait(2), poll(2), ppoll(2), select(2), and pselect(2).

       The sleep(3) function is also never restarted if interrupted by a
       handler, but gives a success return: the number of seconds
       remaining to sleep.




### sa_mask
- sa_mask 是一个信号集，仅当信号捕捉函数正在执行时，才阻塞sa_mask中的信号，当从信号捕捉函数返回时进程的信号屏蔽字复位为原先值。
- 这个复位动作是sigaction函数内部处理，不用调用者自己处理
- 阻塞的信号默认包括正被递送的信号，也就是说自己也被阻塞，除非设置了SA_NODEFER
- 如果在某种信号被阻塞时它发生了5次，那么对这种信号解除阻塞后，它也只会被处理一次。


```cpp
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <errno.h>

#define BUFSIZE (1024)

void sig_usr(int signo)
{
    int nRemainSecond = 0;

    if (signo == SIGUSR1)
    {
        printf("received SIGUSR1=%d\n", SIGUSR1);
        nRemainSecond = sleep(50);
        printf("over...nRemainSecond=%d\n", nRemainSecond);
    }
    else
    {
        printf("received other\n");
    }
}

int main(int argc, char **argv)
{
    int nSize = 0;
    char acBuf[BUFSIZE] = {0};

    struct sigaction act;
    act.sa_handler = sig_usr;

    sigemptyset(&act.sa_mask);
    // sigaddset(&act.sa_mask, SIGQUIT);

    sigaction(SIGUSR1, &act, NULL);

    while (1)
    {
        memset(acBuf, '\0', BUFSIZE);
        nSie = read(STDIN_FILENO, acBuf, BUFSIZE);
        if (errno == EINTR)
            printf("interrupt, size=%d\n", nSize);
        if (nSize != -1)
        {
            printf("nSize=%d, acBuf=%s", nSize, acBuf);
        }
    }

    return 0;
}
```

```sh
# test1----------------------
# 终端1执行程序会阻塞在这
1$ gcc block.c && ./a.out

# 终端2 发送usr1信号
2$ pgrep -f a.out | xargs  kill -USR1

# 终端1执行信号处理函数
1$ gcc block.c && ./a.out
received SIGUSR1=10
over...nRemainSecond=0
interrupt, size=-1

# test2----------------------
# 如果终端2 短时间内多次发送usr1信号，则终端1在处理了第一次信号之后,只会再处理一次，总共处理2次

# test3----------------------
# 终端2 在发送usr1信号后，紧接着又发送quit信号
2$ -f a.out | xargs  kill -USR1
2$ -f a.out | xargs  kill -quit

#则终端1还没有执行完信号处理函数就结束了程序
1$
received SIGUSR1=10
Quit (core dumped)

# test4----------------------
# 如果取消sigaddset(&act.sa_mask, SIGQUIT);注释，执行test3相同的步骤，终端1则会等到信号处理函数结束后才结束程序
1$
received SIGUSR1=10
over...nRemainSecond=0
Quit (core dumped)
```
