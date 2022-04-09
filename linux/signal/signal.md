概念：信号是软件中断

实例
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>


static void int_handler(int s){
    write(1,"!\n",2);
}

int main(){
    //signal(SIGINT,SIG_IGN);  //这句话会忽略Ctrl+C 
    signal(SIGINT,int_handler);

    for(int i=0;i<10;i++){
        write(1,"*\n",2);
        sleep(1);
    }

    exit(0);
}
```

```sh
ubuntu@VM-12-3-ubuntu:~/projects/kernel_test/net_test$ ./a.out 
*
*
*
^C!
*
^C!
*
^C!
*
^C!
*
^C!
*
^C!
*
^C!
*
```
^C!

信号会打断阻塞的系统调用
上例，如果一直按着Ctrl+c的话，还是会输出10个"*"，但是程序不会运行10s，很快就结束了


## 信号通知流程
Linux下的信号采用的异步处理机制，信号处理函数和当前进程是两条不同的执行路线。
具体的，当进程收到信号时，操作系统会中断进程当前的正常流程，转而进入信号处理函数执行操作，完成后再返回中断的地方继续执行。
此时errno为EINTR

为避免信号竞态现象发生，信号处理期间系统不会再次触发它。所以，为确保该信号不被屏蔽太久，信号处理函数需要尽可能快地执行完毕。

这里的解决方案是，信号处理函数仅仅发送信号通知程序主循环，将信号对应的处理逻辑放在程序主循环中，由主循环执行信号对应的逻辑代码。


## 常用函数

### 发信号
#### kill 给任意进程或进程组发送任意信号
```c
//成功返回0，失败返回-1，错误值在errno中
int kill(pid_t pid, int sig);
```

       If pid is positive, then signal sig is sent to the process with the ID specified by pid.
       If pid equals 0, then sig is sent to every process in the process group of the calling process.
       If pid equals -1, then sig is sent to every process for which the calling process has permission to send signals, except for process 1 (init), but see below.
       If pid is less than -1, then sig is sent to every process in the process group whose ID is -pid.

#### sigqueue 给任意进程发送任意信号，并且可以传递数据
只能发送给一个进程，不能发送给进程组
```cpp
int sigqueue(pid_t pid, int sig, const union sigval value);

union sigval {
     int sival_int;
     void *sival_ptr;
};
```


#### raise 给本进程或线程发送任意信号
```sh
int raise(int sig);
```
1.在单线程程序中等价于kill(getpid(), sig);
2.在多线程程序中等价于pthread_kill(pthread_self(), sig);
3.该函数会在信号处理函数执行完成后返回

#### alarm 在seconds秒后给本进程发送SIGALRM信号
```cpp
//如果以前没有设置过alarm或者已经超时，那么返回0, 如果以前设置过alarm，那就返回剩余的时间，并且重新设定定时器
//若seconds=0，则任何未决的alarm都会被取消
unsigned int alarm(unsigned int seconds);
```

```cpp
#include <stdio.h>
### 
#include <stdlib.h>
#include <unistd.h>

int main(){
    alarm(3);
    while(1);
    exit(0);
}
```

```sh
$ ./a.out 
Alarm clock
```

#### abort 给本进程发送SIGABRT信号
```cpp
void abort(void);
```
1.该函数先解除对SIGABRT信号的屏蔽
2.不论该信号被屏蔽或是注册了信号处理函数，它总会终止进程，该函数通过回复SIGABRT的默认配置然后再次发出该信号来完成此操作。（除非你未从信号处理函数返回（see longjump）

### 进程对信号的响应
忽略信号	即对信号不做任何处理，其中SIGKILL和SIGSTOP不可忽略
捕捉信号	信定义信号处理函数，当信号发生时执行相应的处理函数
缺省操作	执行信号默认的缺省操作，其中实时信号的缺省操作是进程终止


### 信号处理函数
#### signal 注册简单的信号处理函数
```c
//signal函数成功时返回一个 _sighandler_类型的函数指针,返回旧的__handler。出错返回 SIG_ERR，并设置 errno。
//注意：SIGKILL和SIGSTOP不可注册处理函数
__sighandler_t signal (int __sig, __sighandler_t __handler)

typedef void (*__sighandler_t) (int);
```

有两种预先定义的信号处理方式(系统实现的__sighandler_t函数)
* SIG_DFL	默认信号处理
* SIG_IGN	忽略信号

#### sigaction
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
  
```

#### sa_sigaction 参数信号处理函数
void (*sa_sigaction)(int, siginfo_t *, void *);
```cpp
//参数：sig，info，ucontext
//sig是信号值，第三个参数未使用，info参数结构体定义如下：
typedef struct {
    int si_signo;
    int si_errno;           
    int si_code;            
    union sigval si_value;  
    } siginfo_t;
//这个结构体中的第四个参数，就是sigqueue给信号传递的那个结构体了
```

