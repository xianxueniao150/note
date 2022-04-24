## df      
磁盘情况查询
查询系统整体磁盘使用情况
df -h



## du (disk usage)
查询指定目录的磁盘占用情况，默认为当前目录
基本语法
```sh
du -h    /目录

-s 指定目录占用大小汇总
-h 带计量单位
-a 含文件
--max-depth=1    子目录深度
-c 列出明细的同时，增加汇总值

mac例
du -mh -d=2 *  #查询当前目录每个文件夹的大小
du -ach --max-depth=1 /root/nginx-1.10.1

linux例
# 查看当前目录总共占的容量，而不单独列出各子项占用的容量 ，在所在目录输入du -sh：
du -sh

# 查看当前目录下一级子文件和子目录占用的磁盘容量：
du -h --max-depth=1
# 或者
du -sh *
# 并且排序
du -sh * | sort -n

# 查看指定文件大小可以使用du -sh：
du -sh installmongofor3.6.log
```


## dd
复制文件
dd if=/dev/zero of=sun.txt bs=1M count=1

该命令创建了一个1M大小的文件sun.txt，其中参数解释：
if 代表输入文件。如果不指定if，默认就会从stdin中读取输入。
of 代表输出文件。如果不指定of，默认就会将stdout作为默认输出。
bs 代表字节为单位的块大小。
count 代表被复制的块数。
/dev/zero 是一个字符设备，会不断返回0值字节（\0）。
/dev/urandom


