编译时，必须在最后加上 -lrt
在Linux上，posix 消息队列是以虚拟文件系统实现的，必须将其挂载到某个目录才能看见
```cpp
#include <mqueue.h>
mqd_t mq_open(const char *name, int oflag);
mqd_t mq_open(const char *name, int oflag, mode_t mode, struct mq_attr *attr);
```

#### mq_close 关闭消息队列
```cpp
int mq_close(mqd_t mqdes);
```
其功能与关闭一个已打开文件的close函数类似：调用进程可以不再使用该描述符，但其消息队列并不从系统中删除。一个进程终止时，它的所有打开着的消息队列都关闭。

#### mq_unlink 删除消息队列
```cpp
int mq_unlink(const char *name);
```
每个消息队列有一个保存其当前打开着描述符数的引用计数器（就像文件一样）因而本函数能够实现类似于unlink函数删除一个文件的机制：name能够删除，但是该队列的析构（这与从系统中删除其名字不同）要到最后一个mq_close 发生时才进行
一个消息队列的名字在系统中的存在本身也占用其引用计数器的一个引用数。nq_unlink从系统中删除该名字 意味着同时将其引用计数滅1，若变为0则真正拆除该队列。
跟mq_unlink—样，mq_close也将当前消息队列的引用计数减1,若变为0则附带拆除该队列。

#### 获取、设置属性
```cpp
int mq_getattr(mqd_t mqdes, struct mq_attr *attr);
int mq_setattr(mqd_t mqdes, const struct mq_attr *newattr, struct mq_attr *oldattr);

struct mq_attr {
   long mq_flags;       /* Flags: 0 or O_NONBLOCK */
   long mq_maxmsg;      /* Max. # of messages on queue */
   long mq_msgsize;     /* Max. message size (bytes) */
   long mq_curmsgs;     /* # of messages currently in queue */
};
```
指向某个mq_attr结构的指针可作为mq_open的第四个参数传递，从而允许我们在该函数的实际操作是创建新队列时，给它指定mq_maxmsg和mq_msgsize属性。mq_open忽略该结构的另外两个成员。
mq_setattr给所指定队列设置属性，但是只使用由attr指向的mq_attr结构的mq_flags成员，以设置或清除非阻塞标志。该结构的另外三个成员被忽略：每个队列的最大消息数和每个消息的最大字节数只能在创建队列时设置，队列中的当前消息数则只能获取而不能设置。

#### 发送和接收
```cpp
int mq_send(mqd_t mqdes, const char *msg_ptr, size_t msg_len, unsigned int msg_prio);
ssize_t mq_receive(mqd_t mqdes, char *msg_ptr, size_t msg_len, unsigned int *msg_prio);

msg_prio:消息优先级,如果应用不必使用优先级不同的消息，那就设为0
```
mq_receive的len参数的值不能小于能加到所指定队列中的消息的最大大小（该队列 mq_attr结构的mq_msgsize成员）。要是小于该值，mq_receive就立即返回EMSGSIZE错误。
	这意味着使用Posix消息队列的大多数应用程序必须在打开某个队列后调用mq_getattr 确定最大消息大小，然后分配一个或多个那样大小的读缓冲区.通过要求每个缓冲区总是足以存放队列中的任意消息

接收的顺序是首先优先级最高的，优先级相同的情况下时间最早的

例子
```cpp
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <mqueue.h>

int main(int argc, char **argv)
{
    mqd_t mqd;
    void *ptr;
    size_t len;
    unsigned int prio;

    if (argc != 4)
    {
        printf("usage: mqsend <name> <#bytes> <priority>");
        exit(1);
    }
    len = atoi(argv[2]);
    prio = atoi(argv[3]);

    mqd = mq_open(argv[1], O_WRONLY);
    if (mqd < 0)
    {
        perror("mq_open:");
        exit(1);
    }

    ptr = malloc(len);
    if (mq_send(mqd, ptr, len, prio) < 0)
    {
        perror("mq_send:");
        exit(1);
    }

    exit(0);
}
```


