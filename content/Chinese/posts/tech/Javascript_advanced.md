---
title : '学习: JavaScript 进阶篇'
date : 2024-03-14
lastmod: 2024-03-22
draft : false
author : "Jingyi Wu"
comments: true #是否展示评论
showToc: true # 显示目录
TocOpen: false # 自动展开目录
hidemeta: false # 是否隐藏文章的元信息，如发布日期、作者等
##disableShare: true # 底部不显示分享栏
Showbreadcrumbs: true #顶部显示当前路径
ShowShareButtons: true
ShowReadingTime: true
ShowWordCounts: true
ShowPageViews: true
ShowLastMod: true #显示文章更新时间
hasCJKLanguage: true
summary: "JavaScript 进阶篇!! 学习完看框架啦!!"

categories: 
- tech

tags:
- Javascript
- VUB
- Frontend

keywords:
- Javascript


cover:
    image: ""
    caption: "" #图片底部描述
    alt: ""
    relative: true
---

# Day1

## 1. 作用域

>  了解作用域对程序执行的影响及作用域链查找机制。使用闭包函数 创建隔离作用域避免全局变量污染

作用域 (scope) 规定了变量能够被访问的 “范围”， 离开了这个“范围”变量便不能访问

### 1.1 局部作用域

1. 函数作用域 ： 

   在函数内部声明的变量只能在函数内部被访问，外部无法直接访问

   a.  函数内部声明的变量，在函数外部无法被访问

   b.  函数的参数也是函数内部的局部变量

   c. 不同函数内部声明的变量无法访问

   d. 函数执行完毕后，函数内部的变量实际被清空了

2. 块作用域：

   在`JavaScript`中使用`{ }`包裹的代码称为代码块，代码块内部声明的变量外部将 `[有可能]` 无法被访问（因为var是全局变量）

   a. `let `声明的变量会产生块作用域, `var`不会产生作用域

   b. `const` 声明的敞亮也会产生块作用域

   c. 不同代码块之间的变量无法相互访问

   d. 推荐使用`let` 或 `const`

### 1.2 全局作用域

`<script>` 标签 和` .js` 文件的 [ 最外层 ] 就是所谓的全局作用域，在此声明的变量在函数内部也可以被访问。


 全局作用域中声明的变量，任何其他作用域都可以被访问

+ 为 window 对象动态添加的属性默认也是全局的，不推荐!!
+ 函数中未使用任何关键词声明的变量为全局变量，不推荐!!
+ 尽可能少的声明全局变量，防止全局变量污染

### 1.3 作用域链

作用域链本质上是底层的变量查找机制

+ 函数被执行时，会优先查找当前函数作用域中查找变量
+ 如果当前作用域查找不到会依次逐级查找父级作用域直到全局作用域

总结：

+ 嵌套关系的作用域串联起来形成了作用域链
+ 相同作用域链按照从小到大的规则查找变量
+ 子作用域能够访问作用域，父级作用域无法访问子级作用域

### 1.4 垃圾回收机制

垃圾回收机制（Garbage Collection）

JS 中内存的分配和回收都是自动完成的，内存在不使用的时候会被垃圾回收器自动回收

#### 1.4.1 内存的生命周期

+ 内存分配： 当我们声明变量、函数、对象的时候，系统会自动为他们分配内存
+ 内存使用：读写内存，也就是使用变量、函数等等
+ 内存回收：使用完毕，由垃圾回收器自动回收不再使用的内存

注意：

+ 全局变量一般不会被回收（关闭页面回收）
+ 一般情况下局部变量的值，不用会被自动回收掉

#### 1.4.2 内存泄漏

程序中分配的内存由于某种原因程序未释放或无法释放叫内存泄漏

### 1.5 垃圾回收机制算法说明

#### 1. 堆/栈的空间分配

+ 栈 （操作系统）：由操作系统自动分配释放函数的参数值、局部变量、基本数据类型放到栈里面
+ 堆 （操作系统）：一般由程序员分配释放，若程序员不释放，由垃圾回收机制回收。复杂数据类型放在堆内。（数组、对象都在堆内）

#### 2. 垃圾回收算法

##### a. 引用计数法

IE采用的引用计数算法，定义“内存不再使用”，就是看一个对象是否有指向它的引用，没有引用就回收对象。

+ 跟踪记录被引用的次数
+ 如果被引用了一次，那么记录次数1，多次引用会累加 ++
+ 如果减少一个引用就减1 --
+ 如果引用次数是0，则释放内存

<b>缺点</b>

+ 嵌套引用 （循环引用）
+ 如果两个对象相互引用，尽管他们已不再使用，垃圾回收器不会进行回收，导致内存泄漏

```javascript
funcion fn(){
    let o1 = {}
    let o2 = {}
    o1.a = o2
    o2.a = o1
    return '引用计数无法回收'
}
fn()
// 他们的引用次数永远不会为0，这样相互引用会导致内存泄漏
```

![](/img/Javascript/image-20240313215653582.png)

![](/img/Javascript/image-20240313215758285.png)

```javascript
// 普通
const arr = [1,2,3,4]
arr = null
```

![](/img/Javascript/image-20240313214658670.png)

![](/img/Javascript/image-20240313214726431.png)

```javascript
let person = {
    age : 18,
    name: '佩奇'
}
let p = person
person = 1 
p = null
```

![](/img/Javascript/image-20240313215008884.png)

![image-20240313215028983](/img/Javascript/image-20240313215028983.png)

##### b. 标记清除法 (常用)

+ 标记清除算法将“不再使用的对象”定义为“无法达到的对象”
+ 从根部（在JS中就是全局对象）出发定时扫描内存中的对象。凡是能从根部到达的对象，都还是需要使用
+ 无法由根部出发触及到的对象标记为不再使用，稍后进行回收

![](/img/Javascript/image-20240313220153403.png)

### 1.6 闭包 closure

#### 1. 简单理解： 闭包 = 内存函数+外层函数的变量

> 上案例：

```javascript
function outer(){
    const a = 1
    function f(){
        console.log(a)
        // 内部函数使用外层函数的变量, 二者捆绑在一起
    }
    f()// 调用一下，不然没使用函数
}
outer()
```

![](/img/Javascript/image-20240313220956773.png)

#### 2. 闭包基本格式

+ 外部可以访问函数内部的变量. （正常情况下内部变量为局部变量，不能使用）

```javascript
function outer(){
    let a = 10
    function fn(){
        console.log(a)
    }
    return fn 
    // 返回一个函数
}
outer()
// 所以outer() === fn === function fn(){}

// 新增一个外部函数,fun()可以直接输出outer内部的值
// 外层函数使用内部函数的变量
const fun = outer()
fun()
```

#### 3. 闭包应用

> 实现数据私有

```javascript
// 非闭包
let i = 0
function fn(){
    i++
    console.log(`函数被调用${i}`)
    // 这时候 i是全局变量，容易被修改，
    // 太像java的getter setter方法了
}
```

