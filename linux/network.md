```sh
# 创建一个名为netns1的network namespace
ip netns add netns1

# 列出系统中有所有network namespace
ip netns list

#进入netns1这个network namespace查询网卡信息
ip netns exec netns1 ip link list
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00

ip netns exec netns1 ping 127.0.0.1
ping: connect: Network is unreachable
```