#### 异步通知
```cpp
int mq_notify(mqd_t mqdes, const struct sigevent *sevp);

struct sigevent {
   int          sigev_notify; /* Notification method */
   int          sigev_signo;  /* Notification signal */
   union sigval sigev_value;  /* Data passed with
								 notification */
   void       (*sigev_notify_function) (union sigval);
					/* Function used for thread
					   notification (SIGEV_THREAD) */
   void        *sigev_notify_attributes;
					/* Attributes for notification thread
					   (SIGEV_THREAD) */
   pid_t        sigev_notify_thread_id;
					/* ID of thread to signal (SIGEV_THREAD_ID) */
};

union sigval {          /* Data passed with notification */
   int     sival_int;         /* Integer value */
   void   *sival_ptr;         /* Pointer value */
};
```
- 如果notification参数非空，那么当前进程希望在有一个消息到达所指定的先前为空的队列时得到通知。我们说“该进程被注册为接收该队列的通知"
- 如果notification参数为空指针，而且当前进程目前被注册为接收所指定队列的通知，那么己存在的注册将被撤销。
- 任意时刻只有一个进程可以被注册为接收某个给定队列的通知。
- 当有一个消息到达某个先前为空的队列，而且已冇个进程被注册为接收该队列的通知时，只有在没有任何线程阻塞在该队列的mq_receive调用中的前提下，通知才会发出。这就是说，在mq_reveive调用中的阻塞比任何通知的注册都优先。
- 当该通知被发送给它的注册进程时，其注册即被撤销。该进程必须再次调用mq_notify 以重新注册（如果想要的话）。
	 Unix信号最初的问题之一是：每当一个信号产生后，其行为就被复位成默认行为.信号处理程序调用的第一个函数通常是signal,用于重新建立处理程序.这么一来提供了一个短的时间窗口，它处于该信号的产生与当前进程重建其信号处理程序之间，这段时间内再次产生的同一信号可能终止当前进程.初看起来，mjnotify似乎有类似的问题，因为当前进程必须在每次通知发生后重新注册.然而消息队列不同于信号，因为在队列变空前通知不会再次发生.因此我们必须小心，保证在从队列中读出消息之前（而不是之后）重新注册.

例子
```cpp
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <mqueue.h>
#include <signal.h>

#define MQ_NAME "/testQueue"

mqd_t mqd;
void *buff;
struct mq_attr attr;
struct sigevent sigev;

static void sig_usr1(int);

int main(int argc, char **argv)
{
    mqd = mq_open(MQ_NAME, O_RDWR | O_CREAT, 0664, NULL);
    if (mqd < 0)
    {
        perror("mq_open");
        exit(1);
    }
    mq_getattr(mqd, &attr);
    buff = malloc(attr.mq_msgsize);

    /* establish signal handler, enable notification */
    signal(SIGUSR1, sig_usr1);
    sigev.sigev_notify = SIGEV_SIGNAL;
    sigev.sigev_signo = SIGUSR1;
    if (mq_notify(mqd, &sigev) < 0)
    {
        perror("mq_nofity");
        exit(1);
    }

    for (;;)
        pause(); /* signal handler does everything */
    exit(0);
}

static void
sig_usr1(int signo)
{
    ssize_t n;

    if (mq_notify(mqd, &sigev) < 0) /* reregister first */
    {
        perror("mq_nofity");
        exit(1);
    }
    printf("SIGUSR1 received, read %ld bytes\n", (long)n);
    return;
}
```

```sh
# 终端1,会阻塞在这直到其他进程向队列中发送消息
ubuntu@VM-12-3-ubuntu:~/unix_pro/mq$ ./a.out 
SIGUSR1 received, read 50 bytes
SIGUSR1 received, read 50 bytes

# 终端2
$ ./mqsend /testQueue 50 16
$ ./mqsend /testQueue 50 16
```

我们可以验证每次只有一个进程可被注册为接收通知，方法是从另一个窗口中启动该样序 的另一个副本
```cpp
ubuntu@VM-12-3-ubuntu:~/unix_pro/mq$ ./a.out 
mq_nofity: Device or resource busy
```
