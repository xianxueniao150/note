系统调用

## system
execute a shell command
```cpp
int system(const char *command);
```
在代码当中写这个可以达到和在shell中写命令一样的效果
```cpp
system("echo hello >> a.txt");
```

## exec
```cpp
#include <unistd.h>
int execl(const char *path, const char *arg, ...
                       /* (char  *) NULL */);
                       
//文件路径默认在环境变量里                       
int execlp(const char *file, const char *arg, ...
               /* (char  *) NULL */);
int execle(const char *path, const char *arg, ...
               /*, (char *) NULL, char * const envp[] */);
int execv(const char *path, char *const argv[]);
int execvp(const char *file, char *const argv[]);
int execvpe(const char *file, char *const argv[],
               char *const envp[]);
```

The  exec()  family  of functions replaces the current process image with a new process image（但是pid不变）


其中环境变量数组最后一个元素也必须是NULL

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




