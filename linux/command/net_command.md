## tcpdump
```sh
-i : 选择要捕获的接口，通常是以太网卡或无线网卡
-nn : 单个 n 表示不解析域名，直接显示 IP；两个 n 表示不解析域名和端口。（解析的话就会这样显示:localhost.localdomain.webcache）
-l  如果想实时将抓取到的数据通过管道传递给其他工具来处理，需要使用 -l 选项来开启行缓冲模式
-v 显示详细信息
-X : Show the packet’s contents in both hex and ascii.

tcpdump -i ens33  port 8080 -nn
tcpdump -i ens33  port 8080 -nn -v -l | grep -i  "Host:"   #提取 HTTP 用户代理


过滤器
	port: 端口过滤器，表示仅抓取指定端口上的流量
	host: 过滤主机
	net : 过滤网段,可以使用四元组（x.x.x.x）、三元组（x.x.x）、二元组（x.x）,三元组表示子网掩码为 255.255.255.0
	proto: 过滤协议, 因为通常的协议名称是保留字段，所以在使用时，必须根据 sh 类型使用一个或两个反斜杠（/）来转义。Linux 中的 sh 要使用两个反斜杠来转义，MacOS 只需要一个。如 proto \\icmp

tcpdump host 1.2.3.4      该命令会抓取所有发往主机 1.2.3.4 或者从主机 1.2.3.4 发出的流量。如果想只抓取从该主机发出的流量，可以使用下面的命令：
tcpdump src host 1.2.3.4

过滤的真正强大之处在于你可以随意组合它们，而连接它们的逻辑就是常用的
and or &&
or or ||
not or !
```

### 返回数据

> 符号代表数据的方向。

常见的 TCP 报文的 Flags:
- [S] : SYN（开始连接）
- [.] : 没有 Flag
- [P] : PSH（推送数据）
- [F] : FIN （结束连接）
- [R] : RST（重置连接）
- [S.]     SynAcK Packet


## lsof 显示Linux系统当前已打开的所有文件列表
```sh
#列出指定进程号所打开的文件:
lsof -p $pid

lsof -i tcp:8055
```

## date

```sh
# 时间戳转时间
date -r 1460710262 "+%Y-%m-%d %H:%M:%S"
```

![](../../../../../youdaonote-images/90BA0891293C4758B8EAC6E9B7F7F791.png)


minikube start --image-repository registry.cn-hangzhou.aliyuncs.com/google_containers

## curl
https://curl.se/docs/manual.html
```sh
-L 参数会让 HTTP 请求跟随服务器的重定向
-v 详细输出，包含请求和响应的首部

# 最基本的GET请求
 curl http://127.0.0.1:8080/login?name=admin&passwd=12345678
 
#添加json
curl -X POST -H "Content-Type:application/json" --data '{"dmac": "00:0C:29:EA:39:70"}' https://cms-api-qa.vvork.net/audit/callback

#添加表单
curl --data "birthyear=1905&press=%20OK%20"  http://www.example.com/when.cgi
# 使用URL编码
curl --data-urlencode "name=I am Daniel" http://www.example.com

#文件上传
curl --form upload=@localfilename --form press=OK [URL]
```

## wget 下载命令

## nc(可以连接redis）
yum install -y nc
```sh
-l		Listen mode, for inbound connects
-p		Specify local port for remote connects
-u		UDP mode
-v
```


聊天
```sh
Server
$nc -l -p 1567     #netcat 命令在1567端口启动了一个tcp 服务器

Client
$nc 172.31.100.7 1567
不管你在机器B上键入什么都会出现在机器A上。
```


# 监控

## dstat 查看网络流量
```sh
yum install -y dstat
dstat -tnf 1 10    #输出接下来10秒内每秒的网络数据
```

## netstat 查看Linux中网络系统状态信息
可以看到tcp建立的每一条连接，包括正在尝试建立的
```sh
-t或--tcp：显示TCP传输协议的连线状况；
-a或--all：显示所有连线中的Socket；
-n或--numeric：直接使用ip地址，而不通过域名服务器；


netstat -rn   #查看网关设置
```

## ss 比 netstat 好用的socket统计信息
```sh
#统计当前活跃的连接数
ss -n | grep ESTAB | wc -l  
```

## nload 可以查看各个网络设备的当前网络速率，也会展示流经设备的总流量。
```sh
#查看eth0网卡流量 
nload eth0
```

## tc 模拟 网络延迟、网络丢包、网络中断
```sh
tc [ OPTIONS ] OBJECT COMMAND 

command: add/delete/change


# 该命令将网卡 ens33 的传输设置为延迟300ms发送
sudo tc qdisc add dev ens33 root netem delay 300ms

#对应的删除命令
sudo tc qdisc del dev ens33 root netem

#模拟网络丢包,随机丢掉 30% 的数据包
sudo tc qdisc add dev ens33 root netem loss 30%

#模拟网络中断,随机产生 30% 的损坏的数据包
sudo tc qdisc add dev ens33 root netem corrupt 30%

#模拟乱序,delay 必须要指定，设置为30%的数据包会被立即发送，其他延迟1秒
sudo tc qdisc change  dev ens33 root netem delay 1000ms reorder 30%
```

## tcconfig
https://github.com/thombashi/tcconfig
```sh
sudo tcset lo --delay 200ms --loss 30% --port 9981
sudo tcshow lo
```

## Linux终端聊天 write，wall
```sh
who 查看一下哪些人登录：
heylin   tty7         2010-05-03 20:17 (:0)
heylin   pts/2        2010-05-03 20:24 (t.xiaoji.com)
heylin   pts/4        2010-05-03 22:28 (:0.0)
heylin   pts/5        2010-05-03 22:08 (debian-2.local)

pts/2是我登录的，pts/5是某人的。pts/4是他登录的 tty7是gnome的
命令格式：write heylin /dev/pts/4  回车
输入消息：hello, msg from xiaoji
不过不支持中文。write执行后，可以接受别人的消息，也可以继续发消息，但如果一开始是别人先发送给你，你就必须再打开一个终端才能发消息。

wall ，wall命令是广播，所有的人都可以收到。
echo "hello,This is a message" | wall

通过管道发送。
Linux的聊天蛮有意思的，不过，如果你正在终端编辑一个文件，那就惨了，因为消息会直接插入到你的编辑文件中！慎用~

```

## sysctl 查看参数值
```sh
sysctl -n net.ipv4.tcp_keepalive_time
```

## ip
```sh
# 显示网络设备的运行状态
ip link list
```

```sh
ip [ OPTIONS ] OBJECT { COMMAND | help }

常用对象的取值含义如下：
	link：网络设备
	address：设备上的协议（IP或IPv6）地址
	addrlabel：协议地址选择的标签配置
	route：路由表条目
	rule：路由策略数据库中的规则
```

## route 查看路由表
```sh
-n 名称转换为ip地址


```
字段解释:
	flags:G表示路由为网关















