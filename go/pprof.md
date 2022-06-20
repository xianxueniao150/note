https://blog.wolfogre.com/posts/go-ppof-practice/
示例程序
```go
package main

import (
	// 略
	_ "net/http/pprof" // 会自动注册 handler 到 http server，方便通过 http 接口获取程序运行采样报告
	// 略
)

func main() {
	// 略

	runtime.GOMAXPROCS(1) // 限制 CPU 使用数，避免过载
	runtime.SetMutexProfileFraction(1) // 开启对锁调用的跟踪
	runtime.SetBlockProfileRate(1) // 开启对阻塞操作的跟踪

	go func() {
		// 启动一个 http server，注意 pprof 相关的 handler 已经自动注册过了
		if err := http.ListenAndServe(":6060", nil); err != nil {
			log.Fatal(err)
		}
		os.Exit(0)
	}()

	// 略
}
```
保持程序运行，打开浏览器访问 http://localhost:6060/debug/pprof/
页面上展示了可用的程序运行采样数据，分别有：

- allocs	内存分配情况的采样信息	可以用浏览器打开，但可读性不高
- blocks	阻塞操作情况的采样信息	可以用浏览器打开，但可读性不高
- cmdline	显示程序启动命令及参数	可以用浏览器打开，这里会显示 ./go-pprof-practice
- goroutine	当前所有协程的堆栈信息	可以用浏览器打开，但可读性不高
- heap	堆上内存使用情况的采样信息	可以用浏览器打开，但可读性不高
- mutex	锁争用情况的采样信息	可以用浏览器打开，但可读性不高
- profile	CPU 占用情况的采样信息	浏览器打开会下载文件
- threadcreate	系统线程创建情况的采样信息	可以用浏览器打开，但可读性不高
- trace	程序运行跟踪信息	浏览器打开会下载文件

## go tool
由于直接阅读采样信息缺乏直观性，我们需要借助 go tool pprof 命令来排查问题，这个命令是 go 原生自带的，所以不用额外安装。
top、list、web

web图形化显示调用栈信息，这很酷，但是需要你事先在机器上安装 graphviz，大多数系统上可以轻松安装它：
brew install graphviz # for macos

### 排查 CPU 占用过高
```sh
$ go tool pprof http://localhost:6060/debug/pprof/profile
Fetching profile over HTTP from http://localhost:6060/debug/pprof/profile
Saved profile in /Users/bowen/pprof/pprof.samples.cpu.001.pb.gz
Type: cpu
Time: Jun 15, 2022 at 10:26pm (CST)
Duration: 30.23s, Total samples = 13.35s (44.17%)
Entering interactive mode (type "help" for commands, "o" for options)
(pprof) top
Showing nodes accounting for 13.25s, 99.25% of 13.35s total
Dropped 32 nodes (cum <= 0.07s)
Showing top 10 nodes out of 11
      flat  flat%   sum%        cum   cum%
    12.84s 96.18% 96.18%     13.14s 98.43%  github.com/wolfogre/go-pprof-practice/animal/felidae/tiger.(*Tiger).Eat
     0.30s  2.25% 98.43%      0.30s  2.25%  runtime.asyncPreempt
     0.11s  0.82% 99.25%      0.11s  0.82%  runtime.kevent
         0     0% 99.25%     13.15s 98.50%  github.com/wolfogre/go-pprof-practice/animal/felidae/tiger.(*Tiger).Live
         0     0% 99.25%     13.17s 98.65%  main.main
         0     0% 99.25%      0.11s  0.82%  runtime.findrunnable
         0     0% 99.25%     13.17s 98.65%  runtime.main
         0     0% 99.25%      0.12s   0.9%  runtime.mcall
         0     0% 99.25%      0.11s  0.82%  runtime.netpoll
         0     0% 99.25%      0.11s  0.82%  runtime.park_m


(pprof) list Eat
Total: 13.35s
ROUTINE ======================== github.com/wolfogre/go-pprof-practice/animal/felidae/tiger.(*Tiger).Eat in /Users/bowen/go/src/test/go-pprof-practice/animal/felidae/tiger/tiger.go
    12.84s     13.14s (flat, cum) 98.43% of Total
         .          .     19:}
         .          .     20:
         .          .     21:func (t *Tiger) Eat() {
         .          .     22:	log.Println(t.Name(), "eat")
         .          .     23:	loop := 10000000000
    12.84s     13.14s     24:	for i := 0; i < loop; i++ {
         .          .     25:		// do nothing
         .          .     26:	}
         .          .     27:}
         .          .     28:
         .          .     29:func (t *Tiger) Drink() {
(pprof) web
```

