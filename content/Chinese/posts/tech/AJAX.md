---
title : '学习：AJAX '
date : 2024-03-23
Lastmod: 
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
summary: axios,API, XMLHttpRequest, asyn, await, Promise, EventLoop, 

categories: 
- tech

tags:
- AJAX
- VUB
- Frontend

keywords:
- AJAX


cover:
    image: ""
    caption: "" #图片底部描述
    alt: ""
    relative: true
---

# Day 1

## 1. AJAX 导入

### 什么是AJAX ?

+ 异步的 JavaScript 和 XML (Asynchronous JavaScript And XML)

+ 使用`XMLHttpRequest` 对象与服务器通信，可以使用`JSON/ XML/ HTML/ text ` 文本等格式发送和接受数据。

+ AJAX 有异步特性，在不重新刷新页面的情况下与服务器通信，交换数据，或更新页面

### 使用 AJAX

+ 使用 `axios` 库，与服务器进行数据通信

  将`XMLHttpRequest`封装，代码简单

  Vue React 项目中都会使用 `axios`

  ```javascript
  axios({
      url: 'http://hmajax.itheima.net/api/province'
      //'请求的服务器连接'
  }).then(result)=>{
      // 对服务器返回的数据做后续处理
  }
  ```

+ 学习`XMLHttpRequest`对象，了解AJAX底层原理

## 2. URL

1. http协议： 超文本传输协议，规定浏览器和服务器之间传输数据的格式

   ![image-20240323121243815](/img/Javascript/image-20240323121243815.png)

   网址： http://hmajax.itheima.net/api/province

   网址：协议://域名/资源路径

   | 名称     | 网址               | 作用                         |
   | -------- | ------------------ | ---------------------------- |
   | 协议     | http               | 规定传输数据的格式           |
   | 域名     | hmajax.itheima.net | 标记服务器在互联网中的方位   |
   | 资源路径 | /api/province      | 标记资源在服务器下的具体位置 |

2. URL 查询参数

> 浏览器提供给服务器的额外信息，让服务器返回浏览器想要的数据

​	 http://xxxx.com/xxx/xxx?param1 = value && param2 = value2

![image-20240323221541982](/img/Javascript/image-20240323221541982.png)

​	Axios 查询参数

+ axios 提供 `params` 选项

```javascript
axios({
    url:' http://hmajax.itheima.net'
    params: {
    pname:'河北省'
}
      }).then(result=>{
    // 处理后续code
})
```

3. 常用的请求方法

> 对服务器资源，执行的操作

| 请求方法 | 操作            |
| -------- | --------------- |
| GET      | 获取数据        |
| POST     | 提交数据        |
| PUT      | 修改数据 (全部) |
| DELETE   | 删除数据        |
| PATCH    | 修改数据 (部分) |

+ axios 请求配置

  `url`：请求URL网址

  `method`：请求方法，GET可以省略（不区分大小写）

  `data`：提交的数据

  `header`: 请求头数据，通常用于传递`token`，可以在axios中的请求拦截器中设置公共的 headers 选项 

```javascript
axios({
    url : '目标资源地址',
    method : '请求方法', 
    data :{
        params ：value
    }
}).then((result)=>{
    
})
```

```javascript
axios({
    url:'',
    headers: {
        Authorization: `Bearer ${token}`
        // Bearer是授权类型
    }
})
```

+ axios 请求拦截器：本质是配置函数，在发起请求之前触发，对请求参数进行额外配置。一般放在基地址`.baseURL`的`.js`内

```javascript

axios.interceptor.request.use(function (config) {
  const token = location.getItem('token')
  token && config.headers.Authorization = `Bearer ${token}`
  // 在发送请求之前做些什么
  return config
}, function (error) {
    // 对请求错误做些什么
  return Promise.reject(error)
})
```

+ Axios 响应拦截器

  响应(response)回到 `then/catch`之前，触发的拦截函数，对响应结果统一处理，例如身份验证失败，统一判断并作处理；如果成功设置返回数据对象里的某个属性，在其他操作中更加简洁。一般放在基地址`.baseURL`的`.js`内

