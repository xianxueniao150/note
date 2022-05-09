不同于 Go 语言，libco 的协程一旦创建之后便跟创建时的那个线程绑定了的，是不支持在不同线程间迁移（migrate）的。

### 对称和非对称
当调用一个函数时，程序从函数的头部开始执行，当函数退出时，这个函数的声明周期也就结束了。一个函数在它的生命周期中，只可能返回一次。

而协程则不同，协程在执行过程中，可以调用别的协程自己则中途退出执行，之后又从调用别的协程的地方恢复执行。这有点像操作系统的线程，执行过程中可能被挂起，让位于别的线程执行，稍后又从挂起的地方恢复执行。在这个过程中，协程与协程之间实际上不是普通“调用者与被调者”的关系，他们之间的关系是对称的（symmetric）。

实际上，协程不一定都是这种对称的关系，还存在着一种非对称的协程模式（asymmetric coroutines）。

具体来讲，非对称协程（asymmetric coroutines）是跟一个特定的调用者绑定的，协程让出 CPU 时，只能让回给原调用者。其实，非对称在于程序控制流转移到被调协程时使用的是 call/resume 操作，而当被调协程让出 CPU 时使用的却是 return/yield 操作。此外，协程间的地位也不对等，caller 与 callee 关系是确定的，不可更改的，非对称协程只能返回最初调用它的协程。

对称协程（symmetric coroutines）则不一样，启动之后就跟启动之前的协程没有任何关系了。协程的切换操作，一般而言只有一个操作 — yield，用于将程序控制流转移给另外的协程。对称协程机制一般需要一个调度器的支持，按一定调度算法去选择 yield 的目标协程。

Go 语言提供的协程，其实就是典型的对称协程。除了对称，Goroutines 还可以在多个线程上迁移。这种协程跟操作系统中的线程非常相似，甚至可以叫做“用户级线程”了。

而 libco 提供的协程本质上却是一种非对称协程。

事实上，libco 内部还为保存协程的调用链留了一个 stack 结构，而这个 stack 大小只有固定的 128。使用 libco，如果不断地在一个协程运行过程中启动另一个协程，随着嵌套深度增加就可能会造成这个栈空间溢出。

### 栈内存
实现 stackful 协程（与之相对的还有一种stackless协程）的两种技术：Separate coroutine stacks 和 Copying the stack（又叫共享栈）。


这里要提到实现细节上，前者为每一个协程分配一个单独的、固定大小的栈；而后者则仅为正在运行的协程分配栈内存，当协程被调度切换出去时，就把它实际占用的栈内存 copy 保存到一个单独分配的缓冲区；当被切出去的协程再次调度执行时，再一次 copy 将原来保存的栈内存恢复到那个共享的、固定大小的栈内存空间。
libco默认前者，且默认给每个协程分配的栈内存是固定的 128KB 的大小。我们可以计算一下，每个协程 128K 内存，那么一个进程启 100 万个协程则需要占用高达 122GB 的内存。

通常情况下，一个协程实际占用的（从 esp 到栈底）栈空间，相比预分配的这个栈大小（比如 libco 的 128KB）会小得多；这样一来， copying stack 的实现方案所占用的内存便会少很多。当然，协程切换时拷贝内存的开销有些场景下也是很大的。因此两种方案各有利弊，而 libco 则同时实现了两种方案，默认使用前者，也允许用户在创建协程时指定使用共享栈。

## 示例
## API
### 创建协程（Creating coroutines）
```cpp
int co_create(stCoRoutine_t** co, const stCoRoutineAttr_t* attr, void* (*routine)(void*), void* arg);

co: 输出参数，co_create 内部会为新协程分配一个“协程控制块”，*co 将指向这个分配的协程控制块。
attr: 输入参数，用于指定要创建协程的属性，可为 NULL。实际上仅有两个属性：栈大小、指向共享栈的指针（使用共享栈模式）。
routine: 指向协程的任务函数，即启动这个协程后要完成什么样的任务。
arg: 传递给任务函数的参数，类似于 pthread 传递给线程的参数。
```