### 排查内存占用过高
```sh
$ go tool pprof http://localhost:6060/debug/pprof/heap
(pprof) top
Showing nodes accounting for 768MB, 100% of 768MB total
      flat  flat%   sum%        cum   cum%
     768MB   100%   100%      768MB   100%  github.com/wolfogre/go-pprof-practice/animal/muridae/mouse.(*Mouse).Steal
         0     0%   100%      768MB   100%  github.com/wolfogre/go-pprof-practice/animal/muridae/mouse.(*Mouse).Live
         0     0%   100%      768MB   100%  main.main
         0     0%   100%      768MB   100%  runtime.main
(pprof) list Steal
Total: 768MB
ROUTINE ======================== github.com/wolfogre/go-pprof-practice/animal/muridae/mouse.(*Mouse).Steal in /Users/bowen/go/src/test/go-pprof-practice/animal/muridae/mouse/mouse.go
     768MB      768MB (flat, cum)   100% of Total
         .          .     45:
         .          .     46:func (m *Mouse) Steal() {
         .          .     47:	log.Println(m.Name(), "steal")
         .          .     48:	max := constant.Gi
         .          .     49:	for len(m.buffer)*constant.Mi < max {
     768MB      768MB     50:		m.buffer = append(m.buffer, [constant.Mi]byte{})
         .          .     51:	}
         .          .     52:}
(pprof) web
```

### 排查频繁内存回收
获取程序运行过程中 GC 日志，
```sh
GODEBUG=gctrace=1 ./go-pprof-practice | grep gc
```

```sh
$ go tool pprof http://localhost:6060/debug/pprof/allocs
(pprof) top
Showing nodes accounting for 512MB, 100% of 512MB total
      flat  flat%   sum%        cum   cum%
     512MB   100%   100%      512MB   100%  github.com/wolfogre/go-pprof-practice/animal/canidae/dog.(*Dog).Run (inline)
         0     0%   100%      512MB   100%  github.com/wolfogre/go-pprof-practice/animal/canidae/dog.(*Dog).Live
         0     0%   100%      512MB   100%  main.main
         0     0%   100%      512MB   100%  runtime.main
(pprof) list Run
Total: 512MB
ROUTINE ======================== github.com/wolfogre/go-pprof-practice/animal/canidae/dog.(*Dog).Run in /Users/bowen/go/src/test/go-pprof-practice/animal/canidae/dog/dog.go
     512MB      512MB (flat, cum)   100% of Total
         .          .     38:	log.Println(d.Name(), "pee")
         .          .     39:}
         .          .     40:
         .          .     41:func (d *Dog) Run() {
         .          .     42:	log.Println(d.Name(), "run")
     512MB      512MB     43:	_ = make([]byte, 16*constant.Mi)
         .          .     44:}
         .          .     45:
         .          .     46:func (d *Dog) Howl() {
         .          .     47:	log.Println(d.Name(), "howl")
         .          .     48:}
```


### 排查协程泄露
```sh
$ go tool pprof http://localhost:6060/debug/pprof/goroutine
(pprof) top
Showing nodes accounting for 106, 100% of 106 total
Showing top 10 nodes out of 43
      flat  flat%   sum%        cum   cum%
       104 98.11% 98.11%        104 98.11%  runtime.gopark
         1  0.94% 99.06%          1  0.94%  net/http.(*connReader).backgroundRead
         1  0.94%   100%          1  0.94%  runtime/pprof.runtime_goroutineProfileWithLabels
         0     0%   100%          2  1.89%  bufio.(*Reader).ReadLine
         0     0%   100%          2  1.89%  bufio.(*Reader).ReadSlice
         0     0%   100%          2  1.89%  bufio.(*Reader).fill
         0     0%   100%        100 94.34%  github.com/wolfogre/go-pprof-practice/animal/canidae/wolf.(*Wolf).Drink.func1
         0     0%   100%          1  0.94%  github.com/wolfogre/go-pprof-practice/animal/felidae/cat.(*Cat).Live
         0     0%   100%          1  0.94%  github.com/wolfogre/go-pprof-practice/animal/felidae/cat.(*Cat).Pee
         0     0%   100%          1  0.94%  internal/poll.(*FD).Accept
(pprof) list Drink
Total: 106
ROUTINE ======================== github.com/wolfogre/go-pprof-practice/animal/canidae/wolf.(*Wolf).Drink.func1 in /Users/bowen/go/src/test/go-pprof-practice/animal/canidae/wolf/wolf.go
         0        100 (flat, cum) 94.34% of Total
         .          .     29:
         .          .     30:func (w *Wolf) Drink() {
         .          .     31:	log.Println(w.Name(), "drink")
         .          .     32:	for i := 0; i < 10; i++ {
         .          .     33:		go func() {
         .        100     34:			time.Sleep(30 * time.Second)
         .          .     35:		}()
         .          .     36:	}
         .          .     37:}
         .          .     38:
         .          .     39:func (w *Wolf) Shit() {
```

### 排查锁的争用
```sh
go tool pprof http://localhost:6060/debug/pprof/mutex
```

### 排查阻塞操作(channel阻塞)
```sh
go tool pprof http://localhost:6060/debug/pprof/block
```

