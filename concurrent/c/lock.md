
## 互斥量
#### 初始化
```cpp
int pthread_mutex_destroy(pthread_mutex_t *mutex);
int pthread_mutex_init(pthread_mutex_t *restrict mutex, const pthread_mutexattr_t *restrict attr);
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER; //使用默认属性初始化
```
Posix互斥锁被声明为具有pthread_mutex_t数据类型的变量。
如果互斥锁变量是静态分配的，那么我们可以把它初始化成常值PTHREAD_MUTEX_INITIALIZER
如果互斥锁是动态分配的（例如通过调用malloc）,或者分配在共享内存区中，那么我们必须在运行之时通过调用pthread_mutex_init函数来初始化它
你可能会碰到省略了初始化操作的代码，因为它所在的实现把初始化常值定义为0（而且静态分配的变量被自动地初始化为0).不过这是不正确的代码.


#### 上锁和解锁
```cpp
int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_trylock(pthread_mutex_t *mutex);
int pthread_mutex_unlock(pthread_mutex_t *mutex);
```
pthread_mutex_trylock是对应的非阻塞函数，如果该互斥锁己锁住， 它就返回一个EBUSY错误

如果有多个线程阻塞在等待同一个互斥锁上，那么当该互斥锁解锁时，哪一个线程会开始运行呢？ 
不同线程可被赋予不同的优先级，同步函数(互斥锁、 读写锁、信号量)将唤醒优先级最高的被阻塞线程
