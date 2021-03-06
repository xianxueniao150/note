
根据初始值的不同，信号量可以细分为 2 类，分别为二进制信号量和计数信号量：
- 二进制信号量：指初始值为 1 的信号量，此类信号量只有 1 和 0 两个值，通常用来替代互斥锁实现线程同步；
- 计数信号量：指初始值大于 1 的信号量，当进程中存在多个线程，但某公共资源允许同时访问的线程数量是有限的（出现了“狼多肉少”的情况），这时就可以用计数信号量来限制同时访问资源的线程数量。

二进制信号量
```cpp
sem_t mySem = sem_open(SEM_MUTEX, O_CREAT | O_EXCL, FILE_MODE, 1);

//相当于上锁
sem_wait(&mySem);
...
//相当于解锁
sem_post(&mySem);
```


#### 创建有名信号量
```cpp
 #include <semaphore.h>
sem_t *sem_open(const char *name, int oflag);
sem_t *sem_open(const char *name, int oflag, mode_t mode, unsigned int value);
```

#### 关闭和删除有名信号量
```cpp
// 关闭打开的信号量，进程终止时自动调用
int sem_close(sem_t *sem);

// 删除信号量
int sem_unlink(const char *name);
```

#### 创建和删除基于内存的信号量
```cpp
int sem_init(sem_t *sem, int pshared, unsigned int value);
int sem_destroy(sem_t *sem);

sem:指向应用程序必须分配的sem_t变量。 
shared:为0，那么待初始化的信号量是在同一进程的各个线程间共享的
	   非0，该信号量是在进程间共享的。此时该信号量必须存放在某种类型的共享内存区中，并且即将使 用它的所有进程都要能访问该共享内存区。
value:该信号量的初始值。
```
Posix有名信号量:这些信号量由一个参数标识，它通常指代文件系统中的某个文件。
然而Posix也提供基于内存的信号量，它们由应用程序分配信号量的内存空间（也就是分配一个sem_t数据类型的内存空间），然后由系统初始化它们的值。
sem_open和sem_init的基本差异:前者返回一个指向某个sem_t 变量的指针，该变量由（sem_open）函数本身分配并初始化.后者的第一个参数是一个指向某个sem_t变量的指针，该变量由调用者分配，然后由（sem_init ）函数初始化.

彼此无亲缘关系的 不同进程需使用信号量时，通常使用有名信号量。其名字就是各个进程标识信号量的手段。
基于内存的信号量至少具有随进程的持续性，然而它们真正的持续性 却取决于存放信号量的内存区的类型。只要含有某个基于内存信号量的内存区保持有效，该信号量就一直存在。
- 如果某个基于内存的信号量是由单个进程内的各个线程共享的,那么该信号量具有随进程的持续性，当该进程终止时它也消失。
- 如果某个基于内存的信号量是在不同进程间共享的,那么该信号量必须存放在共享内存区中，因而只要该共享内存区仍然存在，该信号量也就继续存在。

#### wait
```cpp
int sem_wait(sem_t *sem);
int sem_trywait(sem_t *sem);
int sem_timedwait(sem_t *sem, const struct timespec *abs_timeout);
```
sem_wait函数测试所指定信号量的值，如果该值大于0,那就将它减1并立即返冋。如果该值等于0,调用线程就被投入睡眠中，直到该值变为大于0,这时再将它减1,函数随后返冋。考虑到访问同一信号量的其他线程，“测试并减1"操作必须是原子的。

#### post
```cpp
int sem_post(sem_t *sem);
```
把所指定信号量的值加1,然后唤醒正在等待该信号量值变为正数的任意线程。

#### getvalue
```cpp
int sem_getvalue(sem_t *sem, int *sval);
```
sem_getvalue在由sval指向的整数中返回所指定信号量的当前值。如果该信号量当前己上锁，那么返回值或为0,或为某个负数，其绝对值就是等待该信号量解锁的线程数(取决于实现,Linux这种情况下只会返回0)


## 互斥锁、信号量比较
- 互斥锁必须总是由给它上锁的线程解锁。信号量没有这种限制
- 任何线程都可以挂出一个信号（譬如说将它的值由0增为1),即使当时没有线程在等待该信号量值变为正数也没有关系。然而，如果某个线程调用了pthread_cond_signal,并且当时没有任何线程阻塞在pthread_cond_wait调用中，那么发往相应条件变量的信号将丢失。
