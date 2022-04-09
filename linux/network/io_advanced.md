## pipe 创建管道，实现进程间通信
```cpp
#include <unistd.h>
int pipe(int pipefd[2]);
```

pipe函数的参数是一个包含两个int型整数的数组指针。该函数成功时返冋0,并将一对打开的文件描述符值填入其参数指向的数组。如果失败，则返回-1并设置errno.
通过pipe函数创建的这两个文件描述符 fd[0] 和 fd[1] 分别构成管道的两端，往 fd[1] 写入的数据可以从fd［O］读出。
并且，fd［O］只能用于从管道读出数据，fd［1］则只能用于往管道写入数据，而不能反过来使用。如果要实现双向的数据传输，就应该使用两个管道。
默认情况下，这一对文件描述符都是阻塞的。此时如果我们用read系统调用来读取一个空的管道， 则read将被阻塞，直到管道内有数据可读；如果用write系统调用来往一个满的管道中写入数据，则write亦将被阻塞，直到管道有足够多的空闲空间可用。
但如果应用程序将fd［O］和fd［1］都设置为非阻塞的，则read和write会有不同的行为。
如果管道的写端文件描述符fd［1］的引用计数减少至0, 即没有任何进程需要往管道中写入数据，则针对该管道的读端文件描述符fd［O］的read操作将返冋0,即读取到了文件结束标记（End Of File, EOF）；反之，如果管道的读端文件描述 符fd［O］的引用计数减少至0,即没有任何进程需要从管道读取数据，则针对该管道的写端文件描述符fd[1]的write操作将失败，并引发SIGPIPE信号。
管道内部传输的数据是字节流，这和TCP字节流的概念相同。但二者又有细微的区别。 应用层程序能往一个TCP连接中写入多少字节的数据，取决于对方的接收通告窗口的大小和本端的拥塞窗口的大小。而管道本身拥冇一个容量限制，它規定如果应用程序不将数据从管道读走的话，该管道最多能被写入多少字节的数据。自Linux 2.6.11内核起，管道容量的大小默认是65536字节。我们可以使用fcntl函数来修改管道容量。

此外，socket的基础API中冇一个socketpair函数。它能够方便地创建双向管道。其定义如下：
```cpp
#include <sys/types.h>          
#include <sys/socket.h>
int socketpair(int domain, int type, int protocol, int sv[2]);
```

socketpair前三个参数的含义与socket系统週用的三个参数完全相同，但domain只能使 用UNIX本地域协议族AF_UNIX,因为我们仅能在本地使用这个双向管道。最后一个参数则和pipe系统调用的参数一样，只不过socketpair创建的这对文件描述符都是既可读又可写的。socketpair成功时返回0,失败时返回-1并设置errno

## dup函数和dup2函数
有时我们希望把标准输入重定向到一个文件，或者把标准输出重定向到一个网络连接 (比如CGI编程)。这可以通过下面的用于复制文件描述符的dup或dup2函数来实现：
```cpp
#include <unistd.h>
int dup(int oldfd);
int dup2(int oldfd, int newfd);
```
dup函数创建一个新的文件描述符，该新文件描述符和原有文件描述符file_descriptor指向相同的文件、管道或者网络连接。并且dup返回的文件描述符总是取系统当前可用的最小整数值。dup2和dup类似，不过它将返回第一个不小于file_descriptor_two的整数值。dup和 dup2系统调用失败时返回-1并设置errno
注意 通过dup和dup2创建的文件描述符井不继承原文件描述符的属性，比如 non-biocking 等。

## sendfile 函数
sendfile函数在两个文件描述符之间直接传递数据（完全在内核中操作），从而避免内核缓冲区和用户緩冲区之间的数据拷贝，效率很高，这被称为零拷贝
专门为在网络上传输文件而设计的
```cpp
 #include <sys/sendfile.h>
ssize_t sendfile(int out_fd, int in_fd, off_t *offset, size_t count);

in_fd 	待读出内容的文件描述符,必须是一个支持类似mmap函数的文件描述符，即它必须指向真实的文件，不能是socket和管道
out_fd	待写入内容的文件描述符,必须是一个socket
offset 	指定从读入文件流的哪个位置开始读，如果为空，则使用读入文件流默认的起始位置。 
count	指定在文件描述符in_fd和out_fd之间传输的字节数。

成功时返冋传输的字节数，失败则返冋-1并设置errno。
```

