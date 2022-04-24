在一个程序中运行另一个程序
## system
execute a shell command
```cpp
int system(const char *command);
```
在代码当中写这个可以达到和在shell中写命令一样的效果
```cpp
system("echo hello >> a.txt");
```

## exec 用新的程序替换正在运行的程序
```cpp
#include <unistd.h>
//不管参数放不放在数组中，第一个都必须是程序名,最后一个都必须是NULL
int execl(const char *path, const char *arg, ...  /* (char  *) NULL */);
int execv(const char *path, char *const argv[]);
                       

int execlp(const char *file, const char *arg, ...  /* (char  *) NULL */);
int execvp(const char *file, char *const argv[]);
p代表路径，会在环境变量PATH指定的路径中查找第一个参数指定的程序
execlp("ls","ls","-a",NULL)
如果准确知道这个文件的位置,那么就能够在execl中的第一个参数指定它的完整路径(不用搜索更高效,同时也更安全，因为PATH容易被篡改)
execl("/bin/ls","ls","-a",NULL)


int execle(const char *path, const char *arg, ...  /*, (char *) NULL, char * const envp[] */);
int execvpe(const char *file, char *const argv[], char *const envp[]);
e代表环境变量，比如"POWER=4"
其中环境变量数组最后一个元素也必须是NULL

```

The  exec()  family  of functions replaces the current process image with a new process image（但是pid不变）
exec系统调用从当前进程中把当前程序的机器指令清除,然后在空的进程中载入调用时指定的程序代码，最后运行这个新的程序。
exec调整进程的内存分配使之适应新的程序对内存的要求。相同的进程,不同的内容。
exec将替换进程中运行的程序，但它不会改变进程的属性和进程中所有的连接。也就是说，在运行过exec之后，进程的用户ID不会改变，其优先级不会改变，并且其文件描述符也和运行exec之前一样


```cpp
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(){

    puts("Begin");
    
    //现象：这里不刷新缓冲区的话，如果执行结果是往文件输出的话，上面的Begin就不会打印
    //个人理解：下面子进程把父进程替换了，替换后的子进程是全新的，缓冲区为空，如果不在替换之前赶紧打印，就没机会打印了
    fflush(NULL);  
    execl("/bin/date","date","+%s",NULL);
    perror("execl()");  //上面执行成功的话，函数是不会返回的，这里就不会执行
    
    puts("end");
    exit(0);
}
```




