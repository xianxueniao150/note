## API
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script src="../../node_modules/@vue/reactivity/dist/reactivity.global.js"></script>
    <div id="app"></div>
    <script>
        const {reactive,effect } = VueReactivity;

		//reactive 通过proxy将数据变成响应式
        const state = reactive({name:"zf",age:13});

		//effect函数依赖的数据如果发生变化了，会重新执行
		//默认会先执行一次，执行过程中构造里面的响应式数据和当前effect的关联关系
        effect(()=>{
            app.innerHTML = state.name + state.age + "岁了"
        })

        setTimeout(() => {
           state.age = 14; 
        }, 1000);

    </script>
    
</body>
</html>
```
现象:打开网页后会发现开始是13岁，然后1s后变为14岁，打印state会发现是一个proxy对象

## 依赖收集过程
当effect执行时，会将自己标记为activeEffect(全局属性),然后执行用户定义的函数，其中必然会获取响应式对象的属性值(比如上面的state.name),
这样就会走到proxy的get方法里面,在该方法里会记录某个对象的某个属性和activeEffect的关联关系(track方法)。
当响应式对象的属性发生变化时，会走到proxy的set方法里面,在该方法里会找到该属性对应的effect，然后重新执行(trigger方法)
