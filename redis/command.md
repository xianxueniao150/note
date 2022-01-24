```
重复执行某个命令5次，每次间隔1s
redis-cli -h 119.28.46.74 -p 6379 -r 5 -i 1 BRPOPLPUSH zeus:vulgar:picture lp:vulgar:picture 5
```