```javascript
// 添加响应拦截器
axios.interceptors.response.use(function (response) {
  // 2xx 范围内的状态码都会触发该函数
  // 对响应数据 返回对象中的 data属性
  const result = response.data
  // 不用写 response.data.data这么繁琐
  return result;
}, function (error) {
  if (error?.response?.status === 401) {
    // 这是一个条件语句，首先检查 error 对象是否存在，如果存在则继续检查其 response 属性是否存在，
    // 最后再检查 response 对象中的 status 属性是否等于 401。这里使用了可选链操作符 ?.
    // 以避免当某些属性为 null 或 undefined 时引发错误。
    alert('登录状态过期，请重新登录')
    localStorage.clear()
    location.href = 'login/index.html'
  }
  return Promise.reject(error);
});
```



总结：

1. 请求方法表明对服务器资源的操作，POST 提交数据 GET查询数据

2. axios 核心配置

   url ：请求URL网址

   method : 请求方法， get可以省略

   params ： 查询参数

   data ： 提交数据, 请求体

3. axios 是一个调用函数，对请求参数进行设置

   在公共配置和设置是，统一设置在请求拦截器中

+ __在 axios的使用中，发现data后面时对象的格式，会自动转换成json格式__

+ 浏览器发送至服务器 叫做 请求体， 在network -> playload中可以查看

+ 服务器返回给浏览器 叫做 响应体， 在 network -> 响应中可以查看




## 3. axios错误处理

> Axios 会在控制台返回错误信息， 为了增加用户体验，开发人员可以讲错误信息以探矿的形式展现给用户

语法： 在 `then` 方法的后面，通过点语法调用 `catch` 方法，传入回调函数并定义形参

```javascript
axios({
    // 请求选项
}).then(result=>{
    
}).catch(error=>{
    
})

axios({
      url: 'http://hmajax.itheima.net/api/register',
      method: 'post',
      data: {
        'username': 'itheima789',
        'password': '123456'
      }
    }).then(result => {
      console.log(result)
    }).catch(error => {
      console.log(error)
      console.log(error.response.data.message)
    // 错误信息存放的位置
    alert（error.response.data.message）
    })
```

## 4. HTTP协议 - 请求报文

+ HTTP 协议： 规定了浏览器发送服务器返回内容的格式
+ 请求报文：浏览器按照HTTP 协议要求的格式，发送给服务器的内容。所以请求报文就是遵守格式的内容集合

![image-20240323234251464](/img/Javascript/image-20240323234251464.png)

### 请求报文的组成部分

1. 请求行： 请求方法， URL， 协议
2. 请求头： 以键值对的格式携带的附加信息 `Content-Type: application/json`

3. 空行： 分隔请求头，空行之后是发送给服务器的资源
4. 请求体： 浏览器发送的资源

## 5. HTTP协议 - 响应报文

+ HTTP 协议： 规定了浏览器发送及服务器返回内容的格式
+ 响应报文： 服务器按照HTTP协议要求的格式，返回给浏览器的内容

1. 响应报文的组成部分

   1. 响应行（状态行）：协议、HTTP响应状态码、状态信息

      | 状态码 | 说明       |
      | ------ | ---------- |
      | 1xx    | 信息       |
      | 2xx    | 成功       |
      | 3xx    | 重定向消息 |
      | 4xx    | 客户端错误 |
      | 5xx    | 服务端错误 |

   1. 响应头：以键值对的格式携带的附加信息 `Content-Type:Application/JSON`
   2.  空行： 分隔响应头，空行之后的是服务器返回的资源
   3. 响应体：返回的资源

## 6. 接口文档

> 描述接口的文章

接口是什么？

> 使用AJAX和服务器通讯时，使用的URL, 请求方法，以及参数

## 7. form-serialize 插件

> 快速收集表单元素的值

```javascript
const form = document.querySelector('.example-form')
const data = serialize(form, {hash: true, empty:true})
```

使用解读：

+ 参数1：要获取哪个表单的数据

  表单元素设置name属性，值会作为对象的属性名。建议name属性的值，最好与接口文档参数名一致

+ 参数2:   配置对象

  hash 设置获取数据结构

  - true： JS 对象（推荐）一般请求体提交至服务器的格式。
  - false：查询字符串

  empty 设置是否获取空值

  + true：获取空值（推荐）数据结构和标签结构一致
  + false：不获取空值

