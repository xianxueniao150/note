## 信号量
信号量是包含一个非负整数型的变量，并且带有两个原子操作wait和signal。
Wait还可以被称为P或lock，signal还可以被称为V、unlock或post。

P(sv)：如果sv的值大于零，就给它减1；如果它的值为零，就挂起该进程的执行
V(sv)：如果有其他进程因等待sv而被挂起，就让它恢复运行，如果没有进程因等待sv而挂起，就给它加1.

System v 中的信息量
信号量和其它的IPC结构（前面总结过管道、消息队列）不同。它本质就是一个计数器，用于为多个进程提供对共享数据对象的访问。通常进程为了获得共享的资源，需要执行以下操作：
- 测试控制该资源的信号量
- 若此信号量>0,则进程可以使用该资源。此种情况下，进程会将信号量值减1，表明它使用了一个资源单位。
- 否则，此信号量的值为0，则使该进程进入休眠状态，直至信号量值>1。如果有进程正在休眠状态等待此信号量，则唤醒它们

还有就是为了正确的实现信号量，信号量值的测试及减1操作还应当是原子的。为此，信号量通常是在内核中实现的。一般而言，信号量初值可以是任意一个正值，该值表明有多少个共享资源单位可供共享应用。


然而遗憾的是，这里的信号量也是有缺陷的。

这源于①信号量并非是单个非负值，它被定义为一个可能含有多个信号量值的集合。通常在创建信号量的时候，对该集合中信号量数量进行指定 ②信号量创建独立于它的初始化。这是最致命的，因为这将导致的是不能原子的创建一个信号量集合，并对该集合中的各个信号量值赋初值。③有的程序1在终止时可能并没有释放掉已经分配给它的信号量。

 


## 使用步骤
使用semget()创建和打开一个信号量
使用semctl()带上SETVAL或SETALL flag初始化信号量的值（只需一个进程做这个）。
使用semop()操作信号量的值，加减一般用来代表释放和请求资源。
当所有的进程使用完信号量集，使用semctl() IPC_RMID删除集合。

## API
### 创建或打开信号量集
```cpp
int semget(key_t key, int nsems, int semflg);

nsems 指定集合中信号量的数量,如果是创建新集合，则必须指定它；如果是引用现有的信号集（通常客户进程中），则将其指定为0.
返回信号量集ID
```

### 初始化或改变信号量的属性
```cpp
int semctl(int semid, int semnum, int cmd, .../*union semun arg*/);

union semun {
   int              val;    /* Value for SETVAL */
   struct semid_ds *buf;    /* Buffer for IPC_STAT, IPC_SET */
   unsigned short  *array;  /* Array for GETALL, SETALL */
   struct seminfo  *__buf;  /* Buffer for IPC_INFO (Linux-specific) */
};

semnum:set中的第几个semaphore(从0开始计数),对于在单个信号量上执行的操作有意义，对于其他操作则会忽略这个参数，并且可以将其设置为0。
cmd:要执行的的操作，如果此操作需要参数，那么使用第四个参数向其提供所需的参数。
	SETVAL : 使用arg.val初始化对应的信号量值
	IRC_RMID : 删除信号量,和相关的 semid_ds数据结构（这里面记录信号量的一些权限啊、操作时间等）
	IPC_STAT: 在arg.buf指向的缓冲区中放置一份与这个信号量集相关联的semid_ds数据结构的副本。


获取单个信号量的信息
下面操作返回semid引用的集合中第semnum个信号量的信息。所有这些操作都需要在信号量集合中具备读权限，并且无需arg参数。
	GETPID：返回上一个在该信号量上执行semop()的进程的进程ID; 如果还没有进程在该信号量上执行semop()，那么就返回0。
	GETNCNT: 返回当前等待该信号量的值增长的进程数; 这个值被称为semncnt值。
	GETZCNT: 返回当前等待该信号量的值变成0的进程数; 这个值被称为semzcnt值。

函数返回值根据cmd的不同有不同的意义：

GETNCNT ：semncnt的值
GETPID ：sempid的值
GETVAL ：semval的值
GETZCNT ：semzcnt的值
IPC_INFO ： 内核中记录所有信号量的数组已使用下标的最大值。 the index of the highest used entry in the kernel’s internal array recording information about all semaphore sets. (This information can be used with repeated SEM_STAT or SEM_STAT_ANY operations to obtain information about all semaphore sets on the system.)
SEM_INFO ：和IPC_INFO一样
SEM_STAT ： 所给semid对应的信号量集的标识符。
SEM_STAT_ANY ： 和SEM_STAT一样
其他 ：0 on success.

struct semid_ds {
   struct ipc_perm sem_perm;  /* Ownership and permissions */
   time_t          sem_otime; /* Last semop time */
   time_t          sem_ctime; /* Last change time */
   unsigned long   sem_nsems; /* No. of semaphores in set */
};


```

