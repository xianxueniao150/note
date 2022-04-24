## 阻塞与非阻塞
```javascript

//开启http服务，回调里面根据不同的路径调用不同的函数来处理
http.createServer(function(request, response) {
	...
}).listen(8888);

//假设/start路径对应的处理方法非常耗时，那么当请求这个路径之后会发现网页一直在转圈，
//此时立即去请求另一个路径，会发现也在转圈,直到前面那额请求处理完这个请求才响应
function start() {
  console.log("Request handler 'start' was called.");

  function sleep(milliSeconds) {
    var startTime = new Date().getTime();
    while (new Date().getTime() < startTime + milliSeconds);
  }

  sleep(10000);
  return "Hello Start";
}
```

这到底是为什么呢？原因就是start()包含了阻塞操作。形象的说就是“它阻塞了所有其他的处理工作”。
这显然是个问题，因为Node一向是这样来标榜自己的：“在node中除了代码，所有一切都是并行执行的”。

Node.js是单线程的。它通过事件轮询（event loop）来实现并行操作，对此，我们应该要充分利用这一点 —— 尽可能的避免阻塞操作，取而代之，多使用非阻塞操作。 然而，要用非阻塞操作，我们需要使用回调
```javascript
var exec = require("child_process").exec;

function start(response) {
  console.log("Request handler 'start' was called.");

  exec("ls -lah", function (error, stdout, stderr) {
    response.writeHead(200, {"Content-Type": "text/plain"});
    response.write(stdout);
    response.end();
  });
}
```
此时，哪怕exec执行的命令非常耗时，也不妨碍其他请求的正常返回，只不过/start的请求会在exec执行完后才返回
