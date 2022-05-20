## od 输出二进制内容
第一列表示文件偏移地址,默认为八进制
后面几列表示文件内容，默认一行展示16字节,默认展示的值目前不知道代表什么?
```sh
# 第一列地址用十进制表示
od -A d  a.txt
# 以十六进制输出，每列输出一字节
od -tx1 a.txt
# 以十六进制显示的同时显示原字符。
od -tx1c a.txt



-A  影响第一列,-A d 表示地址用十进制表示
-c  使用ASCII码进行输出，注意其中包括转义字符
-t<输出格式>: 设置输出格式
	d[SIZE]    signed decimal, SIZE bytes per integer
	x[SIZE]    hexadecimal, SIZE bytes per integer
	结尾添加z的话，就会在最后额外添加一列展示printable characters 
```

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



## jq

curl --location --request POST 'http://qa-live-sort.linkv.sg/liveSort/getNew?page_index=1&pageSize=30' | jq '.data | .video_info | .[] | .anchor_level,.vid'


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

