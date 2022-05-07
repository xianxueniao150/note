以下三种类型的IPC合称为“Posix IPC”：
- Posix消息队列
- Posix信号量
- Posix共享内存区

## 创建与打开IPC通道
mq_open、sem_open和shm_open这三个创建或打开一个IPC对象的函数
它们的名为oflag 的第二个参数指定怎样打开所请求的对象。这与标准open函数的第二个参数类似
首先指定怎样打开对象：只读、只写或读写。消息队列能以其中任何一种模式打开，信号量（任意信号暈操作，都需要读写访问权），共享内存区对象则不能以只写模式打开。

### O_CREAT
若不存在则创建。
创建一个新的消息队列、信号量或共享内存区对象时，至少需要另外一个称为mode的参数。该参数指定权限位，它是由所示常值按位或形成的。
- S_IRUSR	用户（属主）读
- S_IWUSR	用户（属主）写
- S_IRGRP	（属）组成员读
- S_IWGRP	（属）组成员写
- S_IROTH	其他用户读
- S_IWOTH	箕他用户写

这些常值定义在＜sys/stat.h＞头文件中。所指定的权限位受当前进程的文件模式创建掩码（file mode creation mask）修正，而该掩码可通过调用umask 函数或使用shell的umask命令来设置。

### O_EXCL
如果该标志和O_CREAT 一起指定，那么IPC函数只在所指定名字的消息队列、 信号量或共享内存区对象不存在时才创建新的对象。如果该对象已经存在， 而且指定了O_CREAT | O_EXCL,那么返回一个EEXIST错误。
考虑到其他进程的存在，检査所指定名字的消息队列、信号量或共享内存区对象的存在与否和创建它（如果它不存在）这两步必须是原子的（atomic）。 

## unlink
删除文件系统中一个路径名的unlink,删除一个Posix消息队列的mq_unlink,删除一个Posix有名信号量的sem_unlink, 删除一个共享内存区对象的shm_unlink.
删除一个名字不会影响对于其底层支撑对象的现有引用，直到对于该对象的引用全部关闭为止。删除一个名字仅仅防止后续的open、mq_open或sem_open调用取得成功。

有一个小技巧就是需要调用unlink的程序可以把调用提前，比如说之前在程序最后清理阶段调用，可以提前到open调用之后，这样既不会立即删除该对象，
又可以防止程序异常退出导致unlink没有被调用