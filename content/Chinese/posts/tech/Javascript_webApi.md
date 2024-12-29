---
title : '学习: JavaScript WebAPIs篇'
date : 2024-02-27
lastmod: 2024-03-06
draft : false
author : "Jingyi Wu"
comments: true #是否展示评论
showToc: true # 显示目录
TocOpen: false # 自动展开目录
hidemeta: false # 是否隐藏文章的元信息，如发布日期、作者等
##disableShare: true # 底部不显示分享栏
ShowBreadCrumbs: true
ShowShareButtons: true
ShowReadingTime: true
ShowWordCounts: true
ShowPageViews: true
ShowLastMod: true #显示文章更新时间
hasCJKLanguage: true
summary: "JavaScript WebApi!! 程序媛养成之路"

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

## 变量声明

> <b>var、 let 、const<b>

在使用中应该优先使用const

+ const 语义化更好
+ 很多变量在声明时表示标量不会更改
+ 实际开发中，react框架，基本const
+ 如果事后发现需要被更改，再改为let

案例:

以下案例可不可以把let改外const ?

```javascript
let name = '刘德华'
let song = '忘情水'
document.write(name + song) //可以，因为值没有被改变
```

```javascript
let num1 = +prompt('请输入第一个数值: ')
let num2 = +prompt('请输入第二个数值: ')
alert(`两者相加的结果是：${num1} + ${num2} `)
//可以，因为值没有被改变
```

```javascript
let num = 1
num = num + 1 //不可以，值被改变了

//如下同理
for (let i = 0;i < nums.length; i++){
    document.write(nums[i])
}  
//i的值一直被改变
```

```javascript
let arr = ['red','green']
arr.push('pink')
// 可以，因为arr的地址没有变，只是内容发生了变化

let person = {
    uname: 'pink老师',
    age: 18,
    gender:'女'
}
person.address = '武汉黑马'
// 也可以 ，同理地址没变，只是内容发生了变化
```

+ const 声明的值不能更改，而且const声明变量的时候需要提前初始化
+ 但对于引用数据类型,   const声明变量，里面存的不是值，而是地址

```javascript
const names = []
names = [1, 2, 3]
// 不可以！！！，因为 [1,2,3]意味着是新的数组，新的地址

const obj = {}
obj = {
    uname: 'pink老师'
}
// 不可以！！ obj 已经是{},不能再次新建{}
// obj.name = 'pink老师' 可以通过这种形式
```

<b>为什么const声明的对象可以修改里面的属性？</b>

+ 因为对象是引用类型，里面存储的是地址，只要地址不变，就不会报错
+ 建议数组和对象使用const来声明

> 什么时候使用let声明变量？

+ 如果基本数据类型的值或者引用类型的地址发生变化的时候
+ 比如 一个变量进行加减运算，比如for循环中的i++

## 作用及分类

+ 使用 JS 去操作 html 和 浏览器

+ DAM(文档对象模型) 

  BOM(浏览器对象模型)

## DOM ( Document Object Model )

> 用来呈现以及任意 html 或 xml 文档交互的API
>
> DOM 是浏览器提供的一套专门操作网页内容的功能
>
> + 开发网页内容特效和实现用户交互

### DOM树

+ 将HTML文档以树状结构直观的表现出来，称为DOM树
+ 描述网页内容关系的名词
+ 作用： DOM树直观的体现了标签之间的关系

### DOM 对象

> 浏览器根据 html 标签生成 JS对象

+ 所有的标签属性都能在这个对象上面找到
+ 修改这个对象的属性会自动映射到标签身上

### DOM 的核心思想

+ 将网页当作对象处理

```javascript
const div = document.querySelector('div')
// typeof div  为dom对象 object
```

### document 对象

+ 是 DOM 里提供的一个对象, DOM里面最大的对象

+ 所以他提供的属性和方法都是用来访问和操作网页内容的

  > document.write ( )

+ 网页的所有内容都在document里面

### 获取 DOM 元素

<b>根据 CSS 选择器来获取 DOM 元素 （重点）</b>

#### 语法

##### 1. 选择匹配一个元素

```javascript
// 获取匹配的第一个元素
document.querySelector('css选择器')

// example
// 用标签获取
const box1 = document.querySelector('tag')
// 用class获取
const box2 = document.querySelector ('.class')
// 用id获取
const box3 = document.querySelector ('#id') 
// 嵌套标签
const box4 = document.querySelector ('ul li')
const box4 = document.querySelector ('ul li:first-child')
```

##### 2. 选择匹配多个元素

```javascript
document.querySelecorAll ('css选择器')
```

#### 参数

+ 包含一个或多个有效的 css 选择器 字符串

#### 返回值

+ `document.querySelector()`

  CSS 选择器匹配的第一个元素 (HTMLElement 对象)

+ `document.querySelectorAll('ul li')`

  CSS 选择器匹配的 NodeList 对象集合

  !! <b>NodeList 是伪数组</b>

  1. 有长度、有索引
  2. 但没有pop(), push()等数组方法

  想要得到里面的每个对象，需要<b>遍历(for)的方式</b>获得，注意数组的遍历用for，对象的遍历用 for in

#### 总结

+ 获取一个DOM元素使用querySelector(), 可以直接修改
+ 获取多个DOM元素使用querySelectorAll( ), 通过遍历的方式修改



<b>其他获取DOM元素方法 (了解)</b>

```javascript
document.getElementById('nav')
document.getElementsByTagName('div')
document.getElementsByClassName('w')
```

### 操作元素内容

> 能够修改元素的文本，更换内容

+ DOM 对象都是根据标签生成，所以操作标签，本质上是操作DOM对象

+ 操作对象使用 的点语法

+ 如果想要修改标签元素里面的内容，则可以使用如下几种方式：

  `obj.innerText`-> 属性

  `obj.innerHTML`-> 属性

#### 元素innerText属性

+ 将文本内容添加/更新到任意标签位置
+ 显示纯文本，不解析标签

#### 元素innerHTML属性

+ 与上方innerText大致相同，但是解析html标签

