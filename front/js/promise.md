Promise 对象用于表示一个异步操作的最终完成 (或失败)及其结果值。
使得异步方法可以像同步方法那样返回值：异步方法并不会立即返回最终的值，而是会返回一个 promise，以便在未来某个时候把值交给使用者。

## 示例
```javascript
// 普通的异步回调函数
> setTimeout(()=>console.log(Math.random()),1000)
0.8923743583460673

//promise版
p = new Promise((resolve, reject) => {
    setTimeout(() => {
        //如果成功了, 调用 resolve()并传入成功的 value
        //如果失败了, 调用 reject()并传入失败的 reason
        resolve("成功的数据 " + Math.random());
      }, 1000)
});

p.then(
  (value) => {
    // 成功的回调函数 onResolved, 得到成功的 vlaue
    console.log("成功的 value: ", value);
  },
  (rason) => {
    // 失败的回调函数 onRejected, 得到失败的 reason
    console.log("失败的 reason: ", reason);
  }
);

成功的 value:  成功的数据 0.9196600195117131
```

打印promise对象
```javascript
> p
< Promise {<fulfilled>: '成功的数据 0.9196600195117131'}
[[Prototype]]: Promise
[[PromiseState]]: "fulfilled"
[[PromiseResult]]: "成功的数据 0.9196600195117131"
```
可以看到重点就是状态和结果值

## Promise 状态
一个 Promise 必然处于以下几种状态之一：
- 待定（pending）: 初始状态，既没有被兑现，也没有被拒绝。
- 已兑现（fulfilled）: 意味着操作成功完成。
- 已拒绝（rejected）: 意味着操作失败。
待定状态的 Promise 对象要么会通过一个值被兑现（fulfilled），要么会通过一个原因（错误）被拒绝（rejected）。当这些情况之一发生时，我们用 promise 的 then 方法排列起来的相关处理程序就会被调用。如果 promise 在一个相应的处理程序被绑定时就已经被兑现或被拒绝了，那么这个处理程序就会被调用。

### 如何改变 promise 的状态?
(1) resolve(value): 如果当前是 pending 就会变为 resolved
(2) reject(reason): 如果当前是 pending 就会变为 rejected
(3) 抛出异常: 如果当前是 pending 就会变为 rejected

### 一个 promise 指定多个成功/失败回调函数, 都会调用
```javascript
let p = new Promise((resolve, reject) => {  resolve('OK');});
  ///指定回调 - 1
  p.then(value => {  console.log(value); });
  //指定回调 - 2
  p.then(value => { alert(value);});
```

### promise.then()返回的新 promise 的结果状态由什么决定?
(1) 简单表达: 由 then()指定的回调函数执行的结果决定
(2) 详细表达:
	① 如果抛出异常, 新 promise 变为 rejected, reason 为抛出的异常
	② 如果返回的是非 promise 的任意值, 新 promise 变为 resolved, value 为返回的值
	③ 如果返回的是另一个新 promise, 此 promise 的结果就会成为新 promise 的结果

```javascript
let p = new Promise((resolve, reject) => {
	resolve('ok');
});
//执行 then 方法
let result = p.then(value => {
console.log(value);
// 1. 抛出错误 ,变为 rejected
throw '出了问题';
// 2. 返回结果是非 Promise 类型的对象,新 promise 变为 resolved
return 521;
// 3. 返回结果是 Promise 对象,此 promise 的结果就会成为新 promise 的结果
```
Ⅴ- promise 如何串连多个操作任务?
(1) promise 的 then()返回一个新的 promise, 可以开成 then()的链式调用

(2) 通过 then 的链式调用串连多个同步/异步任务,这样就能用then()将多个同步或异步操作串联成一个同步队列

<script>
let p = new Promise((resolve, reject) => { setTimeout(() => {resolve('OK'); }, 1000); });
p.then(value => {return new Promise((resolve, reject) => { resolve("success"); });})
.then(value => {console.log(value);})
.then(value => { console.log(value);})
</script>

## 如何中断 promise 链?
在回调函数中返回一个 pendding 状态的promise 对象
```javascript
let p = new Promise((resolve, reject) => {setTimeout(() => { resolve('OK');}, 1000);});
p.then(value => {return new Promise(() => {});})//有且只有这一个方式
.then(value => { console.log(222);})
.then(value => { console.log(333);})
.catch(reason => {console.warn(reason);});
```

