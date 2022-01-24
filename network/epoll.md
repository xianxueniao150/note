select

select 代收员比较懒，她记不住快递员的单号，还有快递货物的数量。她只会告诉你快递到了，但是是谁到的，你需要挨个快递员问一遍。
while true {
	select(流[]); //阻塞

  //有消息抵达
	for i in 流[] {
		if i has 数据 {
			读 或者 其他处理
		}
	}
}




以事件为单位组织文件描述符
//nfds nfds should be set to the highest-numbered file descriptor in any of the three sets, plus 1
//readfds,writefds,exceptfds分别指向可读、可写和异常等事件对应的描述符集合
//timeout:告诉内核select等待多长时间之后就放弃等待。timeout == NULL 表示等待无限长的时间
int select(int nfds, fd_set *readfds, fd_set *writefds,
                  fd_set *exceptfds, struct timeval *timeout);

void FD_CLR(int fd, fd_set *set);
int  FD_ISSET(int fd, fd_set *set);
void FD_SET(int fd, fd_set *set);
void FD_ZERO(fd_set *set);

struct timeval {
   long    tv_sec;         /* seconds */
   long    tv_usec;       /* microseconds */
};

返回值：超时返回0;失败返回-1；成功返回大于0的整数，这个整数表示就绪描述符的数目。

深入理解select模型：
理解select模型的关键在于理解fd_set,为说明方便，取fd_set长度为1字节，fd_set中的每一bit可以对应一个文件描述符fd。则1字节长的fd_set最大可以对应8个fd。
（1）执行fd_set set; FD_ZERO(&set); 则set用位表示是0000,0000。
（2）若fd＝5,执行FD_SET(fd,&set);后set变为0001,0000(第5位置为1)
（3）若再加入fd＝2，fd=1,则set变为0001,0011
（4）执行select(6,&set,0,0,0)阻塞等待
（5）若fd=1,fd=2上都发生可读事件，则select返回，此时set变为0000,0011。注意：没有事件发生的fd=5被清空。
基于上面的讨论，可以轻松得出select模型的特点：
（1）可监控的文件描述符个数取决与sizeof(fd_set)的值。我这边服务器上sizeof(fd_set)＝512，每bit表示一个文件描述符，则我服务器上支持的最大文件描述符是512*8=4096。据说可调，另有说虽然可调，但调整上限受于编译内核时的变量值。
（2）将fd加入select监控集的同时，还要再使用一个数据结构array保存放到select监控集中的fd，一是用于再select返回后，array作为源数据和fd_set进行FD_ISSET判断。二是select返回后会把以前加入的但并无事件发生的fd清空，则每次开始select前都要重新从array取得fd逐一加入（FD_ZERO最先），扫描array的同时取得fd最大值maxfd，用于select的第一个参数。
（3）可见select模型必须在select前循环加fd，取maxfd，select返回后利用FD_ISSET判断是否有事件发生。

select总结：
select本质上是通过设置或者检查存放fd标志位的数据结构来进行下一步处理。这样所带来的缺点是：
1、单个进程可监视的fd数量被限制，即能监听端口的大小有限。一般来说这个数目和系统内存关系很大，具体数目可以cat/proc/sys/fs/file-max察看。32位机默认是1024个。64位机默认是2048.
2、 对socket进行扫描时是线性扫描，即采用轮询的方法，效率较低：当套接字比较多的时候，每次select()都要通过遍历FD_SETSIZE个Socket来完成调度,不管哪个Socket是活跃的,都遍历一遍。这会浪费很多CPU时间。如果能给套接字注册某个回调函数，当他们活跃时，自动完成相关操作，那就避免了轮询，这正是epoll与kqueue做的。
3、需要维护一个用来存放大量fd的数据结构，这样会使得用户空间和内核空间在传递该结构时复制开销大。


poll
以文件描述符为单位组织事件
//nfds指定前面有几个pollfd 
//返回值：超时返回0;失败返回-1；成功返回大于0的整数，这个整数表示就绪描述符的数目。
int poll(struct pollfd *fds, nfds_t nfds, int timeout);

struct pollfd {
   int   fd;         /* file descriptor */
   short events;     /* requested events，a bit mask */
   short revents;    /* returned events，output parameter，内核会把实际发生的event放进去 */
};

pollfd 结构体中的events 可以是以下几个宏的集合：
POLLIN     //表示对应的文件描述符可以读（包括对端SOCKET正常关闭）；
POLLOUT    //表示对应的文件描述符可以写；


## epoll

https://www.cnblogs.com/skyfsm/p/7102367.html
epoll的两种工作模式
epoll在内核维护了一个事件表，存放用户关心的文件描述符上的事件，这个事件表由一个描述符epfd来唯一标识

LT(level triggered，水平触发模式)是缺省的工作方式，并且同时支持 block 和 non-block socket。在这种做法中，内核告诉你一个文件描述符是否就绪了，然后你可以对这个就绪的fd进行IO操作。如果你不作任何操作，内核还是会继续通知你的，所以，这种模式编程出错误可能性要小一点。比如内核通知你其中一个fd可以读数据了，你只读了一部分，下一次循环的时候内核发现里面有数据，就又通知你。

ET(edge-triggered，边缘触发模式)是高速工作方式，只支持no-block socket。在这种模式下，内核通知过的事情不会再说第二遍。

如果fd是block的，比如阻塞在读操作（比如想读500个字节，只读到了200个字节），而此时即使有多的数据到来，因为无法允许到epoll_wait，也无法通知该fd去读取了，所以就造成了类似死锁的效果。

### 基础API
#### 创建epfd(相当于创建红黑树的根节点)
```
//the size argument is ignored, but must be greater than zero
//创建一个epoll的句柄,在使用完epoll后，必须调用close()关闭
//调用成功返回一个非负值的 epollfd，调用失败返回 -1
int epoll_create(int size);
```


#### 控制EPOLL(相当于在红黑树上进行crud)
```
//epoll的事件注册函数,op表示执行什么操作，fd表示监听哪个文件，event会告诉内核需要监听的事件,event会保存在红黑树节点当中，最终返回给用户
//调用成功返回 0，调用失败返回 -1，你可以通过 errno 错误码获取具体的错误原因。
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);

op有以下三个选项
//POLL_CTL_ADD    注册新的fd到epfd中；
//EPOLL_CTL_MOD   修改已经注册的fd的监听事件；
//EPOLL_CTL_DEL   从epfd中删除一个fd；
                 
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


等待EPOLL
```
//等待事件的到来，如果检测到事件，就将所有就绪的事件从内核事件表中复制到它的第二个参数events指向的数组
//存疑？ maxevents 告知内核这个events有多大, 注意: 值 不能大于创建epoll_create()时的size.
//timeout 是超时时间，单位是毫秒，如果设置为 0，epoll_wait 会立即返回
//返回值：超时返回0;失败返回-1；成功返回大于0的整数，这个整数表示就绪描述符的数目。
int epoll_wait(int epfd, struct epoll_event *events,
                      int maxevents, int timeout);
```





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
