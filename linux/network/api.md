## socket
socket()打开一个网络通讯端口，如果成功的话，就像open()一样返回一个文件描述符，应用程序可以像读写文件一样用read/write在网络上收发数据
协议族（domain）中的一个协议（protocol）对于该种实现方式（type）进行支持
```cpp
int socket(int domain, int type, int protocol);

domain(协议族)
Name                Purpose                          Man page
AF_UNIX, AF_LOCAL   Local communication              unix(7)
AF_INET             IPv4 Internet protocols          ip(7)
AF_INET6            IPv6 Internet protocols          ipv6(7)
AF_NETLINK          Kernel user interface device     netlink(7)
AF_PACKET           Low level packet interface       packet(7)

其中AF_INET 这是大多数用来产生socket的协议，使用TCP或UDP来传输，用IPv4的地址

type(实现方式)
SOCK_STREAM(流式,典型TCP)     Provides sequenced, reliable, two-way, connection-based byte streams. 
SOCK_DGRAM(报式,典型UDP)      Supports atagrams (connectionless, unreliable messages of a fixed maximum length).
SOCK_RAW              Provides raw network protocol access

protocol
    传0 表示使用默认协议

成功：返回指向新创建的socket的文件描述符，失败：返回-1，设置errno
```

## bind
bind()的作用是将参数sockfd和addr绑定在一起，使sockfd这个用于网络通讯的文件描述符监听addr所描述的地址和端口号
```cpp
int bind(int sockfd, const struct sockaddr *addr,socklen_t addrlen); 

addrlen:sizeof(addr)长度
 
sockaddr 每个协议族都有自己的     
The sockaddr structure is defined as something like:

struct sockaddr {
   sa_family_t sa_family;
   char        sa_data[14];
} 

对于IPV4协议
struct sockaddr_in {
   sa_family_t    sin_family; /* address family: AF_INET */
   in_port_t      sin_port;   /* port in network byte order */
   struct in_addr sin_addr;   /* internet address */
}; 

struct in_addr {
   uint32_t       s_addr;     /* address in network byte order */
};                                    
```


```servaddr.sin_addr.s_addr = htonl(INADDR_ANY);```
INADDR_ANY，这个宏表示本地的任意IP地址，因为服务器可能有多个网卡，每个网卡也可能绑定多个IP地址，这样设置可以在所有的IP地址上的指定端口进行监听，直到与某个客户端建立了连接时才确定下来到底用哪个IP地址

把IP地址转换为上面需要的 struct in_addr
```cpp
int inet_pton(int af, const char *src, void *dst);
```

This  function  converts  the character string src into a network address structure in the af address family, then copies the network address structure to dst.  The af argument must be either  AF_INET or AF_INET6.


```cpp
const char *inet_ntop(int af, const void *src,
                             char *dst, socklen_t size);
```


## listen函数
指定同时允许多少个客户端和我建立连接
如果达到了限制数量，再来一个连接时，accept函数就阻塞在那，直到有一个连接关闭，空出空位，（存疑）
```cpp
int listen(int sockfd, int backlog);
```
backlog表示最大可接受连接的个数，默认128

## accept函数
```cpp
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);

addr:
传出参数，用来保存客户端地址信息，含IP地址和端口号

addrlen:
传入传出参数（值-结果）,传入sizeof(addr)大小，函数返回时返回真正接收到地址结构体的大小

返回值：
成功返回一个新的socket文件描述符，用于和客户端通信，失败返回-1，设置errno
```


## connect函数 发起连接
```cpp
// sockfd 由socket系统调用返回一个socket
// addr: 指定对端地址信息，含IP地址和端口号
//成功则返回0，失败返回-1，错误原因存于errno中。
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);

```
一但成功建立连接,sockfd就唯一的标识了这个连接,客户端就可以通过读写sockfd来与服务端通信

常见errno
ECONNREFUSED 目标端口不存在,连接被拒绝。
ETIMEDOUT 连接超时。

udp协议也可以调用，调用之后，就可以使用send函数向对端发送数据，而不用指定目的地了


## close 关闭连接
```cpp
#include <unistd.h>
int close(int sockfd)
```
close 系统调用并非总是立即关闭一个连接,而是将sockfd的引用计数减1,只有当sockfd的引用计数为0时,才真正关闭连接.
多进程程序中一次fork系统调用默认将父进程中打开的socket的引用计数加1，因此我们必须在父进程和子进程中都对该socket执行close调用才能将连接关闭。

## shutdown 关闭连接
如果要立即终止连接，而不是引用计数减一，使用shutdown。(专为网络编程设计)
```cpp
#include<sys/socket.h>
// 成功返回1，失败返回-1并设置errno
int shutdown(int sockfd,int howto);
```
howto: 
	SHUT_RD，只关闭读，接收缓冲区数据全部丢弃；
	SHUT_WR，关闭写，程序不能继续写，缓冲区数据会发送完，此时处于半连接状态；
	SHUT_RDWR，同时关闭读写。



## Socket Option
```cpp
#include <sys/socket.h>
// level指定操作哪个协议的选项
// option_name指定选项的名字
// option_value、option_len是选项操作的值和长度
// 成功时返回0，失败返回-1并设置errno
int getsockopt(int sockfd, int level, int optname, void *restrict optval, socklen_t *restrict optlen);
int setsockopt(int sockfd, int level, int optname, const void *optval, socklen_t optlen);
```
对服务器而言，有些socket选项只能在listen系统调用前针对socket设置才有效
对监听socket设置socket选项，则accept返回的链接socket将自动继承这些选项

### SO_REUSEADDR选项
  通过SO_RESUSEADDR选项可以强制使用被处于TIME_WAIT状态的链接占用的socket地址
```cpp
int reuse = 1;
setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
```

5.11.2 SO_RCVBUF和SO_SNDBUF选项
  SO_RCVBUF和SO_SNDBUF选项分别表示TCP接收缓冲区和发送缓冲区的大小，可确保TCP连接拥有足够的空闲缓冲区来处理拥塞。

5.11.3 SO_RCVLOWAT和SO_SNDLOWAT选项
  SO_RCVLOWAT和SO_SNDLOWAT选项分别表示TCP接收缓冲区和发送缓冲区的低水位标记，其默认为1。一般被IO复用系统调用时判断socket是否刻度或可写。

5.11.4 SO_LINGER选项
  SO_LINGER选项用于控制close系统调用在关闭TCP连接时的行为，当设置SO_LINGER值时，会将setsockopt系统调用传递给linger结构体

#include <sys/socket.h>
struct linger{
    int l_onoff;            // 开启或关闭该选项
    int l_linger;           // 留置时间
};
1
2
3
4
5
l_onoff == 0：该选项不起作用。
l_onoff != 0, l_linger == 0：close系统调用立即返回，TCP模块丢弃被关闭的socket对应的TCP缓冲区残留数据，并给对方发送一个复位报文段。此方法给服务器提供了异常终止的连接方法。
l_onoff != 0， l_linger>0：阻塞的socket，close等待l_linger的时间，知道TCP模块发送完所有的残留数据并得到对方确认，若未得到返回-1并设置errno；非阻塞的socket，close立即返回，根据返回值和errno怕段擦流数据是否已经发送完毕。

————————————————
版权声明：本文为CSDN博主「甄姬、巴豆」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_46267443/article/details/120722283
## EINTR
表示某种阻塞的操作，被接收到的信号中断，造成的一种错误返回值。
我们经常在网络编程中会看到这样，当执行一个可能会阻塞的系统调用后，在返回的时候需要检查下错误码（if errno == EINTR），如果是这样的错误，那我们一般会重新执行该系统调用。