## 8. API要求请求体FormData()

+ 文件选择元素 -> 使用change改变事件，使用files获取监听事件的文件列表
+ 使用FormData()传输文件

```javascript
document.querySelector('.upload').addEventListener('change',e=>{
    //1. 获取图片文件,使用files获取监听事件的文件列表
    console.log(e.target.files[0])
    const fd = new FormData()
    fd.append('img',e.target.files[0])
    axios({
        // api
        url:'',
        method:'post',
        data:fd
    }).then(result=>{
        console.log(result)
        const imgUrl = result.data.data.url
        document.querySelector('.img').src = imgUrl
    })
}
```

# Day3

## 1. AJAX 原理 - XMLHttpRequest

> XMLHttpRequest （XHR）对象用于与服务器交互。通过XMLHttpRequest 可以在不刷新页面的情况下请求特定的URL，获取数据。
>
> 这允许网页在不影响用户操作的情况下，更新页面的局部内容。
>
> XMLHttpRequest 在AJAX编程中被大量使用

关系：axios 内部采用 `XMLHttpRequest`与服务器交互

![image-20240326133541516](/img/Javascript/image-20240326133541516.png)

### 1. 使用 XMLHttpRequest

步骤&语法

```javascript
const xhr = new XMLHttpRequest()
xhr.open('请求方法','请求url网址')
xhr.addEventListener('loadend',()=>{
    // 响应结果
    console.log(xhr.response)
    // 接受服务端的响应
})
xhr.send() // 给服务端发送请求
```

```javascript
// 再来一个案例
const xhr = new XMLHttpRequest()
    xhr.open('get', 'http://hmajax.itheima.net/api/province')
    xhr.addEventListener('loadend', () => {
      // 无论成功或失败，都会返回数据
      // 返回json字符串， axios帮忙转成了js对象
      console.log(xhr.response)
      // 转换成js对象
      const data = JSON.parse(xhr.response)
      // 转换成字符串
      console.log(data.list.join('<br>'))
    })
    // 发起请求
    xhr.send()
```

总结：

1. AJAX原理

   XMLHttpRequest 对象

2. 为什么学习 XHR？

   了解axios内部原理

   了解服务器数据通信的方式

3. XHR使用步骤？

   创建XHR对象

   调用open方法，设置url和请求方法

   监听loadend事件，接收结果

   调用send方法，发起请求

### 2. XMLHttpRequest  -查询参数

定义： 浏览器提供给服务器的额外信息，让服务器返回浏览器想要的数据

语法：`http://xxxx.com/xxx/xxx?参数名1=值1 & 参数名2=值2`

![image-20240326134942164](/img/Javascript/image-20240326134942164.png)

### 3. URLSearchParams()

> 用来生成查询参数

```javascript
const paramsObj = new URLSearchParams({
    参数名1:值1,
    参数名2:值2
})
const queryString = paramsObj.toString()
```

### 4. XMLHttpRequest() 数据提交

请求头设置 Content-Type：application/json

请求体携带JSON 字符串

在开发者控制台的 网络-> Fetch/XHR->选择调用的接口

```javascript
const xhr = new XML HttpRequest()
xhr.open('请求方法'，'请求url网址')
xhr.addEventListener('loadend',()=>(
    console.log(xhr.response)
))
// 提交时，设置请求头
xhr.setRequestHeader('content-type','application/json')

const user = {username:'itheima007',password:'7654321'}

// 转换成json
const userJson = JSON.stringify(user)

xhr.send(userJson)
```

## 2. Promise对象

> 定义： Promise 对象用于表示一个异步操作的最终完成（或失败）及其结果值
>
> 目前学过的异步：AJAX, setTimeout(), setTimeInterval()

### 1. 了解

优势：

1. 逻辑更清晰
2. 了解axios 函数内部运作机制
3. 能解决回调函数地狱问题

```javascript
    // 创建Promise对象
const p = new Promise((resolve, reject)=>{
    // 执行一步任务并传递结果
    // 成功调用： resolve(值)触发 then()执行
    // 失败调用： reject(值)触发 catch()执行
})
p.then(result=>{
    // 成功
}).catch(error=>{
    // 失败
})

```

![image-20240327145303599](/img/Javascript/image-20240327145303599.png)