## API 用法详解
### 创建Promise
Promise 对象是由关键字 new 及其构造函数来创建的。该构造函数会把一个叫做“处理器函数”（executor function）的函数作为它的参数。这个“处理器函数”接受两个函数——resolve 和 reject ——作为其参数。当异步任务顺利完成且返回结果值时，会调用 resolve 函数；而当异步任务失败且返回失败原因（通常是一个错误对象）时，会调用reject 函数。
```javascript
const myFirstPromise = new Promise((resolve, reject) => {
  // ?做一些异步操作，最终会调用下面两者之一:
  //
  //   resolve(someValue); // fulfilled
  // ?或
  //   reject("failure reason"); // rejected
});
```

想要某个函数拥有promise功能，只需让其返回一个promise即可。
```javascript
function myAsyncFunction(url) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.onload = () => resolve(xhr.responseText);
    xhr.onerror = () => reject(xhr.statusText);
    xhr.send();
  });
};
```

### Promise.prototype.then()
Promise 实例具有then方法，也就是说，then方法是定义在原型对象Promise.prototype上的。它的作用是为 Promise 实例添加状态改变时的回调函数。
then方法的第一个参数是resolved状态的回调函数，第二个参数（可选）是rejected状态的回调函数。
```javascript
promise.then(function(value) {
// 当promise状态返回为resolve 时会执行的回调函数
}, function(error) {
// 当promise状态返回为rejected 时会执行的回调函数
});
```
then方法返回的是一个新的Promise实例
采用链式的then, 会等待前一个Promise状态发生改变才会被调用

使用箭头函数简写
如果采用箭头函数，上面的代码可以写得更简洁 (实际代码中基本都是这样写了)
```javascript
getJSON("./hong.json")
.then(json => getJSON(json.name) )
.then(
    name => console.log("resolved: My name is ", name), 
    err => console.log("rejected: ", err)
   );
```

### Promise.prototype.catch()
Promise.prototype.catch()方法是.then(null, rejection)或.then(undefined, rejection)的别名，用于指定发生错误时的回调函数。

异常穿透问题
当使用 promise 的 then 链式调用时, 可以在最后指定失败的回调, 前面任何操作出了异常, 都会传到最后失败的回调中处理
```javascript
> Promise.resolve(223)
    .then(res=> {throw new Error("err2");})
    .then(res=>"success")
    .catch(err=>err)
< Promise {<fulfilled>: Error: err2


> Promise.resolve(223)
    .then(res=> {throw new Error("异常");})
    .then(res=>"success",e=>console.log('被then的错误回调捕获',e))
    .catch(err=>err)

	被then的错误回调捕获 Error: 异常
< Promise {<fulfilled>: undefined}
```
注:可以在每个then()的第二个回调函数中进行err处理,也可以利用异常穿透特性,到最后用catch去承接统一处理,两者一起用时,前者会生效(因为err已经将其处理,就不会再往下穿透)而走不到后面的catch

### Promise.resolve(value)
返回一个状态由给定value决定的Promise对象。
如果传入的参数为非Promise类型的对象，则返回的结果为成功promise对象
如果传入的参数为Promise类型的对象，则参数的结果决定了resolve的结果
```javascript
> Promise.resolve(123)
< Promise {<fulfilled>: 123}
	[[Prototype]]: Promise
	[[PromiseState]]: "fulfilled"
	[[PromiseResult]]: 123

> Promise.resolve(new Promise((resolve,reject)=>{
    reject("error");
}))
< Promise {<rejected>: 'error'
```
通常而言，如果您不知道一个值是否是Promise对象，使用Promise.resolve(value) 来返回一个Promise对象,这样就能将该value以Promise对象形式使用。

### Promise.reject(reason)
返回一个状态为失败的Promise对象，并将给定的失败信息传递给对应的处理方法


## async
await关键字只在async函数内有效。如果在async函数体之外使用它，就会抛出语法错误。但async函数中可以没有await
await右侧的表达式一般为promise对象。如果表达式是promise对象，await返回的是promise成功的值。如果表达式是其他值，直接将此值作为await的返回值。
如果await的promise失败了，就会抛出异常。使用async / await关键字就可以在异步代码中使用普通的try / catch代码块。