调用 co_create 将协程创建出来后，这时候它还没有启动，也即是说我们传递的 routine 函数还没有被调用。实质上，这个函数内部仅仅是分配并初始化 stCoRoutine_t 结构体、设置任务函数指针、分配一段“栈”内存，以及分配和初始化 coctx_t。

为什么这里的“栈”要加个引号呢？因为这里的栈内存，无论是使用预先分配的共享栈，还是 co_create 内部单独分配的栈，其实都是调用 malloc 从进程的堆内存分配出来的。对于协程而言，这就是“栈”，而对于底层的进程（线程）来说这只不过是普通的堆内存而已。

### 启动协程（Resume a coroutine）
```cpp
void co_resume(stCoRoutine_t* co);
```

不同于 Go 语言，这里 co_resume() 启动一个协程的含义，不是“创建一个并发任务”。进入 co_resume() 函数后发生协程的上下文切换，协程的任务函数是立即就会被执行的，而且这个执行过程不是并发的（Concurrent）。

为什么不是并发的呢？因为 co_resume() 函数内部会调用 coctx_swap() 将当前协程挂起，然后就开始执行目标协程的代码了。本质上这个过程是串行的，在一个操作系统线程（进程）上发生的，甚至可以说在一颗 CPU 核上发生的（假定没有发生 CPU migration）。

让我们将 coroutine 当做一种特殊的 subroutine 来看，问题会显得更清楚：A 协程调用 co_resume(B) 启动了 B 协程，本质上是一种特殊的过程调用关系，A 调用 B 进入了 B 过程内部，这很显然是一种串行执行的关系。那么，既然 co_resume() 调用后进入了被调协程执行控制流，那么 co_resume() 函数本身何时返回？这就要等被调协程主动让出 CPU了。

### 协程的挂起（Yield to another coroutine）
在非对称协程理论，yield 与 resume 是个相对的操作。A 协程 resume 启动了 B 协程，那么只有当 B 协程执行 yield 操作时才会返回到 A 协程。

yield 操作的内部逻辑。在被调协程要让出 CPU 时，会将它的 stCoRoutine_t 从 pCallStack 弹出，“栈指针” iCallStackSize 减 1，然后 co_swap() 切换 CPU 上下文到原来被挂起的调用者协程恢复执行。这里“被挂起的调用者协程”，即是之前调用 co_resume() 切换 CPU 上下文被挂起的那个协程。

co_yield_env() 函数
```cpp
void co_yield_env(stCoRoutineEnv_t *env) {
    stCoRoutine_t *last = env->pCallStack[env->iCallStackSize - 2];
    stCoRoutine_t *curr = env->pCallStack[env->iCallStackSize - 1];
    env->iCallStackSize--;
    co_swap(curr, last);
}

void co_yield_ct()
{

	co_yield_env( co_get_curr_thread_env() );
}
void co_yield( stCoRoutine_t *co )
{
	co_yield_env( co->env );
}
```
 
我们知道 co_resume 是有明确目的对象的，可以通过 resume 将 CPU 交给任意协程。但 yield 则不一样，你只能 yield 给当前协程的调用者。而当前协程的调用者，即最初 resume 当前协程的协程，是保存在 stCoRoutineEnv_t 的 pCallStack 中的。

事实上，libco 提供了一个co_yield(stCoRoutine_t*) 的函数。看起来你似乎可以将 CPU 让给任意协程。实际上并非如此：
如果你调用 co_yield(co)，就以为将 CPU 让给 co 协程了，那就错了。最终通过 co_yield_env() 还是会将 CPU 让给原来启动当前协程的调用者。

