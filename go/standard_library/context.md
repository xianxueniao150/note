每一个 context.Context 都会从最顶层的 Goroutine 一层一层传递到最下层。context.Context 可以在上层 Goroutine 执行出现错误时，将信号及时同步给下层。

可以看到，最终实现的效果就是使多个goroutine同时结束

设计原理 — 多个 Goroutine 同时订阅 ctx.Done() 管道中的消息，一旦接收到取消信号就立刻停止当前正在执行的工作。

### context.WithCancel 实现优雅退出
```go
var wg sync.WaitGroup

func worker(ctx context.Context) {
	go worker2(ctx)
LOOP:
	for {
		fmt.Println("worker")
		time.Sleep(time.Second)
		select {
		case <-ctx.Done(): // 等待上级通知
			break LOOP
		default:
		}
	}
	wg.Done()
}

func worker2(ctx context.Context) {
LOOP:
	for {
		fmt.Println("worker2")
		time.Sleep(time.Second)
		select {
		case <-ctx.Done(): // 等待上级通知
			break LOOP
		default:
		}
	}
}
func main() {
	ctx, cancel := context.WithCancel(context.Background())
	wg.Add(1)
	go worker(ctx)
	time.Sleep(time.Second * 3)
	cancel() // 通知子goroutine结束
	wg.Wait()
	fmt.Println("over")
}
```

- context.WithCancel() 创建可取消的 Context 对象，即可以主动通知子协程退出。
- 如果需要往子协程中传递参数，可以使用 context.WithValue()。
- 如果需要控制子协程的执行时间，可以使用 context.WithTimeout 创建具有超时通知机制的 Context 对象。
- 超时退出可以控制子协程的最长执行时间，那 context.WithDeadline() 则可以控制子协程的最迟退出时间。