总结：

1. 什么是Promise? 管理一个异步操作最终状态和结果的值的对象

2. 为什么学习Promise？

   成功和失败状态，可以关联对应处理程序

   了解axios内部原理

3. Promise使用步骤

   1. 创建对象
   2. 定义两个形参并执行回调函数，执行异步代码
   3. 成功和失败执行不同的函数
   4. 在.then() .catch()方法中捕捉成功或失败的结果

### 2. Promise 三种状态

作用： 了解Promise对象如何关联和处理函数，以及代码执行顺序

概念： 一个Promise对象，必然处于以下几种状态之一

- 待定 (pending)： 初始状态，即没有被兑现，也没有被拒绝
- 已兑现 (fulfilled)： 操作成功完成
- 已拒绝 (rejected)：操作失败

__注意：__ Promise 对象一旦被兑现/拒绝，此状态无法被改变

![image-20240327150915921](/img/Javascript/image-20240327150915921.png)

```javascript
// 1. 创建Promise对象 （pending - 待定状态）
const p = new Promise((resolve, reject) => {
      console.log('Promise对象内开始执行')
    // Promise对象被创建时，代码立刻执行
    // 2. 执行异步代码
      setTimeout(() => {
         // 当resolve()=>被调用时，Promise的状态会更改为‘fulfilled 已兑现’ 
         // 导致then()中的回调函数执行
        resolve('模拟ajax请求成功')
         // 当reject()=>被调用时，Promise的状态会更改为‘rejected 已拒绝’ 
         // 导致catch()中的回调函数执行
        // reject(new Error('失败！'))

      }, 2000)
    })
    p.then(result => {
      console.log(result);
    }).catch(error => {
      console.log(error)
    })
```

总结：

1. Promise 对象有哪三种状态？

   待定 pending

   已兑现 fulfilled

   已拒绝 rejected

2. Promise 状态有什么用？

   状态改变后，调用关联的处理函数

案例： Promise 和 XMLHttpRequest 的结合

```javascript
const p = new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      xhr.open('GET', 'http://hmajax.itheima.net/api/provincedhdhdh')
      xhr.addEventListener('loadend', () => {
        // xhr使用响应码判断 响应成功还是失败 2xx开头都是成功 4xx都是错
        // 响应码
        console.log(xhr.status)
        console.log(xhr.response)

        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(JSON.parse(xhr.response))
        } else {
          reject(new Error(xhr.response))
        }
      })
      xhr.send()
    })
    p.then(result => {
      document.querySelector('.my-p').innerHTML =
        result.list.join('<br>')
    }).catch(error => {
      // 错误对象要用console.dir详细打印
      console.dir(error)
      console.log(error)
      document.querySelector('.my-p').innerHTML = error.message
    })
```

# Day4

## 1. 同步代码&异步代码

同步代码

> 实际上浏览器按照我们书写代码的顺序一行一行地执行程序。浏览器会等待代码的解析和工作，在上一行完成后才会执行下一行。这样就很有必要，因为每一行新的代码都是建立在前面的代码的基础之上的。
>
> 这也使得它成为一个同步程序

异步代码

> 异步编程技术使你的程序可以执行一个可能长期运行的任务同时继续对其他事件做出反应而不必等待任务完成。与此同时，你的程序也将在任务完成后显示结果

总结： 

+ 同步代码：逐行执行，需要在原地等待结果，才能继续向下执行
+ 异步代码：调用后耗时，不阻塞代码继续执行（不必原地等待），在将来完成后触发一个回调函数。异步代码接收结果，使用回调函数

```javascript
// 数字打印顺序
const result = 0+1
console.log(result) //1
setTimeout(()=>{
    console.log(2)
},2000) //2 

// 事件相关的代码都是异步，因为不会阻塞代码执行
document.querySelector('.btn').addEventListener('click',()=>{
    console.log(3)
})
document.body.style.backgroundColor = 'pink'
console.log(4)

// 打印顺序应该是 1 4 2 
```

总结：

1. 什么是同步代码？ 逐行执行，原地等待结果，才继续向下执行其他的代码

2. 什么是异步代码？调用后耗时，不阻塞代码执行，将来完成后触发回调函数

3. JS 中有哪些异步代码 ?

   setTimeout/setInterval

   事件

   AJAX

