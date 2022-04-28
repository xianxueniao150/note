以下均为POSIX标准

## 获取当前线程id
```cpp
pthread_t pthread_self(void);
```

## 创建线程
```cpp
#include <pthread.h>
int pthread_create(pthread_t *thread, const pthread_attr_t *attr,
                          void *(*start_routine) (void *), void *arg);
```
On success, pthread_create() returns 0; on error, it returns an error number

## 等待线程结束
```cpp
int pthread_join(pthread_t thread, void **retval);
```
retval是上面pthread_exit传过来的值

## 线程终止
```cpp
void pthread_exit(void *retval);
```

## 线程清理
```cpp
void pthread_cleanup_push(void (*routine)(void *), void *arg);
void pthread_cleanup_pop(int execute);
```
上面两个是宏，必须配对使用

## 线程取消
```cpp
int pthread_cancel(pthread_t thread);
int pthread_setcancelstate(int state, int *oldstate); //设置是否允许取消
int pthread_setcanceltype(int type, int *oldtype);  //设置取消方式
void pthread_testcancel(void);  //添加一个取消点
```
取消有两种状态：允许和不允许
允许取消又分为：异步cancel，推迟cancel（默认）->推迟至cancel点再响应
cancel点，POSIX定义的cancel点，都是可能引发阻塞的系统调用




