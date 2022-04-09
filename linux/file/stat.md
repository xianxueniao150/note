### 文件占用空间的大小
```sh
ubuntu@VM-12-3-ubuntu:~$ echo "hello world" > a.txt
ubuntu@VM-12-3-ubuntu:~$ ll a.txt
-rw-rw-r-- 1 ubuntu ubuntu 12 Nov  1 02:28 a.txt
ubuntu@VM-12-3-ubuntu:~$ du -h a.txt
4.0K	a.txt
```
a.txt只有12个字节，但是占用了4k字节的磁盘空间
cluster：簇。文件系统是以簇为单位进行分配的，簇的大小可以调节

### 文件信息
```javascript
ubuntu@VM-12-3-ubuntu:~$ stat a.txt
  File: a.txt
# 实际大小            占用多少个扇区        簇的大小  
  Size: 12        	Blocks: 8          IO Block: 4096   regular file
Device: fc01h/64513d	Inode: 132389      Links: 1
Access: (0664/-rw-rw-r--)  Uid: (  500/  ubuntu)   Gid: (  500/  ubuntu)
#      2进制   110 110 100
#      8进制   6    4   4
Access: 2021-11-01 02:28:33.086420749 +0800
Modify: 2021-11-01 02:28:33.086420749 +0800
Change: 2021-11-01 02:28:33.086420749 +0800
```

### 使用debugfs命令观察文件的扇区内容
```sh
ubuntu@VM-12-3-ubuntu:~$ sudo debugfs /dev/vda1
debugfs 1.44.1 (24-Mar-2018)
debugfs:  blocks a.txt
a.txt: File not found by ext2_lookup
debugfs:  blocks /home/ubuntu/a.txt #查看a.txt文件占用的扇区号
576211
debugfs:  bdump 576211 #将指定编号扇区的内容打印出来
0000  6865 6c6c 6f20 776f 726c 640a 0000 0000  hello world.....
0020  0000 0000 0000 0000 0000 0000 0000 0000  ................
*

#我们试着将a文件删除
ubuntu@VM-12-3-ubuntu:~$ rm a.txt

#再次进入debugfs 查看之前的扇区内容
ubuntu@VM-12-3-ubuntu:~$ sudo debugfs /dev/vda1
debugfs 1.44.1 (24-Mar-2018)
debugfs:  bdump 576211 #发现文件虽然删除了，但是扇区中的文件内容还在，可以用来反删除
0000  6865 6c6c 6f20 776f 726c 640a 0000 0000  hello world.....
0020  0000 0000 0000 0000 0000 0000 0000 0000  ................
*
```



## 获取文件属性
stat  既是一个函数也是一个shell命令，面对符号链接文件时获取的是所指向文件的属性
```cpp
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
int stat(const char *pathname, struct stat *statbuf);
// fstat：通过文件描述符获取属性
int fstat(int fd, struct stat *statbuf);
//lstat：面对符号链接文件时获取的是符号链接文件的属性
int lstat(const char *pathname, struct stat *statbuf);

struct stat {
	   dev_t     st_dev;         /* ID of device containing file */
	   ino_t     st_ino;         /* Inode number */
	   mode_t    st_mode;        /* File type and mode */
	   nlink_t   st_nlink;       /* Number of hard links */
	   uid_t     st_uid;         /* User ID of owner */
	   gid_t     st_gid;         /* Group ID of owner */
	   dev_t     st_rdev;        /* Device ID (if special file) */
	   off_t     st_size;        /* Total size, in bytes */
	   blksize_t st_blksize;     /* Block size for filesystem I/O */
	   blkcnt_t  st_blocks;      /* Number of 512B blocks allocated */
	   struct timespec st_atim;  /* Time of last access */
	   struct timespec st_mtim;  /* Time of last modification */
	   struct timespec st_ctim;  /* Time of last status change */

   };
```

文件类型和许可权限是如何存储在st_mode中？又如何将它们转成10个字符的串？八进制的100664又与“-rw-rw-r--”有什么关系呢？
```sh
st_mode是一个16位的二进制数，文件类型和权限被编码在这个数中

				    | user| group| other|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| type(4字节) |u|g|s|r|w|x|r|w|x|r|w|x|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

其中前4位用作文件类型，最多可以标识16种类型，目前已经使用了其中的7个。
接下来的3位是文件的特殊属性,1代表具有某个属性,0代表没有，这3位分别是set- user-ID位、set-groupTD位和sticky位，它们的含义以后介绍。
最后的9位是许可权限，分为3组，对应3种用户，它们是文件所有者、同组用户和其他用户。其他用户指与用户不在同一个组的人。每组3位，分别是读、写和执行的权限。相应的地方如果是1,就说明该用户拥有对应的权限，0代表没有。
```

怎么来读取被编码的值呢？比如怎么知道212-222-4444所对应的区号是212?很简单，一种方法是将号码的前3位同212比较，另一种方法是将暂时不需要的地方置0,这里把电话号码的后7位置0,然后同212-000-0000比较。
为了比较，把不需要的地方置0,这种技术称为掩码（masking）,就如同带上面具把其他部位都遮起来，就只留下眼睛在外面。