可能有的读者会有疑问，同一个线程上所有协程共享 stCoRoutineEnv_t，那么我 co_yield() 给其他线程上的协程呢？对不起，如果你这么做，那么你的程序就挂了。libco 的协程是不支持线程间迁移（migration）的，如果你试图这么做，程序一定会挂掉。

再补充说明一下，协程库内虽然提供了 co_yield(stCoRoutine_t*) 函数，但是没有任何地方有调用过该函数（包括样例代码）。使用的较多的是另外一个函数— co_yield_ct()，其实本质上作用都是一样的。
## 源码解析
### 挂起协程与恢复的执行
协程究竟在什么时候需要 yield 让出 CPU，又在什么时候恢复执行呢？

先来看 yield，实际上在 libco 中共有 3 种调用 yield 的场景：
- 用户程序中主动调用 co_yield_ct()；
- 程序调用了 poll() 或 co_cond_timedwait() 陷入“阻塞”等待；
- 程序调用了 connect(), read(), write(), recv(), send() 等系统调用陷入“阻塞”等待。

相应地，重新 resume 启动一个协程也有3种情况：
- 对应用户程序主动 yield 的情况，这种情况也有赖于用户程序主动将协程 co_resume() 起来；
- poll() 的目标文件描述符事件就绪或超时，co_cond_timedwait() 等到了其他协程的 co_cond_signal() 通知信号或等待超时；
- read(), write() 等 I/O 接口成功读到或写入数据，或者读写超时。





### 全局变量
```cpp
static __thread stCoRoutineEnv_t* gCoEnvPerThread = NULL;

struct stCoRoutineEnv_t
{
	//保存协程之间调用链的栈
	stCoRoutine_t *pCallStack[ 128 ];
	int iCallStackSize;
	stCoEpoll_t *pEpoll;

};
```
每当启动（resume）一个协程时，就将它的协程控制块 stCoRoutine_t 结构指针保存在 pCallStack 的“栈顶”，然后“栈指针” iCallStackSize 加 1，最后切换 context 到待启动协程运行。当协程要让出（yield）CPU 时，就将它的 stCoRoutine_t从pCallStack 弹出，“栈指针” iCallStackSize 减 1，然后切换 context 到当前栈顶的协程（原来被挂起的调用者）恢复执行。


```cpp
struct stCoRoutine_t {
    stCoRoutineEnv_t *env; //协程执行的环境。运行在同一个线程上的各协程共享该结构，是个全局性的资源。

	//实际待执行的协程函数以及参数。
    pfn_co_routine_t pfn;
    void *arg; 

    coctx_t ctx; //用于协程切换时保存 CPU 上下文（context）的；所谓的上下文，即 esp、ebp、eip 和其他通用寄存器的值。
 
    char cStart;
    char cEnd;
    char cIsMain;
    char cEnableSysHook;
    char cIsShareStack;
 
    void *pvEnv; //保存程序系统环境变量的指针
 
    //协程运行时的栈,char sRunStack[ 1024 * 128 ];
    stStackMem_t* stack_mem;
 
    //共享栈相关，save satck buffer while confilct on same stack_buffer;
    char* stack_sp; 
    unsigned int save_size;
    char* save_buffer;
 
    stCoSpec_t aSpec[1024];
};
 

struct stCoEpoll_t
{
	int iEpollFd; //epoll 实例的文件描述符。
	static const int _EPOLL_SIZE = 1024 * 10; //作为 epoll_wait() 系统调用的第三个参数，即一次 epoll_wait 最多返回的就绪事件个数。

	struct stTimeout_t *pTimeout; //时间轮（Timing wheel）定时器

	struct stTimeoutItemLink_t *pstTimeoutList; //该指针实际上是一个链表头。链表用于临时存放超时事件的 item。

	struct stTimeoutItemLink_t *pstActiveList; //指向一个链表。该链表用于存放 epoll_wait 得到的就绪事件和定时器超时事件。

	co_epoll_res *result; //epoll_wait() 第二个参数的封装，即一次 epoll_wait 得到的结果集。

};

```

