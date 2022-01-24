## 查看端口占用
lsof -i tcp:8055

## date
```sh
# 时间戳转时间
date -r 1460710262 "+%Y-%m-%d %H:%M:%S"
```

## jq
curl --location --request POST 'http://qa-live-sort.linkv.sg/liveSort/getNew?page_index=1&pageSize=30' | jq '.data | .video_info | .[] | .anchor_level,.vid'

## tcpdump

```sh
-i : 选择要捕获的接口，通常是以太网卡或无线网卡
-nn : 单个 n 表示不解析域名，直接显示 IP；两个 n 表示不解析域名和端口。（解析的话就会这样显示:localhost.localdomain.webcache）
-l  如果想实时将抓取到的数据通过管道传递给其他工具来处理，需要使用 -l 选项来开启行缓冲模式
-v 显示详细信息
-X : Show the packet’s contents in both hex and ascii.

tcpdump -i ens33  port 8080 -nn
> 
tcpdump -i ens33  port 8080 -nn -v -l | grep -i  "Host:"   #提取 HTTP 用户代理

```



```sh
过滤器
port: 端口过滤器，表示仅抓取指定端口上的流量
host: 过滤主机
net : 过滤网段,可以使用四元组（x.x.x.x）、三元组（x.x.x）、二元组（x.x）,三元组表示子网掩码为 255.255.255.0
proto: 过滤协议, 因为通常的协议名称是保留字段，所以在使用时，必须根据 sh 类型使用一个或两个反斜杠（/）来转义。Linux 中的 sh 需要使用两个反斜杠来转义，MacOS 只需要一个。如 proto \\icmp

tcpdump host 1.2.3.4      该命令会抓取所有发往主机 1.2.3.4 或者从主机 1.2.3.4 发出的流量。如果想只抓取从该主机发出的流量，可以使用下面的命令：
tcpdump src host 1.2.3.4

过滤的真正强大之处在于你可以随意组合它们，而连接它们的逻辑就是常用的
and or &&
or or ||
not or !

```



![](../../../../../youdaonote-images/90DE9C83E2D54D34B04070BE04743CA3.png)

ACK 也就是我们所熟悉的ack包，用来告诉对方上一个数据包已经成功收到。不过一般不会为了ack单独发送一个包，都是在下一个要发送的packet里设置ack位

PSH 接收方接收到P位的flag包需要马上将包交给应用层处理，一般我们在http request的最后一个包里都能看到P位被设置。





![](../../../../../youdaonote-images/F75B7D6DCD754AADB1FB786052334A70.png)

最基本的信息就是数据报的源地址/端口和目的地址/端口，上面的例子第一条数据报中，源地址 ip 是 192.168.39.1，源端口是 10879，目的地址是 192.168.39.129，目的端口是 8080。 > 符号代表数据的方向。

常见的 TCP 报文的 Flags:

- [S] : SYN（开始连接）

- [.] : 没有 Flag

- [P] : PSH（推送数据）

- [F] : FIN （结束连接）

- [R] : RST（重置连接）

- [S.]     SynAcK Packet









谷歌浏览器发送请求

![](../../../../../youdaonote-images/8CA299DACDA04D69B234169295B11032.png)



SpringBoot 返回响应

![](../../../../../youdaonote-images/90BA0891293C4758B8EAC6E9B7F7F791.png)