#### 掩码的概念: 将不需要的字段置0,需要的字段的值不发生改变。

#### 使用掩码来解码得到文件类型
文件类型在模式字段的第一个字节的前四位，可以通过掩码来将其他的部分置0,从而得到类型的值。
在＜sys/stat. h＞中有以下定义：
S_IFMT     0170000   bit mask for the file type bit field

S_IFSOCK   0140000   socket
S_IFLNK    0120000   symbolic link
S_IFREG    0100000   regular file
S_IFBLK    0060000   block device
S_IFDIR    0040000   directory
S_IFCHR    0020000   character device
S_IFIFO    0010000   FIFO

S_IFMT是一个掩码，它的值是0170000,可以用来过滤岀前四位表示的文件类型。下面的代码:
```cpp
stat(pathname, &sb);
if ((sb.st_mode & S_IFMT) == S_IFREG) {
	/* Handle regular file */
}
```
通过掩码把其他无关的部分置0,再与表示普通文件的代码比较，从而判断这是否是一个普通文件。

 Because tests of the above form are common, additional macros are defined by POSIX to allow the test of the file type in st_mode to be written more concisely:

S_ISREG(m)  is it a regular file?
S_ISDIR(m)  directory?
S_ISCHR(m)  character device?
S_ISBLK(m)  block device?
S_ISFIFO(m) FIFO (named pipe)?
S_ISLNK(m)  symbolic link?  (Not in POSIX.1-1996.)
S_ISSOCK(m) socket?  (Not in POSIX.1-1996.)

 The preceding code snippet could thus be rewritten as:
```cpp
stat(pathname, &sb);
if (S_ISREG(sb.st_mode)) {
   /* Handle regular file */
}
```


完整的
S_IFSOCK   0140000   socket
S_IFLNK    0120000   symbolic link
S_IFREG    0100000   regular file
S_IFBLK    0060000   block device
S_IFDIR    0040000   directory
S_IFCHR    0020000   character device
S_IFIFO    0010000   FIFO

S_ISUID     04000   set-user-ID bit
S_ISGID     02000   set-group-ID bit (see below)
S_ISVTX     01000   sticky bit (see below)

S_IRWXU     00700   owner has read, write, and execute permission
S_IRUSR     00400   owner has read permission
S_IWUSR     00200   owner has write permission
S_IXUSR     00100   owner has execute permission

S_IRWXG     00070   group has read, write, and execute permission
S_IRGRP     00040   group has read permission
S_IWGRP     00020   group has write permission
S_IXGRP     00010   group has execute permission

S_IRWXO     00007   others (not in group) have read, write, and  execute permission
S_IROTH     00004   others have read permission
S_IWOTH     00002   others have write permission
S_IXOTH     00001   others have execute permission

## 三个特殊的位
### set-user-ID 位
在这3位中，第一位叫做set-user-ID位，它的出现是为了解决一个重要的问题，即用户如何更改自己的密码？
看起来好像很容易，用passwd命令就可以。
接下来研究一下passwd的工作原理,先来看/etc/passwd这个文件，注意这个文件的所有者和文件访问权限设置：
```sh
$ ls -l /etc/passwd
-rw-r--r-- 1 root root 1606 Feb 15 15:39 /etc/passwd
```
更改密码会导致上述文件内容的变化，但是普通用户没有修改这个文件的权限，只有 root用户才可以修改它,passwd命令怎么能够修改这个文件呢？
解决的办法，不是给所有用户修改这个文件的权限,而是给passwd命令一个特殊的权限, 使passwd命令的文件所有者是root，而且它的特殊属性中包含set-user-ID位,如下：
```sh
$ ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 68208 Jul 15  2021 /usr/bin/passwd
```
SUID位告诉内核，运行这个程序的时候认为是由文件所有者在运行这个程序，在这里就是root,而root有修改/etc/passwd的权限。
1.是否可以更改其他用户的密码？
答案是否定的,passwd命令知道是谁在运行程序。它用系统调用getuid来得到用户ID, passwd命令是可以修改/etc/passwd这个文件,但它只会修改该用户ID所对应的密码。
2.set -user-1D的其他用处
SUID位经常用来给某些程序提供额外的权限，比如系统中的打印队列。有可能同时有 很多用户发出打印请求，但系统只有一台打印机，这时要把打印请求都放到打印队列中去， 命令Ipr负责把用户要打印的文件复制到一个特定的系统目录中去。如果这个目录所有用户都有访问权限，那将会产生一些不安全因素，恶意用户有删除别人的打印作业的可能。设置Ipr的SUID位就可以解决这个问题，使Ipr的文件所有者是root和Ipr。当一个普通用户调用Ipr时，Ipr就以root或Ipr的权限运行，可以对这个系统目录进行操作，而普通用户却不能直接对这个目录进行控制。执行从打印队列移除操作的程序也是设置SUID的。


