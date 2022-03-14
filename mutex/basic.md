## 互斥 (mutual exclusion)，“互相排斥”

实现 lock_t 数据结构和 lock/unlock API:
```cpp
typedef struct {
  ...
} lock_t;
void lock(lock_t *lk);
void unlock(lock_t *lk);
```
一把 “排他性” 的锁——对于锁对象 lk
	如果某个线程持有锁，则其他线程的 lock 不能返回

### 在共享内存上实现互斥
(部分) 成功的尝试
peterson-barrier.c
实现互斥的根本困难：不能同时读/写共享内存

	load (环顾四周) 的时候不能写，只能 “看一眼就把眼睛闭上” 看到的东西马上就过时了
	store (改变物理世界状态) 的时候不能读，只能 “闭着眼睛动手” 也不知道把什么改成了什么

## 自旋锁 (Spin Lock)
 (软件不够，硬件来凑)
 假设硬件能为我们提供一条 “瞬间完成” 的读 + 写指令
请所有人闭上眼睛，看一眼 (load)，然后贴上标签 (store)
如果多人同时请求，硬件选出一个 “胜者”, “败者” 要等 “胜者” 完成后才能继续执行
	
	实现互斥：自旋锁
```cpp
int table = YES;

void lock() {
retry:
  int got = xchg(&table, NOPE);
  if (got == NOPE)
    goto retry;
  assert(got == YES);
}

void unlock() {
  xchg(&table, YES)
}
```

```cpp
int locked = 0;
void lock() { while (xchg(&locked, 1)) ; }
void unlock() { xchg(&locked, 0); }
```
