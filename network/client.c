#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>

int main(int argc, char *argv[])
{
	char *addr="1.116.74.213";
	if (argc==2) {  
		char *addr=argv[1];
		/* printf("Usage:%s <IP Address>\n",argv[0]);   */
		/* exit(1);   */
	}  
	//创建套接字
	int sock = socket(AF_INET, SOCK_STREAM, 0);
	//向服务器（特定的IP和端口）发起请求
	struct sockaddr_in serv_addr;
	memset(&serv_addr, 0, sizeof(serv_addr));              //每个字节都用0填充
	serv_addr.sin_family = AF_INET;                        //使用IPv4地址
	serv_addr.sin_addr.s_addr = inet_addr(addr); //具体的IP地址
	serv_addr.sin_port = htons(8888);                      //端口
	if(connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr))==-1){
		printf("connect() error:%s\n",strerror(errno));  
		exit(1); 
	}else{
		printf("connect() success\n");  
		/* sleep(50); */
		/* exit(1);  */
	}

	while (1)
	{
		//读取服务器传回的数据
		char buffer[40];
		int num = recv(sock, buffer, sizeof(buffer) - 1,0);
		if (num<=0){
			printf("num: %d,%s\n", num,strerror(errno));
		}else{
			printf("Message form server: %s\n", buffer);
		}
		//关闭套接字
		/* close(sock); */
		return 0;
	}

	//关闭套接字
	close(sock);
	return 0;
}