4. 异步代码如何接收结果？依靠回调函数来接收

## 2. 回调函数地狱

> 在回调函数中 嵌套回调函数，一直嵌套下去就形成了回调函数地狱

缺点： 可读性差，异常无法捕获，耦合性严重，牵一发动全身

## 3. Promise - 链式调用

概念： 依靠 `then()`方法会返回一个新生成的 `Promise`对象特性，继续串联下一环任务，直到结束

细节：`then()`回调函数中的返回值，会影响新生成`Promise`对象最终状态和结果

好处： 通过链式调用，解决回调函数嵌套问题

![image-20240327234206178](/img/Javascript/image-20240327234206178.png)

`setTimeout` 被用来模拟一个耗时 2 秒的异步操作。当这个异步操作完成后（即 2 秒后），`resolve` 被调用，并传递了字符串 `'上海市'` 作为参数。这会导致 `Promise` 对象 `p` 的状态变为 `fulfilled`，并且 `'上海市'` 这个值会被传递给 `p.then` 中注册的回调函数，并被打印出来。

```javascript
 /**
     * 目标：掌握Promise的链式调用
     * 需求：把省市的嵌套结构，改成链式调用的线性结构
    */
    // 1. 创建Promise对象
    const p = new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve('上海市')
      }, 2000)
    })
    // 获取省份名称
    const p2 = p.then(result => {
      console.log(result) // 上海市
      // 3， 创建Promise对象 模拟请求城市名字
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(result + '上海市' + '城市')
        }, 2000)
      })
    })
    // 获取城市名字
    p2.then(result => {
      // 这个result里面是 上一个resolve中传递进来的参数
      console.log(result)
    })

    // 会发现 p 和 p2 并不全等,就意味着then()返回一个新的对象
    console.log(p2 === p)
```

总结：

1. 什么是 `Promise` 的链式调用？

   使用 `then()`返回新的`Promise`对象，一直串联下去

2. `then` 回调函数中，` return` 的值会传给哪里？

   传给then函数生成的新 `Promise`对象

3. `Promise`  链式调用 解决了 回调函数嵌套问题

![image-20240328131153325](/img/Javascript/image-20240328131153325.png)

## 4. async函数和await

### 1. 定义

` async()` 使用`async`关键字声明的函数。async函数是`AsyncFunction`构造函数的实例，并且其中允许使用`await`关键字。`async`和`await`关键字让我们可以使用一种更简洁的方式写出基于Promise的异步行为，而无需刻意地链式调用`promise`

### 2. 案例

```javascript
async function getDefaultArea(){
    const pObj = await axios({url:'http://hmajax.itheima.net/api/province'})
    const pname = pObj.data.list[0]
    const cObj = await axios({url:'http://hmajax.itheima.net/api/city',params:{pname}})
    const cname = cObj.data.list[0]
    const aObj = await axios({url:'http://hmajax.itheima.net/api/city',params:{pname,cname}})
    const aname = aObj.data.list[0]
    
    document.querySelector('.province').innerHTML = pname
document.querySelector('.city').innerHTML = cname
document.querySelector('.area').innerHTML = aname
}

getDefaultArea()
```

### 3. 步骤

概念： 在 async 函数内，使用await关键字取代then函数，等待获取promise对象成功状态

1. async 修饰函数，使普通函数变为异步函数
2. await 后面增加异步任务
3. await 后面成功的结果 赋给 左边的变量 

## 5. async函数和await 捕获错误

### 1. try...catch

​      一旦在try这个代码块中出现错误，下面的函数都无法执行

```javascript
async function getDefaultData() {
      try {
          // 1. try 可能产生错误的代码
        const pObj = await axios({ url: 'http://hmajax.itheima.net/api/province' })
        const pname = pObj.data.list[0]

        const cObj = await axios({ url: 'http://hmajax.itheima.net/api/city', params: { pname } })
        const cname = cObj.data.list[0]

        const aObj = await axios({ url: 'http://hmajax.itheima.net/api/area', params: { pname, cname } })
        const aname = aObj.data.list[0]

        document.querySelector('.province').innerHTML = pname
        document.querySelector('.city').innerHTML = cname
        document.querySelector('.area').innerHTML = aname
      } catch (error) {
          // 2. 接着调用catch块，接收错误信息
          // 如果try某行代码报错后，try中剩余的代码不会执行
        cosole.dir(error.response.data.message)
      }
    }
```

