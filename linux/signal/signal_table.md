## 信号表
在终端，可通过kill -l查看所有的signal信号

1	SIGHUP	挂起	 
2	SIGINT	中断 ctrl+c
3	SIGQUIT	退出	 
4	SIGILL	非法指令	 
5	SIGTRAP	断点或陷阱指令	 
6	SIGABRT	abort发出的信号	 
7	SIGBUS	非法内存访问	 
8	SIGFPE	浮点异常	 
9	SIGKILL	kill信号	不能被忽略、处理和阻塞
10	SIGUSR1	用户信号1	 
11	SIGSEGV	无效内存访问	 
12	SIGUSR2	用户信号2	 
13	SIGPIPE	管道破损，没有读端的管道写数据	 
14	SIGALRM	alarm发出的信号	 
15	SIGTERM	终止信号	kill pid 
16	SIGSTKFLT	栈溢出	 
17	SIGCHLD	子进程退出	默认忽略
18	SIGCONT	进程继续	 
19	SIGSTOP	进程停止	不能被忽略、处理和阻塞
20	SIGTSTP	进程停止   ctrl+z 
21	SIGTTIN	进程停止，后台进程从终端读数据时	 
22	SIGTTOU	进程停止，后台进程想终端写数据时	 
23	SIGURG	I/O有紧急数据到达当前进程	默认忽略
24	SIGXCPU	进程的CPU时间片到期	 
25	SIGXFSZ	文件大小的超出上限	 
26	SIGVTALM	虚拟时钟超时	 
27	SIGPROF	profile时钟超时	 
28	SIGWINCH	窗口大小改变	默认忽略
29	SIGIO	I/O相关	 
30	SIGPWR	关机	默认忽略
31	SIGSYS	系统调用异常	 


一、SIGHUP信号处理
信号产生的情景：
1.如果终端接口检测到一个连接断开，则将此信号送给与该终端相关的控制进程（会话首进程）
在我们登录Linux时，系统会分配给登录用户一个终端(Session)。在这个终端运行的所有程序，包括前台进程组和后台进程组，一般都属于这个 Session。当用户退出Linux登录时，前台进程组和后台有对终端输出的进程将会收到SIGHUP信号。这个信号的默认操作为终止进程，因此前台进 程组和后台有终端输出的进程就会中止。

程序对此信号的默认动作为终止程序

通常用此信号通知守护进程再次读取它们的配置文件。选用SIGHUP的理由是，守护进程不会有控制终端，通常绝不会接收到这种信号。一个典型的例子就是xinetd超级服务程序（见下面的演示案例）
当xinetd程序在接收到SIGHUP信号之后调用hard_reconfig函数，它将循环读取/etc/xinetd.d/目录下的每个子配置文件，并检测其变化。如果某个正在运行的子服务的配置文件被修改以停止服务，则xinetd主进程讲给该子服务进程发送SIGTERM信号来结束它。如果某个子服务的配置文件被修改以开启服务，则xinetd将创建新的socket并将其绑定到该服务对应的端口上。
```sh
kill -HUP xxx
```
