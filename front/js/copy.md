Javascript 的对象只是指向内存中某个位置的指针。这些指针是可变的，也就是说，它们可以重新被赋值。所以仅仅复制这个指针，其结果是有两个指针指向内存中的同一个地址。
```javascript
var foo = {
    a : "abc"
}

var bar = foo;

bar.a = "whatup bar?";
console.log(foo.a); // whatup bar?
```

## 浅拷贝
如果要操作的对象拥有的属性都是值类型，那么可以使用扩展语法或 Object.assign(...)
```javascript
var obj = { foo: "foo", bar: "bar" };
var copy = { ...obj };
var copy = Object.assign({}, obj);

//上面两种方法也可以把多个不同来源对象中的属性复制到一个目标对象中。
var obj1 = { foo: "foo" };
var obj2 = { bar: "bar" };
var copySpread = { ...obj1, ...obj2 };
var copyAssign = Object.assign({}, obj1, obj2);
```

如果对象的属性也是对象，那么上面这种方法是存在问题的，实际被拷贝的只是那些指针。
```javascript
var foo = { a: 0 , b: { c: 0 } };
var copy = { ...foo };
copy.a = 1;
copy.b.c = 2;
console.dir(foo);
// { a: 0, b: { c: 2 } }
console.dir(copy);
// { a: 1, b: { c: 2 } }
```

## 深拷贝（有限制）
想要对一个对象进行深拷贝，一个可行的方法是先把对象序列化为字符串，然后再对它进行反序列化。
```javascript
var obj = { a: 0, b: { c: 0 } };
var copy = JSON.parse(JSON.stringify(obj));
```
不幸的是，这个方法只在对象中包含可序列化值，同时没有循环引用的情况下适用。常见的不能被序列化的就是日期对象 —— 尽管它显示的是字符串化的 ISO 日期格式，但是 JSON.parse 只会把它解析成为一个字符串，而不是日期类型。

### 自己封装
```javascript
function deepClone(obj) {
  var copy;

  // Handle the 3 simple types, and null or undefined
  if (null == obj || "object" != typeof obj) return obj;

  // Handle Date
  if (obj instanceof Date) {
    copy = new Date();
    copy.setTime(obj.getTime());
    return copy;
  }

  // Handle Array
  if (obj instanceof Array) {
    copy = [];
    for (var i = 0, len = obj.length; i < len; i++) {
        copy[i] = deepClone(obj[i]);
    }
    return copy;
  }

  // Handle Function
  if (obj instanceof Function) {
    copy = function() {
      return obj.apply(this, arguments);
    }
    return copy;
  }

  // Handle Object
  if (obj instanceof Object) {
      copy = {};
      for (var attr in obj) {
          if (obj.hasOwnProperty(attr)) copy[attr] = deepClone(obj[attr]);
      }
      return copy;
  }

  throw new Error("Unable to copy obj as type isn't supported " + obj.constructor.name);
}
```