## 6. 事件循环 (EventLoop)

### 1. 概念

JavaScript 有一个__基于事件循环的并发模型__，事件循环负责执行代码、收集和处理事件以及执行队列中的子任务。这个模型与其他语言中的模型截然不同，比如C和Java

### 2. 原因

JavaScript单线程（某一刻只能执行一行代码），为了让耗时代码不阻塞其他代码运行，设计了事件循环模型

### 3. 执行过程

```javascript
console.log(1)  // 调用栈
setTimeout(()=>{
    console.log(2)
},0) // 宿主环境
console.log(3)
setTimeout(()=>{
    console.log(4)
},2000)
console.log(5)

// 控制台输出： 1 3 5 2 4
```

还是看一下老师的视频讲解，比较清晰。大致步骤是：普通的非异步函数（立即执行函数）在调用栈内执行；异步函数在宿主环境（浏览器）中等待执行并加入任务队列，如果调用栈内任务执行完毕， 会循环反复的查找任务队列的回调函数执行。

{{< bilibili BV1MN411y7pw >}}  

### 4. 总结

1. 什么是事件循环？

   执行代码和收集异步任务，在调用栈空闲时，反复调用任务队列里回调函数执行机制

2. 为什么有事件循环？

   JavaScript 是单线程，为了不阻塞JS引擎，设计执行代码的模型

3. JavaScript 内代码如何执行？

   - 执行同步代码，遇到异步代码交给宿主浏览器环境执行

   - 异步有了结果后，把回调函数放入任务队列排队

   - 当调用栈空闲后，反复调用任务队列里面的回调函数

## 7. 宏任务与微任务

> ES6 之后引入Promise对象，让JS引擎也可以发起异步任务

异步任务分为：

- 宏任务： 由浏览器环境执行的异步代码
- 微任务：由 JS 引擎环境执行的异步代码

![image-20240328161951410](/img/Javascript/image-20240328161951410.png)

| 任务（代码）             | 执行所在环境 |
| ------------------------ | ------------ |
| JS 脚本执行事件 (script) | 浏览器       |
| setTimeour/setInterval   | 浏览器       |
| AJAX 请求完成事件        | 浏览器       |
| 用户交互事件等等         | 浏览器       |
| Promise对象.then()       | JS引擎       |

>  Promise 本身是同步的，而then 和 catch 回调函数是异步的

```javascript
console.log(1)
setTimeout(()=>{
    console.log(2)
},0)
const p 
```

### 1. 总结

1. 什么是宏任务？

   浏览器执行的异步代码

   例如： JS 执行脚本事件  `setTimeout/setInterva`，AJAX请求完成事件，用户交互事件等等

2. 什么是微任务？

   JS 引擎执行的异步代码

   例如： Promise对象.then() 的回调

3. JavaScript 内部代码如何执行？

   执行第一个script脚本事件宏任务里面的同步代码

   遇到宏任务/微任务 交给宿主环境（浏览器/JS引擎），执行后的回调函数分别放在 【微任务队列/宏任务队列】 

   当执行栈空闲时，清空微任务队列，再执行下一个宏任务....

## 8. Promise.all 静态方法

### 1. 概念：

合并多个Promise对象，等待所有同时成功完成（或某一个失败），做后续逻辑

![image-20240328165206817](/img/Javascript/image-20240328165206817.png)

```javascript
const p = Promise.all([Promise对象, Promise对象, ...])
    p.then(result => {
      // result 结果：[Promise对象成功结果, Promise对象成功结果, ...]
    }).catch(error => {
      // 失败的promise对象 抛出的异常
    })
```

# 补充 验证码流程

![image-20240329004645316](/img/Javascript/image-20240329004645316.png)

## 1. token 

> 访问权限令牌，本质是一串字符串

+ 创建： 正确登录后，由后端签发返回
+ 作用：判断是否有登录状态等，控制访问权限

注意： 前端智能判断 token 是否存在，而后端才能判断token的有效性

![image-20240329004928001](/img/Javascript/image-20240329004928001.png)