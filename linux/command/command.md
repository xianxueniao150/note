## 进制转换
```sh
# 10进制转为16进制
$ echo 'ibase=10;obase=16;800'|bc
$ printf %x 880
```

## 计算
```sh
$ python -c "print(64*14)"
# 计算结果用16进制打印
$ python -c "print('0x%x'%(0x2a8+0x74))"
```

## ps
f：显示树状结构，表达程序间的相互关系。
x：显示所有程序，不以终端机来区分。
u：以用户为主的格式来显示程序状况。


## time 查看程序运行时间
```sh
# 命令行查看程序运行时间，并且不打印程序运行结果
time XXX > /dev/null
```

## less
-R 输出彩色

## ls
```sh
ls -lht  
-h		以人们可读的格式，而不是以字节数来显示文件的大小。
-l		以长格式显示结果。
-r		以相反的顺序来显示结果。通常，ls 命令的输出结果按照字母升序排列。
-S		命令输出结果按照文件大小来排序。
-t		按照修改时间来排序。


ls 长格式列表的字段
字段	含义
-rw-r--r--	对于文件的访问权限。第一个字符指明文件类型。
            在不同类型之间， 开头的“－”说明是一个普通文件，“d”表明是一个目录。
            其后三个字符是文件所有者的访问权限，再其后的三个字符是文件所属组中成员的访问权限，
            最后三个字符是其他所有人的访问权限。
1	         文件的硬链接数目

ls -lht | head -n 5  显示前几行
ls -lht | sed -n '4,4p'   显示指定行

```


## tar
```sh
#这条命令是将所有.jpg的文件打成一个名为all.tar的包。-c是表示产生新的包，-f指定包的文件名。
tar -cf all.tar *.jpg 
# 解压到im文件夹，im文件夹必须提前创建好
tar -xvf a.tar -C im

基础选项（必须）
	-c: 建立压缩档案
	-x：解压
	-t：查看内容
	-r：向压缩归档文件末尾追加文件
	-u：更新原压缩包中的文件

这五个是独立的命令，压缩解压都要用到其中一个，可以和别的命令连用但只能用其中一个。

下面的参数是根据需要在压缩或解压档案时可选的。
	-v：显示所有过程


参数-f是必须的
-f: 使用档案名字，切记，这个参数是最后一个参数，后面只能接档案名。
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

## 查看端口占用

lsof -i tcp:8055

## date

```sh
# 时间戳转时间
date -r 1460710262 "+%Y-%m-%d %H:%M:%S"
```

![](../../../../../youdaonote-images/90BA0891293C4758B8EAC6E9B7F7F791.png)


minikube start --image-repository registry.cn-hangzhou.aliyuncs.com/google_containers

## curl
-L 参数会让 HTTP 请求跟随服务器的重定向
-v 详细输出，包含请求和响应的首部

添加json
curl -X POST -H "Content-Type:application/json" --data '{"dmac": "00:0C:29:EA:39:70"}' https://cms-api-qa.vvork.net/audit/callback

## grep

```sh
显示匹配某个结果之后的3行，使用 -A 选项：
显示匹配某个结果之前的3行，使用 -B 选项：
显示匹配某个结果的前三行和后三行，使用 -C 选项：

* 和 + 限定符都是贪婪的，因为它们会尽可能多的匹配文字，只要在它们的后面加上一个?就可以实现懒惰或最小匹配
  grep -oP "app:.*?;"

cat access.log | grep -v '"time":0.0'

pgrep -f a.out //直接输出对应程序的进程号
```

while true; do ; sleep 1;done
test

1. find

find是最常见和最强大的查找命令，你可以用它找到任何你想找的文件。

find的使用格式如下：

　　$ find <指定目录> <指定条件> <指定动作>

　　- <指定目录>： 所要搜索的目录及其所有子目录。默认为当前目录。

　　- <指定条件>： 所要搜索的文件的特征。

　　- <指定动作>： 对搜索结果进行特定的处理。

如果什么参数也不加，find默认搜索当前目录及其子目录，并且不过滤任何结果（也就是返回所有文件），将它们全都显示在屏幕上。

find的使用实例：

　　$ find . -name 'my*'

搜索当前目录（含子目录，以下同）中，所有文件名以my开头的文件。

　　$ find . -name 'my*' -ls

搜索当前目录中，所有文件名以my开头的文件，并显示它们的详细信息。

　　$ find . -type f -mmin -10

搜索当前目录中，所有过去10分钟中更新过的普通文件。如果不加-type f参数，则搜索普通文件+特殊文件+目录。

2. locate

locate命令其实是"find -name"的另一种写法，但是要比后者快得多，原因在于它不搜索具体目录，而是搜索一个数据库（/var/lib/locatedb），这个数据库中含有本地所有文件信息。Linux系统自动创建这个数据库，并且每天自动更新一次，所以使用locate命令查不到最新变动过的文件。为了避免这种情况，可以在使用locate之前，先使用updatedb命令，手动更新数据库。

locate命令的使用实例：

　　$ locate /etc/sh

搜索etc目录下所有以sh开头的文件。

　　$ locate ~/m

搜索用户主目录下，所有以m开头的文件。

　　$ locate -i ~/m

搜索用户主目录下，所有以m开头的文件，并且忽略大小写。

3. whereis

whereis命令只能用于程序名的搜索，而且只搜索二进制文件（参数-b）、man说明文件（参数-m）和源代码文件（参数-s）。如果省略参数，则返回所有信息。

whereis命令的使用实例：

　　$ whereis grep

## 4. which
在PATH变量指定的路径中，搜索某个系统命令的位置，并且返回第一个搜索结果。也就是说，使用which命令，就可以看到某个系统命令是否存在，以及执行的到底是哪一个位置的命令。

5. type

type命令其实不能算查找命令，它是用来区分某个命令到底是由shell自带的，还是由shell外部的独立二进制文件提供的。如果一个命令是外部命令，那么使用-p参数，会显示该命令的路径，相当于which命令。

type命令的使用实例：

　　$ type cd

系统会提示，cd是shell的自带命令（build-in）。

　　$ type grep

系统会提示，grep是一个外部命令，并显示该命令的路径。
