## 示例 makefile
```sh
mymain:main.o tool1.o tool2.o
	gcc main.o tool1.o tool2.o -o mymain

main.o:main.c
	gcc main.c -c -o main.o

tool1.o:tool1.c
	gcc tool1.c -c -o tool1.o

tool2.o:tool2.c
	gcc tool2.c -c -o tool2.o

clean:
	rm *.o mymain -rf
```

变量替换
CC默认值就是gcc
```cpp
OBJS=main.o tool1.o tool2.o
CFLAGS+=-c -Wall -g

mymain:$(OBJS)
	$(CC) $^ -o $@ 

main.o:main.c
	$(CC) $^  $(CFLAGS) -o $@

tool1.o:tool1.c
	$(CC) $^  $(CFLAGS) -o $@

tool2.o:tool2.c
	$(CC) $^  $(CFLAGS) -o $@

clean:
	rm *.o mymain -rf
```


再简化
```cpp
OBJS=main.o tool1.o tool2.o
CFLAGS+=-c -Wall -g

mymain:$(OBJS)
	$(CC) $^ -o $@ 

%.o:%.c
	$(CC) $^  $(CFLAGS) -o $@


clean:
	rm *.o mymain -rf
```

## 单个文件
单个文件可以不需要makefile
安装完make命令后直接敲

## 语法
### 回声（echoing）
正常情况下，make会打印每条命令，然后再执行，这就叫做回声（echoing）。
在命令的前面加上@，就可以关闭回声。

## .PHONY
在Makefile中，.PHONY后面的target表示的也是一个伪造的target, 而不是真实存在的文件target，注意Makefile的target默认是文件。
```sh
$ cat -n Makefile1
     1    clean:
     2        rm -f foo
$ cat -n Makefile2
     1    .PHONY: clean
     2    clean:
     3        rm -f foo
     
$ touch clean
$ ls -l
total 8
-rw-r--r-- 1 huanli huanli  0 Jul 13 18:06 clean
-rw-r--r-- 1 huanli huanli 18 Jul 13 17:51 Makefile1
-rw-r--r-- 1 huanli huanli 32 Jul 13 17:51 Makefile2
$ make -f Makefile1 clean
make: 'clean' is up to date.
$ make -f Makefile2 clean
rm -f foo     
```

区别来了，Makefile1拒绝了执行clean, 因为文件clean存在。而Makefile2却不理会文件clean的存在，总是执行clean后面的规则。

## 隐含规则
### 老式风格的“后缀规则”¶
后缀规则是一个比较老式的定义隐含规则的方法。后缀规则会被模式规则逐步地取代。因为模式规则更强更清晰。
为了和老版本的Makefile兼容，GNU make同样兼容于这些东西。后缀规则有两种方式：“双后缀”和“单后缀”。
双后缀规则定义了一对后缀：目标文件的后缀和依赖目标（源文件）的后缀。如 .c.o 相当于 %o : %c 。单后缀规则只定义一个后缀，也就是源文件的后缀。如 .c 相当于 % : %.c 。
