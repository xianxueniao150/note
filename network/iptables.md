```sh
# 查看filter表中各个链的规则
iptables -L
# 不允许被ping
iptables -I INPUT -p icmp -j DROP
# 记录所有ssh请求
iptables -I INPUT -p tcp --dport 22 -m state --state NEW -j LOG

Apr 17 20:02:08 localhost kernel: [540764.643734] IN=eth0 OUT= MAC=52:54:00:a2:9e:4e:fe:ee:5e:4d:d7:bb:08:00 SRC=36.110.206.39 DST=10.0.12.3 LEN=64 TOS=0x00 PREC=0xA0 TTL=46 ID=0 DF PROTO=TCP SPT=49470 DPT=22 WINDOW=65535 RES=0x00 SYN URGP=0


-t, --table table 对指定的表 table 进行操作， table 必须是 raw， nat，filter，mangle 中的一个。如果不指定此选项，默认的是 filter 表。

# 查看管理命令
-L, --list [chain] 列出链 chain 上面的所有规则，如果没有指定链，列出表上所有链的所有规则。

# 规则crud
-A, --append chain rule-specification 在指定链 chain 的末尾插入指定的规则，也就是说，这条规则会被放到最后，最后才会被执行。
-I, --insert chain [rulenum] rule-specification 在链 chain 中的指定位置插入一条或多条规则。rulenum 默认是1，即在链的头部插入。
-D, --delete chain rule-specification -D, --delete chain rulenum 在指定的链 chain 中删除一个或多个指定规则。
-R num：替换/修改第几条规则
-F, --flush [chain] 清空指定链 chain 上面的所有规则。如果没有指定链，清空该表上所有链的所有规则。

# 规则中的匹配选项,"!" 表示取反。
-p：指定要匹配的数据包协议类型
-s, --source [!] address[/mask] ：把指定的一个／一组地址作为源地址，按此规则进行过滤。当后面没有 mask 时，address 是一个地址，比如：192.168.1.1；
	当 mask 指定时，可以表示一组范围内的地址，比如：192.168.1.0/24。
-d, --destination [!] address[/mask] ：地址格式同上，但这里是指定地址为目的地址，按此进行过滤。
-i, --in-interface [!] <网络接口name> ：指定数据包进来的网络接口，比如最常见的 eth0 。注意：它只对 PREROUTING,INPUT，FORWARD 这三个链起作用。
-o, --out-interface [!] <网络接口name> ：指定数据包出去的网络接口。只对 OUTPUT，FORWARD，POSTROUTING 三个链起作用。
--dport num	匹配目标端口号
--sport num	匹配来源端口号

# 扩展匹配选项
-m state --state{NEW,...} 检测某种状态，比如可以用于允许A主动和B建立连接，收发消息，但不允许B来和A建立连接
-m limit --limit num/{second,minute,...} 限制某段时间内包的数量

# 动作
ACCEPT ：接收数据包。
DROP ：丢弃数据包。
LOG ：日志记录。(ubuntu日志位于/var/log/kern.log) 可以在最后加上 --log-prefix "xxx" 指定日志前缀
REDIRECT ：重定向、映射、透明代理。
SNAT ：源地址转换。
DNAT ：目标地址转换。
MASQUERADE ：IP伪装（NAT），用于ADSL。
SEMARK : 添加SEMARK标记以供网域内强制访问控制（MAC）
```

## 工作机制
```sh

		         		↑						↓
传输层             		↑         				↓
		................↑.......................↓...................
		                ↑          		        ↓                   
		               input链         		 output链              
		                ↑         		        ↓                   
网络层	             +-----------+				+-------------+     
		             | 		  	 |>>>foward链>> |             |     
		             +-----------+				+-------------+     
		                ↑          		        ↓                   
		            prerouting链   		      postrouting链         
		                ↑          		        ↓                   
		................↑.......................↓...................
		                ↑          		        ↓                  
		        +----------------+ 		   +----------------+       
网卡	        |      网卡1     | 		   |      网卡2     |      
		        +----------------+ 		   +----------------+       
		                ↑          		         |                  
		----------------↑----------		---------|------------------
```
规则链名包括(也被称为五个钩子函数（hook functions）)：
- INPUT链 ：处理输入数据包。
- OUTPUT链 ：处理输出数据包。
- FORWARD链 ：处理转发数据包。(一个网卡的话不涉及转发，没有用，多于一个网卡就有用)
- PREROUTING链 ：用于目标地址转换（DNAT）。
- POSTOUTING链 ：用于源地址转换（SNAT）。
