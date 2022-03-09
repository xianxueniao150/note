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


## connect函数
```cpp
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);

addr:
传入参数，指定对端地址信息，含IP地址和端口号
```

udp协议也可以调用，调用之后，就可以使用send函数向对端发送数据，而不用指定目的地了


## send
```cpp
ssize_t send(int sockfd, const void *buf, size_t len, int flags);
ssize_t sendto(int sockfd, const void *buf, size_t len, int flags,
              const struct sockaddr *dest_addr, socklen_t addrlen);

dest_addr 指定了发送的目的地，对于TCP来说不用指定，指定也会被忽略
ERRORS：
EMSGSIZE：UDP单次发送数据超过最大字节限制，则会引发这个错误
```

## recv
读取数据
```cpp
ssize_t recv(int sockfd, void *buf, size_t len, int flags);

ssize_t recvfrom(int sockfd, void *buf, size_t len, int flags,
                struct sockaddr *src_addr, socklen_t *addrlen);

len指定要读取的字节个数，如果实际收到的大于它就会被截断，所以通常需要循环读取
返回值表示实际读取多少个字节，
recvfrom可以额外记录从哪读的
```
send 和 recv 函数的各种返回值意义

## Socket Option
```cpp
int getsockopt(int sockfd, int level, int optname,
                      void *optval, socklen_t *optlen);
int setsockopt(int sockfd, int level, int optname,
              const void *optval, socklen_t optlen);
```