```javascript
// 闭包版
function count(){
    let i = 0
    function fn(){
        i++
        console.log(`函数被调用${i}`)
    }
    return fn
}

const fun = count() // 全局变量，当页面关闭时才回收，引用count()中的fn()函数，不会回收
// 这时没有人可以影响函数中的i值，但是闭包也存在内存泄漏的风险
```

![](/img/Javascript/image-20240313222507900.png)

总结：

1. 怎么理解闭包？ 

   闭包 = 内层函数 + 外层函数的变量

2. 闭包的作用？ 

   封闭数据，实现数据私有，外部也可以访问函数内部变量

   闭包很有用，因为它允许将函数与其操作的某些数据（环境）关联起来

3. 闭包的问题？

   内存泄漏

### 变量提升

> 变量提升是JavaScript中比较 奇怪 的现象，允许在变量声明之前被访问 (仅存在于var声明变量)

代码执行前，检查当前作用域下，所有var声明的变量，他会把var声明的所有变量提到 <b>当前作用域的最前面</b>。但是!!! 只提升声明不提升赋值!!! 

```javascript
console.log(num + '件')
var num = 10 // undefined

// 所以上方两行代码 等于以下代码

var num
console.log(num +'件')
```

注意：

+ 变量在未声明就被访问时，会报错
+ 变量在var声明之前被访问，变量值为undefined
+ let/const声明的变量不存在变量提升
+ 变量提升出现在相同作用域中
+ 实际开发中推荐先声明再访问变量

## 2. 函数进阶

### 1. 函数提升

函数提升 和 变量提升有些类似

#### 可以将函数声明提升到当前作用域的前面，只提升函数声明

```javascript
function fn(){
    console.log ('函数提升')
}
fn()

// 两种情况都一样

fn()
function fn(){
    console.log ('函数提升')
}

// 但是这种形式 不一样！！函数表达式(赋值),函数表达式必须先声明赋值 再调用，否则报错

fun()
var fun = function fn(){
    console.log ('函数提升')
}
```

总结：

+ 函数提升能够使函数的声明调用更灵活
+ 函数表达式不存在提升的现象
+ 函数提升出现在相同的作用域中

### 2. 函数参数

#### 1. 动态参数

arguments 是函数内部内置的伪数组变量，包含了调用函数时传入的所有实参

+ arguments 是一个伪数组，只存在于函数中
+ arguments 的作用是动态获取函数的实参
+ 可以通过for循环一次得到传递过来的实参

```javascript
// 不管用户传入几个参数，都要接受
function getSum(){// 不知道用户传多少参数
    // arguments 动态参数 只存在函数里
    // arguments 是伪数组
    console.log(arguments)
    let sum = 0
    for (let i = 0; i<argument.length; i++){
        sum+=arguments[i]
    }
    return sum
}
getSum (2,3,4)
```

#### 2. 剩余参数

+ 剩余参数允许我们将一个不定数量的参数表示为一个数组
+ `...`是语法符号，置于最末函数形参之前，用于获取多余的实参
+ 借助`...` 获取的剩余实参，是个真数组
+ 开发中，提倡多使用剩余实参

```javascript
function getSum(...arr){ 
    // ... 就是剩余参数的语法符号 arr随便写
    console.log(arr)
}
getSum(1,2,3)

// 第二种用法
function getSum(a,b, ...arr){ 
    // ... 就是剩余参数的语法符号 arr随便写
    console.log(arr) // arr = 3
}
getSum(1,2,3)
```

补充：

展开运算符（不要和剩余参数搞混）

> 展开运算符 (...) 讲一个数组进行展开

一个在函数里，一个在数组/对象里...

```javascript
const arr = [1,4,5,8,2] // 数组 对象都能用
console.log(...arr) //1 4 5 8 2
```

+ 不会修改原数组

+ 运用场景，数组最值

   `console.log(Math.max(...arr))`

+ 运用场景，合并数组

  ```javascript
  const arr2 = [3,4,5]
  // 合并数组
  const arr = [...arr1, ...arr2]
  ```

### 3. 箭头函数

目的： 引入箭头函数可以使用更简短的函数写法并且不绑定`this`,箭头函数的语法比函数表达式更简洁

使用场景： 箭头函数更适用于本来需要匿名函数的地方

#### 1. 基本语法

##### 语法1

```javascript
// 普通函数
const fn = function(){
    console.log('我是普通函数')
}
fn()

// 箭头函数
const fn = () => {
     console.log('我是普通函数')
}
fn()	
```

语法2: 只有一个参数可以省略小括号

```javascript
//普通函数
const fn = function(x){
    return x+x
}

//箭头函数
const fn = x =>{
    return x+x
}
console.log(fn(1))
```

语法3:  如果函数体只有一行代码，可以写到一行上，省略大括号，并且无需写return直接放回值

```javascript
// 普通函数
const fn = function(x,y){
    return x+y
}
console.log(fn(1,2)) //3

// 箭头函数
const fn = (x,y) => x+y
console.log(fn(1,2)) //3
```

实际中的写法

```javascript
const form = document.querySelector('form')
form.addEventListener('click',ev => ev.preventDefault())
```

语法4:  加括号的函数体返回对象字面量的表达式

```javascript
const fn1 = uname => ({uname: uname})
console.log(fn1('pink老师'))
```

#### 总结

+ 箭头函数属于表达式函数，因此不存在函数提升
+ 箭头函数只有一个参数时可以省略圆括号`( )`
+ 箭头函数的函数体只有一行代码时，可以省略花括号`{}`, 并自动作为返回值被返回
+ 加括号的函数体返回对象字面量表达式 `uname =>({uname:uname})`

#### 2. 箭头函数参数

1. 普通函数有arguments动态参数
2. 箭头函数没有arguments动态参数，但是有剩余参数 `...args`

```javascript
const getSum = (...args) => {
    let sum = 0
    for (let i = 0; i<args.length;i++){
        sum += args[i]
    }
    return sum 
    // 注意函数体有多行代码时需要return
    // 大括号也不能省
}
console.log(getSum(1,2,3))
```

#### 3. 箭头函数 this

以前`this`的指向：谁调用这个函数，`this`就指向谁

```javascript
console.log(this) //此处为window
const sayHi = function({
    cnosole.log(this)
	// 普通函数指向调用者，此处为window
})
btn.addEventListener('click',function(){
    console.log(this)
    // 当前this，指向btn
})
```

箭头函数不会创建自己的`this`,只会从自己的作用域链的上一层沿用`this`. （说简单点，父亲的this就是箭头函数的this ）

```javascript
const fn = ()=>{
    console.log(this) //window
}
// 因为箭头函数没有this!!, 所以会调用父亲window的this
```

对象方法箭头函数`this`

```javascript
const obj = {
    uname : 'pink老师'，
    sayHi : () => {
        console.log(this) //this指向谁？window
    }
}

obj.sayHi()
// 因为sayHi()方法中没有this，沿用上一级obj的this， window 调用obj，所以this指向window
```

​	复杂一点的案例

```javascript
const user = {
    name: '小明',
    sayHi: function(){
        // 注意这是普通函数，this指向函数的调用者
        console.log(this) //user
        let i = 10
        const count = () =>{
            console.log(this) //user
        }
        count() // user
        // 因为箭头函数的作用域中没有this，所以指向上层作用域的this
    }
}
```

