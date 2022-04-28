## pipe 创建管道，实现进程间通信
```cpp
#include <unistd.h>
int pipe(int pipefd[2]);
```
pipe函数的参数是一个包含两个int型整数的数组指针。该函数成功时返冋0,并将一对打开的文件描述符值填入其参数指向的数组。如果失败，则返回-1并设置errno.
并且，fd［O］只能用于从管道读出数据，fd［1］则只能用于往管道写入数据，而不能反过来使用。如果要实现双向的数据传输，就应该使用两个管道。
通过pipe函数创建的这两个文件描述符 fd[0] 和 fd[1] 分别构成管道的两端，前者打开来读，后者打开来写
默认情况下，这一对文件描述符都是阻塞的。此时如果我们用read系统调用来读取一个空的管道， 则read将被阻塞，直到管道内有数据可读；如果用write系统调用来往一个满的管道中写入数据，则write亦将被阻塞，直到管道有足够多的空闲空间可用。
如果管道的写端文件描述符fd［1］的引用计数减少至0, 即没有任何进程需要往管道中写入数据，则针对该管道的读端文件描述符fd［O］的read操作将返冋0,即读取到了文件结束标记（End Of File, EOF）；反之，如果管道的读端文件描述符fd［O］的引用计数减少至0,即没有任何进程需要从管道读取数据，则针对该管道的写端文件描述符fd[1]的write操作将失败，并引发SIGPIPE信号。

## socketpair
此外，socket的基础API中冇一个socketpair函数。它能够方便地创建双向管道。其定义如下：
```cpp
#include <sys/types.h>          
#include <sys/socket.h>
int socketpair(int domain, int type, int protocol, int sv[2]);

socketpair前三个参数的含义与socket系统週用的三个参数完全相同
* domain表示协议族，只能是本地域协议族PF_UNIX或者AF_UNIX,因为我们仅能在本地使用这个双向管道
* type表示协议，可以是SOCK_STREAM或者SOCK_DGRAM，SOCK_STREAM基于TCP，SOCK_DGRAM基于UDP
* protocol表示类型，只能为0
* sv[2]表示套节字柄对，该两个句柄作用相同，均能进行读写双向操作
* 返回结果， 0为创建成功，-1为创建失败，并且errno来表明特定的错误号
```
一般不会这样用，因为分不清是谁写入的，一般如果两个进程要相互传递数据的话会使用两个管道。


## popen()函数：建立管道I/O
popen()会调用fork()产生子进程，然后从子进程中调用/bin/sh -c 来执行参数command 的指令。
参数type 可使用 "r"代表读取，"w"代表写入。依照此type 值，popen()会建立管道连到子进程的标准输出设备或标准输入设备，然后返回一个文件指针。随后进程便可利用此文件指针来读取子进程的输出设备或是写入到子进程的标准输入设备中。

此外，所有使用文件指针(FILE*)操作的函数也都可以使用，除了fclose()以外。

```cpp
FILE * popen(const char * command, const char * type);
```
返回值：若成功则返回文件指针, 否则返回NULL, 错误原因存于errno 中.

注意事项：在编写具 SUID/SGID 权限的程序时请尽量避免使用popen()、popen()会继承环境变量，通过环境变量可能会造成系统安全的问题。

示例
```cpp
#include <stdio.h>
main()
{
    FILE * fp;
    char buffer[80];
    fp = popen("cat /etc/passwd", "r");
    fgets(buffer, sizeof(buffer), fp);
    printf("%s", buffer);
    pclose(fp);
}
```

执行：
root :x:0 0: root: /root: /bin/bash

## 命名管道
通常的管道没有名字，只能连接相关的进程。我们无法在无亲缘关系的两个进程间创建一个管道并将它用作IPC通信。

