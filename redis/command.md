```sh
#重复执行某个命令5次，每次间隔1s
redis-cli -h 119.28.46.74 -p 6379 -r 5 -i 1 BRPOPLPUSH zeus:vulgar:picture lp:vulgar:picture 5

#删除指定前缀的key,更优雅实现https://blog.ops-coffee.cn/s/x48wmx_k55hmpfzl0tybyq
redis-cli keys "ops-coffee-*" | xargs redis-cli del
```