```html
<body>
    <div class = "box"> 我是文字内容 </div>
    <script>
        const box = document.querySelector('.box')
        console.log(box.innerText) //获取文字内容
        box.innerText = '我是一个盒子' //修改文字内容
        box.innerText = '<strong> 我是一个盒子 </strong>'
        // strong 会按照文本形式输出，不会解析为加粗
        
        //innerHTML
        console.log(box.innerHTML) //获取内容
        box.innerHTML = '<strong> 我是一个盒子 </strong>'
        //会变粗，解析html标签
    </script>
    
</body>
```

### 操作元素属性

#### 操作元素常用属性

+ 通过 JS 设置/修改标签元素属性，比如通过src更换图片

+ 常见属性：href、title、src

+ 语法: `obj.attribute = value`

  ```javascript
  //1. 获取元素
  const pic = document.querySelector('img')
  //2. 操作元素
  pic.src = '/images/b-2.ipg'
  pic.title = '刘德华黑马演唱会'
  //3. body不需要获取，直接选择
  document.body = '....'
  ```

#### 操作元素样式属性

+ 还可以通过 JS 设置/修改标签元素的样式属性

  > 轮播图小圆点自动更换样式颜色
  >
  > 点击按钮可以滚动图片，移动图片位置等等

##### style属性操作CSS

语法

`obj.style.attribute = value`

```html
CSS 样式
<style>
    div{
        width: 200px;
        height: 200px;
        background-color: pink;
    }
</style>

<body>
    <div class = 'box'></div>
    <script>
        // 1. 获取元素
        const box = document.querySelector('.box')、
        // 2. 修改样式 对象.style.样式属性 = '值'  记得+单位
        //    style 关键词是固定不变的！！！
        box.style.width = '300px'
        // css多组单词， background-color 转换成小驼峰命名法
        box.style.backgroundColor = 'hotpink'
        box.style.border = '2px solid blue'
        box.style.borderTop = '2px solid red'
    </script>
</body>
```

<b>总结</b>

+ 设置/修改元素样式属性通过 <b>style属性引出来</b>

+ 如果修改div盒子的样式，比如padding-left，如何写？

  Element.style.paddingLeft = '300px' <b>小驼峰命名法</b>

+ 因为我们是样式属性，大部分数字方面需要➕单位px

##### 类名className操作CSS

+ 如果修改的样式比较多，直接通过style属性修改比较繁琐，我们可以通过借助css类名的形式

+ 语法

  ```javascript
  元素.className = 'css里面的类名'
  ```

+ 由于class是保留词、关键字，所以使用className去代替
+ className是使用新值换旧值

```html
<head>
	<style>
    	div {
        	width: 200px;
        	height:200px;
        	background-color: pink;
        }
        .nav{
            color: red
        }
    	.box{
            width: 300px;
        	height: 300px;
        	background-color: skyblue;
        	margin: 100px auto;
        }
    </style>
</head>
<body>
    <div class = 'nav'> 123 </div>
    // nav class会被 js 覆盖掉,换成box，样式也会被替换

    <script>
        const div = document.querySelector('div')
        // 把div的class设置为box，这样可以更换样式
        div.className = 'box'
        
        //如果我两个类名的样式都想保留
        div.className = 'nav box'
    </script>
</body>
```

##### 常用!! classList -> 操作类控制CSS

+ 为了解决className容易覆盖以前的类名，通过classList方式追加和删除类名
+ 语法

```javascript
// 追加一个类
元素.classList.add('类名')
// 删除一个类
元素.classList.remove('类名')
//切换一个类
元素.classList.toggle('类名')
```

+ 案例

```html
<head>
    <style>
        .box {
            width: 200px;
            height: 200px;
            color: #333
        }
        .active {
            color: red;
            background
            
        }
    </style>
</head>
<body>
    <div class = 'box '> 文字 </div>
    <script>
        // 通过classList添加
        // 1. 获取元素
        const box = document.querySlector('.box')
        // 2.1 修改样式->追加
        box.classList.add('active')
        // 2.2 修改样式->移除
        box.classList.remove('box')
        // 2.3 修改样式->切换
        // 先查看此类有还是没有，有就删掉，没有就添加,像是开关
        box.classList.toggle('active')
        
    </script>
</body>

```

<b>总结</b>：使用className 和 classList区别

+ 修改样式方便
+ classList 是追加、删除不影响之前的类名



#### 操作表单元素属性

+ 用value提取内容，不能是使用innerHTML
+ 用type切换文本和密码的展现形式

```html
<body>
    <input type = "text" value = "电脑">
    <script>
    const uname = document.querySelector('input')
    uname.value //电脑
    uname.value //设置表单value值
        
	// 设置密码形式
    uname.type = 'password'
    </script>
</body>
```

+ 表单属性中添加就有效果，移除没有效果，使用布尔值来表示
+ `true -> 添加钙属性`，`false -> 移除该属性`
+ `disable /checked/ selected`

```html
<input type = "checkbox" name = '' id = "" checked> 
	//属性与值相同，可省略
<script>
    // 获取
    const ipt = document.querySelector('input')
    console.ipt(ipt.checked) //true
    // 修改check的状态
    ipt.checked = true //更改为勾选状态，布尔值不加“”
</script>
```

#### 自定义属性

+ 标准属性： 自带的属性 class、 id、 title等等，可以直接使用 点语法操作

  `disabled checked selected`

+ 自定义属性：

  HTML 5 退出来专门data的自定义属性

  标签上一律以`data-`开头

  在DOM对象上一律以`dataset`对象方式获取

```html
<body>
    <div class = "box" data-id = "10">盒子</div>
    <script>
        const box = documet.querySelector('.box')
        console.log(box.dataset.id)
    </script>
</body>
```

#### 间歇函数-定时器

> 定时器函数可以开启和关闭定时器

1. 开启定时器

   > 定时器的返回值是，定时器独有的 ID 号

