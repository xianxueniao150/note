# 与目录树相关的命令和系统调用

## mkdir
命令mkdir用来创建新的目录。它接受命令行上的一个或多个目录名，使用mkdir系统调用：
mkdir创建一个新的目录节点并把它链接至文件系统树。即mkdir创建了这个目录的i-节点；分配了一个磁盘块用以存储它的内容；在目录中设置两个入口："."和".."并正确 配置了它们的i-节点号；在它的父目录中增加一个该节点的链接。

## rmdir
命令rmdir用来删除一个目录。它接受命令行上一个或多个目录名，使用rmdir系统调用：
rmdir从目录树中删除一个目录节点。这个目录必须是空的。即除了 "."和".."的入口，这个目录不能包含其他任何的文件和子目录。同时在父目录中删除这个目录的链接。 如果这个目录本身并未被其他的进程占用，它的i-节点和数据块将被释放。

## rm
命令rm用来从一个目录文件中删除一个记录，它接受命令行上一个或多个文件名，使用unlink系统调用：
```cpp
#include <unistd.h>
int unlink(const char *pathname);
```
unlink用来删除目录文件中的一个记录，减少相应i-节点的链接数。如果该i-节点的链接数减为0，数据块和i-节点将被释放。如果该i-节点有其他的链接，则数据块和i-节点将不受影响。unlink不能被用来删除目录。

## ln
命令In用来创建一个文件的链接,使用系统调用link：
```cpp
#include <unistd.h>
int link(const char *oldpath, const char *newpath);
```
link生成一个i-节点的链接。新链接包含原始链接的i-节点号并且具有特定的名字。 如果已经存在一个和新链接名相同的链接，则link将失败。link不能被用来生成目录的新链接。

## mv
命令mv用来改变文件和目录的名字或位置，是这小节中所讲述的最为灵活的一个命 令。在很多情况下,mv仅仅使用系统调用rename：
```cpp
 #include <stdio.h>
int rename(const char *oldpath, const char *newpath);
```
rename用来改变文件或目录的名字或位置。rename适用于文件和目录。和link不同， rename将删除第一个参数所指定的已存在的文件或空目录。
rename是如何将一个文件移动到另一个目录的呢？文件实际上并不存在于目录中，目录中存放的仅仅是它的链接。因此,rename将链接从一个目录移动到另一个目录。
在Linux内核,rename的基本逻辑是：
- 复制链接至新的名字/位置
- 删除原来的链接

Unix提供系统调用link和unlink完成这两个操作。因此,rename( "x", "z”)是这样运 作的：
```cpp
if ( link( "x", "z") != -1 )
	unlink("x")；
```

## cd
cd用来改变进程的当前目录。cd对进程产生影响，但是并不影响目录。

Unix上的每个运行程序都有一个当前目录,chdir系统调用改变进程的当前目录。在系统内部，进程有一个存放当前目录i-节点号的变量。从一个目录进入另一个目录只是改变那个变量的值。
