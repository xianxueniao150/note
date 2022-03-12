跨主机传输要注意的问题

1.字节序问题
大端：低地址处放高字节
小端：低地址处放低字节
主机字节序：host
网络字节序：network
转换：htons，htonl，ntohs，ntohl

2.对齐
禁止编译器自动对齐

3.类型长度问题
解决：int32_t，uint32_t，int64_t，int8_t （不管是什么类型，比如char，我不要你的类型，我只要你的长度）

socket 其实就是一个五元组，包括：源IP, 源端口, 目的IP, 目的端口, 类型(TCP or UDP)