## mmap函数和munmap函数
mmap函数用于申请一段内存空间。我们可以将这段内存作为进程间通信的共享内存, 也可以将文件直接映射到其中。munmap函数则释放由mmap创建的这段内存空间
```cpp

#include <sys/mman.h>

void *mmap(void *addr, size_t length, int prot, int flags,
		  int fd, off_t offset);
int munmap(void *addr, size_t length);

addr	 建议的内存起始地址,一般设为null,系统自动分配一个地址
length 	指定内存段的长度
prot	 设置内存段的访问权限,可以取以下几个值的按位或
	PROT_EXEC     内存段可执行
	PROT_READ     内存段可读
	PROT_WRITE    内存段可写
	PROT_NONE     内存段不能被访问

flags 控制内存段内容被修改后程序的行为,按位或(其中MAP_SHARED和MAP_PRIVATE是互斥的，不能同时指定）)
	MAP_PRIVATE：对映射区域的写入操作会产生一个映射的复制(copy-on-write)，任何内存中的改动并不反映到文件之中。也不反映到其他映射了这个文件的进程之中。
	MAP_SHARED：和其他进程共享这个文件。往内存中写入相当于往文件中写入。会影响映射了这个文件的其他进程。

offset 设置从文件的何处开始映射

成功执行时，mmap()返回被映射区的指针。失败时，mmap()返回MAP_FAILED[其值为(void *)-1]， 并设置error
```
mmap是一种内存映射文件的方法，即将一个文件映射到进程的地址空间，实现文件磁盘地址和进程虚拟地址空间中一段虚拟地址的一一对映关系。实现这样的映射关系后，进程就可以采用指针的方式读写操作这一段内存，而系统会自动回写脏页面到对应的文件磁盘上，即完成了对文件的操作而不必再调用read,write等系统调用函数。

mmap和常规文件操作的区别

常规文件操作需要从磁盘到内核空间再到用户空间的两次数据拷贝。而mmap操控文件，只需要从磁盘到用户空间的一次数据拷贝过程。

```cpp
//刷新内存到文件中
int msync(void *addr, size_t length, int flags);

flags：
MS_ASYNC 异步，立即返回
MS_SYNC  同步，结束后返回
MS_INVALIDATE   使其他进程对该文件的映射失效 (so that  they can be updated with the fresh values just written).
```


## splice 用于在两个文件描述符之间移动数据，也是零拷贝操作
```cpp
#include <fcntl.h>
ssize_t splice(int fd_in, loff_t *off_in, int fd_out, loff_t *off_out, size_t len, unsigned int flags);

fd_in	待输入数据的文件描述符。
off_in 	从输入数据流的何处开始读取数据。若被设置为NULL,则表示从输入数据流的当前偏移位置读入
如果fd_in是一个管道文件描述符，那么off_in 参数必须被设置为NULL
fd_out/off_out的含义与fd_in/off_in相同，不过用于输出数据流。
len		指定移动数据的长度； 
flags	控制数据如何移动，它可以被设置为以下某些值的按位或。

	SPLICE_F MOVE	如果合适的话，按整页内存移动数据。这只是给内核的一个提示。不过因为它的实现存在BUG,所以自内核2.6.21后.它实际上没有任何效果
	SPLICE_F NONBLOCK	非阻塞的splice操作.但实际效果还会受文件描述符本身的阻塞状态的影响
	SPLICE_F MORE	给内核的一个提示：后续的splice调用将读取更多数据	
	SPLICE_F GIFT	对splice没有效果

使用splice函数时，fd_in和fd_out必须至少冇一个是管道文件描述符。
splice函数调用成功时返冋移动字节的数量。它可能返回0,表示没有数据需要移动，这发生在从管道中读取数据而该管道没有被写入任何数据时。
splice函数失败时返回-1并设置errno 常见的errno
	EBADF	参数所指文件描述符有错
	EINVAL	目标文件系统不支持splice,或者目标文件以追加方式打开.或者两个文件描述符都不是管道文件描述符，或者某个ffset參数被用于不支持随机访问的设备（比如字符设备）
	ENOMEM	内存不够
	ESP1PE	参数fd_in（或fd_out〉是管道文件描述符，而off_in（或off_out）不为NULL
```