在开发中 【 使用箭头函数前需要考虑函数中的this值 】，事件回调函数使用箭头函数时，this为全局的window，因此DOM事件回调函数为了简便，不推荐使用箭头函数

```javascript
// DOM 节点
const btn = document.querySelector('.btn')
// 箭头函数，此时this指向window
btn.addEventListener('click',() =>{
    console.log(this)
})
// 普通函数，此时this指向了DOM对象
btn.addEventListener('click',function(){
    console.log(this)
})
```

总结：

+ 箭头函数里面有`this`吗？

  箭头函数不会创建自己的`this,` 它只会从自己的作用域链的上一层沿用`this`

+ `DOM` 事件回调函数推荐使用箭头函数吗？

  不推荐，特别是需要用到`this`的时候

  事件回调函数使用箭头函数时，`this`为全局的`window`

## 3. 解构赋值

### 1. 数组解构

数组解构是将数组的单元值快速批量赋值给一系列变量的简洁语法

#### 引入

```javascript
// 普通写法
const arr = [100,60,80]
const max = arr[0]
const min = arr[1]
const avg = arr[2]
console.log(max) 
console.log(min)
console.log(avg)

// 解构赋值版本
const [max, min, avg] = [100, 60, 80]
console.log(max) 
console.log(min)
console.log(avg)
```

#### 基本语法

1. 赋值运算符 = 左侧的 `[]` 用于批量声明变量，右侧数组的单元值被赋值给左侧的变量

2. 变量的顺序对应数组单元值的位置依次进行赋值操作

   ```javascript
   // 普通的数组
   const arr = [1,2,3]
   // 批量声明变量 a,b,c
   // 同时将数组单元值1，2，3 依次赋值给变量a b c
   const [a,b,c] = arr
   console.log(a) //1
   console.log(b) //2
   console.log(c) //3
   // 再来一个
   const [max,min,avg] = arr
   ```

   交换变量应用

   ```javascript
   let a = 1
   let b = 2; //必须加分号
   [b,a] = [a,b] 
   ```

3. 变量多，单元值少的情况

   ```javascript
   const [a,b,c,d] = [1,2,3]
   console.log(a) //1
   console.log(b) //2
   console.log(c) //3
   console.log(d) //undefined
   
   ```

4. 变量少，单元值多的情况

   使用剩余参数解决变量少，单元值多的情况

   ```javascript
   const [a,b,c] = [1,2,3,4,5]
   console.log(a) //1
   console.log(b) //2
   console.log(c) //3
   
   // 剩余参数
   const [a,b,...c] = [1,2,3,4]
   console.log(a) //1
   console.log(b) //2
   console.log(c) //[3,4] 真数组
   
   // 防止undefined传递,给了默认参数
   const [a = 0,b=0] = [1,2]
   const [a = '手机', b='华为'] = ['小米']
   console.log(a) //小米
   console.log(b) //华为
   ```

5. 按需导入复制

   ```javascript
   const [a,b,,d] = [1,2,3,4]
   console.log(a) //1
   console.log(b) //2
   console.log(d) //4
   ```

6. 支持多维数组解构

   ```javascript
   const arr = [1,2,[3,4]]
   console.log(arr[0]) //1
   console.log(arr[1]) //2
   console.log(arr[2]) //[3,4]
   console.log(arr[2][0]) //[3]
   
   // 解构
   const [a,b,c] = [1,2,[3,4]]
   const [a,b,[c,d]] = [1,2,[3,4]]
   ```

注意： JS 必须加分号的情况`;`

1. 立即执行函数

```javascript
(function t(){})();
// 或者
;(function t(){})()
```

2. 数组解构

```javascript
// 数组开头的，特别是前面有语句的一定要注意加分号
;[b,a] = [a,b]
```



总结：

1. 数组解构赋值的作用是什么？

   将数组的单元值快速批量赋值给一系列变量的简洁语法

2. JS 前面有有哪两种情况必须要加分号?

   立即执行函数 和 数组开头的情况

3. 变量的数量大于单元值数量时，多余变量将被赋值为`undefined`

4. 变量的数量小于单元值数量时，可以通过剩余参数获取剩余单元值，但只能置于最末位

### 2. 对象解构

对象解构是将对象属性和方法快速批量赋值给一系列变量的简洁语法

#### 1. 基本语法

+ 赋值运算符 = 左侧的`{}`用于批量声明变量，右侧对象的属性值将赋值给左侧的变量
+ 对象属性的值将被赋值给与属性名相同的变量
+ 注意解构的变量不要和外面的变量名冲突，否则报错
+ 对象中找不到与变量名一致的属性时变量为`undefined`

```javascript
const obj = {
    uname : 'pink老师',
    age : 18
}
// 对象解构
const {uname,age} = {
    uname : 'pink老师',
    age : 18
}
// 等价于 const uname = obj.name
const uname = obj.uname
```

#### 2. 解构的属性改名

```javascript
const obj = {
    uname : 'pink老师',
    age : 18
}
const {uname: username,age} = obj
```

#### 3. 解构数组对象

```javascript
const pig = [
    {
        uname: 'pig',
        age: 18
    }
]

const[{uname, age}]  = pig
```

#### 4. 多级对象解构

```javascript
const pig = {
    name : '佩奇',
    family: {
        mother:'猪妈妈',
        father:'猪爸爸',
        sister:'乔治',
    },
    age:6
}

const {name, family{mother,father, sister},age} = pig
cosole.log(name)
cosole.log(mother)
cosole.log(father)
cosole.log(sister)
cosole.log(age)
```

再来一个案例, 数组+对象

```javascript
const people = [
    {
        name : '佩奇',
        family : {
            mother:'猪妈妈',
        	father:'猪爸爸',
        	sister:'乔治'
        },
        age : 6
    }  
]

const[{name,family:{mother,father,sister},age}] = people

cosole.log(name)
cosole.log(mother)
cosole.log(father)
cosole.log(sister)
cosole.log(age)
```

#### forEach()

> 用于调用数组的每个元素，并将元素传递给回调函数。 只遍历数组，不能遍历对象。
>
> 使用场景： 遍历数组的每个元素
>
> 只遍历，不返回数组

##### 语法

+ `forEach` 主要遍历数组，适合于遍历数组对象!!
+ 参数中，当前元素数组`item`是必须要写的，索引号`index`可选

```java
被遍历的数组.forEach(function(当前数组元素，当前元素所引号)){
    // 函数体
}
```

```javascript
const arr = ['red','green','pink']
arr.forEach(function(item, index){
    console.log(item) // red green pink
    console.log(index) // 0，1，2
})
```

#### filter() 重点

1. filter() 方法创建一个新的数组，新数组中元素是通过检查指定数组中符合的所有元素

2. 使用场景：筛选数组符合条件的元素，并返回筛选之后元素的新数组

##### 语法

```javascript
被遍历的数组.filter(function(item,value){
    return 筛选条件
})
```

也是数组方法，和`map()`更像，有返回值。

