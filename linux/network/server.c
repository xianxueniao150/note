#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
#include <signal.h>
#define MAXLINE 1024
void handle_client(int fd)
{
    // signal(SIGPIPE, SIG_IGN); // 忽略 SIGPIPE 信号
    // 假设此时 client 奔溃, 那么 server 将接收到 client 发送的 FIN
    sleep(5);

    // 写入第一条消息
    char msg1[MAXLINE] = {"first message"};
    ssize_t n = write(fd, msg1, strlen(msg1));
    printf("write %ld bytes\n", n);
    // 此时第一条消息发送成功，server 接收到 client 发送的 RST
    sleep(5);
    // 写入第二条消息，出现 SIGPIPE 信号，导致 server 被杀死
    char msg2[MAXLINE] = {"second message"};
    printf("ready to write\n");
    n = write(fd, msg2, strlen(msg2));

    printf("writed\n");
    printf("%ld, %s\n", n, strerror(errno));
}

int main()
{
    unsigned short port = 8888;
    struct sockaddr_in server_addr;
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(port);
    int listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (bind(listenfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1)
    {
        perror("Binderror.");
        exit(1);
    }
    listen(listenfd, 128);
    int fd = accept(listenfd, NULL, NULL);
    handle_client(fd);
    sleep(5);
    // close(fd);
    // close(listenfd);
    return 0;
}
