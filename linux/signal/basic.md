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

## 实时信号
早期Unix系统只定义了32种信号。
后面又加入32个信号表示实时信号，又叫可靠信号

实时信号有以下的特点：
- 进程接受多个同样的实时信号并不会合并，标准信号的话，在没有得到处理的时候，多个标准信号会被合为一个。
- 如果有多个不同的实时信号处于等待状态，那么将率先传递具有最小编号的信号。换言之，信号的编号越小，其优先级越高。如果是同一类型的多个信号在排队，那么信号的传递顺序与信号发送来时的顺序保持一致。
- 当发送一个实时信号时，可为信号指定伴随数据（一整型数或者指针值），供接收进程的信号处理器获取。

1.增加了信号从SIGRTMIN到SIGRTMAX的实时信号，可以通过sysconf(_SC_RTSIG_MAX)获得当前操作系统支持的实时信号的个数。如在arm linux中，SIGRTMIN在signal.h中定义为32，而SIGRTMAX是64。但是要注意，一般libc会对SIGRTMIN进行修改，保留几个预设的值用于pthread内部，比如glibc就保留了3个值。所以在使用实时信号的时候，应该使用SIGRTMIN+n、SIGRTMAX-n的方式，而不是直接使用数值。
2.实时信号和标准信号不一样，他没有明确的含义，而是由使用者自己来决定如何使用。
4.实时信号使用sigqueue发送的时候，可以携带附加的数据(int或者pointer)
5.实时信号有时间顺序的概念，所以同样的实时信号会按次序被处理。


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
用来描述信号的集合
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

## 信号阻塞
### 相关概念介绍
#### 未决状态	
在信号产生(generation)和递送(delivery)之间(可能相当长)的时间间隔内，该信号处于未决(pending)状态，这种信号称为挂起(suspending)的信号
#### 未决（未处理的）信号队列
内核为每个进程维护一个未决（未处理的）信号队列，信号产生时无论是否被阻塞，首先放入未决队列里。当时间片调度到当前进程时，内核检查未决队列中是否存在信号。若有信号且未被阻塞，则执行相应的操作并从队列中删除该信号；否则仍保留该信号

#### 信号屏蔽字（信号阻塞集）
每个进程都有一个用来描述哪些信号递送到进程时将被阻塞的信号集，该信号集中的所有信号在递送到进程后都将被阻塞
所谓阻塞并不是禁止传送信号, 而是暂缓信号的传送。若将被阻塞的信号从信号阻塞集中删除，且对应的信号在被阻塞时发生了，进程将会收到相应的信号

#### sigprocmask
```cpp
int (int how, const sigset_t *set, sigset_t *oldset);

how:操作
	SIG_BLOCK：在进程当前屏蔽信号集中添加set指向信号集中的信号
	SIG_UNBLOCK：如果进程屏蔽信号集中包含set指向信号集中的信号，则解除对该信号的阻塞
	SIG_SETMASK：更新进程屏蔽信号集为set指向的信号集
	
oldset:若不为NULL，则将旧的信号阻塞集通过该参数返回

//获得当前进程的未决信号队列
int sigpending(sigset_t *set);


//以上函数成功返回0，失败返回错误码
```

#### sigsuspend
用mask信号集代替当前信号阻塞集，直到信号到达,信号处理完毕后，返回并且恢复之前的信号阻塞集
若信号的处理是终止进程，则该函数不返回
```cpp
int sigsuspend(const sigset_t *mask);
```

示例
如下是一个信号处理程序，程序会阻塞直到SIGINT信号到达，在执行期间会暂时阻塞该信号，
直到执行完毕后解除阻塞再次等待该信号
```cpp
#include <unistd.h>
#include <signal.h>
#include <stdio.h>

void handler(int sig) //信号处理函数的实现
{
    printf("!\n");
}
int main()
{
    sigset_t new, old;
    signal(SIGINT, handler);
    sigemptyset(&new);
    sigaddset(&new, SIGINT);
    while (1)
    {
        sigprocmask(SIG_BLOCK, &new, &old); //将SIGINT信号阻塞，同时保存当前信号集
        printf("Blocked\n");
        sleep(1);
        sigprocmask(SIG_SETMASK, &old, NULL); //取消阻塞
        pause();
    }
    return 0;
}
```

```sh
ubuntu@VM-12-3-ubuntu:~/unix_pro$ ./a.out 
Blocked
^C!
Blocked
^C^C!
^C!
Blocked
```
可以看到在执行期间如果再次接收到该信号后，解除阻塞后，pause之前信号就直接被处理了，根本没有机会砸到pause上,
问题就是解除阻塞和pause两个操作并不是原子完成的

```cpp
#include <unistd.h>
#include <signal.h>
#include <stdio.h>

void handler(int sig) //信号处理函数的实现
{
    printf("!\n");
}
int main()
{
    sigset_t new, old;
    signal(SIGINT, handler);
    sigemptyset(&new);
    sigaddset(&new, SIGINT);
    sigprocmask(SIG_BLOCK, &new, &old); //将SIGINT信号阻塞，同时保存当前信号集
    while (1)
    {
        printf("Blocked\n");
        sleep(1);
        sigsuspend(&old);
    }
    sigprocmask(SIG_SETMASK, &old, NULL); //取消阻塞
    return 0;
}
```
```sh
ubuntu@VM-12-3-ubuntu:~/unix_pro$ ./a.out 
Blocked
^C!
Blocked
^C^C^C^C!
Blocked
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





## 异步信号安全
- 重入：同一个函数被不同的执行流调用，当前一个流程还没有执行完，就有其他的进程已经再次调用（执行流之间的相互嵌套执行）；
- 可重入：多个执行流反复执行一个代码，其结果不会发生改变，通常访问的都是各自的私有栈资源；
- 不可重入：多个执行流反复执行一段代码时，其结果会发生改变；
- 可重入函数：当一个执行流因为异常或者被内核切换而中断正在执行的函数而转为另外一个执行流时，当后者的执行流对同一个函数的操作并不影响前一个执行流恢复后执行函数产生的结果；

### 可重入函数 
所有的系统调用都是可重入的，一部分库函数也是可重入的
如何编写可重入函数：
1. 不使用全局变量或静态变量；
2. 不调用动态内存分配、释放的函数。
3. 不调用任何不可重入的函数（如标准I/O函数）
即使信号处理函数使用的都是可重入函数（常见的可重入函数），也要注意进入处理函数时，首先要保存errno的值，结束时，再恢复原值。因为，信号处理过程中，errno值随时可能被改变。

### 线程安全
简单来说线程安全就是多个线程并发同一段代码时，不会出现不同的结果，我们就可以说该线程是安全的；
线程安全不一定是可重入的，而可重入函数则一定是线程安全的。
线程安全函数能够使不同的线程访问同一块地址空间，而可重入函数要求不同的执行流对数据的操作互不影响使结果是相同的。


### 线程安全但不可重入的函数:
假设该函数在某次执行过程中，在已经获得资源锁之后，有异步信号发生，程序的执行流转交给对应的信号处理函数；再假设在该信号处理函数中也需要调用函数 func() ，那么func() 在这次执行中仍会在访问共享资源前试图获得资源锁，然而我们知道前一个func() 实例已然获得该锁，因此信号处理函数阻塞——另一方面，信号处理函数结束前被信号中断的线程是无法恢复执行的，当然也没有释放资源的机会，这样就出现了线程和信号处理函数之间的死锁局面。
因此，func() 尽管通过加锁的方式能保证线程安全，但是由于函数体对共享资源的访问，因此是非可重入。