FIFO 与管道类似，是一个单向数据流,它们两者之间最大的差别在于 FIFO 在文件系统中拥有一个名称，并且其打开方式与打开一个普通文件是一样的。这样就能够将 FIFO 用于非相关进程之间的通信（如客户端和服务器）。
一旦打开了 FIFO，就能在它上面使用与操作管道和其他文件的系统调用一样的 I/O 系统调用了（如 read()、write()和 close()）。与管道一样，FIFO 也有一个写入端和读取端，并且从管道中读取数据的顺序与写入的顺序是一样的。FIFO 的名称也由此而来：先入先出。FIFO 有时候也被称为命名管道。
与管道一样，当所有引用 FIFO 的描述符都被关闭之后，所有未被读取的数据会被丢弃。
命名管道可以独立于进程存在。

### 示例
### 直接通过命令行创建
```sh
# 终端1
ubuntu@VM-12-3-ubuntu:~/unix_pro$ mkfifo /tmp/pipe
ubuntu@VM-12-3-ubuntu:~/unix_pro$ ls -l /tmp/pipe 
prw-rw-r-- 1 ubuntu ubuntu 0 Apr 19 23:33 /tmp/pipe
# 会阻塞在这直到终端2去读
ubuntu@VM-12-3-ubuntu:~/unix_pro$ ls -l > /tmp/pipe

# 终端2
ubuntu@VM-12-3-ubuntu:~/unix_pro$ cat /tmp/pipe 
total 80
-rw-rw-r-- 1 ubuntu ubuntu   187 Apr 18 21:30 a.c
-rwxrwxr-x 1 ubuntu ubuntu 16880 Apr 18 21:30 a.out
```

### 代码创建
```cpp
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <fcntl.h>

#define FIFO_FILE "/tmp/pipe"
#define BUFFER_SIZE 1024

int main(int argc, char **argv)
{
    //创建管道
    if ((mkfifo(FIFO_FILE, 0644) < 0))
    {
        perror("mkfifo error");
        exit(EXIT_FAILURE);
    }
    int read_fd, write_fd;
	//open 会阻塞在这里直到第一个客户只写打开管道
    read_fd = open(FIFO_FILE, O_RDONLY);
    if (read_fd == -1)
    {
        perror("open error");
        exit(EXIT_FAILURE);
    }
    char buf[BUFFER_SIZE];
    int n = 0;
    while ((n = read(read_fd, buf, BUFFER_SIZE)))
    {
        printf("%s", buf);
    }
    perror("read error");
    close(read_fd);
    unlink(FIFO_FILE);
    return 0;
}
```

```sh
# 终端1会阻塞在这，直到终端2向管道写入数据
ubuntu@VM-12-3-ubuntu:~/unix_pro/pipe$ gcc server.c && ./a.out 
total 24
-rwxrwxr-x 1 ubuntu ubuntu 17104 Apr 19 11:07 a.out
prw-r--r-- 1 ubuntu ubuntu     0 Apr 18 23:41 pipe
-rw-rw-r-- 1 ubuntu ubuntu   810 Apr 19 11:06 server.c
n:0 errno:0
read error: Success


# 终端2
ubuntu@VM-12-3-ubuntu:~/unix_pro/pipe$ ls -l /tmp/pipe
prw-r--r-- 1 ubuntu ubuntu 0 Apr 19 11:07 /tmp/pipe
ubuntu@VM-12-3-ubuntu:~/unix_pro/pipe$ ls -l >/tmp/pipe 
ubuntu@VM-12-3-ubuntu:~/unix_pro/pipe$ ls -l /tmp/pipe
ls: cannot access '/tmp/pipe': No such file or directory
```


疑问：如果打开管道两次，但是只从fd1读，那么写入两次才能读到数据。
可以看到第二次才能读到的情况下是因为第一次写入之后阻塞在了第二次open调用上
```cpp
int read_fd, read_fd2, write_fd;
read_fd = open(FIFO_FILE, O_RDONLY);
if (read_fd == -1)
{
	perror("open error");
	exit(EXIT_FAILURE);
}
else
{
	printf("read_fd:%d \n", read_fd);
}
read_fd2 = open(FIFO_FILE, O_RDONLY);
if (read_fd2 == -1)
{
	perror("open error");
	exit(EXIT_FAILURE);
}
else
{
	printf("read_fd2:%d", read_fd2);
}
```