### 协程上下文
前面也说了协程不过是一段子程序(其实也就是个函数)罢了，因此只要保存下当前的函数栈状态、寄存器值，就可以描述出这个协程的全部状态，这个结构被称为协程上下文。

协程上下文其实就是保存了当前所有寄存器的值，这些寄存器描述了当前的函数栈，程序执行状态等信息。

在libco的 coctx.h 文件下可以找到这个结构体。
```cpp
struct coctx_t
{
	void *regs[ 14 ];       // 一个数组，保存了14个寄存器的值 
	size_t ss_size;         // 协程栈大小
	char *ss_sp;            // 协程栈指针
};
```
可以看到，在coctx_t这个结构体中。ss_size和ss_sp则描述了协程的栈空间大小。regs是一个数组，保存着14个寄存器当前的值。

```asm
其中 %rdi %rsi 存储的是coctx_swap的第一个和第二个参数，其实就是两个coctx_t结构的指针
coctx_swap:
    leaq (%rsp),%rax        ;把rsp寄存器所存的地址赋值给 rax寄存器。 在调用 coctx_swap函数时，rsp存储的还是上一级函数的栈顶指针，也就是上一个协程的栈顶。
    movq %rax, 104(%rdi)    ;把rax寄存器里面的值取出来，放到（rdi寄存器的所存地址 + 104字节）的位置，其实就是 regs数组的最后一个元素，这个元素存的就是rsp内存储的地址值。
    movq %rbx, 96(%rdi)     ;同上，存 rbx的值到regs数组的第13个元素
    movq %rcx, 88(%rdi)     
    movq %rdx, 80(%rdi)
    movq 0(%rax), %rax      ;（把rax寄存器所存地址 + 0）得到一个内存地址，然后到内存中取得这个地址里面所存的值，并放到rax寄存器中，这个值其实就是函数调用返回地址，即执行 call指令的下一句指令地址。
    movq %rax, 72(%rdi)     ; 把rax所存的值存在regs数组的第10个元素，即返回地址。
    movq %rsi, 64(%rdi)
    movq %rdi, 56(%rdi)
    movq %rbp, 48(%rdi)
    movq %r8, 40(%rdi)
    movq %r9, 32(%rdi)
    movq %r12, 24(%rdi)
    movq %r13, 16(%rdi)
    movq %r14, 8(%rdi)
    movq %r15, (%rdi)
    xorq %rax, %rax         ; 异或算法，这里就是将rax寄存器清0

    movq 48(%rsi), %rbp     ; （把rsi寄存器里所存的值 + 48)得到一个地址，取这个地址所存内容，其实存的就是 rbp栈底指针的值，再赋值给rbp寄存器。即恢复第二个协程上下文的栈底
    movq 104(%rsi), %rsp    ; 同上，恢复第二个协程的栈顶。 现在rsp rbp两个寄存器已经指向新协程的栈了。
    movq (%rsi), %r15       ; 恢复其他寄存器
    movq 8(%rsi), %r14
    movq 16(%rsi), %r13
    movq 24(%rsi), %r12
    movq 32(%rsi), %r9
    movq 40(%rsi), %r8
    movq 56(%rsi), %rdi
    movq 80(%rsi), %rdx
    movq 88(%rsi), %rcx
    movq 96(%rsi), %rbx
    leaq 8(%rsp), %rsp      ; 将栈顶指针上移8位，因为call命令会将调用方的返回地址压栈，而由于协程切换后应该返回新的协程的返回地址，因此上移八位。
    pushq 72(%rsi)          ; 把第二个协程的 返回地址 压入栈
    movq 64(%rsi), %rsi     ; 恢复rsi寄存器
    ret                     ; 返回，取栈顶所存的地址为返回地址，而栈顶的地址为第二个协程的返回地址，因此就转到新协程去了
```



