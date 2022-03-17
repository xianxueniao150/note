跨主机传输要注意的问题

## 字节序问题
大端：低地址处放高字节
小端：低地址处放低字节

检验字节序代码
```cpp
#include <stdio.h>
void byteorder()
{
	union
	{
		short value;
		char union_bytes[sizeof(short)];
	} test;
	test.value = 0x0102;
	if ((test.union_bytes[0] == 1) && (test.union_bytes[1] == 2))
	{
		printf("big endian\n");
	}
	else if ((test.union_bytes[0] == 2) && (test.union_bytes[1] == 1))
	{
		printf("little endian\n");
	}
	else
	{
		printf("unknown...\n");
	}
}

int main(int argc, char const *argv[])
{
	byteorder();
	return 0;
}
```

现代PC大多采用小端字节序，因此小端字节序又被称为主机字节序。
当格式化的数据（比如32 bit整型数和16 bit短整型数）在两台使用不同字节序的主机之间直接传递时，接收端必然错误地解释之。解决问题的方法是:发送端总是把要发送的数据转化成大端字节序数据后再发送，而接收端知道对方传送过来的数据总是采用大端字节序，所以接收端可以根据自身采用的字节序决定是否对接收到的数据进行转换（小端机转换，大端机不转换）。
因此大端字节序也称为网络字节序，它给所有接收数据的主机提供了 一个正确解释收到的格式化数据的保证。
需要指出的是，即使是同一台机器上的两个进程（比如一个由C语言编写，另一个由 JAVA编写）通信，也要考虑字节序的问题（JAVA虚拟机釆用大端字节序）。

主机字节序：host
网络字节序：network
Linux提供了如下4个函数来完成主机字节序和网络字节序之间的转换：
转换：htons，htonl，ntohs，ntohl
它们的含义很明确，比如htonl表示"host to network long",即将长整型（32 bit）的主 机字节序数据转化为网络字节序数据。这4个函数中，长整型函数通常用来转换IP地址，短整型函数用来转换端口号（当然不限于此。任何格式化的数据通过网络传输时，都应该使用这些函数来转换字节序）。

## 2.对齐
禁止编译器自动对齐

## 3.类型长度问题
解决：int32_t，uint32_t，int64_t，int8_t （不管是什么类型，比如char，我不要你的类型，我只要你的长度）

socket 其实就是一个五元组，包括：源IP, 源端口, 目的IP, 目的端口, 类型(TCP or UDP)

## socket
socket()打开一个网络通讯端口，如果成功的话，就像open()一样返回一个文件描述符，应用程序可以像读写文件一样用read/write在网络上收发数据
```cpp
#include <sys/types.h>
#include <sys/socket.h>
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

## socket地址
### 通用socket地址
```cpp
struct sockaddr {
   sa_family_t sa_family;
   char        sa_data[14];
} 
```

但通用的不好用，所以每个协议族都定义了自己专用的, 所有专用socket地址(以及sockaddr_storage)类型的变量在实际使用时都需要转化为通用socket地址类型sockaddr (强制转换即可)，因为所有socket编程接口使用的地址参数的类型都是sockaddr

### 对于IPV4协议
```cpp
struct sockaddr_in {
   sa_family_t    sin_family; /* address family: AF_INET */
   in_port_t      sin_port;   /* port in network byte order */
   struct in_addr sin_addr;   /* internet address */
}; 

struct in_addr {
   uint32_t       s_addr;     /* address in network byte order */
};                                    
```

## IP地址转换函数
通常，人们习惯用可读性好的字符串来表示ip地址，比如用点分十进制字符串表示IPv4地址，以及用十六进制字符串表示IPv6地址。但编程中我们需要先把它们转化为整数 (二进制数)方能使用。而记录日志时则相反，我们要把整数表示的IP地址转化为可读的字符串。下面3个函数可用于用点分十进制字符串表示的IPv4地址和用网络字节序整数表示的IPv4地址之间的转换：
```cpp
#include <arpa/inet.h>
//inet_addr函数将用点分十进制字符串表示的IPv4地址转化为用网络字节序整数表示的 IPv4地址。它失败时返回INADDR_NONE
in_addr_t inet_addr( const char* strptr );
//inet_aton函数完成和inet_addr同样的功能，但是将转化结果存储于参数inp指向的地址 结构中。它成功时返回1,失败则返回0。
int inet_aton( const char* cp, struct in_addr* inp );
//inet_ntoa函数将用网络字节序整数表示的IPv4地址转化为用点分十进制字符串表示的 IPv4地址。但需要注意的是，该函数内部用一个静态变量存储转化结果，函数的返回值指向 该静态内存，因此inet_ntoa是不可重入的。下面代码揭示了其不可重入性。
char* inet_ntoa( struct in_addr in );

//下面这对更新的函数也能完成和前面3个函数同样的功能，并且它们同时适用于IPv4 地址和IPv6地址：
//The af argument must be either  AF_INET or AF_INET6
int inet_pton( int af, const char* src, void* dst );
const char* inet_ntop( int af, const void* src, char* dst, socklen_t ent );
```

不可重入的inet ntoa函数
```cpp
char* szValuel - inet_ntoa( "1.2.3.4");
char* szValue2 - inet_ntoa( "10.194.71.60");
printf ( "address 1: %s\n" , szValuel );
printf ( "address 2 :%s\n" , szValue2 );
```
运行这段代码，得到的结果是：
addressl: 10.194.71.60
address2: 10.194.71.60


## 修改内核参数有3种办法：一种临时修改，两种永久修改。
- 临时修改
	- 使用sysctl [选项] [参数名=值]命令；
- 永久修改
	- 修改/etc/sysctl.conf文件
	- 修改/proc/sys/目录下的对应文件（例如，修改net.ipv4.tcp_synack_retries=0，即echo 0 > /proc/sys/net/ipv4/tcp_synack_retries）。
