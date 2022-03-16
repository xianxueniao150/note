条件变量
```cpp
//初始化条件变量
int pthread_cond_init(pthread_cond_t *restrict cond, const pthread_condattr_t *restrict attr);
int pthread_cond_destroy(pthread_cond_t *cond);

pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

//用于等待目标条件变量。该函数调用时需要传入 mutex参数(加锁的互斥锁) ，函数执行时，先把调用线程放入条件变量的请求队列，然后将互斥锁mutex解锁，当函数成功返回为0时，表示重新抢到了互斥锁，互斥锁会再次被锁上， 也就是说函数内部会有一次解锁和加锁操作.
int pthread_cond_wait(pthread_cond_t *restrict cond, pthread_mutex_t *restrict mutex);

int pthread_cond_broadcast(pthread_cond_t *cond);  //叫醒所有
int pthread_cond_signal(pthread_cond_t *cond);  //叫醒任意一个

int pthread_cond_timedwait(pthread_cond_t *restrict cond,
           pthread_mutex_t *restrict mutex,
           const struct timespec *restrict abstime);   //可以设置等待时间
```

## 使用pthread_cond_wait方式如下：
```cpp
pthread _mutex_lock(&mutex)

while(线程执行的条件是否成立){
    pthread_cond_wait(&cond, &mutex);
}

pthread_mutex_unlock(&mutex);
```

### pthread_cond_wait执行后的内部操作分为以下几步：
1. 将线程放在条件变量的请求队列后，内部解锁
2. 线程等待被pthread_cond_broadcast信号唤醒或者pthread_cond_signal信号唤醒，唤醒后去竞争锁
3. 若竞争到互斥锁，内部再次加锁

### 为什么判断线程执行的条件用while而不是if？
一般来说，在多线程资源竞争的时候，在一个使用资源的线程里面（消费者）判断资源是否可用，不可用，便调用pthread_cond_wait，在另一个线程里面（生产者）如果判断资源可用的话，则调用pthread_cond_signal发送一个资源可用信号。

在wait成功之后，资源就一定可以被使用么？答案是否定的，如果同时有两个或者两个以上的线程正在等待此资源，wait返回后，资源可能已经被使用了。
再具体点，有可能多个线程都在等待这个资源可用的信号，信号发出后只有一个资源可用，但是有A，B两个线程都在等待，B比较速度快，获得互斥锁，然后加锁，消耗资源，然后解锁，之后A获得互斥锁，但A回去发现资源已经被使用了，它便有两个选择，一个是去访问不存在的资源，另一个就是继续等待，那么继续等待下去的条件就是使用while，要不然使用if的话pthread_cond_wait返回后，就会顺序执行下去。

所以，在这种情况下，应该使用while而不是if
