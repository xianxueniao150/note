# 内核缓冲技术
应用缓冲技术对提高系统的效率是很明显的，它的主要思想是一次读入大量的数据放入缓冲区，需要的时候从缓冲区取得数据。

为了提高效率，内核也使用缓冲技术来提高对磁盘的访问速度

当一个用户空间中的进程要从磁盘上读数据时，内核一般不直接读磁盘，而是将内核缓冲区中的数据复制到进程中。
当进程所要求的数据块不在内核缓冲区时，内核会把相应的数据块加入到请求数据列表中，然后把该进程挂起，接着为其他进程服务。
一段时间之后（很短），内核把相应的数据块从磁盘读到内核缓冲区，然后再把数据复制到进程中，最后唤醒被挂起的进程。

理解内核缓冲技术的原理有助于更好地掌握系统调用read和write, read把数据从内核缓冲区复制到进程中，write把数据从进程中复制到内核缓冲区，它们并不等价于数据在内核缓冲和磁盘之间的交换。
从理论上讲，内核可以在任何时候写磁盘，但并不是所有的write操作都会导致内核的写动作。内核会把要写的数据暂时存在缓冲区中，积累到一定数量后再一次写入。有时会导致意外情况，比如突然断电，内核还来不及把内核缓冲区中的数据写到磁盘上，这些更新的数据就会丢失。

## 磁盘文件属性
```sh
O_CREAT 如果不存在，创建该文件。
O_TRUNC 如果文件存在，将文件长度置为0。
```

### O_SYNC
位逻辑或操作 打开位O_SYNC 该位告诉内核，对write的调用仅能在数据写入实际的硬件时才能返回，而不是在数据复制到内核缓冲时就执行默认的返回操作。
设置O_SYNC会关闭内核的缓冲机制，如果没有很充分的理由，最好不要关闭缓冲。

### O_APPEND
自动添加模式对于若干个进程在同一时间写入文件是很有用的。

向日志文件中添加内容分为两个步骤:1.lseek定位到文件结尾 2.write写入日志
如果两个进程同时写入，可能会发生覆盖情况.
如何避免这种竞争？有很多方法避免竞争。在这个特定的情况中，内核提供一个简单的解决办法：自动添加模式。当文件描述符的O_APPEND位被开启后，每个对write的调用自动调用lseek将内容添加到文件的末尾。
```cpp
# include <fcntl. h>
int s ；	//settings
s = fcntl ( fd, F_GETFL)；	//get flags
s | = O_APPEND；	//set APPEND bit
result = fcntl ( fd, F_SETFL, s)；	//set flags
if ( result == - 1)	//if error
	perror ( "setting APPEND")；	// report
else	
	write (fd, &rec, 1)；	//write record at end
```
术语竞争和原子操作(atomoc operation)密切相关。对lseek和write的调用是独立的系统调用，内核可以随时打断进程，从而使后面这两个操作被中断。当O_APPEND被置位， 内核将lseek和write组合成一个原子操作，被连接成一个不可分割的单元。�

### O_EXCL
防止两个进程创建同样的文件。如果文件存在且O_EXCL被置位，则返回-1。
O_CREAT和O_EXCL的组合用来消除以下竞争情况
例如,如果两个进程都要写wtmp,但是这个文件不存在时，都要创建该文件，此时会发生什么情况？程序能够先调用stat查看文件是否存在，如果不存在，就调用 creat。当stat和creat间的过程被打断时，问题就出现了。O_EXCL/O_CREAT的组合将这两个调用构成了一个原子操作。虽然想法很好，但是这种方法在某些重要场合并不可行。一个可靠的替代方案是使用link。本章的练习提供了一个例子。


## read
```cpp
//返回值：成功返回读取的字节数，出错返回-1并设置errno
ssize_t read(int fd, void *buf, size_t count);  
```

从终端设备读，通常以行为单位，读到换行符就返回了。

读常规文件是不会阻塞的，不管读多少字节，read一定会在有限的时间内返回。从终端设备或网络读则不一定，
如果从终端输入的数据没有换行符，调用read读终端设备就会阻塞，如果网络上没有接收到数据包，调用read从网络读就会阻塞。
同样，写常规文件是不会阻塞的，而向终端设备或网络写则不一定。


如果在open一个设备时指定了O_NONBLOCK标志，read/write就不会阻塞。
以read为例，如果设备暂时没有数据可读就返回-1，同时置errno为EWOULDBLOCK（或者EAGAIN，这两个宏定义的值相同），表示本来应该阻塞在这里（would block，虚拟语气），事实上并没有阻塞而是直接返回错误，调用者应该试着再读一次（again）。这种行为方式称为轮询（Poll），调用者只是查询一下，而不是阻塞在这里死等，这样可以同时监视多个设备：


