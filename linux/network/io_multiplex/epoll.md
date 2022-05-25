

## poll
poll系统调用和select类似，也是在指定时间内轮询一定数量的文件描述符，以测试其中是否冇就绪者
```cpp
#include <poll.h>
int poll(struct pollfd *fds, nfds_t nfds, int timeout);

1)fds 指定我们感兴趣的文件描述符，和对应描述符上发生的感兴趣事件
struct pollfd {
   int   fd;         /* file descriptor */
   short events;     /* requested events，a bit mask */
   short revents;    /* returned events，output parameter，内核会把实际发生的event放进去 */
};

其中，fd成员指定文件描述符：events成员告诉poll监听fd上的哪些事件，它是一系列事件的按位或；revents成员则由内核修改，以通知应用程序fd上实际发生了哪些事件.

pollfd 结构体中的events 可以是以下几个宏的集合：
POLLIN     //表示对应的文件描述符可以读（包括对端SOCKET正常关闭）；
POLLOUT    //表示对应的文件描述符可以写；

2)nfds	指定被监听事件集合fds的大小.其类型nfds_t的定义如下
typedef unsigned long int nfds_t;

3)timeout	指定poll的超时值，単位是毫秒。当timeout 为-1时，poll调用将永远阻塞，直到某个事件发生；当timeout为0时，poll调用将立即返回

返回值：超时返回0;失败返回-1；成功返回大于0的整数，这个整数表示就绪描述符的数目。
```








## epoll
epoll是Linux特有的I/O复用函数。它在实现和使用上与select, poll有很大差异。
首先，epoll使用一组函数来完成任务，而不是单个函数。
其次，epoll把用户关心的文件描述符上的事件放在内核里的一个事件表中，从而无须像select和poll那样每次调用都要重复传入文件描述符集或事件集。
但epoll需要使用一个额外的文件描述符，来唯一标识内核中的这个事件表.这个文件描述符使用如下epoll_create函数来创建：
### 基础API
#### 创建epfd(相当于创建红黑树的根节点)
```cpp
#include <sys/epoll.h>
//the size argument is ignored, but must be greater than zero
//创建一个epoll的句柄,在使用完epoll后，必须调用close()关闭
//调用成功返回一个非负值的 epollfd，调用失败返回 -1
int epoll_create(int size);
```

#### 控制EPOLL(相当于在红黑树上进行crud)
```cpp
#include <sys/epoll.h>
//调用成功返回 0，调用失败返回 -1 并设置 errno 
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);

op表示执行什么操作,有以下三个选项
	POLL_CTL_ADD    注册新的fd到epfd中；
	EPOLL_CTL_MOD   修改已经注册的fd的监听事件；
	EPOLL_CTL_DEL   从epfd中删除一个fd；
	
	
event会告诉内核需要监听的事件                
struct epoll_event {
   uint32_t     events;    /* Epoll events */
   epoll_data_t data;      /* 用户传递的数据 */
};

typedef union epoll_data {
   void    *ptr;
   int      fd;
   uint32_t u32;
   uint64_t u64;
} epoll_data_t;

epoll_event结构体中的events 可以是以下几个宏的集合：
	EPOLLIN     //表示对应的文件描述符可以读（包括对端SOCKET正常关闭）；
	EPOLLOUT    //表示对应的文件描述符可以写；
	EPOLLERR    //表示对应的文件描述符发生错误；
	EPOLLET     //将EPOLL设为边缘触发(Edge Triggered)模式,即重复触发
```

#### 等待EPOLL
```cpp
//等待事件的到来，如果检测到事件，就将所有就绪的事件从内核事件表中复制到它的第二个参数events指向的数组
//存疑？ maxevents 告知内核这个events有多大, 注意: 值 不能大于创建epoll_create()时的size.
//timeout 是超时时间，单位是毫秒，如果设置为 0，epoll_wait 会立即返回
//返回值：超时返回0;失败返回-1；成功返回大于0的整数，这个整数表示就绪描述符的数目。
int epoll_wait(int epfd, struct epoll_event *events,
                      int maxevents, int timeout);
```

