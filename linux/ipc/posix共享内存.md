## 打开和删除
```cpp
 #include <sys/mman.h>
#include <sys/stat.h>        /* For mode constants */
#include <fcntl.h>           /* For O_* constants */

int shm_open(const char *name, int oflag, mode_t mode);

oflag:
	0_TRUNC:所需的共享内存区对象巳经存在，那么它将被截短成0长度。
返冋值是一个整数描述符，它随后用作mmap的第五个参数。

int shm_unlink(const char *name);
```
Link with -lrt.
