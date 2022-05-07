## 劝告性上锁
```cpp
#include <unistd.h>
#include <fcntl.h>

int fcntl(int fd, int cmd, ... /* arg */ );

struct flock {
   ...
   short l_type;    /* Type of lock: F_RDLCK,
					   F_WRLCK, F_UNLCK */
   short l_whence;  /* How to interpret l_start:
					   SEEK_SET, SEEK_CUR, SEEK_END */
   off_t l_start;   /* Starting offset for lock */
   off_t l_len;     /* Number of bytes to lock */
   pid_t l_pid;     /* PID of process blocking our lock
					   (set by F_GETLK and F_OFD_GETLK) */
   ...
};

l_len: 为0的话表示从指定位置到文件结尾
```
如下三个命令要求第三个参数arg是指向某个flock结构的指针


F_SETLK 	获取（l_type成员为F_RDLCK或F_WRLCK）或释放（l_type成员为F_UNLCK） 由指向的flock结构所描述的锁。 如果无法将该锁授予调用进程，该函数就立即返回一个EACCES或EAGAIN错误而不阻塞。

F_SETLKW	该命令与上一个命令类似，不过如果无法将所请求的锁授予调用进程，调用线程将阻塞到该锁能够授予为止。（该命令的名字中最后一个字母W意思是“wait”）

F_GETLK		检査由arg指向的锁以确定是否有某个已存在的锁会妨碍将新锁授予调用进程。如果当前没有这样的锁存在，由arg指向的flock结构的l_type成员就被置为F_UNLCK。否则，关于这个已存在锁的信息将在由arg指向的flock结构中返回（也就是说，该结构的内容由fcntl函数覆写），其中包括持有该锁的进程的进程ID。

对于一个打开着某个文件的给定进程来说，当它关闭该文件的所有描述符或它本身终止时，与该文件关联的所有锁都被删除。锁不能通过fork由子进程继承。
确实如此，甚至于所关闭的描述符先前是在其文件己由本进程（通过该文件的另一个描述符）上锁后才打开也不例外.看来删除锁时关键的是进程ID,而不是引用同一文件的描述符數日及打开目的（只读、只写、读写）. 既然锁跟进程ID紧密关联，它不能通过fork由子进程继承也就顺理成章，因为父子进程有不同的进程ID・
