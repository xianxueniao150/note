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
^C!
```

信号会打断阻塞的系统调用
上例，如果一直按着Ctrl+c的话，还是会输出10个"*"，但是程序不会运行10s，很快就结束了


## 常用函数

### 发信号
#### kill
```sh
int kill(pid_t pid, int sig);
```
The kill() system call cn be used to send any signal to any process group or process.

       If pid is positive, then signal sig is sent to the process with the ID specified by pid.
       If pid equals 0, then sig is sent to every process in the process group of the calling process.
       If pid equals -1, then sig is sent to every process for which the calling process has permission to send signals, except for process 1 (init), but see below.
       If pid is less than -1, then sig is sent to every process in the process group whose ID is -pid.
	   
#### raise
向自己发信号
```sh
int raise(int sig);
```
The raise() function sends a signal to the calling process or thread

#### alarm
```cpp
unsigned int alarm(unsigned int seconds);
```
alarm() arranges for a SIGALRM signal to be delivered to the calling process in seconds seconds.

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
ubuntu@VM-12-3-ubuntu:~/projects/kernel_test/net_test$ ./a.out 
Alarm clock
```

### 信号处理函数
目标进程在接收到信号后，需要设定信号处理函数
#### signal
```sh
#signal函数成功时返回一个 _sighandler_类型的函数指针,返回旧的__handler。出错返回 SIG_ERR，并设置 errno。
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


## 信号表
在终端，可通过kill -l查看所有的signal信号

取值	名称	解释	默认动作
1	SIGHUP	挂起	 
2	SIGINT	中断	 
3	SIGQUIT	退出	 
4	SIGILL	非法指令	 
5	SIGTRAP	断点或陷阱指令	 
6	SIGABRT	abort发出的信号	 
7	SIGBUS	非法内存访问	 
8	SIGFPE	浮点异常	 
9	SIGKILL	kill信号	不能被忽略、处理和阻塞
10	SIGUSR1	用户信号1	 
11	SIGSEGV	无效内存访问	 
12	SIGUSR2	用户信号2	 
13	SIGPIPE	管道破损，没有读端的管道写数据	 
14	SIGALRM	alarm发出的信号	 
15	SIGTERM	终止信号	 
16	SIGSTKFLT	栈溢出	 
17	SIGCHLD	子进程退出	默认忽略
18	SIGCONT	进程继续	 
19	SIGSTOP	进程停止	不能被忽略、处理和阻塞
20	SIGTSTP	进程停止	 
21	SIGTTIN	进程停止，后台进程从终端读数据时	 
22	SIGTTOU	进程停止，后台进程想终端写数据时	 
23	SIGURG	I/O有紧急数据到达当前进程	默认忽略
24	SIGXCPU	进程的CPU时间片到期	 
25	SIGXFSZ	文件大小的超出上限	 
26	SIGVTALRM	虚拟时钟超时	 
27	SIGPROF	profile时钟超时	 
28	SIGWINCH	窗口大小改变	默认忽略
29	SIGIO	I/O相关	 
30	SIGPWR	关机	默认忽略
31	SIGSYS	系统调用异常	 

对于signal信号，绝大部分的默认处理都是终止进程或停止进程，或dump内核映像转储。 上述的31的信号为非实时信号，其他的信号32-64 都是实时信号。


## 可重入函数 
函数返回值是一个指针的话，指针所指的区域可能是堆，也可能是静态区，如果是堆的话一般有一个配套函数XXclose，如果时静态区的话，有可能第一次调用还没用返回值，第二次调用就改变了返回值，这种函数就是不可重入的
所有的系统调用都是可重入的，一部分库函数也是可重入的
