
## bind
bind()的作用是将参数sockfd和addr绑定在一起，使sockfd这个用于网络通讯的文件描述符监听addr所描述的地址和端口号
```cpp
#include <sys/types.h>
#include <sys/socket.h>
int bind(int sockfd, const struct sockaddr *addr,socklen_t addrlen); 

addrlen:sizeof(addr)长度
```

bind成功时返回0,失败则返回-1并设置errno 常见的errno:
- EACCES,被绑定的地址是受保护的地址，仅超级用户能够访问。比如普通用户将 socket绑定到知名服务端口（端口号为0〜1023）上时，bind将返回EACCES错误。
- EADDRINUSE,被绑定的地址正在使用中。比如将socket绑定到一个处于TIME_ WAIT状态的socket地址。


INADDR_ANY，这个宏表示本地的任意IP地址，因为服务器可能有多个网卡，每个网卡也可能绑定多个IP地址，这样设置可以在所有的IP地址上的指定端口进行监听，直到与某个客户端建立了连接时才确定下来到底用哪个IP地址


## listen函数
指定同时允许多少个客户端和我建立连接
backlog 在现在的内核版本中，是决定半连接队列和全连接队列大小的一个因子。
试验:当指定backlog为3时,调用listen后一直睡眠，不调用connect函数，则当建立四个连接后，客户端再发送sync请求建立连接，服务端不会回应（服务端会一直保持半连接队列为空，全连接队列为4）,客户端会一直尝试建立连接直至超时
```cpp
int listen(int sockfd, int backlog);
```
backlog表示最大可接受连接的个数，默认128

## accept函数
```cpp
#include <sys/types.h>
#include <sys/socket.h>
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);

sockfd: 执行过listen系统调用的监听socket
addr: 传出参数，用来保存客户端地址信息，含IP地址和端口号
addrlen: 传入传出参数（值-结果）,传入sizeof(addr)大小，函数返回时返回真正接收到地址结构体的大小

返回值：成功返回一个新的socket文件描述符，用于和客户端通信，失败返回-1，设置errno
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
关闭一个连接实际上就是关闭该连接对应的socket,这可以通过如下关闭普通文件描述符的系统调用来完成：
```cpp
#include <unistd.h>
int close(int sockfd)
```
close 系统调用并非总是立即关闭一个连接,而是将sockfd的引用计数减1,只有当sockfd的引用计数为0时,才真正关闭连接.
多进程程序中一次fork系统调用默认将父进程中打开的socket的引用计数加1，因此我们必须在父进程和子进程中都对该socket执行close调用才能将连接关闭。

## shutdown 关闭连接
如果要立即终止连接，而不是引用计数减一，使用shutdown。(专为网络编程设计)
```cpp
#include <sys/socket.h>
// 成功返回1，失败返回-1并设置errno
int shutdown(int sockfd,int howto);
```
howto: 
	SHUT_RD，只关闭读，程序不能继续读，且接收缓冲区数据全部丢弃；
	SHUT_WR，关闭写，程序不能继续写，缓冲区数据会在真正关闭连接之前全部发送出去，此时处于半关闭状态；
	SHUT_RDWR，同时关闭读写。



