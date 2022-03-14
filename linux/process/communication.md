## socketpair
Linux实现了一个源自BSD的socketpair调用，可以实现在同一个文件描述符中进行读写的功能。
在Linux中，完全可以把这一对socket当成pipe返回的文件描述符一样使用，唯一的区别就是这一对文件描述符中的任何一个都可读和可写，函数原型如下：

```cpp
int socketpair(int domain, int type, int protocol, int sv[2]);
```

* domain表示协议族，PF_UNIX或者AF_UNIX
* type表示协议，可以是SOCK_STREAM或者SOCK_DGRAM，SOCK_STREAM基于TCP，SOCK_DGRAM基于UDP
* protocol表示类型，只能为0
* sv[2]表示套节字柄对，该两个句柄作用相同，均能进行读写双向操作
* 返回结果， 0为创建成功，-1为创建失败，并且errno来表明特定的错误号

