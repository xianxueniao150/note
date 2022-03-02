## Vue中watch对象内属性的方法
2.用字符串来表示对象的属性调用
```sh
new Vue({
  data: {
    count: 10，
    blog:{
        title:'my-blog',
        categories:[]
    }
  },
  watch: {
    'blog.categories'(newVal, oldVal) {
        console.log(`new:${newVal}, old:${oldVal}`);
    }, 
  }
})
```
