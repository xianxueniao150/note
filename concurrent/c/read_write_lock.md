
问题:
1. 如果有一个请求写锁的线程阻塞在读锁上，此时又来了一个请求读锁的线程，这个请求读锁的线程会不会阻塞住（如果不阻塞的话请求写锁的线程可能永远都抢不到锁，饿死）

## API
POSIX 标准中，读写锁用 pthread_rwlock_t 类型的变量表示
```cpp
pthread_rwlock_t myRWLock;
```
由此，我们就成功创建了一个读写锁。但要想使用 myRWLock 读写锁，还需要进行初始化操作。

### 初始化读写锁
初始化读写锁的方法有两种
```cpp
pthread_rwlock_t myRWLock = PTHREAD_RWLOCK_INITIALIZER;
int pthread_rwlock_init(pthread_rwlock_t *rwlock, const pthread_rwlockattr_t *attr);
```

当 pthread_rwlock_init() 函数初始化成功时，返回数字 0，反之返回非零数。

### 线程发出“读锁”请求
```cpp
int pthread_rwlock_rdlock(pthread_rwlock_t* rwlock);
int pthread_rwlock_tryrdlock(pthread_rwlock_t* rwlock);
```

当读写锁处于“无锁”或者“读锁”状态时，以上两个函数都能成功获得读锁；当读写锁处于“写锁”状态时：
- pthread_rwlock_rdlock() 函数会阻塞当前线程，直至读写锁被释放；
- pthread_rwlock_tryrdlock() 函数不会阻塞当前线程，直接返回 EBUSY。

以上两个函数如果能成功获得读锁，函数返回数字 0，反之返回非零数。

### 线程发出“写锁”请求
```cpp
int pthread_rwlock_wrlock(pthread_rwlock_t* rwlock);
int pthread_rwlock_trywrlock(pthread_rwlock_t* rwlock); 
```

当读写锁处于“无锁”状态时，两个函数都能成功获得写锁；当读写锁处于“读锁”或“写锁”状态时：
- pthread_rwlock_wrlock() 函数将阻塞线程，直至读写锁被释放；
- pthread_rwlock_trywrlock() 函数不会阻塞线程，直接返回 EBUSY。

以上两个函数如果能成功获得写锁，函数返回数字 0，反之返回非零数。

### 释放读写锁
无论是处于“无锁”、“读锁”还是“写锁”的读写锁，都可以使用如下函数释放读写锁：
```cpp
int pthread_rwlock_unlock (pthread_rwlock_t* rwlock);
```

当函数成功释放读写锁时，返回数字 0，反之则返回非零数。注意，由于多个线程可以同时获得“读锁”状态下的读写锁，这种情况下一个线程释放读写锁后，读写锁仍处于“读锁”状态，直至所有线程都释放读写锁，读写锁的状态才为“无锁”状态。

### 销毁读写锁
```cpp
int pthread_rwlock_destroy(pthread_rwlock_t* rwlock);
```

如果函数成功销毁指定的读写锁，返回数字 0，反之则返回非零数。