```javascript
setInterval(函数/函数名，间隔时间)

// 间歇函数一旦开启，永不停歇
// 案例
// 使用匿名函数
setInterval (function(){console.log('一秒执行一次')},1000)
// 使用指定函数
function fn(){
    console.log('一秒执行一次')
}
setInterval (fn, 1000)
// 因为fn()表示立即调用函数，不符合每隔一秒钟调用

// 定时器又开有关，在内存中可能会用变化，使用let声明
let n = setInterval (fn, 1000)
console,log(n)  // id = 2
```

2. 关闭定时器

+ 作用： 每隔一段时间调用这个函数
+ 间隔单位是毫秒

```javascript
let 变量名 = setInterval(函数，间隔时间)
clearInterval(变量名)

//一般不会刚创建就停止，而是满足了一定条件再停止

//案例
let timer = setInterval(function(){
    console.log('hi!!!~~~'), 1000
})
clearInterval(timer)
```

# Day2

>  能够给DOM元素添加事件监听​	

1. 什么是事件？

   事件是编程时系统内发生的动作或者发生的事情

   比如用户在网页上单击一个按钮

2. 什么是事件监听？

   让程序检测是否有事件产生，一旦有时间触发，立即调用一个函数做出响应，称为绑定事件或者注册事件。比如鼠标经过显示下拉菜单，如果点击可以播放轮播图等等

## 事件监听

### 语法

 `元素对象.addEventListener('事件类型'，要执行的函数)`

### 三要素

- 事件源：被事件触发的dom元素
- 事件类型： 用什么方式触发，比如鼠标单击 <b>click</b>,  鼠标经过<b>mouseover</b> 等等
- 事件调用函数： 要做什么事

```html
<button>
    <script>
        const btn = document.querySelector('.btn')
        //修改元素样式
        //注意事件类型必须是字符串形式
        //此函数是，点击之后再去执行，每次点击都会执行一次
        btn.addEventListener('click',function(){
            alert('点击了～～')
        })
    </script>
</button>
```

### 事件类型

|      鼠标事件       |      焦点事件       |      键盘事件      |      文本事件       |
| :-----------------: | :-----------------: | :----------------: | :-----------------: |
|   <i>鼠标触发</i>   | <i>表单获得光标</i> |  <i>键盘触发</i>   | <i>表单输入触发</i> |
|   click 鼠标点击    |   focus 获得焦点    |  keydown 键盘按下  |  input用户输入事件  |
| mouseenter 鼠标经过 |    blur 失去焦点    | keyup 键盘抬起触发 |                     |
| mouseleave 鼠标离开 |                     |                    |                     |

## 事件对象

​	事件对象是什么？

- 有事件触发时的相关信息

  例如： 鼠标点击事件中，事件对象存储了鼠标点的位置信息等等

- 使用场景

  可以判断用户按下拿个键，比如按下回车键可以发布新闻

  可以判断鼠标点击了哪个元素，从而做相应的操作

### 语法

- 在事件绑定的回调函数的第一个参数就是事件对象

- 一般命名为 `event  ev  e`

- 部分常用属性

- 补充 `str.trim()` ->去除字符串两侧空格

  | 属性              | 描述                                     |
  | ----------------- | ---------------------------------------- |
  | type              | 获取当前的事件类型                       |
  | clientX / clientY | 获取光标相对于浏览器可见窗口左上角的位置 |
  | offsetX / offsetY | 获取光标相对于当前DOM元素左上角的位置    |
  | key               | 用户按下的键盘的值                       |


```javascript
元素.addEventListener('click', function(e)){} 
// e就是事件对象

// 案例
const input = document.querySelector('input')
input.addEventListener('keyup',function(e){
    if (e.key === 'Enter'){
    console.log('我按下了回撤键盘')
}
})
```

## 环境对象

> 能够分析判断函数运行在不同环境中 this 所指代的对象

定义：指的是函数内部特殊的<b>变量this</b>，代表着当前函数运行时所处的环境。

- 简单一点，this 指的是函数的调用者
- 直接调用函数，相当于window.函数，所以this指代window

```javascript
const btn = document.querySelector('button')
btn.addEventListener('click', function(){
    //先前的写法
    btn.style.color = 'red'
    //this 版本
    this.style.color = 'red'
})
```

## 回调函数

> 被当作参数的函数，此函数就叫 call function 回调函数

如果将函数A作为参数传递给函数B，我们称函数A 为回调函数

```javascript
function fn(){
    console.log('我是回调函数!!')
}
//fn 传递给了setInterval，fn就是回调函数
setInterval(fn,1000)

//事件点击的本身也是回调函数
box.addEventListener('click', function(){
    console.log('也是回调函数!!')
})
```

总结

- 将函数当作另一个函数的参数传递，此函数叫回调函数
- 回调函数本质还是函数，只不过把它当成参数
- 使用匿名函数作为回调函数比较常见

​	
# Day3

## 事件流

> 事件流指的是事件完整执行过程中的流动路径

![image-20240302131910970](/Users/jingyiwu/Library/Application Support/typora-user-images/image-20240302131910970.png)

### 事件捕获

> 从大到小    例子： 中国->浙江->杭州

- 若给盒子都注册同名事件，在执行时，从DOM的根元素开始去执行对应的事件（从外到里）

- 事件捕获需要写对应代码才能看到效果

- 语法

  `DOM.addEventListener(事件类型，事件处理函数，是否使用捕获机制)`

- addEventListener 第三个参数传入 `true`代表捕获阶段触发（很少使用）
- 默认为false, 代表冒泡阶段
- 若使用L0事件监听, `onclick`，只有冒泡没有捕获

### 事件冒泡

> 从小到大    例子： 杭州->浙江->中国

- 当一个元素的事件被触发时，同样的事件将会在该元素的所有祖先元素中一次出发，这一过程被称为事件冒泡
- 当一个元素触发事件后，会依次向上调用所有父级元素的同名事件

#### 阻止冒泡

> 因为默认出现冒泡模式，导致事件影响到父级元素
>
> 若想把事件限制在当前元素内，需要组织事件冒泡
>
> 先拿到事件对象

##### 语法

```javascript
事件对象.stopPropagation()   
//e为事件对象
//此方法可以组织事件流动传播，对冒泡/捕获都有效
//案例
son.addEventListener('click',function(e){
    alert('我是儿子')
    e.stopPropagation()
}
```