### co_resume
讲到 resume 一个协程，我们一定得注意，这可能是第一次启动该协程，也可以是要准备重新运行挂起的协程。
```cpp
void co_resume(stCoRoutine_t *co) {
    stCoRoutineEnv_t *env = co->env;
    stCoRoutine_t *lpCurrRoutine = env->pCallStack[env->iCallStackSize-1];
	//当且仅当协程是第一次启动时才会执行到
    if (!co->cStart) {
        coctx_make(&co->ctx, (coctx_pfn_t)CoRoutineFunc, co, 0);
        co->cStart = 1;
    }
    env->pCallStack[env->iCallStackSize++] = co;
    co_swap(lpCurrRoutine, co);
}
```


#### 初始化
```cpp
env->cond = co_cond_alloc();
stCoCond_t *co_cond_alloc()
{
	return (stCoCond_t*)calloc( 1,sizeof(stCoCond_t) );
}

struct stCoCond_t
{
	stCoCondItem_t *head;
	stCoCondItem_t *tail;
};
```
可以看到cond就是一个链表，初始化就是分配内存


#### wait
```cpp
co_cond_timedwait(env->cond, -1);

int co_cond_timedwait( stCoCond_t *link,int ms )
{
	stCoCondItem_t* psi = (stCoCondItem_t*)calloc(1, sizeof(stCoCondItem_t));
	//将当前协程保存到pArg
	psi->timeout.pArg = GetCurrThreadCo();
	//保存动作就是恢复该协程的执行
	psi->timeout.pfnProcess = OnSignalProcessEvent;

	AddTail( link, psi);

	co_yield_ct();

	RemoveFromLink<stCoCondItem_t,stCoCond_t>( psi );
	free(psi);

	return 0;
}

static void OnSignalProcessEvent( stTimeoutItem_t * ap )
{
	stCoRoutine_t *co = (stCoRoutine_t*)ap->pArg;
	co_resume( co );
}

struct stCoCondItem_t 
{
	stCoCondItem_t *pPrev;
	stCoCondItem_t *pNext;
	stCoCond_t *pLink;

	stTimeoutItem_t timeout; //链表节点存的东西
};

struct stTimeoutItem_t
{

	enum
	{
		eMaxTimeout = 40 * 1000 //40s
	};
	stTimeoutItem_t *pPrev;
	stTimeoutItem_t *pNext;
	stTimeoutItemLink_t *pLink;

	unsigned long long ullExpireTime;

	OnPreparePfn_t pfnPrepare;
	OnProcessPfn_t pfnProcess;

	void *pArg; // routine 
	bool bTimeout;
};

```

#### signal
```cpp
int co_cond_signal( stCoCond_t *si )
{
	//从cond链表弹出
	stCoCondItem_t * sp = co_cond_pop( si );
	if( !sp ) 
	{
		return 0;
	}
	RemoveFromLink<stTimeoutItem_t,stTimeoutItemLink_t>( &sp->timeout );

	AddTail( co_get_curr_thread_env()->pEpoll->pstActiveList,&sp->timeout );

	return 0;
}

```

