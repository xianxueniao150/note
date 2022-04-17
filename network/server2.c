server.c
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <ctype.h>

#define MAXLINE 80
#define SERV_PORT 6666

int main(void){

    struct sockaddr_in servaddr,cliaddr;
	socklen_t cliaddr_len;
	int listenfd, connfd;
	char buf[MAXLINE];
	char str[INET_ADDRSTRLEN];
	int i, n;

	listenfd = socket(AF_INET, SOCK_STREAM, 0);

//	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);  //INADDR_ANY 宏，编译器会自动转换成本地任意一个可用的ip
	servaddr.sin_port = htons(SERV_PORT);

	bind(listenfd, (struct sockaddr *)&servaddr, sizeof(servaddr));
	listen(listenfd, 20);

	printf("Accepting connections ...\n");
	
   cliaddr_len = sizeof(cliaddr);  //必须先初始化
	connfd = accept(listenfd, (struct sockaddr *)&cliaddr, &cliaddr_len);
	while (1) {
		n = read(connfd, buf, MAXLINE);
		printf("received from %s at PORT %d\n",
		inet_ntop(AF_INET, &cliaddr.sin_addr, str, sizeof(str)),
		ntohs(cliaddr.sin_port));
		for (i = 0; i < n; i++)
			buf[i] = toupper(buf[i]);
		write(connfd, buf, n);
	//	close(connfd);
	}
	return 0;
}
```


用nc命令模拟客户端进行测试
```sh
$ nc 127.0.0.1 6666
hello
HELLO
```
 