## 解绑事件

### 1. on事件方式

​     直接使用null覆盖后就可以实现事件的解绑

```javascript
//L0 绑定事件
btn.onclick = function(){
    alert('点击了')
}
btn.onclick = null
```

### 2. L2事件方式

- 必须使用removeEventListerner (事件类型，事件函数，[获取捕获或冒泡阶段] )
- 匿名函数无法解绑 !!

```javascript
function fn(){
    alert('点击了')
}
//绑定事件
btn.addEventListener('click',fn)
//解绑事件
btn.removeEventListener('click',fn)
```

## 两种注册事件区别

|                                | 传统 on 注册(L0)   | 事件监听注册(L2)                           |
| ------------------------------ | ------------------ | ------------------------------------------ |
| 同一对象覆盖之前的同一注册事件 | 会                 | 不会                                       |
| 解绑事件方式                   | obj.onclick = null | obj.remove('click', fn) 匿名函数无法被解绑 |
| 可选冒泡/捕获                  | 只冒泡             | 可冒泡可捕获                               |

## 事件委托

> 事件委托利用事件流的特征解决一些开发需求的知识技巧 (事件冒泡)

- 优点： 减少注册次数，提高程序性能

- 原理：利用事件冒泡的特点

  给<b>父元素</b>注册事件，当触发子元素时，会冒泡到父元素身上，从而触发父元素的事件

- 实现：事件对象.target.tagName 可以获得真正的触发事件元素

```html
<ul>
    <li>第1个</li>
    <li>第2个</li>
    <li>第3个</li>
    <li>第4个</li>
    <li>第5个</li>
</ul>
```

```javascript
// 无事件委派
const lis = document.querySelector('ul li')
    for (let i = 0;i < lis.length; i++){
        lis[i].addEventListener('click',function(){
            alert('我被点击了')
        })
    }
// 事件委派
// 父元素添加点击事件
// 目前li子元素没有点击事件，但会冒泡至 ul 元素的点击事件
const parent = document.querySelector('ul')
parent.addEventListener('click', function (e) {
  console.log(e.target)
  // 我们点击的对象
  console.dir(e.target)
  //打印对象
  if (e.target.tagName == 'LI') {
    e.target.style.color = 'red';
  }
})
```

### 阻止默认行为发生

`	事件对象.preventDefalut`

```html
<a href = "http://www.baidu.com">百度一下</a>
## 正常链接会跳转，现在阻止他不让跳转
<script>
    const form = document.querySelector('form')
    form.addEventListerner('submit',function(e){
        e.preventDefalut()
    })
 ##   现在不会跳转了  
</script>
```

## 其他事件

### 页面加载事件

> 记载外部资源 (如图片、外联 css 和 javascript 等) 加载完毕时触发的事件

需要场景：

- 有些时候需要等页面资源全部处理完，再做一些事情
- 老代码喜欢把script 写在head中，这时候直接找dom元素找不到

事件名： `load`

1. 监听页面所有资源加载完毕，就执行回调函数

- 给window添加load事件

  ```javascript
  window.addEventListener('load', function(){
      //执行操作，等页面所有资源加载完毕，执行回调函数
      //避免了dom元素找不到的情况
      const btn = document.querySelector('button')
      btn.addEventListener('click',function(){
          alert(11)
      })
  })
  ```

1. 监听单个元素

- 注意： 不光可以监听整个页面资源加载完毕，也可针对某个资源绑定load事件

  ```javascript
  img.addEventListener('load',function(){
      //等待图片加载完毕，再去执行里面的代码
  })
  
  ```

1. 监听HTML 加载事件

- 当初始的HTML 文档被完全加载和解析完成之后, `DOMContentLoaded`事件被触发，无需等待样式表，图像等完全加载

- 事件名：`DOMComtentLoaded`

- 此时监听页面不是window 而是<b>document</b>!!

  ```javascript
  document.addEventListener('DOMContentLoaded',function(){
      //执行操作
  })
  ```

### 元素滚动事件

> 滚动条在滚动时持续触发的事件

1. 使用场景： 

很多网页需要检测用户把页面滚动在某一个区域后做一些处理，比如固定导航栏，比如返回顶部。⚠️有滚动条才行!!

1. 事件名：`scroll`

- 监听整个页面滚动（使用最多）

  补充，如果想获取html对象，使用`document.documentElement`

- 监听dom

```javascript
window.addEventListener('scroll',function(){
    //执行操作
    console.log(document.documentElement.scrollTop)
    const n = document.documentElement.scrollTop
    // n为数字型，不带单位
    if (n>=100){
        div.style.display = 'block'
    }else {
        div.style.display = 'none'
    }
})
document.addaddEventListener('scroll',function(){
    //执行操作
})
```

​		页面滚动事件 —获取位置

- scrollLeft 和 scrollTop（属性）

  获取被卷的大小

  获取元素内容向左，向上滚出去看不到的距离

  这两个值可读写

![image-20240302235856319](/Users/jingyiwu/Library/Application Support/typora-user-images/image-20240302235856319.png)

- scrollTo() 方法把内容滚动到指定坐标

```javascript
// 让页面滚动到指定坐标
windows.scrollTo(x,y)
```

### 页面尺寸事件

- 会在窗口尺寸改变时触发事件

```javascript
// resize 浏览器窗口大小发生变化的时候触发事件
windows.addEventListener('resize',function(){
    //z执行代码
})
```

- 检测屏幕宽高

  获取元素的可见部分宽高 (不包含边框, margin, 滚动条等)

```javascript
// clientWidth clientHeight
window.addEventListener('resize',function(){
    let w = document.documentElement.clientWidth
})
```

### 元素尺寸与位置

> 获取宽高

#### 获取宽高

- 获取元素的自身宽高、包含元素自身设置的宽高、padding、border
- `offsetwidth` `offsetHeight`
- 获取出来是数值， 方便计算
- 注意：获取的是<b>可视宽高</b>，如果盒子是隐藏的 (display: none), 获取结果是 0. 

