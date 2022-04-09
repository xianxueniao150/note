终端就像文件，可以对该文件使用任何与文件相关的命令
```sh
#终端1
$ tty
/dev/ttys023

#终端2
$ echo "aaaaa" > /dev/ttys023

#终端1
$ aaaaa
```

## 设备文件的属性
```sh
$ ls -li /dev/ttys016
915 crw--w----  1 bowen  tty   16,  16  4  6 11:52 /dev/ttys016
```
设备文件具有磁盘文件的大部分属性。上面ls的输出内容表明/dev/ttys016 拥有i-节点 915 ,权限位为rw--w---- ,1个链接，文件所有者bowen和组tty,最近修改时间是4.6 11:52。
文件类型是“c”,表示这个文件实际上是以字符为单位进行传送的设备。权限位看起 来有点奇怪，表达式136,2显示在表示文件大小的地方，它有什么特殊的含义呢？
(1)设备文件和i节点	
常用的磁盘文件由字节组成，磁盘文件中的字节数就是文件的大小。设备文件是链接，而不是容器。键盘和鼠标不存储击键数和点击数。
设备文件的i-节点存储的是指向内核子程序的指针，而不是文件的大小和存储列表。内核中传输设备数据的子程序被称为设备驱动程序。
在/dev/ttys016这个例子中,从终端进行数据传输的代码是在设备一进程表中编号为16 的子程序。该子程序接受一个整型参数。在/dev/ttys016中，参数是16。16和16这两个数被称为设备的主设备号和从设备号。
主设备号确定处理该设备实际的子程序，而从设备号被作为参数传输到该子程序。

i-节点可以是磁盘文件的，也可以是设备文件的。i-节点的类型被记录在结构stat的成员变量st_mode的类型区域中。
考虑一下read是如何工作的。内核首先找到文件描述符的i-节点，该i-节点用于告诉内核文件的类型。如果文件是磁盘文件，那么内核通过访问块分配表来读取数据。如果文件是设备文件，那么内核通过调用该设备驱动程序的read部分来读取数据。其他的操作，例 如open、write、lseek和close等都是类似的。

(2)设备文件和权限位
每个文件都有相应的读、写和执行的权限。当文件实际上表示设备时，权限位表示什么意思呢？向文件写入数据就是把数据发送到设备，因此，权限写意味着允许向设备发送数据。在这个例子中，文件所有者和组tty的成员拥有写设备的权限，但是只有文件的所有者 有读取设备的权限。读取设备文件就像读取普通文件一样，从文件获得数据。如果除了文件所有者还有其他用户能够读取/dev/ttys016,那么其他人也能够读取在该键盘上输入的字 符,读取其他人的终端输入会引起某些麻烦。
另一方面，向其他人的终端写入字符是Unix中write命令的目标。

## 终端I/O
```cpp
#include <stdio.h>
main()
{
	int c, n = 0;
	while( ( c = getchar()) != 'Q')
		printf("char %3d is %c code %d\n", n++ , c, c );
}
```

```sh
$ ./a.out
hello
char   0 is h code 104
char   1 is e code 101
char   2 is l code 108
char   3 is l code 108
char   4 is o code 111
char   5 is
 code 10
Q
```
接下来会发生什么事情？如果字符代码直接从键盘流向getchar,则在每个字符后可看到一个响应。输入单词hello中的5个字符并按回车键。然而仅在这个时候,程序才开始处理这些字符。输入看起来被缓冲了。就像流向磁盘的数据，从终端流出的数据在沿途中的某个地方被存储起来了。
程序同时显示了另外一些内容。Enter键或Return键通常发送ASCII码13,即回车符。 程序的输出显示ASCII码13被换行符（代码10）所替代。
第三种处理影响程序的输出。listchars在每个字符串的末尾添加一个换行符（\n。换行符代码告诉鼠标移到下一行，但没有告诉它移到最左边。代码13（回车符）告诉鼠标回到最左端。
运行结果表明在文件描述符的中间必定有一个处理层。

这个例子说明了 3种处理：
1.进程在用户输入Return后才接收数据；
2.进程将用户输入的Return（ASCII码13）看作换行符（ASCII码10）
3.进程发送换行符，终端接收回车换行符。

### stty 读取和修改终端驱动程序的设置
```sh
$ stty
speed 38400 baud; line = 0;
eol = M-^?; eol2 = M-^?;
-brkint ixany iutf8
ubuntu@VM-12-3-ubuntu:~/projects/c$ stty -a
speed 38400 baud; rows 41; columns 99; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>;
start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O;
min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel
iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho
-extproc
```
 一个属性前的减号表示这个操作被关闭。
 icrnl是Input：convert Carriage Return to NewLine（输入时将回车转换为换行）的缩写，即在前面的例子中驱动程序所做的操作。
 onlcr代表Output：add to NewLine a Carriage Return(输出时在新的一行中加入回车）。

（2）使用stty改变驱动程序设置
