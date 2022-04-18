共享内存是内核在物理内存中预留了一片空间用于进程间的通信，这部分内存空间不属于任何一个进程，但每个进程都可以访问它们(通过建立映射)。
共享内存是进程间通信最简单的方式，但是读取和写入必须同步。

我们可以在终端中使用 ipcs -m 查看系统当前开辟的共享内存：

## 相关系统调用
### shmget 创建或者获取共享内存
```cpp
// 成功返回共享内存的标识符，否则返回-1
int shmget(key_t key, size_t size, int shmflg);

size:我们需要共享内存的大小，
shmflg:共享内存的标志位。最后9位是访问权限，要创建新的共享内存需要使用shmflg | IPC_CREA 
```

### shmat 建立映射
```cpp
// 成功返回共享内存的映射的地址，失败返回-1
void *shmat(int shmid, const void *shmaddr, int shmflg);

shmaddr:映射地址，一般设置成NULL，这样内核会自动分配一块空间(也便于移植)；
shmflg:一般不用设置，只填0就行了。
```

### shmdt 解除映射
```cpp
// 成功返回0，否则返回-1
int shmdt(const void *shmaddr);
```
shmdt()函数只是断开进程和共享内存的映射，并没有销毁共享内存，要销毁共享内存需要使用函数shmctl()。

### shmctl()
shmctl()函数原型如下：
```cpp
// 大部分命令成功返回0，所有命令失败都返回-1
int shmctl(int shmid, int cmd, struct shmid_ds *buf);

cmd:
	IPC_RMID 销毁,buf传入NULL
```

### 共享内存实例

#### 写操作
```cpp
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 1. 创建 SHM
    int shm_id = shmget(13, 2048, IPC_CREAT | 0666);
    if (shm_id != -1) {
    	// 2. 映射 SHM
    	void* shm = shmat(shm_id, NULL, 0);
    	if (shm != (void*)-1) {
    	    // 3. 写 SHM
    	    char str[] = "I'm share memory";
    	    memcpy(shm, str, strlen(str) + 1);
    	    // 4. 关闭 SHM
    	    shmdt(shm);
    	} else {
    	    perror("shmat:");
    	}
    } else {
    	perror("shmget:");
    }
    return 0;
}
```

```cpp
ubuntu@VM-12-3-ubuntu:~/unix_pro$ ipcs
------ Shared Memory Segments --------
key        shmid      owner      perms      bytes      nattch     status
0x00000000 0          root       644        80         2
0x00000000 1          root       644        16384      2
0x00000000 2          root       644        280        2
0x0000000d 4          ubuntu     666        2048       0
```

#### 读操作
```cpp
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 1. 获取 SHM
    int shm_id = shmget(13, 2048, IPC_CREAT | 0666);
    
    if (shm_id != -1) {
    	// 2. 映射 SHM
    	void* shm = shmat(shm_id, NULL, 0);
    	if (shm != (void*)-1) {
    	    // 3. 读取 SHM
    	    char str[50] = { 0 };
    	    memcpy(str, shm, strlen("I'm share memory"));
    	    printf("shm = %s\n", (char *)shm);
    	    // 4. 关闭 SHM
    	    shmdt(shm);
    	} else {
    	    perror("shmat:");
    	}
    } else {
        perror("shmget:");
    }
    if (0 == shmctl(shm_id, IPC_RMID, NULL))
    	printf("delete shm success.\n");
    return 0;
}
```