但是只能`return` 后面只能写 `>=, <=, <, >, =`等比较运算符

```javascript
const arr = [10,20,30]
const newArr = arr.filter (function(item,index){
    console.log(item)
    console.log(index)
    return item>=20
    // 返回新数组
})
newArr // [20,30]

// 箭头函数 简洁版
const newArr = arr.filter(item => item>=20)
```

# Day2

## 1. 构造函数

### 1. 深入对象

#### 1. 创建对象的三种方式

##### 1. 对象字面量创建对象

```javascript
const o = {
    name: '佩奇'
}
```

##### 2. `new`

```javascript
const o = new Object()
```

##### 3. 构造函数

+ 构造函数：是一种特殊的函数，主要用来初始化对象
+ 使用场景：常规的`{}`语法允许创建一个对象，构造函数可以快速创建多个类似的对象
+ 上案例

```javascript
function Pig (name, age, gender){
    this.name = name
    this.age = age
    this.gender = gender
}
// 创建佩奇对象
const Peppa = new Pig('佩奇'，6，'女')
const George = new Pig('乔治'，6，'女')
const Mum = new Pig('妈妈'，6，'女')
```

###### 构造函数语法

1. 命名以大写字母开头
2. 只能用`new`操作符来执行

说明：

1. 使用`new`关键字调用函数的行为被称为实例化
2. 实例化构造函数时没有参数时可以省略`()`
3. 构造函数内部无需写`return`, 返回值即为新创建的对象
4. 构造函数内部的`return`返回的值无效，所以不用写`return`
5. `new Object()`  `new Date()`  也是实例化构造函数

##### 4. 实例化的执行过程

1. 创建新的空对象
2. 构造函数`this`指向新对象
3. 执行构造函数代码，修改`this`, 添加新的属性
4. 返回新对象

##### 5. 实例成员

通过构造函数创建的对象称为实例对象，实例对象中的属性和方法称为实例成员`(实例属性和实例方法)`

```javascript
function Person(name){
    // 实例属性
    this.name = name
    // 实例方法
    this.sayHi= () => console.log('hi!!~~')
}
```

##### 6. 静态成员

构造函数的属性和方法被称为静态成员 `(静态属性和静态方法)`

就是Java的类方法, 以下均为静态成员

`Date.now()         Math.PI      Math.random()`

```javascript
function Person(name,age){
    // code...
}
// 静态属性
Person.eyes = 2
// 静态方法
Person.breath = function(){
    console.log('走路ing')
    // 此时 this 指向Person
    console.log(this.eyes) 
}
```

### 2. 内置构造函数

> JavaScript 中最主要的数据类型 6 种
>
> 字符串、数值、布尔、undefined、null、对象

#### 1. 基本包装类型

`JavaScript` 底层完成了将简单数据类型包装为引用数据类型，称为`包装类型`。神似`Java`中的拆箱和装箱, 所以像普通字符串可以使用`str.length`。

#### 2. 引用类型

##### 1. Object

> 内置的构造函数，用于创建普通对象

```javascript
const user = new Object()
const user = {uname:'pink',age:18}
// 原来使用for..in..遍历
// 现在使用 Object.keys(user)
```

###### Object 静态方法

<b>!!! 注意 静态方法只有构造函数Object可以调用!!!</b>

| 静态方法或属性                | 作用                                           | 返回值 |
| ----------------------------- | ---------------------------------------------- | ------ |
| Object.keys(实例化对象)       | 获得所有对象的所有键 (包括属性及方法)          | 数组   |
| Object.values(实例化对象)     | 获得所有对象的所有值 (包括属性及方法)          | 数组   |
| Object.assign(新对象, 老对象) | 将老对象的内容拷贝给新对象，用于给对象添加属性 | 对象   |
|                               |                                                |        |

```javascript
// Object.assign()
const o = {name:'佩奇',age:6}
Object.assign(o, {gender:'女'})
console.log(o) {name: '佩奇', age: 6, gender:'女'}
```

##### 2.Array

> 内置的构造函数，用于创建数组

```javascript
const arr = new Array (2,5,4)
const arr = [2,3,5] //推荐!! 字面量的形式创建数组
```

###### 数组常见的实例方法

| 方法    | 作用     | 说明                                                         |      |
| ------- | -------- | ------------------------------------------------------------ | ---- |
| forEach | 遍历数组 | 不返回数组，经常用于查找遍历数组元素                         |      |
| filter  | 过滤数组 | 返回新数组，返回的是筛选满足条件的数组元素                   |      |
| map     | 迭代数组 | 返回新数组，返回的是处理之后的数组元素，想要使用返回的新数组 |      |
| reduce  | 累计器   | 返回累计处理的结果，用于求和等等                             |      |

![image-20240317014348637](/img/Javascript/image-20240317014348637.png)

###### 1 .reduce( )

```javascript
// 基本语法
arr.reduce(function(){}, 初始值)
arr.reduce(function(上一次值, 当前值){}, 初始值)

// 例子
const arr = [1,5,8]
// 没有初始值
const total = arr.reduce(function(prev,current){
    return prev + current
})
console.log(total) //14

// 有初始值
const total = arr.reduce(function(prev,current){
    return prev + current
},10) //14+10 ==24 

// 箭头函数版
arr.reduce((prev,current) => prev + current,10)
```

+ 参数：

  如果有起始值，则把起始值累加到里面

+ reduce 执行过程

  1. 如果没有起始值，则`上一次值`以`数组的第一个元素的值`
  2. 每一次循环，把`返回值`作为下一次循环的`上一次值`
  3. 如果有`起始值`，则起始值作为`上一次值`
  4. 如果是对象数组，初始值必须设置为`0`

```javascript
const arr = [{
      name: '张三',
      salary: 10000
    }, {
      name: '李四',
      salary: 10000
    }, {
      name: '王五',
      salary: 20000
    },
    ]

    const salaries = Object.values(arr)

    console.log(salaries)
    const total = salaries.reduce(function (pre, next) {
      console.log(pre)
      return pre + next.salary
    }, 0)
    console.log(total)
```

###### 2. 其他常见方法

记不住的查一下`mdn`网站

| 方法          | 作用                                      | 说明                                                         | 语法                                                         |
| ------------- | ----------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| join()        | 为数组元素拼接字符串                      | 返回字符串                                                   |                                                              |
| find()        | 查找元素                                  | 返回符合条件的第一个数组元素值，如果没有符合条件的则返回`undefined` | arr.find(callback, [, thisArg])<br />callback就是回调函数，就是function(){} |
| every()       | 检测数组<b>所有</b>元素是否都符合指定条件 | 如果<b>所有元素</b>都通过检测返回`true`; 否则返回`false`; 若收到一个空数组，在此方法下一切情况都会返回`true` |                                                              |
| some()        | 检测数组中的元素是否满足指定条件          | 如果数组中有元素都通过检测返回`true`; 否则返回`false`        |                                                              |
| concat()      | 合并两个数组                              | 返回生成的新数组                                             |                                                              |
| sort()        | 对原来的数组单元值排序                    |                                                              |                                                              |
| splice()      | 删除或替换原来的数组元素                  |                                                              |                                                              |
| reverse()     | 反转数组                                  |                                                              |                                                              |
| findIndex()   | 查找元素的索引值                          |                                                              |                                                              |
| Array. from() | 将伪数组转换为真数组!! 静态方法           | 返回一个新的真数组                                           | 判定伪数组可以使用pop()方法，伪数组不能使用                  |