#### poll
```cpp
//
poll(NULL, 0, 1000);

//
int poll(struct pollfd fds[], nfds_t nfds, int timeout)
{
	return  co_poll_inner(co_get_epoll_ct(), fds, nfds, timeout, g_sys_poll_func);
}

//
int co_poll_inner( stCoEpoll_t *ctx,struct pollfd fds[], nfds_t nfds, int timeout, poll_pfn_t pollfunc)
{
	int epfd = ctx->iEpollFd;
	stCoRoutine_t* self = co_self();

	//1.struct change
	stPoll_t& arg = *((stPoll_t*)malloc(sizeof(stPoll_t)));
	memset( &arg,0,sizeof(arg) );

	arg.iEpollFd = epfd;
	arg.fds = (pollfd*)calloc(nfds, sizeof(pollfd));
	arg.nfds = nfds;

	stPollItem_t arr[2];
	arg.pPollItems = arr;
	memset( arg.pPollItems,0,nfds * sizeof(stPollItem_t) );

	arg.pfnProcess = OnPollProcessEvent;
	arg.pArg = GetCurrCo( co_get_curr_thread_env() );
	
	
	//2. add epoll

	//3.add timeout
	unsigned long long now = GetTickMS();
	arg.ullExpireTime = now + timeout;
	int ret = AddTimeout( ctx->pTimeout,&arg,now );
	int iRaiseCnt = 0;

	//下面一句执行完之后执行权就交给别的协程了，等到重新拿到执行权之后才会再次执行后面的语句
	co_yield_env( co_get_curr_thread_env() );
	iRaiseCnt = arg.iRaiseCnt;

    {
		//clear epoll status and memory
	}

	return iRaiseCnt;
}
```


### 主协程事件循环源码分析
```cpp
co_eventloop(co_get_epoll_ct(), NULL, NULL);
void co_eventloop( stCoEpoll_t *ctx,pfn_co_eventloop_t pfn,void *arg )
{
	if( !ctx->result )
	{
		ctx->result =  co_epoll_res_alloc( stCoEpoll_t::_EPOLL_SIZE );
	}
	co_epoll_res *result = ctx->result;


	for(;;)
	{
		//调用 epoll_wait() 等待 I/O 就绪事件，为了配合时间轮工作，这里的 timeout 设置为 1 毫秒。
		int ret = co_epoll_wait( ctx->iEpollFd,result,stCoEpoll_t::_EPOLL_SIZE, 1 );

		//这里面可能已经有“活跃”的待处理事件
		stTimeoutItemLink_t *active = (ctx->pstActiveList);
		//临时性的链表， pstTimeoutList 永远为空
		stTimeoutItemLink_t *timeout = (ctx->pstTimeoutList);

		memset( timeout,0,sizeof(stTimeoutItemLink_t) );

		//处理就绪的文件描述符。
		for(int i=0;i<ret;i++)
		{
			stTimeoutItem_t *item = (stTimeoutItem_t*)result->events[i].data.ptr;
			//如果用户设置了预处理回调，则调用 pfnPrepare 做预处理；否则直接将就绪事件 item 加入 active 队列。
			//实际上，pfnPrepare() 预处理函数内部也是会将就绪item加入 active 队列，最终都是加入到 active 队列
			if( item->pfnPrepare )
			{
				item->pfnPrepare( item,result->events[i],active );
			}
			else
			{
				AddTail( active,item );
			}
		}


		unsigned long long now = GetTickMS();
		//从时间轮上取出已超时的事件，放到 timeout 队列。
		TakeAllTimeout( ctx->pTimeout,now,timeout );

		stTimeoutItem_t *lp = timeout->head;
		//遍历 timeout 队列，设置事件已超时标志（bTimeout 设为 true）。
		while( lp )
		{
			lp->bTimeout = true;
			lp = lp->pNext;
		}

		//将 timeout 队列中事件合并到 active 队列。
		Join<stTimeoutItem_t,stTimeoutItemLink_t>( active,timeout );

		lp = active->head;
		//遍历 active 队列，调用工作协程设置的 pfnProcess() 回调函数 resume 挂起的工作协程，处理对应的 I/O 或超时事件。
		while( lp )
		{

			PopHead<stTimeoutItem_t,stTimeoutItemLink_t>( active );
            if (lp->bTimeout && now < lp->ullExpireTime) 
			{
				int ret = AddTimeout(ctx->pTimeout, lp, now);
				if (!ret) 
				{
					lp->bTimeout = false;
					lp = active->head;
					continue;
				}
			}
			if( lp->pfnProcess )
			{
				lp->pfnProcess( lp );
			}

			lp = active->head;
		}
	}
}
```

