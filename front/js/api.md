## setInterval
setInterval() 方法可按照指定的周期来调用函数。
```cpp
setInterval(function, milliseconds, param1, param2, ...)

milliseconds	以毫秒计。
param1, param2, ...	可选。 传给执行函数的其他参数。

技术细节
返回值:	返回一个 ID（数字），可以将这个ID传递给clearInterval()，clearTimeout() 以取消执行。
```
setInterval() 方法会不停地调用函数，直到 clearInterval() 被调用或窗口被关闭。由 setInterval() 返回的 ID 值可用作 clearInterval() 方法的参数

### 例：两种颜色的切换
下面的例子里会每隔一秒就调用函数 flashtext() 一次，直至你通过按下 Stop 按钮来清除本次重复操作的唯一辨识符 intervalID。
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>setInterval/clearInterval example</title>

  <script>
    var nIntervId;

    function changeColor() {
      nIntervId = setInterval(flashText, 1000);
    }

    function flashText() {
      var oElem = document.getElementById('my_box');
      oElem.style.color = oElem.style.color == 'red' ? 'blue' : 'red';
    }

    function stopTextColor() {
      clearInterval(nIntervId);
    }
  </script>
</head>

<body onload="changeColor();">
  <div id="my_box">
    <p>Hello World</p>
  </div>

  <button onclick="stopTextColor();">Stop</button>
</body>
</html>
```