### 信号量操作 
此操作是原子操作,所有操作要么都成功，要么都失败
```cpp
//sops 是一个指向数组的指针，数组中包含了需要执行的操作,nsop给出了数组的大小
int semop(int semid, struct sembuf *sops, size_t nsops);
int semtimedop(int semid, struct sembuf *sops, size_t nsops,
              const struct timespec *timeout);
              
struct sembuf {
     unsiged short  sem_num;    /* semaphore index in array */
     short       sem_op;     /* semaphore operation */
     short       sem_flg;    /* operation flags */
};              

sem_op
sem_op>0:会将sem_op的值加到信号量值上，其结果是其他等待的进程可能会被唤醒并执行它们的操作。调用进程必须具备在信号量上的修改(写)权限。
sem_op=0:检查信号量是否为0， 如果等于0,那么操作将立即结束，否则semop()就会阻塞直到信号量值变成0为止。调用进程必须要具备在信号量上的读权限。
sem_op<0:等待信号量的值为大于或等于该负数的绝对值时返回,同时会将信号量的值减去该负数的绝对值



sem_flg
IPC_NOWAIT:不阻塞,如果semop()本来要发生阻塞的话就会返回EAGAIN错误。
SEM_UNDO:表示如果该进程已经终止了那么该操作就不会进行了
```

当semop()调用阻塞时，进程会保持阻塞直到发生下列某种情况为止。
- 另一个进程修改了信号量值使得待执行的操作能够继续向前。
- 一个信号中断了semop()调用。发生这种情况时会返回EINTR错误。
- 另一个进程删除了semid引用的信号量。发生这种情况时semop()会返回EIDRM错误







Valid values for cmd are:

SETVAL
示例
```cpp
union semun tmp;
tmp.val = value;
semctl(sem_id, 0, SETVAL, tmp)
```



https://songlee24.github.io/2015/04/21/linux-IPC/





### 信号量初始化
程序员必须要使用semctl()系统调用显式地初始化信号量。（在linux上，semget()返回的信号量实际上会被初始化为0,但为了取得移植性就不能依赖于此。）

因创建和初始化信号量是分开进行的，所以当多个进程要对同一个信号量进行创建和初始化信号量时，就会出现竞争，那么信号量的初始值将由最后调用初始化的进程所决定。

解决办法：在一个信号量集首次被创建时，sem_otime字段会被初始化为0,并且只有后续的semop()调用才会修改这个字段的值。因此可以利用这个特性消除竞争条件。即只需要插入额外的代码来强制第二个进程（即没有创建信号量的那个进程）等待直到第一个进程既初始化了信号量又执行了一次semop调用为止(从而更新sem_otime字段)

```cpp
semid = semget(key, 1, IPC_CREAT | IPC_EXCL | perms);

if (semid != -1) {                  /* Successfully created the semaphore */
    union semun arg;
    struct sembuf sop;

    sleep(5);
    printf("%ld: created semaphore\n", (long) getpid());

    arg.val = 0;                    /* So initialize it to 0 */
    if (semctl(semid, 0, SETVAL, arg) == -1)
        errExit("semctl 1");
    printf("%ld: initialized semaphore\n", (long) getpid());

    /* Perform a "no-op" semaphore operation - changes sem_otime
       so other processes can see we`ve initialized the set. */

    sop.sem_num = 0;                /* Operate on semaphore 0 */
    sop.sem_op = 0;                 /* Wait for value to equal 0 */
    sop.sem_flg = 0;
    if (semop(semid, &sop, 1) == -1)
        errExit("semop");
    printf("%ld: completed dummy semop()\n", (long) getpid());

} else {                            /* We didn`t create the semaphore set */

    if (errno != EEXIST) {          /* Unexpected error from semget() */
        errExit("semget 1");

    } else {                        /* Someone else already created it */
        const int MAX_TRIES = 10;
        int j;
        union semun arg;
        struct semid_ds ds;

        semid = semget(key, 1, perms);      /* So just get ID */
        if (semid == -1)
            errExit("semget 2");

        printf("%ld: got semaphore key\n", (long) getpid());
        /* Wait until another process has called semop() */

        arg.buf = &ds;
        for (j = 0; j < MAX_TRIES; j++) {
            printf("Try %d\n", j);
            if (semctl(semid, 0, IPC_STAT, arg) == -1)
                errExit("semctl 2");

            if (ds.sem_otime != 0)          /* Semop() performed? */
                break;                      /* Yes, quit loop */
            sleep(1);                       /* If not, wait and retry */
        }

        if (ds.sem_otime == 0)              /* Loop ran to completion! */
            fatal("Existing semaphore not initialized");
    }
}
```