#### 获取位置

- 获取元素距离自己最近带有定位属性的父级元素的左、上距离

- `offsetLeft` `offsetTop` 是 只读属性

- `element.getBoundingClientRect()`是方法

  返回元素的大小及其相对于<b>视口</b>的位置

总结

- offsetWidth 和 offsetHeight 得到元素的什么宽高？

  内容 + padding + border

- offsetTop 和 offsetLeft 得到的位置以谁为准？

  带有定位的父级

  如果都没有，则以文档左上角为准


| 属性                       | 作用                                   | 说明                                                       |
| -------------------------- | -------------------------------------- | ---------------------------------------------------------- |
| scrollLeft / scrollTop     | 被卷去的头部和左侧                     | 配合页面滚动来使用，可读写                                 |
| clientWidth / clientHeight | 获得元素宽度和高度                     | 不包含border, margin, 滚动条。用于js获取元素大小，只读属性 |
| offsetWidth / offsetHeight | 获得元素宽度和高度                     | 包含border、padding、滚动条等等，只读属性                  |
| offsetLeft / offsetTop     | 获取元素距离自己定位父级元素左、上距离 | 获取元素位置时使用，只读属性                               |

# Day4

## 日期对象

> 掌握日期对象，让网页显示日期
>
> 可以得到当前的系统时间

### 对象实例化

1. 在代码中`new`关键字时，将此操作称为实例化

1. 创建一个事件对象并获取时间

   获得当前时间： `const date = new Date()`

   获得指定时间：`const date = new Date('2022-5-1 08:30:00')`

   <i>可以在倒计时中使用</i>

### 日期对象方法

> 在开发中，日期对象返回的数据不能直接使用，需要转化成实际开发中的常用格式

| 方法           | 作用               | 说明             |
| -------------- | ------------------ | ---------------- |
| getFullYear( ) | 获得年份           | 获取四位年份     |
| getMonth( )    | 获得月份           | 取值 0-11        |
| getDate( )     | 获取月份中的每一天 | 不同月份取值不同 |
| getDay( )      | 获取星期           | 取值 0-6         |
| getHours( )    | 获取小时           | 取值 0-23        |
| getMinutes( )  | 获取分钟           | 取值 0-59        |
| getSecond( )   | 获取秒             | 取值 0-59        |

```html
<script>
    const div = document.querySelector('div')
    function getMyDate(){
        const date = new Date()
        let h = date.getHours()
        let m = date.getMinutes()
        let s = date.getSecond()
        h = h < 10 ? '0' + h : h
        m = m < 10 ? '0' + m : m
        h = s < 10 ? '0' + s : s
        return `${date.getFullYear()}Year ${date.getMonth()+1()}Month${date.getDate()}Day ${h}:${m}:${s}`}
    div.innerHTML = getMyDate
    // 让时间动起来
    setInterval (function(){
        div.innerHTML = getMyDate
    },1000)
</script>
```

其他简便形式

```html
<script>
    const div = document.querySelector('div')
    const date = new Date() //对象方法
    div.innerHTML = date.toLocalString() //2022/4/1 09:41:21
    div.innerHTML = date.toLocalDateString() // 2022/4/1
    div.innerHTML = date.toLocalTimeString() //09:41:21
    
    setInterval (function(){
        div.innerHTML = date.toLocalString()
    },1000)
    
</script>
```

### 时间戳

1. 什么是时间戳：

   从1970年1月1日起至现在的毫秒数，是一种特殊的计量时间的方式，使用场景倒计时

2. 算法：

   将来的时间戳 - 现在的时间戳 = 剩余时间毫秒数

   剩余时间毫秒数 转换为 剩余时间的 年 月 日 时 分 秒 就是倒计时时间

3. 举例：

   2000ms - 现在时间戳 1000ms = 1000ms

   转换后-> 0小时 0分 1秒

   `当前的时间戳      + new Date()`

4. 转换公式：

   `d = parseInt (总秒数/ 60/ 60/ 24)  //计算天数`

   `h = parseInt (总秒数/ 60/ 60 % 24) //计算小时`

   `m = parseInt (总秒数 /60 % 60)  //计算分钟`

   `s = parseInt (总秒数%60)  //计算当前秒数`


#### 获取时间戳的方法

1. 使用 `getTime()`  

   必须实例化

   ```javascript
   const date = new Date()
   console.log(date.getTime())
   
   const date = new Date('2022-4-1 18:30')
   ```

2. 简写 `+ new Date()`

3. 使用`Date.now( )`

   但是只能得到当前的时间戳，前面两种可以返回指定时间的时间戳

```javascript
const arr = ['星期天','星期一','星期二','星期三','星期四','星期五','星期六']
console.log(arr[new Date().getDay()])
```

#### 总结

1. 实例化日期对象怎么写？ new Date( )

2. 日期对象方法里面月份和星期有什么注意的?

   月份 0-11 （得+1）， 星期 0-6 (不用+1，0是周日)

1. 获取时间戳有哪三种方式？
   - date.getTime()
   - +new Date()
   - Date.now()
   - 重点记住 +new date() 既可以返回当前时间戳，也可以返回指定时间戳

## 节点操作

### DOM节点

> DOM 树里面的每一个内容都称为节点

#### 节点类型

##### 1. 元素节点-> 所有的标签 body, div；html 是跟节点

##### 2. 属性节点-> 所有的属性，比如href / class属性 

##### 3. 文本节点-> 所有的文本

##### 4. 其他节点

### 查找节点

> 基于关系的查找，返回内容还是对象

#### 父节点查找

1. parentNode属性

2. 返回最近一级的父节点，找不到返回为null. (亲爸爸)

   `子元素.parentNode`

```html
<body>
    <div class = "dad">
        <div class = "baby"></div>
    </div>
    <script>
        const baby = document.querSelector('.body')
        console.log(baby) // 返回dom对象
        console.log(baby.parentNode) // 返回dom对象
    </script>
</body>
```

#### 子节点查找

1. childNodes

   获得所有子节点，包括文本节点 (空格、换行)、注释节点等