async函数可能包含0个或者多个await表达式。await表达式会暂停整个async函数的执行进程并出让其控制权，只有当其等待的基于promise的异步操作被兑现或被拒绝之后才会恢复进程。

async函数一定会返回一个promise对象。如果一个async函数的返回值看起来不是promise，那么它将会被隐式地包装在一个promise中。
async 返回和promise.then()返回是一样的
```javascript
async function foo() {
   return 1
}

//等价于:
function foo() {
   return Promise.resolve(1)
}
```

各种情况下的并发
```javascript
var resolveAfter2Seconds = function() {
  console.log("starting slow promise");
  return new Promise(resolve => {
    setTimeout(function() {
      resolve("slow");
      console.log("slow promise is done");
    }, 2000);
  });
};

var resolveAfter1Second = function() {
  console.log("starting fast promise");
  return new Promise(resolve => {
    setTimeout(function() {
      resolve("fast");
      console.log("fast promise is done");
    }, 1000);
  });
};

//在sequentialStart中，程序在第一个await停留了2秒，然后又在第二个await停留了1秒。直到第一个计时器结束后，第二个计时器才被创建。程序需要3秒执行完毕。
var sequentialStart = async function() {
  console.log('==SEQUENTIAL START==');

  // 1. Execution gets here almost instantly
  const slow = await resolveAfter2Seconds();
  console.log(slow); // 2. this runs 2 seconds after 1.

  const fast = await resolveAfter1Second();
  console.log(fast); // 3. this runs 3 seconds after 1.
}

//在 concurrentStart中，两个计时器被同时创建，然后执行await。这两个计时器同时运行，这意味着程序完成运行只需要2秒，而不是3秒,即最慢的计时器的时间。
//但是 await 仍旧是顺序执行的，第二个 await 还是得等待第一个执行完。在这个例子中，这使得先运行结束的输出出现在最慢的输出之后。
var concurrentStart = async function() {
  console.log('==CONCURRENT START with await==');
  const slow = resolveAfter2Seconds(); // starts timer immediately
  const fast = resolveAfter1Second(); // starts timer immediately

  // 1. Execution gets here almost instantly
  console.log(await slow); // 2. this runs 2 seconds after 1.
  console.log(await fast); // 3. this runs 2 seconds after 1., immediately after 2., since fast is already resolved
}

// same as concurrentStart
var concurrentPromise = function() {
  console.log('==CONCURRENT START with Promise.all==');
  return Promise.all([resolveAfter2Seconds(), resolveAfter1Second()]).then((messages) => {
    console.log(messages[0]); // slow
    console.log(messages[1]); // fast
  });
}

// truly parallel: after 1 second, logs "fast", then after 1 more second, "slow"
var parallel = async function() {
  console.log('==PARALLEL with await Promise.all==');

  // Start 2 "jobs" in parallel and wait for both of them to complete
  await Promise.all([
      (async()=>console.log(await resolveAfter2Seconds()))(),
      (async()=>console.log(await resolveAfter1Second()))()
  ]);
}

// // same as parallel
var parallelPromise = function() {
  console.log('==PARALLEL with Promise.then==');
  resolveAfter2Seconds().then((message)=>console.log(message));
  resolveAfter1Second().then((message)=>console.log(message));
}
```

### 使用async函数重写 promise 链
```javascript
function getProcessedData(url) {
  return downloadData(url) // 返回一个 promise 对象
    .catch(e => {
      return downloadFallbackData(url)  // 返回一个 promise 对象
    })
    .then(v => {
      return processDataInWorker(v); // 返回一个 promise 对象
    });
}

//可以重写为单个async函数：
async function getProcessedData(url) {
  let v;
  try {
    v = await downloadData(url);
  } catch (e) {
    v = await downloadFallbackData(url);
  }
  return processDataInWorker(v);
}
```
return foo;和return await foo;，有一些细微的差异:return foo;不管foo是promise还是rejects都将会直接返回foo。相反地，如果foo是一个Promise，return await foo;将等待foo执行(resolve)或拒绝(reject)，如果是拒绝，将会在返回前抛出异常。