## 信号集
### 相关概念介绍
#### 未决状态	
在信号产生(generation)和递送(delivery)之间(可能相当长)的时间间隔内，该信号处于未决(pending)状态，这种信号称为挂起(suspending)的信号
#### 未决（未处理的）信号队列
内核为每个进程维护一个未决（未处理的）信号队列，信号产生时无论是否被阻塞，首先放入未决队列里。当时间片调度到当前进程时，内核检查未决队列中是否存在信号。若有信号且未被阻塞，则执行相应的操作并从队列中删除该信号；否则仍保留该信号
#### 信号屏蔽字（信号阻塞集）
每个进程都有一个信号屏蔽字(signal mask)，规定当前要阻塞递送到该进程的信号集。对于每个可能的信号，该屏蔽字中都有一位与之对应。对于某种信号，若其对应位已设置，则该信号当前被阻塞
所谓阻塞并不是禁止传送信号, 而是暂缓信号的传送。若将被阻塞的信号从信号阻塞集中删除，且对应的信号在被阻塞时发生了，进程将会收到相应的信号

### 信号集用来描述信号的集合
```cpp
结构定义：
typedef struct {
    unsigned long sig[_NSIG_WORDS]；
} sigset_t

//初始化由set指定的信号集，信号集里面的所有信号被清空
int sigemptyset(sigset_t *set);

//调用该函数后，set指向的信号集中将包含linux支持的64种信号
int sigfillset(sigset_t *set);

//判定信号signum是否在set指向的信号集中
int sigismember(const sigset_t *set, int signum);

//在set指向的信号集中加入signum信号
int sigaddset(sigset_t *set, int signum);

//在set指向的信号集中加入signum信号
int sigdelset(sigset_t *set, int signum);

//以上函数成功返回0，失败返回-1
```

### 信号阻塞
每个进程都有一个用来描述哪些信号递送到进程时将被阻塞的信号集，该信号集中的所有信号在递送到进程后都将被阻塞

```cpp
//根据how参数来对信号集进行对应的操作:
//SIG_BLOCK：在进程当前屏蔽信号集中添加set指向信号集中的信号
//SIG_UNBLOCK：如果进程屏蔽信号集中包含set指向信号集中的信号，则解除对该信号的阻塞
//SIG_SETMASK：更新进程屏蔽信号集为set指向的信号集

//若oldset不为NULL，则将旧的信号阻塞集通过该参数返回
int sigprocmask(int how, const sigset_t *set, sigset_t *oldset);

//获得当前进程的未决信号队列
int sigpending(sigset_t *set);

//挂起线程且暂时使用mask代替当前信号阻塞集，直到信号到达
//1.若信号的处理是终止进程，则该函数不返回
//2.若注册了信号处理函数，则待信号处理函数执行完毕后，该函数再返回
int sigsuspend(const sigset_t *mask);

//以上函数成功返回0，失败返回错误码
```



## 统一事件源
信号处理函数需要尽可能快的执行完毕以确保信号不会被屏蔽（为了避免一些竟态条件，信号在处理期间，系统不会再次触发它）太久。
典型的解决方法是：把信号的主要处理逻辑放到程序的主循环中，信号处理函数只是简单的通知主循环程序接收到信号并把信号值传递给主循环。
主循环再根据接收到的信号值执行目标信号对应的逻辑代码。信号处理函数通常使用管道将信号传递给主循环，
为了让主循环知道管道上何时有数据可读，需要用到 I/O复用系统调用来监听管道的读端文件描述符的可读事件。
如此一来，信号事件就和其它 I/O事件一样被处理，这就是统一事件源。

int pause(void);

pause - wait for signal 

int getitimer(int which, struct itimerval *curr_value);
int setitimer(int which, const struct itimerval *new_value,
             struct itimerval *old_value);
             
struct itimerval {
   struct timeval it_interval; /* Interval for periodic timer */
   struct timeval it_value;    /* Time until next expiration */
};

struct timeval {
   time_t      tv_sec;         /* seconds */
   suseconds_t tv_usec;        /* microseconds */
};                




## 可重入函数 
所有的系统调用都是可重入的，一部分库函数也是可重入的
如何编写可重入函数：
1. 不使用（返回）静态的数据、全局变量（除非用信号量互斥）。
2. 不调用动态内存分配、释放的函数。
3. 不调用任何不可重入的函数（如标准I/O函数）

	即使信号处理函数使用的都是可重入函数（常见的可重入函数），也要注意进入处理函数时，首先要保存errno的值，结束时，再恢复原值。因为，信号处理过程中，errno值随时可能被改变。
