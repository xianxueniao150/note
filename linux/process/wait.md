等待子进程状态的改变，并且获取到该子进程的信息。
```cpp
#include <sys/types.h>
#include <sys/wait.h>
pid_t wait(int *wstatus);
pid_t waitpid(pid_t pid, int *wstatus, int options);
```
对于终止的子进程，wait的执行释放了该子进程关联的资源，如果不执行wait，那么终止的子进程将一直处于"zombie" state

如果子进程已经改变了状态,那么wait调用会立即返回，否则就会阻塞.

options OR

       WNOHANG     设置非阻塞，如果pid指定的目标子进程还没有结束或意外终止，则waitpid立即返回0；
	   			如果目标子进程确实正常退出了，则waitpid返回该子进程的PID


wstatus保存了返回的信息，可以用以下宏查看

       WIFEXITED(wstatus)
              returns  true  if  the  child  terminated normally, that is, by
              calling exit(3) or _exit(2), or by returning from main().

       WEXITSTATUS(wstatus)
              returns the exit status of the child. 即 exit(3) or _exit(2) 的
			  参数或者 main()中return返回的值

       WIFSIGNALED(wstatus)
              returns true if the child process was terminated by a signal.

       WTERMSIG(wstatus)
              returns the number of the signal that caused the child  process
              to  terminate.  


```cpp
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#define DELAY 10

void child_code(int);
void parent_code(int);

void main()
{
    int newpid;
    printf("before:mypid is %d\n", getpid());

    if ((newpid = fork()) == -1)
    {
        perror("fork");
    }
    else if (newpid == 0)
    {
        child_code(DELAY);
    }
    else
    {
        parent_code(newpid);
    }
}

void child_code(int delay)
{
    printf("child %d here. will sleep for %d seconds\n", getpid(), delay);
    sleep(delay);
    printf("child done. about to exit\n");
    exit(17);
}

void parent_code(int childpid)
{
    int wait_rv;
    int child_status;
    wait_rv = wait(&child_status);
    printf("done waiting for %d. wait returned: %d\n", childpid, wait_rv);
    if (WIFEXITED(child_status))
    {
        printf("exited, status=%d\n", WEXITSTATUS(child_status));
    }
    else if (WIFSIGNALED(child_status))
    {
        printf("killed by signal %d\n", WTERMSIG(child_status));
    }
    else
    {
        printf("exited\n");
    }
}
```

```sh
# 终端1运行程序，终端2执行kill -2 48805
$ ./a.out 
before:mypid is 48804
child 48805 here. will sleep for 10 seconds
done waiting for 48805. wait returned: 48805
killed by signal 2

#等待子进程正常退出
$ ./a.out 
before:mypid is 48869
child 48870 here. will sleep for 10 seconds
child done. about to exit
done waiting for 48870. wait returned: 48870
exited, status=17
```

## 高性能编程
要在事件已经发生的情况下执行非阻塞调用才能提高程序的效率。对waitpid函数而言，我们最好在某个子进程退出之后再调用它。那么父进程从何得知某个子进程已经退出了呢？这正是SIGCHLD信号的用途。当一个进程结束时，它将给其父进程发送一个SIGCHLD信号。因此，我们可以在父进程中捕获SIGCHLD信号，并在信号处理函数中调用waitpid函数以“彻底结束” 一个子进程
```cpp
//SIGCHLD信号的典型处理函数
static void handle_child( int sig )
{
	pid_t pid;
	int stat;
	while ( ( pid = waitpid( -1, &stat, WNOHANG ) ) > 0 ) {
		/* 对结求的子进程进行善后处理*/
	}
}
```

## 僵尸进程 zombie
对于多进程程序而言，父进程一般需要跟踪子进程的退出状态。因此，当子进程结束运行时，内核不会立即释放该进程的进程表表项，以满足父进程后续对该子进程退出信息的査洵（如果父进程还在运行）。在子进程结束运行之后，父进程读取其退出状态之前，我们称该子进程处于僵尸态.
另外一种使子进程进入僵尸态的情况是：父进程結束或者异常终止，而子进程继续运行.此时子进程的PPID将被操作系统设置为1,即init进程.init进程接管了该子进程，并等待它结束。在父进程退出之后，子进程退出之前，该子进程处于僵尸态。