![image-20240317095134552](/img/Javascript/image-20240317095134552.png)

```javascript
// find()
const arr = ['red','blue','green']
const re = arr.find(function(item){
    return item === 'blue'
})
console.log(re)
// find()使用场景
const arr = [
    {
        name :'小米'，
        price: 1999
    },
    {
        name:'华为'，
        price: 3999
    },
    {
        name :'小米'，
        price: 1999
    }
]

arr.find(function(item){
    item.name == '小米'
    return item
})
// 箭头函数版 
arr.find (item =>  item.name == '小米')


// every()
[12,5,8,130,44].every(x => x>=10 ); false
[12,130,44].every(x => x>=10); true

// some() 和 every()差不多，类似于&& 和 ||的区别
          
          
```



#### 3. 包装类型

> 之所以基本数据类型具有对象特征，是因为字符串、数值、布尔类型数据是JavaScript底层使用Object构造函数包装形成的，被称为包装类型

##### 1.String

| 属性/方法 | 名称                                                         | 描述                                   |
| --------- | ------------------------------------------------------------ | -------------------------------------- |
| 属性      | .length                                                      | 获取字符粗汉长度                       |
| 方法      | .split('分隔符')                                             | 将字符串拆分称数组                     |
| 方法      | .substring( 需要截取的第一个字符的索引, [结束的索引号])      | 用于字符串截取                         |
| 方法      | startsWith( 搜索字符串 [, 检测位置索引号])， 返回布尔值      | 检测是否以某字符开头                   |
| 方法      | includes(搜索的字符串[, 检测位置索引号])， 返回布尔值。区分大小写!! | 检测一个字符串是否包含在另一个字符串中 |



```javascript
// str.split() 和 arr.join() 作用相反
const str = 'pink, red'
const arr = str.split(',')
console.log(arr); // ['pink', 'red']

const str1 = '2022-4-8'
const arr1 = str1.split('-')
console.log(arr1) //['2022','4','8']

// str.substring()
const anyString = 'Mozilla'
anyString.substring(1) //ozilla

// str.startsWith(searchString [,position])
const str = "To be, or not to be, that is a question"
str.startsWith('To be') //True
str.startsWith('not to be') //False
str.startsWith('not to be',10) //True

// str.includes() 方法区分大小写
'Blue Whale'.includes('blue') // False
str.includes('To be',1) // False
```

##### 2.Number

| 属性/方法 | 名称                       | 描述                 |
| --------- | -------------------------- | -------------------- |
| 方法      | .toFixed()                 | 设置保留小数位的长度 |
| 方法      | String(num)或者.toString() | 转换为字符串         |
|           |                            |                      |

```javascript
const price = 23.345
// 保留两位小数，四舍五入
price.toFixed(2) 23.35
```

# Day3

面向过程编程： 分析出解决问题所需要的步骤，然后用函数把步骤逐步实现，使用的时候再依次调用

面向对象编程：把事务分解成一个对象，由对象之间分工合作。以对象功能来划分问题，而不是步骤

## 1. 面向对象编程 (OOP)

+ 在面向对象程序开发思想中，每一个对象都是功能中心，具有明确的分工

+ 面向对象编程具有灵活、代码可复用、容易维护和开发的优点，更适合多人合作的大型软件项目。

+ 面向对象具有：

  -> 封装性

  -> 继承性

  -> 多态性

### 面向过程编程 vs 面向对象编程

| 名称         | 优点                                                         | 缺点                               |
| ------------ | ------------------------------------------------------------ | ---------------------------------- |
| 面向过程编程 | 性能比面向对象高，适合与硬件联系很紧密，如单片机就采用面向过程编程 | 没有面向对象易维护、易复用、易扩展 |
| 面向对象编程 | 易维护、易复用、易扩展，由于面向对象有封装、继承、多态性的特征。可以设计出低耦合的系统，使系统更加灵活、更加易于维护 | 性能比面向过程低                   |

## 2. 构造函数

+ 封装是面向对象思想中比较重要的一部分，`JS`面向对象可以通过<b>构造函数实现封装</b>
+ 将变量和函数组合到了一起并能通过`this`实现数据的共享，构造函数创建出来的实例对象之间彼此互不影响
+ 但是会出现浪费内存的问题，比如`sing()`方法，每一个对象都会创建

```javascript
function Star(uname, age){
    this.uname = uname
    this.age = age
    this.sing = function(){
        console.log('我会唱歌')
    }
}
const ldh = new Star('刘德华'，55)
const zxy = new Star('张学友'，55)
```

![image-20240320164120130](/img/Javascript/image-20240320164120130.png)

为了避免内存浪费的出现，引入原型知识点

## 3. 原型

### 1. 什么是原型

+ 构造函数通过原型分配的函数是所有对象所共享的
+ `JavaScript`每个<strong><b>构造函数</b>都有一个`prototype`属性</strong>，指向另一个对象，所以我们也称原型对象
+ 原型对象可以挂载函数，对象实例化不会多次创建原型上的函数，从而节约内存
+ <strong>将不变方法，直接定义在`prototype`对象上，这样所有对象的实例就可以共享这些方法</strong>
+ <strong>构造函数和原型对象中的`this`都指向实例化的对象</strong>

```javascript
// 公共的属性写到构造函数里
function Star(uname, age){
    this.uname = uname
    this.age = age
    this.sing = function(){
        console.log('我会唱歌')
    }
}
Star.prototype 
// 看起来像属性，但是返回值是对象

// 公共的方法写到了原型对象身上
Star.prototype.sing = function(){
    console.log('我会唱歌')
}
const ldh = new Star('刘德华'，55)
const zxy = new Star('张学友'，55)
ldh.sing()
zxy.sing()
//此时 
ldh.sing === zxy.sing //true
```

![image-20240320182749734](/img/Javascript/image-20240320182749734.png)

#### 总结：

1. 原型是什么？

   一个对象，我们称 `prototype` 为原型对象

2. 原型的作用是什么？

   共享方法

   可以把那些不变的方法，直接定义在`prototype对象上

3. 构造函数和原型里面的`this`指向实例化对象

#### 案例：

> 给数组对象添加扩展方法， 求和 与 最大值

```javascript
// 数组扩展方法
// 最大值, 添加方法
const arr = [1,2,3]
Array.prototype.max = function(){
    // 展开运算符
    return Math.max(...this)
}
arr.max()

