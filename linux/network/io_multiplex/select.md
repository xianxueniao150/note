## select
该函数允许进程指示内核等待多个事件中的任何一个发生,并只在有一个或多个事件发生或经历一段指定的时间后才唤醒它。
作为一个例子,我们可以调用select,告知内核仅在下列情况发生时才返回:
- 集合{1,4,5}中的任何描述符准备好读;
- 集合{2,7}中的任何描述符准备好写;
- 集合{1,4}中的任何描述符有异常条件待处理;
- 已经历了10.2秒。
也就是说,我们调用select告知内核对哪些描述符(就读、写或异常条件)感兴趣以及等待多长时间。我们感兴趣的描述符不局限于套接字,任何描述符都可以使用select来测试。
```cpp
#include <sys/select.h>
int select(int nfds, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout);

nfds:应该被设定为三个集合中最大文件描述符的值加1,描述符0,1,2一直到nfds-1 均将被测试
readfds,writefds,exceptfds:分别指向可读、可写和异常等事件对应的描述符集合

fd_set结构体仅包含一个整型数组，该数组的每个元素的每一位(bit) 标记一个文件描述符, 举例来说,假设使用32位整数,那么该数组的第一个元素对应于描述符0~31,第二个元素对应于描述符32~63,依此类推
fd_set能容纳的文件描述符数量由FD_SETSIZE(1024)指定，这就限制了select能同时处理的文件描述符的总量。
由于位操作过于烦琐，我们应该使用下面的一系列宏来访问fd_set结构体中的位：
	void FD_SET(int fd, fd_set *set);
	void FD_CLR(int fd, fd_set *set);
	int  FD_ISSET(int fd, fd_set *set);
	void FD_ZERO(fd_set *set);

timeout 设置select函数的超时时间。釆用指针参数是因为内核将修改它以告诉应用程序select等待了多久(只有Linux是这样实现的)。不过我们不能完全信任 select调用返冋后的timeout值，比如调用失败时timeout值是不确定的。
struct timeval {
   long    tv_sec;         /* seconds */
   long    tv_usec;       /* microseconds */
};
如果给timeout变量的tv_sec成员和tv_usec成员都传递0,则select将立即返回.如果给timeout传递NULL,则 select将一直阻塞，直到某个文件描述符就绪.

返回值：超时返回0;成功返回大于0的整数，这个整数表示就绪描述符的数目；失败返回-1 并设置errno.如果在select 等待期间，程序接收到信号，则select立即返回-1,并设置errno为EINTR.
```
select函数的中间三个参数readset、writeset和exceptset中,如果我们对某一个的条件不感兴趣,就可以把它设为空指针。
事实上,如果这三个指针均为空,我们就有了一个比Unix的sleep函数更为精确的定时器(sleep睡眠以秒为最小单位)。

select函数修改由指针readset、writeset和exceptset所指向的的描述符集,因而这三个参数都是值结果参数。调用该函数时,我们指定所关心的描述符的值,该函数返回时,结果将指示哪些描述符已就绪。该函数返回后,我们使用FD_ISSET宏来测试fd_set数据类型中的描述符。描述符集内任何与未就绪描述符对应的位返回时均清成0。为此,每次重新调用select函数时, 我们都得再次把所有描述符集内所关心的位均置为1。



### 深入理解select模型：
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
- 对socket进行扫描时是线性扫描，即采用轮询的方法，效率较低：当套接字比较多的时候，每次select()都要通过遍历FD_SETSIZE个Socket来完成调度,不管哪个Socket是活跃的,都遍历一遍。这会浪费很多CPU时间。如果能给套接字注册某个回调函数，当他们活跃时，自动完成相关操作，那就避免了轮询，这正是epoll与kqueue做的。
- 需要维护一个用来存放大量fd的数据结构，这样会使得用户空间和内核空间在传递该结构时复制开销大。