### API
#### 创建FIFO
库函数mkfifo(char * name, mode_t mode)使用指定的权限模式来创建FIFO。mkfifo 命令通常调用这个函数。
```cpp
#include <sys/types.h>
#include <sys/stat.h>

int mkfifo(const char *pathname, mode_t mode);

pathname:一个普通的Unix路径名，它是该FIFO的名字。
mode:指定文件权限位
```
mkfifo函数己隐含指定O_CREAT | O_EXCL.也就是说，它要么创建一个新的FIFO,要么返回一个EEXIST错误（如果所指定名字的FIFO己经存在）。
如果不希望创建一个新的FIFO, 那就改为调用open而不是mkfifo
mkfifo命令也能创建FIFO.可以从shell脚本或命令行中使用它。
在创建出一个FIFO后，它必须或者打开来读，或者打开来写，所用的可以是open函数，也可以是某个标准I/O打开函数，例如fopen。 FIFO不能打开来既读又写，因为它是半双工的。
对管道或FIFO的write总是往末尾添加数据，对它们的read则总是从开头返回数据。如果对管道或FIFO调用lseek,那就返冋ESPIPE错误。

#### 删除FIFO
管道在所有进程最终都关闭它之后自动消失。FIFO则只有通过调用unlink才从文件系统中删除
```cpp
int unlink(const char *pathname);
```
内核为管道和FIFO维护一个访问计数器，它的值是访问同一个管道或FIFO的打开着的描述符的个数.有了访问计数器后，客户或服务器就能成功地调用unlink.尽管该函数从文件系统中删除了所指定的路径名，先前已经打开该路径名、目前仍打开着的描述符却不受影响. 然而对于其他形式的IPC来说（例如System V消息队列），这样的计数器并不存在，因此要是服务器在向某个消息队列写入自己的最终消息后删除了该队列，那么当客户尝试读出这个最终消息时，该队列可能已消失了

#### 读取FIFO
```cpp
open(fifoname,O_RDONLY)
```
open函数阻塞进程直到某一进程打开FIFO进行写操作。

#### 向FIFO中写入数据
```cpp
open(fifoname,0_WRONLY)
```
此时open函数阻塞进程直到某一进程打开FIFO进行读操作。


## 管道和FIFO的额外属性
首先，一个描述符能以两种方式设置成非阻塞。
(1)调用open时可指定O_NONBLOCK标志。
(2)如果一个描述符已经打开，那么可以调用fcntl以后用O_NONBLOCK标志。对于管道来说，必须使用这种技术，因为管道没有open调用，在pipe调用中也无法指定O_NONBLOCK标志。 使用fcntl时，我们先使用F_GETFL命令取得当前文件状态标志，将它与O_NONBLOCK标志按位或后，再使用F_SETFL命令存储这些文件状态标志：
```cpp
int flags;
if ( (flags = fcntl(fd, F_GETFL, 0)) < 0)
	err_sys("F_GETFL error");
flags I= 0_NONBLOCK;
if (fcntl(fd, F_SETFL, flags) < 0)
	err_sys ("F_SETFI. error")；
```

下面是关于管道或FIFO的读出与写入的若干额外规则。
- 如果请求读出的数据量多于管道或FIFO中当前可用数据量，那么只返回这些可用的数据。我们必须准备好处理来自read的小于所请求数目的返回值。
- 如果请求写入的数据的字节数小于或等于PIPE_BUF （一个Posix限制值），那么write操作保证是原子的。这意味着，如果有两个进程差不多同时往同一个管道或FIFO写，那么或者先写入来自第一个进程的所有数据，再写入来自第二个进程的所有数据，或者颠倒过来。系统不会相互混杂来自这两个进程的数据。然而，如果请求写入的数据的字节数大于PIPE_BUF,那么write操作不能保证是原子的。
- O_NONBLOCK标志的设置对write操作的原子性没有影响——原子性完全是由所请求字节数是否小于等于PIPE_BUF决定的。当一个管道或FIFO设置成非阻塞时，来自write的返回值取决于待写的字节数以及该管道或FIFO中当前可用空间的大小。如果待写的字节数小于等于PIPE_BUF:
	a.如果该管道或FIFO中有足以存放所请求字节数的空间，那么所有数据字节都写入。
	b.如果该管道或FIFO中没有足以存放所请求字节数的空间，那么立即返回一个EAGAIN 错误。既然设置了O_NONBLOCK标志，调用进程就不希望自己被投入睡眠中。但是内核无法在接受部分数据的同时仍保证write操作的原子性，于是它必须返冋一个错误，告诉调用进程以后再试。