https://www.cnblogs.com/skyfsm/p/7102367.html
### epoll的两种工作模式
* LT(level triggered，水平触发模式)是默认的工作方式，并且同时支持 block 和 non-block socket。在这种做法中，内核告诉你一个文件描述符是否就绪了，然后你可以对这个就绪的fd进行IO操作。如果你不作任何操作，内核还是会继续通知你的，所以，这种模式编程出错误可能性要小一点。比如内核通知你其中一个fd可以读数据了，你只读了一部分，下一次循环的时候内核发现里面有数据，就又通知你。
* ET(edge-triggered，边缘触发模式)是高速工作方式，只支持no-block socket。在这种模式下，内核通知过的事情不会再说第二遍。

如果fd是block的，比如阻塞在读操作（比如想读500个字节，只读到了200个字节），而此时即使有多的数据到来，因为无法运行到epoll_wait，也无法通知该fd去读取了，所以就造成了类似死锁的效果。


## EPOLLRDHUP (since Linux 2.6.17)
Stream socket peer closed connection, or shut down writing
half of connection.  (This flag is especially useful for
writing simple code to detect peer shutdown when using
edge-triggered monitoring.)
EPOLLRDHUP实测在对端关闭时会触发，需要注意的是：
对EPOLLRDHUP的处理应该放在EPOLLIN和EPOLLOUT前面，处理方式应该 是close掉相应的fd后，做其他应用层的清理动作；
EPOLLRDHUP想要被触发，需要显式地在epoll_ctl调用时设置在events中；

#### EPOLLONESHOT
即使我们使用ET模式，一个socket上的某个事件还是可能被触发多次。这在并发程序中就会引起一个问题。比如一个线程（或进程，下同）在读取完某个socket上的数据后开始处理这些数据，而在数据的处理过程中该socket上又有新数据可读（EPOLLIN再次被触发），此时另外一个线程被唤醒来读取这些新的数据。于是就出现了两个线程同时操作一个socket的局面。这当然不是我们期望的。我们期望的是一个socket连接在任一时刻都只被一个线程处理。这一点可以使用epoll的EPOLLONESHOT事件实现。
对于注册了EPOLLONESHOT事件的文件描述符，操作系统最多触发其上注册的一个可读、可写或者异常事件，且只触发一次，除非我们使用epoll_ctl函数重置该文件描述符上注册的EPOLLONESHOT事件。这样，当一个线程在处理某个socket时，其他线程是不可能有机会操作该socket的。但反过来思考，注册了EPOLLONESHOT事件的socket —旦被某个线程处理完毕，该线程就应该立即重置这个socket上的EPOLLONESHOT事件，以确保这个socket下一次可读时，其EPOLLIN事件能被触发，进而让其他工作线程有机会继续处理这个 socket 



?前面说过LT会不断触发，所以在处理数据时，不需要在RECV时不断的循环去读一直读到EAGAIN，但如果设置了EPOLLONESHOT后，也得如此办理，否则，就可能会丢掉数据。

epoll_wait 与 poll 的区别
通过前面介绍 poll 与 epoll_wait 函数的介绍，我们可以发现：
epoll_wait 函数调用完之后，我们可以直接在 event 参数中拿到所有有事件就绪的 fd，直接处理即可（event 参数仅仅是个出参）；而 poll 函数的事件集合调用前后数量都未改变，只不过调用前我们通过 pollfd 结构体的 events 字段设置待检测事件，调用后我们需要通过 pollfd 结构体的 revents 字段去检测就绪的事件
调用 epoll_wait 相当于：
1. 你把苹果挨个投入到 epoll 机器中(调用 epoll_ctl);
2. 调用 epoll_wait 加工，你直接通过另外一个袋子就能拿到所有熟苹果。
调用 poll 相当于：
1. 把收到的苹果装入一个袋子里面然后调用 poll 加工；
2. 调用结束后，拿到原来的袋子，袋子中还是原来那么多苹果，只不过熟苹果被贴上了标签纸，你还是需要挨个去查看标签纸挑选熟苹果。
当然，这并不意味着，poll 函数的效率不如 epoll_wait，一般在 fd 数量比较多，但某段时间内，就绪事件 fd 数量较少的情况下，epoll_wait 才会体现出它的优势，也就是说 socket 连接数量较大时而活跃连接较少时 epoll 模型更高效。 