// 求和 
Array.prototype.sum = function(){
    return this.reduce((prev,item)=>{prev+item},0)
}
```

### 2. constructor 属性

>  每一个原型对象都有一个constructor属性

#### 1. 定义

该属性指向该原型对象的构造函数`Star.prototype.constructor`

![image-20240320193128055](/img/Javascript/image-20240320193128055.png)

![image-20240320193548487](/img/Javascript/image-20240320193548487.png)

```javascript
function Star(){}
// Star已经是构造函数了，肯定有prototype的属性了
Star.prototype.contructor
// prototype对象有constructor的属性，指回Star构造函数
```

#### 2. 使用场景

如果有多个对象方法，我们可以给原型对象采取对象形式赋值。但是这样就会覆盖构造函数原型对象原来的内容，意味着修改后的原型对象constructor就不再指向当前的构造函数。此时我们可以在修改后的原型对象中，添加一个contructor指向原来的构造函数。

```javascript
function Star(name){
    this.name = name
}
// 以对象的形式批量添加原型方法
Star.prototype = {
    // 需要手动添加constructor，指回Star构造函数
    constructor: Star,
    sing:function(){console.log('唱歌')},
    dance:function(){console.log('跳舞')}
}
// 这样的话，prototype中的constructor的属性就会被覆盖
```

总结：

​	constructor 属性的作用是什么?

+ 指向该原型对象的构造函数

### 3. 对象原型

实例对象都会有一个属性 `__proto__`指向构造函数的`prototype`原型对象，之所以我们对象可以使用构造函数`prototype`原型对象的属性和方法，就是因为有`__proto__`原型的存在

__对象原型`proto `指向该 构造函数的 原型对象 （对象原型指向原型对象!!）__

```javascript
function Star(){}
const ldh = new Star()
// 对象原型__proto__指向 该 构造函数的原型对象
console.log(ldh.__proto__)
//Star.prototype
// 所以!!!!!!
ldh.__proto__ === Star.prototype
Star.prototype.constructor //是Star
// 所以!!
ldh.__proto__.constructor === Star

```

![image-20240320204447686](/img/Javascript/image-20240320204447686.png)

总结：

1. prototype 是什么? 哪里来？

   原型对象

   每个构造函数都有原型

   `Star.prototype`可以挂载相同的方法

2. constructor属性在哪里? 作用是什么？

   `prototype`原型和对象原型`__proto__`都指向创建实例对象/原型的构造函数

3. `__proto__`属性在哪里？指向谁？

   在实例对象里面，指向prototype原型

   __对象原型指向原型对象__, 只读不可以赋值

### 4. 原型继承

#### 错误版本!! 会导致混乱

```javascript
// 将公共类放在原型上
const Person = {
    eyes: 2,
    head: 1
}
// 女生 构造函数，通过原型继承Person
function Women(){}
Women.prototype = Person
Women.prototype.constructor = Women
// 添加女生类的单独的方法，但是会出现将男生类方法一起修改的情况
Women.prototype.say = function(){
    console.log("我是女生，漂亮的女生")
}

function Man(){
    Man.prototype = Person
    Man.prototype.constructor = Man
}
```

#### 正确版本，利用继承

```javascript
// 将Person变成类 (构造函数)
function Person(){
    eyes: 2,
    head: 1
}
function Woman(){
    
}
// prototype上存一下不变的方法
Woman.prototype = new Person()
Woman.prototype.constructor = Woman
```

### 5. 原型链

> 基于原型对象的继承使得不同构造函数的原型对象挂念在一起，并且这种关联的关系是一种链式结构，我们将原型对象的链状结构关系称为原型链

#### 前提： 

1. 只要是对象都有原型 `__proto__`
2. 只要是原型对象都具备`constructor`属性，指回创造原型对象的构造函数

![image-20240321101145316](/img/Javascript/image-20240321101145316.png)

![image-20240321112732846](/img/Javascript/image-20240321112732846.png)

#### 原型链->查找规则

1. 当访问一个对象的属性(包括方法)时，首先查找这个对象自身有没有该属性。
2. 如果没有就查找它的原型 `.__proto` 指向`prototype`原型对象
3. 如果还是没有就查找原型对象的原型
4. 依次类推一直找到Object为止`(null)`
5. `.__proto__`对象原型的意义在于为对象成员查找机制提供一个方向或路线
6. 可以使用`instanceof`运算符来检测构造函数`prototype`属性是否出现在某个实例对象的原型链上

#### instance

```javascript
ldh instanceof Person // true
ldh instanceof Object // true
ldh instanceof Array // false
[1,2,3] instanceof Array // true
Array instanceof Object // 万物皆对象
```

# Day4

## 1. 深浅拷贝

> 首先浅拷贝和深拷贝只针对于引用类型
>
> 堆中永远存储引用类型，值类型可以存在堆也可以存在栈

### 1. 浅拷贝

拷贝的是地址， 只拷贝最外面的一层。像是嵌套对象还是指向同一个地址。所以单层没问题，如果出现嵌套，就会出现修改原数据的情况。

+ 拷贝对象 `Object.assign()` `{...obj}`
+ 拷贝数组 `Array.prototype.concat()` `[...arr]`

```javascript
const obj = {
    uname: 'pink',
    age: 18
    family:{ // 这一层还是指向同一个地址
    	baby:'pink'
	}
}
const o = {}
Object.assign(o,obj) // 浅拷贝
const o  = {...obj} // 浅拷贝的另一种形式
```

![image-20240321175828112](/img/Javascript/image-20240321175828112.png)

总结：

1. 直接赋值和浅拷贝有什么区别？

   + 直接赋值的方法，只要是对象，都会相互影响，因为是直接拷贝对象栈里面的地址

   + 浅拷贝如果是一层对象，不相互影响，如果出现多层对象拷贝还是会相互影响

2. 浅拷贝如何理解？

   + 拷贝对象之后，里面的属性值是简单数据类型直接拷贝值
   + 如果属性值是引用数据类型则拷贝的是地址


### 2. 深拷贝

> 首先浅拷贝和深拷贝只针对引用类型

深拷贝：拷贝的是对象，不再是地址

#### 三种深拷贝方法

##### 1. 函数递归

> 如果一个函数在内部自己调用自己，此函数就是递归函数

+ 函数内部自己调用自己，这个函数就是递归函数
+ 递归函数的作用和循环效果类似
+ 由于递归很容易发生“栈溢出”错误 (stack overflow), 所以必须要加退出条件`return`

```javascript
let i =1
function fn(){
    console.log(`这是第${i}次`)
    if (i >= 6){ // 退出条件
        return
    } 
    i++
    fn() // 自己调用自己
}
```

条件：

+ 自己调用自己
+ 有终止条件

```javascript
// 为了更好的递归，利用递归函数实现setTimeout模拟setInterval效果
function getTime(){
    document.querySelector('div').innerHTML = new Date().toLocalString()
    setTimeout(getTime, 1000) // 自己调用自己
}
getTime()
```

浅拷贝案例：

```javascript
const obj = {
    uname:'pink',
    age:18
    hobby:['乒乓球','足球']
}
const o = {}
//拷贝函数 本质是浅拷贝
function deepCopy(newObj, oldObj){
    for(let k in oldObj){
        // k 属性名 uname   oldObj[k] 属性值18
        // newObj[k] === o.uname
        newObj[k] = oldObj[k]
    }
}
deepCopy(o,obj) 
//函数调用 两个参数 
// o->新对象 
// obj旧对象
o.age = 20 // 现在对象o改变，也不会影响obj
o.hobby[0] = '篮球' 
//还是会修改obj，所以本质!!! 是浅拷贝!!
```

递归深拷贝

+ 深拷贝的新对象不会影响浅拷贝的旧对象
+ 使用递归实现深拷贝
+ 如果遇到数组形式，加入`instanceof`判断
+ 如果遇到对象形式，再次利用递归解决对象
+ 先Array 后Object

```javascript
const obj = {
    uname:'pink',
    age:18
    hobby:['乒乓球','足球']
}
const o = {}
//拷贝函数 注意深拷贝数组需要在新对象中重新new
function deepCopy(newObj, oldObj){
    for(let k in oldObj){
        if (oldObj[k] instanceof Array){
            newObj[k] = []
            // 调用递归
            deepCopy(newObj[k],oldObj[k])
        } else{
            // k 属性名 uname   oldObj[k] 属性值18
            // newObj[k] === o.uname
        newObj[k] = oldObj[k]
        }
    }
}
deepCopy(o,obj) 
//函数调用 两个参数 
// o->新对象 
// obj旧对象
o.age = 20 // 现在对象o改变，也不会影响obj
o.hobby[0] = '篮球' 
```

##### 2. cloneDeep/lodash

Loads 库 `_.cloneDeep(value)`

```html
<script src = './lodash.min.js'></script>
const obj = {
    uname: 'pink',
    age: 18,
    hobby: ['乒乓球','足球'],
    family:{
        baby:'小pink'
    }
}
const o = _.cloneDeep(obj) // 深拷贝！

