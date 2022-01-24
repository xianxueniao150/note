namespace的本质就是把原来所有进程全局共享的资源拆分成了很多个一组一组进程共享的资源

```sh
man namespaces
```

## Linux内核支持的namespaces

```sh
名称        宏定义             隔离内容
Cgroup      CLONE_NEWCGROUP   Cgroup root directory (since Linux 4.6)
IPC         CLONE_NEWIPC      System V IPC, POSIX message queues (since Linux 2.6.19)
Network     CLONE_NEWNET      Network devices, stacks, ports, etc. (since Linux 2.6.24)
Mount       CLONE_NEWNS       Mount points (since Linux 2.4.19)
PID         CLONE_NEWPID      Process IDs (since Linux 2.6.24)
User        CLONE_NEWUSER     User and group IDs (started in Linux 2.6.23 and completed in Linux 3.8)
UTS         CLONE_NEWUTS      Hostname and NIS domain name (since Linux 2.6.19)
```


每一个进程创建出来时都自动关联了7个namespace，对于每一个类型的namespace，当加入新的后，都自动从旧的中退出

```sh
[root@VM-12-3-centos ~]# ls -l /proc/self/ns/
总用量 0
lrwxrwxrwx 1 root root 0 10月 23 11:06 ipc -> ipc:[4026531839]
lrwxrwxrwx 1 root root 0 10月 23 11:06 mnt -> mnt:[4026531840]
lrwxrwxrwx 1 root root 0 10月 23 11:06 net -> net:[4026531956]
lrwxrwxrwx 1 root root 0 10月 23 11:06 pid -> pid:[4026531836]
lrwxrwxrwx 1 root root 0 10月 23 11:06 user -> user:[4026531837]
lrwxrwxrwx 1 root root 0 10月 23 11:06 uts -> uts:[4026531838]
```


## 跟namespace相关的API
### Using clone() to create processes with new namespaces
clone： 创建一个新的进程，flags如果指定了某些类型的namespace，那么这个进程会继承父进程中除了前面指定的以外的所有namespaces，对于这些指定的namespace，会每种都创建一个新的出来，并把新创建的进程加入进去

```sh
int clone(int (*fn)(void *), void *child_stack,
                 int flags, void *arg, ...
                 /* pid_t *ptid, void *newtls, pid_t *ctid */ );
```

When the fn(arg) function returns, the child process terminates
The child_stack argument specifies the location of the stack used by the child process. Stacks  grow  downward
, so child_stack usually points to the topmost address of the memory space set up for the child stack.


### setns： 将当前进程加入到已有的namespace中
```sh
int setns(int fd, int nstype);
```

Given a file descriptor referring to a namespace, reassociate the calling thread with that namespace.
The  fd  argument  is  a  file  descriptor referring to one of the namespace entries in a /proc/[pid]/ns/ directory;
比如：/proc/50661/ns/uts

nstype表示限定只能加入某种特定类型的namespace，为0的话表示不限制

### unshare: 使当前进程退出指定类型的的namespace，然后创建这些指定类型的的namespace并加入
效果：一个进程有7个namespace，假设现在有一部分execution context我不想shared with other processes (or threads)，我就自己创建一部分新的namespace来代替原来的
```sh
int unshare(int flags);

```

The main use of unshare() is to allow a process to control its shared execution context without creating a new process

The flags argument is a bit mask that specifies which parts of the execution context should be unshared



## 跟namespace相关的Shell 命令

- nsenter：加入指定进程的指定类型的namespace，然后执行参数中指定的命令。

- unshare：离开当前指定类型的namespace，创建且加入新的namespace，然后执行参数中指定的命令。


### unshare
```sh
[root@VM-12-3-centos ~]# unshare --fork --pid --mount-proc /bin/bash
[root@VM-12-3-centos ~]# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.6  0.2 118176  3788 pts/3    S    11:16   0:00 /bin/bash
root        30  0.0  0.0 156500  1872 pts/3    R+   11:16   0:00 ps aux
```

In the above invocation, the unshare utility is forking a new process, calling the unshare() system call to create a new PID namespace and then execs /bin/bash in it.
We also tell the unshare utility to mount the proc file system in the new process. This is where the ps utility gets its information from.



## 其它

当一个namespace中的所有进程都退出时，该namespace将会被销毁。当然还有其他方法让namespace一直存在，假设我们有一个进程号为1000的进程，以ipc namespace为例：

1. 通过mount --bind命令。例如mount --bind /proc/1000/ns/ipc /other/file，就算属于这个ipc namespace的所有进程都退出了，只要/other/file还在，这个ipc namespace就一直存在，其他进程就可以利用/other/file，通过setns函数加入到这个namespace

1. 在其他namespace的进程中打开/proc/1000/ns/ipc文件，并一直持有这个文件描述符不关闭，以后就可以用setns函数加入这个namespace。
旧

