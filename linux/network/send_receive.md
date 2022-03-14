## send
```cpp
ssize_t send(int sockfd, const void *buf, size_t len, int flags);
ssize_t sendto(int sockfd, const void *buf, size_t len, int flags,
              const struct sockaddr *dest_addr, socklen_t addrlen);

dest_addr 指定了发送的目的地，对于TCP来说不用指定，指定也会被忽略

ERRORS：
EMSGSIZE：UDP单次发送数据超过最大字节限制，则会引发这个错误
```
当套接字发送缓冲区变满时，send通常会阻塞，除非套接字设置为非阻塞模式，当缓冲区变满时，返回EAGAIN或者EWOULDBLOCK错误，此时可以调用select函数来监视何时可以发送数据。


## recv
读取数据
```cpp
#include <sys/socket.h>

ssize_t recv(int sockfd, void *buf, size_t len, int flags);
ssize_t recvfrom(int sockfd, void *buf, size_t len, int flags,
                struct sockaddr *src_addr, socklen_t *addrlen);

len指定要读取的字节个数，如果实际收到的大于它就会被截断，所以通常需要循环读取
返回值表示实际读取多少个字节，
recvfrom可以额外记录从哪读的

[EAGAIN]           The socket is marked non-blocking, and the receive operation would block, or a receive timeout had been set, and the timeout expired before data were received.
If no messages are available at the socket, the receive call waits for a message to arrive, unless the socket is nonblocking (see fcntl(2)) in which case the value -1 is returned
     and the external variable errno set to EAGAIN.
```

## send 和 recv 函数的各种返回值意义
* 大于 0:	成功发送 n 个字节
* 0	:       对端关闭连接
* 小于 0:（ -1）	出错或者被信号中断或者对端 TCP 窗口太小数据发不出去（send）或者当前网卡缓冲区已无数据可收（recv）

我们来逐一介绍下这三种情况：
### 返回值大于 0
对于 send 和 recv 函数返回值大于 0，表示发送或接收多少字节，
需要注意的是，在这种情形下，我们一定要判断下 send 函数的返回值是不是我们期望发送的缓冲区长度，而不是简单判断其返回值大于0。 因为存在只发送出去一部分数据的情况。
所以，建议要么认为返回值 n 等于 buf_length 才认为正确，要么在一个循环中调用 send 函数，如果数据一次性发不完，记录偏移量，下一次从偏移量处接着发，直到全部发送完为止。

```cpp
//推荐的方式一
int n = send(socket, buf, buf_length, 0)；
if (n == buf_length)
{
    printf("send data successfully\n");
}
```


```cpp
//推荐的方式二：在一个循环里面根据偏移量发送数据
bool SendData(const char* buf , int buf_length)
{
   //已发送的字节数目
   int sent_bytes = 0;
   int ret = 0;
   while (true)
   {
       ret = send(m_hSocket, buf + sent_bytes, buf_length - sent_bytes, 0);
       if (ret == -1)
       {
	   	   //非阻塞模式下send函数由于TCP窗口太小发不出去数据，错误码是EWOULDBLOCK
           if (errno == EWOULDBLOCK)
           {
               //严谨的做法，这里如果发不出去，应该缓存尚未发出去的数据，后面介绍
               break;
           }             
		   //如果被信号中断，我们继续重试
           else if (errno == EINTR)
               continue;
           else
               return false;
       }
	   //对端关闭了连接，我们也关闭
       else if (ret == 0)
       {
           return false;
       }

       sent_bytes += ret;
       if (sent_bytes == buf_length)
           break;

       //稍稍降低 CPU 的使用率
       usleep(1);
   }

   return true;
}
```

返回值等于 0
通常情况下，如果 send 或者 recv 函数返回 0，我们就认为对端关闭了连接，我们这端也关闭连接即可，这是实际开发时最常见的处理逻辑。

但是，现在还有一种情形就是，假设调用 send 函数传递的数据长度就是 0 呢？send 函数会是什么行为？对端会 recv 到一个 0 字节的数据吗？需要强调的是，在实际开发中，你不应该让你的程序有任何机会去 send 0 字节的数据，这是一种不好的做法。 这里仅仅用于实验性讨论，我们来通过一个例子，来看下

这里省略代码

结果：根据程序输出可以看到send函数调用成功了，但是tcpdump 抓包结果输出中，除了连接时的三次握手数据包，再也无其他数据包，也就是说，send 函数发送 0 字节数据，client 的协议栈并不会把这些数据发出去。
因此，server 端也会一直没有输出，如果你用的是 gdb 启动 server，此时中断下来会发现，server 端由于没有数据会一直阻塞在 recv 函数调用处。
