条件变量
```cpp
//初始化条件变量
int pthread_cond_init(pthread_cond_t *restrict cond, const pthread_condattr_t *restrict attr);
int pthread_cond_destroy(pthread_cond_t *cond);

pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

int pthread_cond_wait(pthread_cond_t *restrict cond, pthread_mutex_t *restrict mutex);

int pthread_cond_broadcast(pthread_cond_t *cond);  //叫醒所有,开销会大一点，但是更稳妥
int pthread_cond_signal(pthread_cond_t *cond);  //叫醒任意一个

//abstime指定这个函数必须返回时的系统时间，即便当时相应的条件变量还没有收到信号。如果发生这种超时情况，该函数就返回ETIMEDOU偏误。
//时间值是绝对时间,而不是时间差.这就是说，abstime是该函数应该返回时刻的系统时间——自UTC吋间1970年1月1日子时以来流逝的秒数和纳秒数。使用绝对时间而不是时冋差的好处是：如果函数过早返回了（也许是因为捕获了某个信号），那么同一函数无需改变其参数中timespec结构的内容就能再次被调用。
int pthread_cond_timedwait(pthread_cond_t *restrict cond, pthread_mutex_t *restrict mutex, const struct timespec *restrict abstime);   //可以设置等待时间
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
4. 如果没抢到锁的话，应该就是阻塞在强锁的过程中，而不是阻塞在wait上（猜想）

### 为什么判断线程执行的条件用while而不是if？
一般来说，在多线程资源竞争的时候，在一个使用资源的线程里面（消费者）判断资源是否可用，不可用，便调用pthread_cond_wait，在另一个线程里面（生产者）如果判断资源可用的话，则调用pthread_cond_signal发送一个资源可用信号。

- 在wait成功之后，资源就一定可以被使用么？答案是否定的，如果同时有两个或者两个以上的线程正在等待此资源，wait返回后，资源可能已经被使用了。 再具体点，有可能多个线程都在等待这个资源可用的信号，信号发出后只有一个资源可用，但是有A，B两个线程都在等待，B速度比较快，获得互斥锁，然后加锁，消耗资源，然后解锁，之后A获得互斥锁，但A回去发现资源已经被使用了.
- 在一些实现上，即使没有其他线程对这个条件变量产生信号，等待着这个条件变量的线程也有可能被唤醒。
- 阻塞的系统调用也可能因为信号等其他错误，就导致线程被唤醒，系统调用相应返回失败。