```

##### 3. JSON.stringify()

```javascript
const obj = {
    uname: 'pink',
    age: 18,
    hobby: ['乒乓球','足球'],
    family:{
        baby:'小pink'
    }
}
// 把对象转换为字符串
JSON.stringify(obj)
// 再把字符串转换成对象
const o = JSON.parse(JSON.stringify(obj))
// 新对象
// 转换成简单数据类型之后，直接存值，在转换成对象时，重新变成了新对象
```

总结：

1. 实现深拷贝的三种方式？

   函数递归

   lodash _cloneDeep

   JSON.stringify()

## 2. 异常处理

> 提升代码健壮性

### 1. throw 抛异常

异常处理是指预估代码执行过程中可能发生的错误，然后最大程度的避免错误的发生导致整个程序无法运行

`throw`会直接终止程序

```javascript
function couter(x,y){
    if(!x || !y){
        throw '参数不能为空' 
    }
}
```

```javascript
function couter(x,y){
    if(!x || !y){
        throw new Error('参数不能为空')
    }
}
```

总结：

+ `throw` 抛出异常信息，程序也会终止执行
+ `throw` 后面是错误提示信息
+ `Error` 对象配合`throw`使用，能够设置更详细的错误信息 `throw new Error('错误信息')`

### 2. try/catch 捕获异常

> 通过 try/catch 捕获错误信息

​	`try{} ` 预估的错误代码

​	`		catch(形参){}` 拦截错误信息，使用浏览器参数`error.message`

​	`finally{}` 不管程序对不对，一定会执行

```javascript
function foo(){
    try{
        // 可能发生错误的代码，写入try模块
        const p = document.querySelector('.p')
        p.style.color = 'red'
    } catch (err){
        console.log(error.message)
        // 错误信息
        // 拦截错误，提示浏览器提供错误信息，但是不中断程序执行，可以与 throw new Error('')配合使用，会中断程序
        return
        // 需要return 中断程序
    }
    finally {
        // 不管程序对不对，一定会执行的代码
        alert('执行')
    }
    console.log('如果出现错误，我的语句不会执行')
}
```

### 3. debugger

相当于断点的代码版，直接在需要调试的代码上一行写`debugger` 就行

## 3. 处理 this

### 1. 普通函数 this 指向

普通函数的调用方式决定了 `this` 的值，谁调用 `this`指向谁

```javascript
console.log(this) //this指向window
// 普通函数
function sayHi(){
    console.log(this)
}
// 函数表达式
const sayHello = function(){
    console.log(this)
}
// 函数的调用方式决定了 this 的值
sayHi()
window.sayHi() // window 调用

setTimeout(function(){
    console.log(this) //window
},1000) // 也是window， 因为本质是
window.setTimeout()

document.querySelector('button').addEventListener('click',function(){console.log(this)})
// 输出的是button，因为是button调用了函数

const obj = {
    sayHi:function(){
        console.log(this)
    }
}
obj.sayHi()
```

注意：

普通函数有严格模式，指向`undefined`

### 2. 箭头函数 this 指向

__箭头函数中并不存在 this__

1. 箭头函数会默认帮我们绑定外层 `this`的值，所以在箭头函数中的`this`值和外层的 `this`是一样的
2. 箭头函数中的 `this`引用的是最近作用域中的 `this`
3. 向外层作用域中，一层一层查找 `this`，直到有 `this`的定义

```javascript
const user = {
    name: '小明',
    walk: ()=>{
        console.log(this)
    }
}
// 此时对象里没有this，向上层寻找 this 指向window
```

注意情况：

1. 在开发中使用箭头函数前需要考虑函数中` this` 的值，事件回调函数使用箭头函数时，`this` 为全局`window`。因此`DOM`事件回调函数如果里面需要`DOM`对象的`this`，则不推荐使用箭头函数

```javascript
// DOM 节点
const btn = document.querySelector('.btn')
// 箭头函数此时 this 指向了window
btn.addEventListener('click',()=>{
    console.log(this)
    // 由于使用箭头函数，所以此时的this指向window
    // 因为this绑定外层
})
btn.addEventListener('click',function(){
    console.log(this)
    // 普通函数的this则指向调用者
})
```

2. 基于原型的面向对象也不推荐采用箭头函数

```javascript
function Person(){
}
// 原型对象上添加箭头函数
Person.prototype.walk = () => {
    console.log('人都是要走路..')
    console.log(this); //指向window
}
const p1 = new Person()
p1.walk()
// 这个位置注意，面向原型本质是挂载方法，让其他实例在创建之后就能使用，如果使用箭头函数，this无法指向实例对象，而是指向window
```

总结：

1. 箭头函数内不存在`this`,沿用上一级
2. 不适用：构造函数、原型函数、dom事件函数
3. 适用：需要使用上层 `this` 的地方

### 3. 改变 this

> JS 中允许指定函数中 this 的指向，有3个方法可以动态指定普通函数中 this 的指向

#### 1. call()

`function.call(thisArg, arg1, arg2, ...)`

+ thisArg: 在fun函数运行时指定的this值
+ arg1, arg2: 传递其他参数
+ 返回值就是函数的返回值，因为他就是调用函数

```javascript
const obj = {
    uname : 'pink'
}
function fn(x,y){
    console.log(this) // window
    console.log(x+y)
}
// 使用call方法改变函数指向
fn.call(obj,1,2)
// 输出obj函数 和3
```

#### 2. apply()

> 使用apply方法调用函数，同时指定被调用函数中的this的值

​	`function.apply(thisArg, [argsArray])`

+ thisArg: 在 fun函数 运行时指定的this值
+ argsArray: 传递值，必须包含在__数组__里面
+ 返回值就是函数的返回值，因为他就是调用函数
+ 因此apply主要跟数组有关系，比如`Math.max()`

```javascript
const obj = {
    age:18
}
function fn(x,y){
    console.log(this) 
    // {age: 18}
    console.log(x+y)
}
fn.apply(obj,[1,2]) // 18 , 3