如果待写的字节数大于PIPE_BUF:
	a.如果该管道或FIFO中至少有1字节空间，那么内核写入该管道或FIFO能容纳数目的数据字节，该数目同时作为来自write的返回值。
	b.如果该管道或FIFO己满，那么立即返回EAGAIN错误。
- 如果向一个没有为读打开着的管道或FIFO写入，那么内核将产生一个SIGPIPE信号：
	a.如果调用进程既没有捕获也没有忽略该SIGPIPE信号，所采取的默认行为就是终止该进程。
	b.如果调用进程忽略了该SIGPIPE信号，或者捕获了该信号并从其信号处理程序中返回，那么write返回一个EPIZPE错误。

	SIGPIPE被认为是一个同步信号，也就是说，这是一个由待定的线程（调用write的线程） 引起的信号.然而处理这个信号最容易的办法是忽略它（把它的处理办法设置成SIG-IGN）, 让write返回一个EPIPE错误.应用程序应该无遗漏地检测由write返回的错误，而检测某个进程被SIGPIPE终止却困难得多.如果该信号未被捕获，我们就得从shell中查看被终止进程的终止状态，以确定该进程是否被某个信号所杀死以及具体是被哪个信号杀死的.

- 如果当前打开操作是为写而打开FIFO时，如果已经有相应进程为读而打开该FIFO，则当前打开操作将成功返回；否则，可能阻塞直到有相应进程为读而打开该FIFO（当前打开操作设置了阻塞标志）；或者，返回ENXIO错误（当前打开操作没有设置阻塞标志）。

- 如果指向管道读端的所有文件描述符都被关闭了,read调用就会返回0
小技巧:可以额外多打开一个写入的文件描述符，那么哪怕客户端写完结束了程序，服务端也不会因为read调用返回0而退出。（这里如果放宽while条件让read返回0依然不退出while循环的话，会发现read调用不再阻塞，而是一直返回0）
```cpp
read_fd = open(FIFO_FILE, O_RDONLY);
write_fd = open(FIFO_FILE, O_WRONLY);
if (read_fd == -1 || write_fd == -1)
{
	perror("open error");
	exit(EXIT_FAILURE);
}
```

2.FIFO类型的IPC小结
访问：FIFO使用与通常文件相同的文件访问。服务器有写权限，而客户端只限于读权限。
多个客户端：命名管道是一个队列而不是常规文件。写者将字节写入队列，而读者从队列头部移出字节。每个客户端都会将时间/日期的数据移出队列，因此服务器必须重写数据。
竞态条件：FIFO版本的时间/日期服务器程序完全不存在竞态条件问题。在信息的长度不超过管道的容量的情况下,read和write系统调用只是原子操作。读取操作将管道清空而写入操作又将管道塞满。在读者和写者连通之前，系统内核将进程挂起。因此锁机制在这里并不需要。


## 管道和FIFO限制
系统加于管道和FIFO的唯一限制为：
OPEN_MAX 一个进程在任意时刻打开的最大描述符数
PIPE_BUF 可原子地写往一个管道或FIFO的最大数据量
```sh
ubuntu@VM-12-3-ubuntu:~$ getconf OPEN_MAX
1024
ubuntu@VM-12-3-ubuntu:~$ getconf PIPE_BUF /
4096
```

