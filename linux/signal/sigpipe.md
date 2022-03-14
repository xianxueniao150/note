在什么场景下会产生SIGPIPE信号？
　　SIGPIPE产生的原因是这样的：如果一个 socket 在接收到了 RST packet 之后，程序仍然向这个 socket 写入数据，那么就会产生SIGPIPE信号。
　　这种现象是很常见的，譬如说，当 client 连接到 server 之后，这时候 server 准备向 client 发送多条消息，但在发送消息之前，client 进程意外奔溃了，那么接下来 server 在发送多条消息的过程中，就会出现SIGPIPE信号。下面我们看看 server 的代码：

```cpp
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>
#include <signal.h>
#define MAXLINE 1024
void handle_client(int fd)
{
    // 假设此时 client 奔溃, 那么 server 将接收到 client 发送的 FIN
    sleep(5);
    // 写入第一条消息
    char msg1[MAXLINE] = {"first message"}; 
    ssize_t n = write(fd, msg1, strlen(msg1));
    printf("write %ld bytes\n", n);
    // 此时第一条消息发送成功，server 接收到 client 发送的 RST
    sleep(1); 
    // 写入第二条消息，出现 SIGPIPE 信号，导致 server 被杀死
    char msg2[MAXLINE] = {"second message"};
    n = write(fd, msg2, strlen(msg2));
    printf("%ld, %s\n", n, strerror(errno));
}

int main()
{
    unsigned short port = 8888;
    struct sockaddr_in server_addr;
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(port);
    int listenfd = socket(AF_INET , SOCK_STREAM , 0);
    bind(listenfd, (struct sockaddr *)&server_addr, sizeof(server_addr));
    listen(listenfd, 128);
    int fd = accept(listenfd, NULL, NULL);
    handle_client(fd);
    return 0;
}
```

我们可以使用 Linux 的 nc 工具作为 client，当 client 连接到 server 之后，就立即杀死 client (模拟 client 的意外奔溃)。这时可以观察 server 的运行情况：
```sh
$ gcc -o server server.c 
$ ./server &              # 后台运行 server,这里如果前台运行的话，看不到报错
$ nc localhost 8888       # 运行 nc 连接到 server
^C                        # Ctrl-C 杀死 nc


# ./server
write 13 bytes
[1]+  Broken pipe             
#[1]+  Exit 141  如果是自己写的client端，则会报这个错，但不影响结果
```

让我们分析一下整个过程：
	client 连接到 server 之后，client 进程意外奔溃，这时它会发送一个 FIN 给 server。
	此时 server 并不知道 client 已经奔溃了，所以它会发送第一条消息给 client。但 client 已经退出了，所以 client 的 TCP 协议栈会发送一个 RST 给 server。
	server 在接收到 RST 之后，继续写入第二条消息。往一个已经收到 RST 的 socket 继续写入数据，将导致SIGPIPE信号，从而杀死 server。
	　　对 server 来说，为了不被SIGPIPE信号杀死，那就需要忽略SIGPIPE信号：

```cpp
int main()
{
    signal(SIGPIPE, SIG_IGN);  // 忽略 SIGPIPE 信号
    // ...
}
```
新运行上面的程序，server 在发送第二条消息的时候，write()会返回-1，并且此时errno的值为EPIPE
```sh
 -1, Broken pipe
```