// 使用场景： 求数组最大值
const max = Math.max(1,2,3)
// 使用Math.max方法
const arr = [100, 44, 77]
const max = Math.max.apply(Math, arr)
const min = Math.min.apply(Math, arr)
// 这个案例写Math和null都可以
const max = Math.max.apply(null, arr)
const min = Math.min.apply(null, arr)

// 第二种求数组最大值的方法, 扩展运算符
console.log(Math.max(...arr))
```

总结：

call 和 apply的区别是什么？

+ 都是调用函数，都能改变 `this` 指向
+ 参数不一样， `apply`传递必须时数组

#### 3. bind() 重点

> bind( ) 方法不会调用函数。但是能改变函数内部 this 指向

​	`function.bind(thisArg, arg1, arg2, ...)`

+ thisArg: 在 function 函数运行时指定的 this 值
+ arg1, arg2: 传递的其他参数
+ 返回值 由指定的 this 值和初始化参数改造的 __原函数拷贝 （新函数）__
+ 因此当我们只是想改变 `this` 指向，并不想调用这个函数的时候，可以使用 `bind`， 比如改变定时器内部的 `this` 指向

```javascript
const obj = {
    age: 18
}
function fn(){
    console.log(this)
}
// 1. bind 不会调用函数
// 2. 能改变 this 窒息那个
// 3. 返回值是一个函数，但是这个函数里面的this是更改过的
const fun = fn.bind(obj)
fun()
```

```javascript
// 定时器内部的例子
document.querySelector('button').addEventListener('click',function(){
    // 禁用按钮
    this.disabled = true
    window.setTimeout(function(){
        this.disabled = false
    }.bind(this), 2000)
})
```

call(), apply(), bind() 总结

1. 相同点

   都可以改变函数内部的 `this` 指向

2. 区别点

   + call 和 apply会调用函数，并且改变函数内部`this`指向

   + call 和 apply传递参数不一样, call 传递参数 `arg1, arg2, ...`形式， apply则必须是数组形式`[arg]`
   + Bind 不会调用函数，可以改变函数内部`this`指向

3. 主要应用场景

   + call 调用函数并且可以传递参数

   + apply 经常与数组有关，比如借助数学对象实现数组最大值最小值

   + bind 不调用函数，但是还想改变 this 指向，比如改变定时器内部 this 指向

## 4. 防抖 (debounce)

> 在单位时间内，频繁触发事件，只执行最后一次。 类似王者荣耀回城，只要被打断就需要重新再来

![image-20240322151457196](/img/Javascript/image-20240322151457196.png)

### 1. lodash 提供防抖处理

`_.debounce(func,[wait = 0],[option=])`

案例： 鼠标在盒子上移动，鼠标停止500ms之后，里面的数字+1

```javascript
const box = document.querySelector('.box')
let i = 1
function mouseMove(){
    box.innerHTML = i++
}
// box.addEventListener('mousemove',mouseMove)

// 利用lodash库实现防抖 500ms之后采取+1
// 语法： _.debounce(fun,时间)
box.addEventListener('mousemove',_.debounce(mouseMove, 500))
```

### 2. 手写防抖函数

核心思路： 防抖核心就是利用定时器 (setTimeout) 来实现

1. 声明一个定时器变量
2. 当鼠标每次滑动都先判断是否有定时器，如果有定时器先清楚以前的定时器
3. 如果没有定时器则开启定时器，记得存在变量里
4. 在定时器里面调用执行的函数

```javascript
// 创建一个函数 第一个参数时方法，第二个是时间
function mouseMove(){
    box.innerHTML = i++
}

function debounce(fn, t){
    let timer 
    return function(){
        // 如果有删除掉
        if（timer）clearTimeout(timer)
        timer = setTimeout(function(){
            fn() 
        },t)
    }
    
}
box.addEventListener('mousemove',debounce(mouseMove, 500))
```

## 5. 节流 （throttle）

> 单位时间内，频繁触发事件，只能执行一次。王者荣耀的技能冷却，期间无法继续释放技能

![image-20240322153915528](/img/Javascript/image-20240322153915528.png)

节流适用于__高频事件: __像是鼠标移动`mousemove`， 页面尺寸缩放`resize`, 滚动条滚动`scroll` 等等

### 1. lodash 提供节流函数

​	`_.throttle(function, 时间)`

案例

```javascript
const box = document.querySelector('box')
let i = 1
function mouseMove(){
    box.innerHTML = i++
    // 如果里面存在大量消耗性能的代码，如dom操作、数据处理，可能会造成卡顿
    // 利用Lodash库实现节流， 500ms之后采取+1
    box.addEventListener('mousemove',_.throttle(mouseMove, 500))
}
```

### 2. 手写节流函数

核心思路： 防抖核心就是利用定时器 (setTimeout) 来实现

1. 声明一个定时器变量
2. 当鼠标每次滑动都先判断是否有定时器，如果有定时器先清楚以前的定时器
3. 如果没有定时器则开启定时器，记得存在变量里
4. 在定时器里面调用执行的函数
5. 在定时器里面把定时器清空

```javascript
const box = document.querySelector('box')
let i = 1
function mouseMove(){
    box.innerHTML = i++
    // 如果里面存在大量消耗性能的代码，如dom操作、数据处理，可能会造成卡顿
    // 利用Lodash库实现节流， 500ms之后采取+1
}
function throttle(fn, t){
    let timer = null
    return function(){
        if(!timer){
            timer = setTimeout(function(){
                fn()
                // 清空定时器
                // 为什么不用clearTimeout？
                // 因为不能在开启的定时器里，删除定时器
                timer = null
            },t)
        }
    }
}
box.addEventListener('mousemove',throttle(mouseMove, 500))
}
```

### 防抖和节流总结

| 性能优化 | 说明                                     | 使用场景                                                     | 王者荣耀类比 |
| -------- | ---------------------------------------- | ------------------------------------------------------------ | ------------ |
| 防抖     | 单位时间内，频繁触发事件，只执行最后一次 | 搜索框搜索输入、手机号、邮箱验证输入检测                     | 回城         |
| 节流     | 单位时间内，频繁触发事件，只执行一次     | 高频事件：鼠标移动mousemove、页面尺寸缩放 resize、滚动条滚动scroll | 技能冷却     |

### 补充视频相关事件

| 事件名称     | 事件描述                                                     |
| ------------ | ------------------------------------------------------------ |
| ontimeupdate | 在视频/音频(audio/video)当前的播放位置发送改变时触发         |
| onloadeddata | 事件当前帧的数据加载完成且还没有足够的数据播放视频/音频(audio/video)的下一帧时触发 |