2. children 属性 (重点)

   仅获得所有元素节点

   返回的还是伪数组, 和.querySelectorAll等价

   `父元素.children`

```html
<ul>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
</ul>
<script>
    const ul = document.querySelector('ul')
    console.log(ul.children) //得到所有子节点，伪数组 【亲儿子】
</script>
```

#### 兄弟关系查找

1. 下一个兄弟节点 `nextElementSibling`
2. 上一个兄弟节点 `previousElementSibling`

### 增加节点

> 需要在页面中增加元素
>
> 创建新的节点放入指定的元素内部

#### 1. 创建节点

> 创造出一个新的网页元素，在添加到网页，一般先创建节点，再插入节点

1. 创建元素节点的方法

```javascript
// 创造一个新的元素节点
document.createElement('标签名')
```

1. 追加节点

> 要想在界面看到，还得插入到某个父元素中

- 插入到父元素的最后一个子元素, 甚至会放到<script>标签后面

```javascript
// 插入到父元素的最后
父元素.appendChild(要插入的元素)
document.createElement('标签名')
const div = document.createElement('div')
document.body.appendChild(div)
```

- 插入到父元素中某个子元素前面

```javascript
父元素.insertBefore(要插入的元素，在哪个元素前面)

// 案例
const ul = document.querySelector('ul')
const li = document.queryElement('li')
li.innerHTML = '我是li'
ul.appendChild(li)   // 添加li为ul的最后与阿苏
ul.insertBefore(li, ul.children[0]) 
// 插入到列表第一个元素之前
// 
```

#### 2. 克隆节点

```javascript
// 克隆一个已有的元素节点
元素.cloneNode(布尔值)
```

cloneNode会克隆出一个跟原标签一样的元素，括号内传入布尔值

- 若为true，则代表克隆时会包含后代节点一起克隆
- 若为false，则代表克隆时不包括后代节点
- 默认为false

```html
<ul>
    <li>1</li>
    <li>2</li>
    <li>3</li>
</ul>
<script>
    const ul = document.querySelector('ul')
    // 1. 克隆节点 元素.cloneNode(true),深克隆
    const li1 = ul.children[0].cloneNode(true)
    ul.appendChild(ul.children[0].cloneNode(true))
    //<li>1</li>
    //<li>2</li>
    //<li>3</li>
    //<li>1</li>
    // 2. 克隆节点 浅克隆， 没有值，只有标签
    //<li>1</li>
    //<li>2</li>
    //<li>3</li>
    //<li></li>
</script>
```

### 删除节点

> JavaScript 原生DOM操作中，要删除元素必须通过父元素删除

```html
父元素.removeChild(要删除的元素)

// 案例
<script>
    const ul = document.querySelector('ul')
    ul.removeChild(ul.children[0])
</script>
```

- 如不存在父子关系，删除不成功
- 删除节点（节点不存在）和隐藏节点（存在于HTML）

## M端事件

> 移动端

### 触屏事件

| 触屏touch事件 | 说明                           |
| ------------- | ------------------------------ |
| touchstart    | 手指触摸到一个DOM元素是触发    |
| touchmove     | 手指在一个DOM元素上滑动时触发  |
| touchend      | 手指从一个DOM元素上 移开时触发 |

## Swiper插件

# Day 5

## 1. BOM

> Browser Object Model

![](/img/Javascript/webApiDay5.png)

- Window 对象是一个全局对象，也可以说是 JavaScript中的顶级对象

- document, alert(), console.log() 这些都是window的属性

  基本BOM的属性和方法都是window的

- 所有通过var定义在全局作用域的变量、函数，都会变成window对象的属性和方法

- window对象下的属性和方法调用时可以省略window

```javascript
document.querySelector()
window.documet.querySelector()
console.log(document === window.document) // true
function fn(){
    console.log(11)
}
window.fn() // 和直接调用fn没什么区别
var num = 10 //注意用var定义，而不用let和const
console.log(window.num)

```

### 定时器-延时函数

`setTimeout` 仅仅执行一次，可以理解为把一段代码延迟执行，平时省略window

#### 语法

```javascript
setTimeout(回调函数，等待的毫秒数)
```

#### 清楚延时函数

```javascript
let timer = setTimeout(回调函数， 等待毫秒数)
clearTimeout(timer)
```

- 延时器需要等待，所以后面的代码会先执行，返回值还是id
- 每次调用延时器都会产生一个新的延时器

### JS 执行机制

`JavaScript` 的特点就是单线程，同一时间只能做一件事

单线程意味着，所有任务需要排队，前一个任务结束，才会执行后一个任务。导致问题： 如果 JS 执行的时间过长，会造成页面渲染不连贯，导致页面渲染加载阻塞。

为了解决问题，允许`JavaScript `脚本创建多个线程， 于是出现 <b>同步 </b>& <b>异步</b>，两者本质区别-> 执行任务的顺序不同

- 同步： 烧水-> 洗菜-> 做饭

- 异步： 烧水的同时洗菜 -> 做饭

#### 同步任务

1. 同步任务在 <b><i>主线程 </i></b>执行，形成一个执行栈

#### 异步任务

1. JS 的异步是通过回调函数实现

2. 任务类型

   1. 普通事件 `click, resize`
   2. 资源加载 `load, error`
   3. 定时器 `setInterval, setTimeout`

   异步任务相关添加到任务队列中 (也称消息队列)

   个人理解是，所有需要时间的事件都会放入任务队列

#### 执行流程

1. 先执行 执行栈中的同步任务
2. 异步任务放入任务队列中
3. 一旦执行栈中的所有同步任务执行完毕，系统会按次序读取任务队列中的异步任务，于是读取的异步任务结束等待状态，进入执行栈，开始执行

![image-20240309235239640](/img/Javascript/wenApiDay5-2.png)
![image-20240309235259716](/img/Javascript/webApiDay5-3.png)

由于主线程不断的重复获得任务、执行任务、再获取任务、在执行，所以这种机制被称为 <b>事件循环 (event loop)</b>

### location 对象

`location` 的数据类型是对象， 拆分并保存了URL地址的各个组成部分

