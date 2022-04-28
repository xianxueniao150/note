
## dup函数和dup2函数
有时我们希望把标准输入重定向到一个文件，或者把标准输出重定向到一个网络连接 (比如CGI编程)。这可以通过下面的用于复制文件描述符的dup或dup2函数来实现：
```cpp
#include <unistd.h>
int dup(int oldfd);
int dup2(int oldfd, int newfd);

//失败时返回-1并设置errno
```
系统调用dup和dup2能够复制文件描述符。dup返回新的文件文件描述符（系统当前可用的文件描述符最小的编号）。
dup2可以让用户指定返回的文件描述符的值。如果dup2指定的newfd已经被使用了，则内核首先会关闭newfd指向的文件,如果newfd还没被使用过，则什么都不会做.
(这里是不是可以理解成因为newfd去关联oldfd指向的文件了，所以和之前自己指向的文件就自动取消关联了)

新老描述符共享文件的偏移量（位置）、标志和锁，但是不共享close-on-exec标志。
注意 通过dup和dup2创建的文件描述符井不继承原文件描述符的属性，比如 non-biocking 等。

一般复制之后就会关闭oldfd

例 “从标准输出到文件的重定向”，
```cpp
#define TESTSTR "Hello dup2\n"
int main() {
	int     fd3;

	fd3 = open("testdup2.dat", 0666);
	if (fd < 0) {
			printf("open error\n");
			exit(-1);
	}

	// 经过dup2后进程A的任何目标为STDOUT_FILENO的I/O操作如printf等，其数据都将流入fd3所对应的文件中。
	if (dup2(fd3, STDOUT_FILENO) < 0) {       
			printf("err in dup2\n");
	}
	printf(TESTSTR);
	return 0;
}
```

### 重定向后恢复
如何在重定向后再恢复原来的状态？首先大家都能想到要保存重定向前的文件描述符。那么如何来保存呢，象下面这样行么？
int s_fd = STDOUT_FILENO;
int n_fd = dup2(fd3, STDOUT_FILENO);
还是这样可以呢？
int s_fd = dup(STDOUT_FILENO);
int n_fd = dup2(fd3, STDOUT_FILENO);
这两种方法的区别到底在哪呢？答案是第二种方案才是正确的，分析如下：按照第一种方法，我们仅仅在"表面上"保存了
而 第二种方法我们首先做一下复制，复制后的状态如下图所示:
进程A的文件描述符表(after dup)
   ------------
fd0 0   | p0
   ------------
fd1 1   | p1 -------------> 文件表1 ---------> vnode1
   ------------                 /|
fd2 2   | p2                /
   ------------             /
fd3 3   | p3 -------------> 文件表2 ---------> vnode2
   ------------          /
s_fd 4   | p4 ------/
   ------------
... ...
... ...
   ------------

调用dup2后状态为：
进程A的文件描述符表(after dup2)
   ------------
fd0 0   | p0
   ------------
n_fd 1   | p1 ------------
   ------------               \
fd2 2   | p2                 \
   ------------                _\|
fd3 3   | p3 -------------> 文件表2 ---------> vnode2
   ------------
s_fd 4   | p4 ------------->文件表1 ---------> vnode1
   ------------
... ...
... ...
   ------------

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
