errno 在 <errno.h> 中定义。
错误 Exx 的宏定义在 /usr/include/asm-generic 文件夹下面的  errno-base.h 和 errno.h，分别定义了 1-34 、35-132 的错误定义。

## perror
```cpp
 #include <stdio.h>
void perror(const char *s);
```
它会自己查找错误代码，并且查找到错误代码对应的错误信息
最终会输出两部分
	第一部分是用户传递进去的描述性信息，第二部分是根据错误代码査到的错误提示

## 通用错误处理
```cpp
void errif(bool condition, const char *errmsg){
    if(condition){
        perror(errmsg);
        exit(EXIT_FAILURE);
    }
}

void errif(bool condition, const char *errmsg){
    if(condition){
        perror(errmsg);
        exit(EXIT_FAILURE);
    }
}

errif(sockfd == -1, "socket create error");
```

## EAGAIN
按照传统,对于不能被满足的非阻塞式I/O操作,System V会返回EAGAIN错误,而源自Berkeley的实现则返回EWOULDBLOCK错误。
顾及历史原因,POSIX规范声称这种情况下这两个错误码都可以返回。幸运的是,大多数当前的系统把这两个错误码定义成相同的值,因此具体使用哪一个并无多大关系。
```cpp
// ubuntu20
#define EWOULDBLOCK     EAGAIN  /* Operation would block */
```

