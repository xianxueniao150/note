## topic
```sh
# 列出所有topic
./kafka-topics.sh --bootstrap-server localhost:9092 --list

# 查看topic里消息
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic CHAT-TOPIC-MONI --from-beginning

# 向kafka中发送消息
./kafka-console-producer.sh  --broker-list  localhost:9092 --topic CHAT-TOPIC-MONI
```

### 获取 topic 消息数
```sh
./kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic test765 --time -1

# 输出信息
test765:0:100000
test765:1:100000
test765:2:100000
test765:3:100000
test765:4:100000
bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic test765 --time -2

# 输出信息
test765:0:0
test765:1:0
test765:2:0
test765:3:0
test765:4:0
--time-1 表示要获取指定topic所有分区当前的最大位移，--time-2 表示获取当前最早位移。

两个命令的输出结果相减便可得到所有分区当前的消息总数。
分区当前的消息总数 = [--time-1] - [--time-2]
相减是因为随着 kafka 的运行，topic 中有的消息可能会被删除，，因此 --time-1 的结果其实表示的是历史上该topic生产的最大消息数，如果用户要统计当前的消息总数就必须减去 --time-2 的结果。
本例中没有任何消息被删除，故 --time-2 的结果全是0，表示最早位移都是0，消息总数等于历史上发送的消息总数。
```
