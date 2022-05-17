```cpp
typedef struct ucontext_t {
    struct ucontext_t *uc_link; //当前context执行结束之后要执行的下一个context，如果uc_link为空，执行完当前context后退出程序。
    sigset_t          uc_sigmask; //执行上下文过程中，要屏蔽的信号集合，即信号掩码。
    stack_t           uc_stack; 
    mcontext_t        uc_mcontext;//保存具体的程序执行上下文，如PC值、堆栈指针和寄存器的值。它的实现依赖于底层，是硬件平台相关的，因此不透明。
    ...
} ucontext_t;
```

```cpp
//初始化ucp结构体，将当前上下文保存在ucp中。
int getcontext(ucontext_t *ucp);

//设置当前上下文为ucp所指向的上下文。然后激活
int setcontext(const ucontext_t *ucp);

//保存当前上下文到oucp结构体中，然后激活upc上下文。
int swapcontext(ucontext_t *oucp, const ucontext_t *ucp);

//修改通过getcontext取得的上下文ucp。当上下文激活后，执行func函数，argc为func的参数个数，后面是func的参数序列。
void makecontext(ucontext_t *ucp, void (*func)(), int argc, ...);

```
setcontext和swapcontext会激活上下文:执行后指令就会切换到指定的上下文

setcontext的上下文ucp应该通过getcontext或者makecontext取得，如果调用成功则不返回。
- 如果程序是通过getcontext取得，则程序会继续执行这个调用。
- 如果context是通过makecontext取得，则程序调用makecontext函数的第二个参数指向的函数，这时，如果函数返回，则恢复ucp->uc_link，如果uc_link为NULL,则线程退出。

makecontext 要修改uc_stack所指定的栈大小，因为你拿到的oucp中的栈大小可能不能满足你后面要执行的函数

## 例子
```cpp
#include <ucontext.h>
#include <stdio.h>

int done = 0;

int main()
{
    ucontext_t context;
    getcontext(&context);
    if (done)
    {
        printf("return from getcontext,exit\n");
        return 0;
    }

    done = 1;
    setcontext(&context);
    printf("finished");
    return 0;//never goto here!
}
```

```sh
$ gcc main.c
$ ./a.out
return from getcontext,exit
```


```cpp
#include <ucontext.h>
#include <stdio.h>

void func1(void * arg)
{
    puts("1");
}
void context_test()
{
    char stack[1024*128];
    ucontext_t child,main;

    getcontext(&child); //获取当前上下文
    child.uc_stack.ss_sp = stack;//指定栈空间
    child.uc_stack.ss_size = sizeof(stack);//指定栈空间大小
    child.uc_stack.ss_flags = 0;
    child.uc_link = &main;//设置后继上下文

    makecontext(&child,(void (*)(void))func1,0);//修改上下文指向func1函数

    swapcontext(&main,&child);//切换到child上下文，保存当前上下文到main
    puts("main");//如果设置了后继上下文，func1函数指向完后会返回此处
}

int main()
{
    context_test();

    return 0;
}
```

```sh
$ ./a.out
1
main
```