#### 语法&常用属性与方法

```javascript
console.log(window.location) 
// 等同于
console.log(location)
```

###### location.href

1. 可以得到当前文件URL地址
2. 可以通过 js 方式跳转到目标地址

```javascript
console.log(location.href)
//  href 赋值跳转页面
location.href = 'http://www.itcast.cn'
```

###### location.search

.search 属性获取地址中携带的参数，符号 `? `之后

```javascript
console.log(location.search)
// '?username=pink&pwd=123456'
```

###### location.hash

.hash属性获取地址中哈希值，符号#后面的部分

```javascript
console.log(location.hash)
// '#friend'
```

##### location.reload()

.reload() 方法用来刷新当前页面，传入参数true表示强制刷新

```html
<button>点击刷新</button>
<script>
    let btn = document.querySelector('button')
    btn.addEventListener('click',function(){
        location.reload()
        // 普通刷新
        location.reload(true)
        // 强制刷新 类似 control + f5
    })

</script>
```

### navigator 对象

> navigator 的数据类型是对象，该对象下记录了浏览器自身相关的信息

##### 常用属性

```navigator.userAgent```

通过userAgent检测浏览器的版本及平台

```javascript
// 检测userAgent(浏览器信息）
!(function(){
    const userAgent = navigator.userAgent
    // 验证是否为Android或iPhone
    const android = userAgent.match((Android);?[¥s¥]))
    const iphone = userAgent.match((iPhone);?[¥s¥])
    
    if (android ||iphone){
        location.href = 'http://www.itcast.cn'
    }                                                                 
})()
```

补充： 关于立即执行函数的不同写法

```javascript
(function(){})();
!function(){}()
```

### history 对象

> 数据类型为对象，主要管理历史记录，该对象与浏览器地址栏的操作相对应， 如前进、后退、历史记录等德

###### 常用方法

| 方法       | 作用                                                         |
| ---------- | ------------------------------------------------------------ |
| back( )    | 后退功能                                                     |
| forward( ) | 前进功能                                                     |
| go (参数)  | 前进后退功能 参数如果是1，则前进1个页面。如果为-1，后退1个页面 |

## 2. 本地存储

### 介绍

1. 数据存储在用户浏览器中
2. 设置、读取方便、页面刷新不丢失数据
3. 容量较大， sessionStorage 和 localStorage 约5M左右

### localStorage

- 可以将数据永久存储在本地（用户的电脑），除非手动删除，否则关闭页面也存在
- 以键值对的形式存储使用
- 在检查页面中的 Application -> local Storage内查看
- 跨域数据不同步
- 本地存储只能存储字符串类型， 如果是数字也会改成文本

#### 语法

本质是增删改查

```javascript
// 存储数据
//key 一定要加‘’，如果不加引号，会被当成变量
localStorage.setItem(key, value)

// 获取数据
localStorage.getItem(key)

// 删除本地存储
localStorage.removeItem(key)

//也可以删除全部【慎用】
clearAll

// 改数据
localStorage.setItem(key, newValue)
```

案例

```html
<script>
    // 要存储一个名字 uname
    localStorage.setItem('uname', 'Jennie')
    // 获取数据
    console.log(localStorage.getItem('uname'))
    // 删除数据
    localStorage.removeItem('uname')
    // 改数据
    localStorage.setItem('uname','Danny')
</script>
```

### sessionStorage

- 声明周期为关闭浏览器窗口
- 在同一窗口下的数据可以共享
- 以键值对的形式存储数据
- 用法与localStorage相同



### 存储复杂数据类型

> 本地只能存储字符串， 无法存储复杂数据类型 (字典或数组)

1. 将数据抓换成 `JSON`字符串，再存储在本地。因为本地存储只能存储字符串

2. 把 `JSON`字符串转换为对象

   `JSON.parse()`

- JSON 对象 属性和值有引号，统一是双引号

```javascript
JSON.stringify(obj)
```

```html
<script>
    const obj = {
        uname: 'pink老师',
        age: 18,
        gender: '女'
    }
    // 存储 复杂数据类型 无法直接使用
	// localStorage.setItem('obj',obj)
	// 因为复杂数据类型存储必须转换为 JSON 字符串存储
    localStorage.setItem('obj',JSON.stringify(obj))
    // 再将JSON字符串转换为对象
    console.log(typeof localStorage.getItem('obj'))
    const str =  localStorage.getItem('obj')
    console.log(JSON.parse(str))
</script>


```

## 3. map( ) & join( )

字符串拼接新思路 `map()` 和`join()`实现字符串拼接

### map()

- 可以遍历数组处理数据，并且 <b>返回新的数组</b>

```javascript
const arr = ['red', 'blue', 'green']
const newArr = arr.map(function(ele, index){
    // 拿到数组中的每个元素
    console.log(ele) //数组元素
    console.log(index) //数组索引号
    return ele + '颜色'
    // ['red'颜色, 'blue颜色', 'green颜色']
}
```

- map 也称为映射，指两个元素的集之间相互 ‘对应’ 的关系

- map与forEach的区别，map有返回值，forEach没有

### join() 方法

将数组转换为字符串

- join() 无参数表示，字符串用，分隔
- join(' ') 参数里面是空字符串，表示无分隔符号

`console.log(newArr.join())`

# Day6

## 正则表达式

>  Regular Expression

### 1. 定义及使用场景

1. 定义

- 在 JavaScript中，正则表达式也是对象
- 通常用来查找、替换符合正则表达式的文本
- 正则表达式是用于匹配字符串中字符组合的模式

1. 使用场景

- 验证表单：用户名表单只能输入英文字母、数字、下划线，昵称输入框可以输入中文（<b>匹配</b>）

  比如用户名： /^[a-z0-9_-]{3,16}$/

- 过滤掉页面中的一些敏感词（<b>替换</b>），或从字符串中获取我们想要的特定部分（<b>提取</b>）等

### 2. 语法

JavaScript 定义正则表达式的语法有两种，学习较为简单的方法

使用步骤：

- 定义规则
- 是否匹配

