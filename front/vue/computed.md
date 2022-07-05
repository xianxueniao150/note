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
        const {reactive,computed } = VueReactivity;

        const state = reactive({name:"zf",age:13});

        const describe = computed(()=>{
            console.log("runner")
            return state.name + state.age + "岁了"
        })

		//特点:缓存，如果依赖的值没变是不会重新计算的
        console.log(describe.value)
        console.log(describe.value)

        setTimeout(() => {
           state.age = 14; 
            console.log(describe.value)
        }, 1000);

    </script>
</body>
</html>
```
控制台打印结果:
runner
zf13岁了
zf13岁了
runner
zf14岁了
可以看到runner只打印了两次


```javascript
import { createDep } from "./dep";
import { ReactiveEffect } from "./effect";
import { trackRefValue, triggerRefValue } from "./ref";

export class ComputedRefImpl {
  public dep: any;
  public effect: ReactiveEffect;

  private _dirty: boolean;
  private _value

  constructor(getter) {
    this._dirty = true;
    this.dep = createDep();
    this.effect = new ReactiveEffect(getter, () => {
      // scheduler
      // 只要触发了这个函数说明响应式对象的值发生改变了
      // 那么就解锁，后续在调用 get 的时候就会重新执行，所以会得到最新的值
      if (this._dirty) return;

      this._dirty = true;
      triggerRefValue(this)
    });
  }

  get value() {
    // 收集依赖
    trackRefValue(this);
    // 锁上，只可以调用一次
    // 当数据改变的时候才会解锁
    // 这里就是缓存实现的核心
    // 解锁是在 scheduler 里面做的
    if (this._dirty) {
      this._dirty = false;
      // 这里执行 run 的话，就是执行用户传入的 fn
      this._value = this.effect.run();
    }

    return this._value;
  }
}

export function computed(getter) {
  return new ComputedRefImpl(getter);
}
```

这里的 triggerRefValue(this) ,trackRefValue(this) 是为了处理effect依赖computed对象的情况
因为computed对象不是proxy类型的，所以此时需要手动收集依赖关系
```javascript
const state = reactive({name:"zf",age:13});

const describe = computed(()=>{
    console.log("runner")
    return state.name + state.age + "岁了"
})
effect(()=>{
    app.innerHTML = describe.value
})
```
