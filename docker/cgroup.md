
```sh
[root@VM-12-3-centos ~]# ll /sys/fs/cgroup/
总用量 0
dr-xr-xr-x 2 root root  0 10月 26 09:32 blkio
lrwxrwxrwx 1 root root 11 10月 26 09:32 cpu -> cpu,cpuacct
lrwxrwxrwx 1 root root 11 10月 26 09:32 cpuacct -> cpu,cpuacct
dr-xr-xr-x 3 root root  0 10月 26 09:32 cpu,cpuacct
dr-xr-xr-x 2 root root  0 10月 26 09:32 cpuset
dr-xr-xr-x 4 root root  0 10月 26 09:32 devices
dr-xr-xr-x 2 root root  0 10月 26 09:32 freezer
dr-xr-xr-x 2 root root  0 10月 26 09:32 hugetlb
dr-xr-xr-x 4 root root  0 10月 26 09:32 memory
lrwxrwxrwx 1 root root 16 10月 26 09:32 net_cls -> net_cls,net_prio
dr-xr-xr-x 2 root root  0 10月 26 09:32 net_cls,net_prio
lrwxrwxrwx 1 root root 16 10月 26 09:32 net_prio -> net_cls,net_prio
dr-xr-xr-x 2 root root  0 10月 26 09:32 perf_event
dr-xr-xr-x 2 root roo  0 10月 26 09:32 pids
dr-xr-xr-x 4 root root  0 10月 26 09:32 systemdt
```

比如我们想限制当前进程可以使用的内存,就可以进入memory目录下，创建自己的文件夹
```sh
#创建一个cgroup
[root@VM-12-3-centos memory]# mkdir test-limit-memory
[root@VM-12-3-centos memory]# cd test-limit-memory/
#设置最大cgroup的最大内存占用为lOOMB
[root@VM-12-3-centos test-limit-memory]# echo 100m > memory.limit_in_bytes
#将当前进程移动到这个cgroup中
[root@VM-12-3-centos test-limit-memory]# echo $$ >tasks
#再次运行占用内存200MB的stressj进程
[root@VM-12-3-centos test-limit-memory]# stress --vm-bytes 200m --vm-keep -m 1
stress: info: [22235] dispatching hogs: 0 cpu, 0 io, 1 vm, 0 hdd
stress: FAIL: [22235] (415) <-- worker 22236 got signal 9
stress: WARN: [22235] (417) now reaping child worker processes
stress: FAIL: [22235] (451) failed run completed in 0s
```