1. 正则表达式语法：

   - /   / 是正则表达式的字面量，只要出现 /   /都是正则表达式

   - 判断是否有符合规则的字符串

     test()方法 -> 用来查看正则表达式与指定字符串是够匹配 

     返回值为布尔值 true or false

   - exec() 返回数组

```javascript
const 变量名 = /表达式/
regObj.test( 被检测的字符串 )
regObj.exec( 被检测的字符串 )
```

```javascript
const str = '我们在学习前端，希望学习前端能找到好工作'
// 正则表达式使用
// 1. 定义规则， 不需要写引号
const reg = /前端/
// 2. 是否匹配
reg.test(str)
```

### 3. 元字符

#### 1. 什么是元字符 (特殊字符) ？

一些具有特殊含义的字符，可以极大提高了灵活性和强大的匹配功能

- 比如，英文26个字母

| 元字符 | 普通字符                   |
| ------ | -------------------------- |
| [a-z]  | abcdefghijklmnopqrstuvwxyz |
| [0-9]  | 123456789                  |

#### 2. 分类

#### a. 边界符

> 表示位置，开头，结尾。必须用什么开头，用什么结尾

正则表达式中的边界符（位置符）用来提示字符所处的位置，只要有两个字符，并且开启精确匹配模式

| 边界符 | 说明                          |
| ------ | ----------------------------- |
| ^      | 表示匹配行首的文本 (以谁开始) |
| $      | 表示匹配行尾的文本 (以谁结束) |

```javascript
console.log(/哈/.test('哈')) //true

// 必须以哈开头
console.log(/^哈/.test('哈')) //true
console.log(/^哈/.test('二哈')) //false
console.log(/^哈$/.test('哈')) //true
console.log(/^哈$/.test('哈哈哈')) 
//false 因为没有给量词，处于精确匹配的情况想，数量不对也是false

```

#### b. 量词

> 表示重复次数

量词用来设定某个模式出现的次数

| 量词   | 说明                    |
| ------ | ----------------------- |
| \*[]() | 重复0次或者更多次 >= 0  |
| +      | 重复1次或者更多次 >=1   |
| ?      | 重复0次或者1次          |
| {n}    | 重复n次 ==n             |
| {n, }  | 重复n次，或更多次 >=n   |
| {n,m}  | 重复n到m次  >=n and <=m |

{n,m}中间千万不能有空格!!!

```javascript
console.log(/^哈$/.test('哈')) // true
console.log(/^哈*$/.test('')) // true 出现>=0 所以返回true
console.log(/^哈*$/.test('哈哈哈')) // true
console.log(/^哈*$/.test('二哈二')) // false 因为要以 哈 开头
```

#### c. 字符类

> 比如 \b 表示 0-9

1. [ ] 匹配字符集合

2. [ ] 里面加上 - 连字符

   使用连字符 - 表示一个范围

   `console.log(/^[a-z]$/.test('c'))`

   - [a-z] 表示 a 到 z 26个英文字母都可以
   - [a-zA-Z] 表示大小写都可以
   - [0-9] 表示0-9 的数字都可以

1. [ ] 里面加上 ^ 取反符号

- `[^a-z]` 注意!! ^在方括号内部才是取反符号!!!!

  表示匹配除小写字母之外的字符

  `.`匹配除换行符之外的任何单个字符

1. 预定义  -> 某些常见模式的简写方式

   | 预定类 | 说明                                                         |
   | ------ | ------------------------------------------------------------ |
   | \d     | 匹配0-9之间的任一数字，相当于[0-9]                           |
   | \D     | 匹配所有0-9以外的字符，相当于[\^0-9]                         |
   | \w     | 匹配任意的字母、数字和下划线，相当于[A-Za-z0-9_]             |
   | \W     | 除所有字母、数字和下划线以外的字符，相当于 [\^A-Za-z0-9_]    |
   | \s     | 匹配空格 (包含换行符、制表符、空格符等)，相等于 [\t\r\n\v\f] |
   | \S     | 匹配非空格的字符，相当于[\^ \t\r\n\v\f]                      |
   |        |                                                              |

```javascript
// 只要中括号里面的任意字符出现都返回true
console.log(/[abc]/.text('andy'))  //true
console.log(/[abc]/.text('baby'))  //true
console.log(/[abc]/.text('cry'))  //true
console.log(/[abc]/.text('die'))  //false

// 字符类[abc] 只选1个!!!!
console.log(/^[abc]$/.text('a'))  //true
console.log(/^[abc]$/.text('b))  //true
console.log(/^[abc]$/.text('c'))  //true
console.log(/^[abc]$/.text('ab'))  //false
// 加量词, 重复2次
console.log(/^[abc]{2}$/.text('ab'))  //false
// 加连字符
console.log(/^[a-z]$/.test('c')) // true
// 集合版 判定qq号 从10000开始 [0-9]重复4次
^[1-9][0-9]{4,}$ 
// 日期格式
^\d{4}-\d{1,2}-\d{1,2}
```

总结：

1. `.`表示匹配除换行符之外的任何单个字符
2. `[abc]`匹配abc其中的任何单个字符
3. `[a-z]`匹配26个小些英文字母其中的任何单个字符
4. `[^a-z]`匹配除26个小写字母之外的其他任何单个字符

### 4. 修饰符

> 修饰符约束正则执行的某些细节行为，如是否区分大小写，是否支持多行匹配等

#### 语法

​	`/表达式/修饰符`

- i 是单词 ignore的缩写，正则匹配时字母不区分大小写
- g 是单词global的缩写，匹配所有满足正则表达式的结果

```javascript
console.log(/a/i.test('a')) //true
console.log(/a/i.text('A')) //true

console.log(/^java$/.test('java')) // true
console.log(/^Java$/i.test('JAVA')) // true
```

#### 替换方法

```javascript
字符串.replace(/正则表达式/,'替换的文本')
// 只替换一个
const str = 'java是一门编程语言，学完有工作'
str.replace(/java/i,'前端')
// 替换文本内全部，全局替换g
const str = 'java是一门编程语言，学完有工作'
str.replace(/java/gi,'前端')
```

