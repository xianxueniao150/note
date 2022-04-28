## 文件树
Unix中磁盘上的文件和目录被组成一棵目录树，每个节点都是目录或文件
在Unix系统中，每个文件都位于某个目录中，在逻辑上是没有驱动器或卷的(当然在物理上一个系统可以有多个驱动器或分区)位于不同驱动器和分区上的目录通过文件树无缝地连接在一起，甚至软盘、光盘这些移动存储介质也被挂到文件树的某一个子目录来处理。
这些使ls的实现极为简单，只需考虑文件和目录两种情况，而无需考虑驱动器或分区。

## 目录文件
Unix/Linux系统中，目录（directory）也是一种文件。打开目录，实际上就是打开目录文件。
目录文件包含很多记录，每个记录的格式由统一的标准定义。每条记录的内容代表一个文件或目录。
与普通文件不同的是，目录文件永远不会空，每个目录都至少包含两个特殊的项:"."表示当前目录，".."表示上一级目录。

Unix支持多种目录类型，有Apple HFS、ISO9660、VFAT、NFS等，如果用read来读，那么需要了解这些不同类型目录各自的结构细节。unix提供了专门的redaddir函数
由于目录文件内只有文件名和inode号码，所以如果只有读权限，只能获取文件名，无法获取其他信息，因为其他信息都储存在inode节点中，而读取inode节点内的信息需要目录文件的执行权限（x）
```cpp
#include <sys/types.h>
#include <dirent.h>

DIR *opendir(const char *name);
int closedir(DIR *dirp);


struct dirent *readdir(DIR *dirp);

DESCRIPTION
       The  readdir() function returns a pointer to a dirent structure representing the next directory entry in the directory stream pointed to by dirp.  It returns NULL on reaching the end of the
       directory stream or if an error occurred.

       In the glibc implementation, the dirent structure is defined as follows:

           struct dirent {
               ino_t          d_ino;       /* Inode number */
               off_t          d_off;       /* Not an offset; see below */
               unsigned short d_reclen;    /* Length of this record */
               unsigned char  d_type;      /* Type of file; not supported
                                              by all filesystem types */
               char           d_name[256]; /* Null-terminated filename */
           };
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

## ftruncate 调整文件大小
```cpp
#include <unistd.h>
#include <sys/types.h>
int ftruncate(int fd, off_t length);
```
Posix就该函数对普通文件和共享内存区对象的处理的定义稍有不同。
- 对于一个普通文件：如果该文件的大小大于length参数，额外的数据就被丢弃掉。如果该文件的大小小于length，那么该文件是否修改以及其大小是否增长是未加说明的。实际上对于一个普通文件，把它的大小扩展到length字节的可移植方法是：先lseek到偏移为length-1处，然后write 1个字节的数据。所幸的是几乎所有Unix实现都支持使用 ftruncate扩展一个文件。
- 对于一个共享内存区对象：ftruncate把该对象的大小设置成length字节。

