客户端使用同一个连接每隔5s请求一次，在客户端刚请求完之后，立即重启服务端
服务端监听端口50051
通过抓包可以看到服务端重启之后客户端又重新建立了连接
```sh
sudo tcpdump -i lo0 port 50051

10:35:16.699195 IP6 localhost.51914 > localhost.50051: Flags [P.], seq 289:336, ack 368, win 6041, options [nop,nop,TS val 1187456420 ecr 1187456420], length 47
10:35:16.699306 IP6 localhost.50051 > localhost.51914: Flags [.], ack 336, win 6081, options [nop,nop,TS val 1187456420 ecr 1187456420], length 0
10:35:16.699352 IP6 localhost.50051 > localhost.51914: Flags [P.], seq 368:385, ack 336, win 6081, options [nop,nop,TS val 1187456420 ecr 1187456420], length 17
10:35:16.699399 IP6 localhost.51914 > localhost.50051: Flags [.], ack 385, win 6040, options [nop,nop,TS val 1187456420 ecr 1187456420], length 0
10:35:17.863867 IP6 localhost.50051 > localhost.51914: Flags [F.], seq 385, ack 336, win 6081, options [nop,nop,TS val 1187457572 ecr 1187456420], ength 0
10:35:17.863909 IP6 localhost.51914 > localhost.50051: Flags [.], ack 386, win 6040, options [nop,nop,TS val 1187457572 ecr 1187457572], length 0
10:35:17.874080 IP6 localhost.51914 > localhost.50051: Flags [F.], seq 336, ack 386, win 6040, options [nop,nop,TS val 1187457582 ecr 1187457572], length 0
10:35:17.874155 IP6 localhost.50051 > localhost.51914: Flags [.], ack 337, win 6081, options [nop,nop,TS val 1187457582 ecr 1187457582], length 0

10:35:21.716699 IP6 localhost.57203 > localhost.50051: Flags [S], seq 3591735288, win 65535, options [mss 16324,nop,wscale 6,nop,nop,TS val 1187461382 ecr 0,sackOK,eol], length 0
10:35:21.716871 IP6 localhost.50051 > localhost.57203: Flags [S.], seq 734052672, ack 3591735289, win 65535, options [mss 16324,nop,wscale 6,nop,nop,TS val 1187461382 ecr 1187461382,sackOK,eol], length 0
10:35:21.716892 IP6 localhost.57203 > localhost.50051: Flags [.], ack 1, win 6371, options [nop,nop,TS val 1187461382 ecr 1187461382], length 0
10:35:21.716907 IP6 localhost.50051 > localhost.57203: Flags [.], ack 1, win 6371, options [nop,nop,TS val 1187461382 ecr 1187461382], length 0
10:35:21.717671 IP6 localhost.50051 > localhost.57203: Flags [P.], seq 1:16, ack 1, win 6371, options [nop,nop,TS val 1187461383 ecr 1187461382], length 15
10:35:21.717740 IP6 localhost.57203 > localhost.50051: Flags [.], ack 16, win 6371, options [nop,nop,TS val 1187461383 ecr 1187461383], length 0
10:35:21.719655 IP6 localhost.57203 > localhost.50051: Flags [P.], seq 1:25, ack 16, win 6371, options [nop,nop,TS val 1187461385 ecr 1187461383], length 24
```

假如服务端在客户端重新来请求之前还没有启动起来，客户端就会报下面错误
```sh
2022/06/09 10:37:56 could not greet: rpc error: code = Unavailable desc = connection error: desc = "transport: Error while dialing dial tcp [::1]:50051: connect: connection refused"
exit status 1
```
