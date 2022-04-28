mmap函数用于申请一段内存空间。我们可以将这段内存作为进程间通信的共享内存, 也可以将文件直接映射到其中。munmap函数则释放由mmap创建的这段内存空间
mmap是一种内存映射文件的方法，即将一个文件映射到进程的地址空间，实现文件磁盘地址和进程虚拟地址空间中一段虚拟地址的一一对映关系。实现这样的映射关系后，进程就可以采用指针的方式读写操作这一段内存，而系统会自动回写脏页面到对应的文件磁盘上，即完成了对文件的操作而不必再调用read,write等系统调用函数。

mmap和常规文件操作的区别: 常规文件操作需要从磁盘到内核空间再到用户空间的两次数据拷贝。而mmap操控文件，只需要从磁盘到用户空间的一次数据拷贝过程。

#### 映射和解除映射
```cpp
#include <sys/mman.h>
void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
int munmap(void *addr, size_t length);

addr:	 建议的内存起始地址,一般设为null,系统自动分配一个地址
length: 	指定内存段的长度
prot:	 设置内存段的访问权限,可以取以下几个值的按位或
	PROT_READ     内存段可读
	PROT_WRITE    内存段可写
	PROT_EXEC     内存段可执行
	PROT_NONE     内存段不能被访问

flags: 控制内存段内容被修改后程序的行为,按位或(其中MAP_SHARED和MAP_PRIVATE是互斥的，不能同时指定）)
	MAP_PRIVATE：对映射区域的写入操作会产生一个映射的复制(copy-on-write)，任何内存中的改动并不反映到文件之中。也不反映到其他映射了这个文件的进程之中。
	MAP_SHARED：往内存中写入会改变对应的文件,对于映射了这个文件的其他进程也是可见的。
  linux
  	MAP_ANONYMOUS: 匿名映射,不需要和文件绑定，fd指定为1

offset: 设置从文件的何处开始映射

成功执行时，mmap()返回被映射区的指针。失败时，mmap()返回MAP_FAILED[其值为(void *)-1]， 并设置error
```
mmap成功返回后，fd可以关闭。该操作对于由mmap建立的映射关系没有影响。
为从某个进程的地址空间删除一个映射关系，我们调用munmap ,之后再次访问这些地址将导致向调用进程产生一个SIGSEGV信号
如果被映射区是使用MAP_PRIVATE标志映射的，那么调用进程对它所作的变动都会被丢弃掉。

#### 刷新
```cpp
//刷新内存到文件中
int msync(void *addr, size_t length, int flags);

flags:
	MS_ASYNC 异步，立即返回
	MS_SYNC  同步，结束后返回
	MS_INVALIDATE   使其他进程对该文件的映射失效 (so that  they can be updated with the fresh values just written).
```

### 父子进程共享内存
默认情况下通过fork派生的子进程并不与其父进程共享内存区
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int *a = NULL;

int main()
{

    int fork_rv, i;

    a = malloc(sizeof(int));
    *a = 1;

    fork_rv = fork();
    if (fork_rv < 0)
    {
        perror("fork error");
        exit(1);
    }
    if (fork_rv == 0) // child
    {
        for (i = 0; i < 3; i++)
        {
            printf("child: %d\n", (*a)++);
        }
    }
    else // parent
    {
        sleep(1);
        printf("a: %d\n", *a);
    }
}
```

```sh
ubuntu@VM-12-3-ubuntu:~/unix_pro$ ./a.out 
child: 1
child: 2
child: 3
a: 1
```
可以看出这两个进程都有各自的全局变量a的副本。

#### 使用mmap
这里unix网络2 分别给出了基于文件和基于内存的信号量的示例代码，前者较简单，如下为描述。后者第一次见，所以记录了下来。
首先创建一个文件，向这个文件中写入整数0，然后将这个文件做映射。fork后，父子进程都各自有属于自己的指针ptr的副本，但是每个副本都指向共享内存区中的同一个整数：这两个进程都对它执行加1操作的计数器。

fork对内存映射文件进行特殊处理，也就是父进程在调用fork之前创建的内存映射关系由子进程共享。因此，我们在打开文件后以MAP_SHARED标志调用nmap的操作实际上提供了一个由父子进程共享的内存区。



```cpp
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <semaphore.h>

#define PATHNAME "/tmp/shared"

struct shared
{
    sem_t mutex; /* the mutex: a Posix memory-based semaphore */
    int count;   /* and the counter */
} shared;

int main(int argc, char **argv)
{
    int fd, i, nloop;
    struct shared *ptr;
    nloop = 3;

    /* 4open file, initialize to 0, map into memory */
    fd = open(PATHNAME, O_RDWR | O_CREAT, 0644);
    if (fd < 0)
    {
        perror("open");
    }
    write(fd, &shared, sizeof(struct shared));
    ptr = mmap(NULL, sizeof(struct shared), PROT_READ | PROT_WRITE,
               MAP_SHARED, fd, 0);
	//这里已经引用了fd，所以不会立即删除，写在这里的话，即使程序异常退出，文件也会被删除
    close(fd);

    /* 4initialize semaphore that is shared between processes */
    sem_init(&ptr->mutex, 1, 1);

    setbuf(stdout, NULL); /* stdout is unbuffered */
    if (fork() == 0)
    { /* child */
        for (i = 0; i < nloop; i++)
        {
            sem_wait(&ptr->mutex);
            printf("child: %d\n", ptr->count++);
            sem_post(&ptr->mutex);
        }
        exit(0);
    }

    /* 4parent */
    for (i = 0; i < nloop; i++)
    {
        sem_wait(&ptr->mutex);
        printf("parent: %d\n", ptr->count++);
        sem_post(&ptr->mutex);
    }
    exit(0);
}
```
```sh
ubuntu@VM-12-3-ubuntu:~/unix_pro$ gcc incr3.c -pthread && ./a.out 
parent: 0
parent: 1
parent: 2
child: 3
child: 4
child: 5
```