非阻塞I/O有一个缺点，如果所有设备都一直没有数据到达，调用者需要反复查询做无用功，如果阻塞在那里，操作系统可以调度别的进程执行，就不会做无用功了。在使用非阻塞I/O时，通常不会在一个while循环中一直不停地查询（这称为Tight Loop），而是每延迟等待一会儿来查询一下，以免做太多无用功，在延迟等待的时候可以调度其它进程执行。
```cpp
while(1) {
   非阻塞read(设备1);
   if(设备1有数据到达)    处理数据;
   非阻塞read(设备2);
   if(设备2有数据到达)    处理数据;
   ...   sleep(n);
  }
```
这样做的问题是，设备1有数据到达时可能不能及时处理，最长需延迟n秒才能处理，而且反复查询还是做了很多无用功。以后要学习的select(2)函数可以阻塞地同时监视多个设备，还可以设定阻塞等待的超时时间，从而圆满地解决了这个问题。

## write
```cpp
#include <unistd.h>
ssize_t write(int fd, const void *buf, size_t count);
```
如果内核不能写入或写入失败,write返回-1,如果写入成功，则返回写入的字节数
为什么实际写入的字节数会少于所要求的呢？有两个原因，第一个是有的系统对文件的最大尺寸有限制，第二个是磁盘空间接近满了。
在上述两种情况下，内核都会尽量把数据往文件中写，并将实际写入的字节数返回，所以调用write后都必须检查返回值是否与要写入的相同，如果不同，就要采取相应的措施。

## lseek
改变已打开文件的当前位置
```cpp
#include <sys/types.h>
#include <unistd.h>
off_t lseek(int fd, off_t offset, int whence);

新的位置由offset和whence来指定，whence是基准位置，offset是从基准位置开始的偏移量。
基准位置可以是文件的开始(SEEK_SET)、当前位置(SEEK_CUR)或文件的结尾(SEEK_END)
注意偏移量可以是负的

最后要说明的是，lseek(fd, 0, SEEK_CUR)返回指针所指向的当前位置

```
Unix每次打开一个文件都会保存一个指针来记录文件的当前位置
当从文件读数据(read)时，内核从指针所标明的地方开始，读取指定的字节，然后移动位置指针，指向下一个未被读取的字节，写文件(write)的操作也是类似的。
指针是与文件描述符相关联的，而不是与文件关联，所以如果两个程序同时打开一个文件，这时会有两个指针，两个程序对文件的读操作不会互相干扰。



## creat 创建普通文件
```cpp
#include <fcntl.h>
int creat(const char *pathname, mode_t mode);

mode 指定了要创建文件的许可位,如0744（0代表八进制）
```
creat告诉内核创建一个名为filename的文件，如果这个文件不存在，就创建它，如果已经存在，就把它的内容清空，把文件的长度设为0。

这个参数只是请求，而不是命令。内核会通过“新建文件掩码"(file-creation-mask) 来得到文件的最终模式。“新建文件掩码”是一个很有用的系统变量，它指定哪些位需要被关掉。例如要防止程序创建能被同组用户和其他用户修改的文件，那么可以通过关掉 ----w-—w-来实现。这可以通过把“新建文件掩码”的值设为八进制数022来实现。 例如：
umask( 022 )；
这里的umask是一个系统命令，可以改变变量umask的的值。

简单的说，文件所有者就是创建文件的用户，用户通过creat建立文件时，内核把文件所有者设为运行程序的用户，如果程序具有set-user-ID位，那么新文件的文件所有者就是程序的文件所有者。

## chmod 更改文件模式
```cpp
#include <sys/stat.h>
int chmod(const char *pathname, mode_t mode);
```
系统调用chmod不受“新建文件掩码”的影响。

## glob 目录解析
```cpp
int glob(const char *pattern, int flags,
                int (*errfunc) (const char *epath, int eerrno),
                glob_t *pglob);
void globfree(glob_t *pglob);

typedef struct {
               size_t   gl_pathc;    /* Count of paths matched so far  */
               char   **gl_pathv;    /* List of matched pathnames.  */
               size_t   gl_offs;     /* Slots to reserve in gl_pathv.  */
           } glob_t;
```


```cpp
#include <stdio.h>
#include <stdlib.h>
#include <glob.h>

#define PAT "/etc/a*.conf"

int main(){

    glob_t globres;
    glob(PAT,0,NULL,&globres);
    //打印出指定pattern的文件
    for(int i=0;i<globres.gl_pathc;i++)
    {
        puts(globres.gl_pathv[i]);
    }
    
    globfree(&globres);

    exit(0);
}
```

## fcntl 函数
fcntl函数，正如其名字（file control）描述的那样，提供了对文件描述符的各种控制操作。
另外一个常见的控制文件描述符属性和行为的系统调用是ioctl,而且ioctl比fcntl能够执行更多的控制。但是，对于控制文件描述符常用的属性和行为，fcntl函数是由POSIX规范指定的首选方法。
```cpp
#include <unistd.h>
#include <fcntl.h>
int fcntl(int fd, int cmd, ... /* arg */ );

fd参数是被操作的文件描述符，cmd参数指定执行何种类型的操作。根据操作类型的不同，该函数可能还需要第三个可选参数arg。
```

修改文件设置的三个步骤
```javascript
# include <fcntl. h>
int s；	//settings
s = fcntl (fd, F_GETFL)；	//1.获取设置
s | = O_SYNC；		//2.修改设置
result = fcntl (fd, F_SETFL, s)；	//3.存储设置
if ( result = = 1)	//if error
	perror ("setting SYNC")；	//report
```


