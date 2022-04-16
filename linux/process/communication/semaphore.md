信号量是包含一个非负整数型的变量，并且带有两个原子操作wait和signal。
Wait还可以被称为P或lock，signal还可以被称为V、unlock或post。

P(sv)：如果sv的值大于零，就给它减1；如果它的值为零，就挂起该进程的执行
V(sv)：如果有其他进程因等待sv而被挂起，就让它恢复运行，如果没有进程因等待sv而挂起，就给它加1.



### 创建信号量集
```cpp
int semget(key_t key, int nsems, int semflg);

nsems 指定集合中信号量的数量
返回信号量集ID
```
用来创建或者改变信号量的权限，如果不是创建的话nsems可以设为0

### 改变信号量的属性
```cpp
int semctl(int semid, int semnum, int cmd, ...);

semnum:set中的第几个semaphore(从0开始计数)
cmd:要执行的的操作，如果此操作需要参数，那么使用第四个参数向其提供所需的参数。

第四个参数类型如下
union semun {
   int              val;    /* Value for SETVAL */
   struct semid_ds *buf;    /* Buffer for IPC_STAT, IPC_SET */
   unsigned short  *array;  /* Array for GETALL, SETALL */
   struct seminfo  *__buf;  /* Buffer for IPC_INFO (Linux-specific) */
};

struct semid_ds {
   struct ipc_perm sem_perm;  /* Ownership and permissions */
   time_t          sem_otime; /* Last semop time */
   time_t          sem_ctime; /* Last change time */
   unsigned long   sem_nsems; /* No. of semaphores in set */
};


struct ipc_perm {
   key_t          __key; /* Key supplied to semget(2) */
   uid_t          uid;   /* Effective UID of owner */
   gid_t          gid;   /* Effective GID of owner */
   uid_t          cuid;  /* Effective UID of creator */
   gid_t          cgid;  /* Effective GID of creator */
   unsigned short mode;  /* Permissions */
   unsigned short __seq; /* Sequence number */
};
```

### 读取或改变信号量
```cpp
//sops可以是一个数组，nsops指定了长度,所有操作要么都成功，要么都失败
//sem_flg可以是IPC_NOWAIT或SEM_UNDO,SEM_UNDO表示如果该进程已经终止了那么该操作就不会进行了
int semop(int semid, struct sembuf *sops, size_t nsops);
int semtimedop(int semid, struct sembuf *sops, size_t nsops,
              const struct timespec *timeout);
              
struct sembuf {
     unsiged short  sem_num;    /* semaphore index in array */
     short       sem_op;     /* semaphore operation */
     short       sem_flg;    /* operation flags */
};              


Each semaphore in a System V semaphore set has the following associated values:
unsigned short  semval;   /* semaphore value */
unsigned short  semzcnt;  /* # waiting for zero */
unsigned short  semncnt;  /* # waiting for increase */
pid_t           sempid;   /* PID of process that last*/


sem_op>0:会把它加到对应的semaphore value上
sem_op=0:
sem_op<0: 如果semval >= sem_op,那么the operation can proceed  immediately:  the  absolute  value  of sem_op is subtracted from semval

```



Valid values for cmd are:

SETVAL
示例
union semun tmp;
tmp.val = value;
semctl(sem_id, 0, SETVAL, tmp)



https://songlee24.github.io/2015/04/21/linux-IPC/





n
