---
title : '学习：Node.js & Webpack '
date : 2024-03-30
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
summary: Basic understanding of front-end engineering

categories: 
- tech

tags:
- Node.js
- Webpack
- VUB
- Frontend

keywords:
- Webpack
- Node.js


cover:
    image: ""
    caption: "" #图片底部描述
    alt: ""
    relative: true
---

# Node.js 引入

## 1. 什么是Node.js? 

> Node.js 是一个跨平台 JavaScript运行环境，使开发者可以搭建服务端的JavaScript的应用程序

作用：使用Node.js 便携服务器端程序

+ 编写数据接口，提供网页资源浏览功能等等
+ 前端工程化：为后续学习Vue和React做铺垫

## 2. 什么是前端工程化？

> 开发项目直到上线，过程中继承的所有工具和技术

+ 压缩工具 -> 体积更小，更流畅
+ 转换工具 -> less 转 css， 转高版本JS
+ 格式化工具
+ 打包工具 -> 整合前端代码
+ 脚手架工具 
+ 自动化部署

node.js 可以主动读取前端代码的内容，对前端代码进行相应的处理

## 3. Node.js 为何能执行 JS ?

+ 首先：浏览器能执行 JS 代码，依靠的是内核中的V8引擎 （C++程序）
+ 其次： Node.js 是基于 Chrome V8 引擎进行封装 （运行环境）

![image-20240330231551295](/img/Javascript/image-20240330231551295.png)

## 4. Node.js 安装

下载 node-v16.19.0 msi 安装程序 (指定版本：兼容vue-admin-template模版)，我不太想下载之前版本的Node.js, 发现 https://juejin.cn/post/7204454572889980965 这个教程中有切换版本的选项。

## 总结

1. Node.js 是什么？

   基于Chrome的V8引擎，独立执行JavaScript代码环境

2. Node.js 与 浏览器环境的 JS 最大区别？

   Node.js 环境中没有 BOM 和 DOM

3. Node.js 有什么用？

   编写后端程序： 提供数据和网页资源等等

   前端工程化：集成各种开发使用的工具和技术

4. Node.js 如何执行代码? 

   在VSCode终端输入： `node xxx.js` 回车即可（注意路径）

# Node.js模块

## 1. fs 模块 - 读写文件

+ 模块： 类似插件，封装了方法/属性

+ fs模块：封装了与本机文件系统进行交互的方法/属性

+ 语法：

  加载 fs 模块对象

  写入文件内容

  读取文件内容

```javascript
const fs = require('fs')   // fs是模块标识符：模块的名字

fs.writeFile('文件路径', '写入内容',err=>{
    // 写入后的回调函数
})

fs.readFile('文件路径',(err,data)=>{
    // 读取后的回调函数
    if(err)console.log(err)
    else console.log(data)
    // data是文件内容的Buffer数据流
    // 这时候是16进制
    //如果想显示原有字符
    console.log(data.toString())
})
```

## 2. path 模块-路径处理

> 问题： Node.js 代码中，相对路径是根据终端所在路径来查找，可能无法找到你想要的文件

```javascript
const fs = require('fs')
fs.readFile('../test.txt',(err,data)=>{
    if (err)  console.log(err)
    else console.log(data.toString())
})
```

解决方案：

建议： 在Node.js 代码中使用绝对路径

补充： _dirname 内置变量 (获取当前模块目录-绝对路径)

注意：path.join() 会使用特定于平台的分隔符，作为定界符，将所有给定的路径片段连接在一起

```javascript
const fn = request ('fs')
const path = require('path')
cnosole.log(__dirname)
fs.readFile(path.join(__dirname,'../test.txt'),(err,data)=>{
    if (err)console.log(err)
    else console.log(data.toString())
})
```

## 3. 案例-压缩前端 html

需求：把 回车符 (\r) 和换行符 (\n)去掉后，写入到新的html文件中

步骤：

1. 读取源html文件内容
2. 正则替换字符串
3. 写入到新的html文件中

## 4. URL 的端口号

- URL: 统一资源定位符
- 端口号：标记服务器里不同功能的服务程序
- 端口号范围： 0-65535之间的任意整数

![image-20240331233448750](/img/Javascript/image-20240331233448750.png)

![image-20240401110756115](/img/Javascript/image-20240401110756115.png)

注意：http协议，默认访问80端口

![image-20240401110917410](/img/Javascript/image-20240401110917410.png)

### 常见的服务程序

- web服务程序： 用于提供网上信息浏览功能
- 注意： 0-1023 和一些特定端口号被占用，自己编写服务程序请避开使用

总结

- 端口号的作用？ 

  标记区分服务器里__不同的服务程序__，通过端口号访问不同的功能

- 什么叫web服务程序？

  提供浏览器 网上信息浏览的程序代码

## 5. http 模块 - 创建web服务

> 创建web服务并响应内容给浏览器

步骤：

1. 加载 http模块， 创建Web服务对象

2. 监听request请求事件，设置响应头和响应体

   res 是响应对象

3. 配置端口号并启动Web服务

4. 浏览器请求： http://localhost:3000 测试

   (localhost： 固定代表本机的域名)

```javascript
const http = require('http')
const server = http.creatServer()

server.on('request',(req,res)=>{
    // 设置响应头：内容类型，普通文本；编码格式utf-8
    res.setHeader('Content-Type','text/plain;charset=utf-8')
    // 设置响应体内容，结束本次请求与响应
    res.end('您好，欢迎使用node.js创建的web服务')
})
// 1.3 配置端口号并启动Web服务
// 启动计算机进程监听 是否有人请求
server.listen(3000,()=>{
    console.log('Web 服务已经启动')
})
```

## 6. 案例 - 浏览时钟

> 基于Web服务，开发提供网页资源的功能

![image-20240401142410736](/img/Javascript/image-20240401142410736.png)

步骤：

1. 基于 http 模块，创建 Web 服务
2. 使用 req.url 获取请求资源路径，判断并读取 index.html 里面的字符串内容返回给请求方
3. 其他路径，暂时返回不存在的提示
4. 运行 Web 服务，用浏览器发起请求测试

```javascript
// 1. 引入模块
const fs = require('fs')
const path = require('path')
const http = require('http')
const server = http.createServer()


// 2.  使用req.url 获取请求资源路径，并读取index.html 里面的字符串返回至请求方
server.on('request', (req, res) => {
  if (req.url === '/index.html') {
    fs.readFile(path.join(__dirname, 'dist/index.html'), (err, data) => {
      if (err) console.log(err)
      else {
        // 设置响应内容类型 html 超文本字符串，让浏览器解析成标签网页等
        res.setHeader('Content-Type', 'text/html;charset=utf-8')
        res.end(data.toString())
      }
    })
  }
  else {
    // 3. 其他路径暂时返回不存在提示
    res.setHeader('Content-Type', 'text/html;charset=utf-8')
    res.end('请求路径不存在')
  }
})

server.listen(8080, () => {
  console.log('原神启动!!')
})
```

# 模块化

## 1. 定义

- `CommonJS` 模块是为 `Node.js` 打包 JavaScript 代码的原始方式。
- `Node.js` 还支持浏览器和其他 JavaScript 运行时使用的`ECMAScript`模块 标准。
- 在Node.js中，每一个文件都被视为一个单独的模块

1. 概念： 项目是由很多的模块文件组成

2. 好处： 提高代码复用性，按需加载，独立作用域

3. 使用：需要标准语法导出、导入进行使用。这个标准语法就是 CommomJS

## 2. 使用

### 1. 语法

1. 导出： module.exports = {}
2. 导入：require('模块名或路径')

### 2. 模块名或路径

### CommomJS 标准

- [x] 内置模块：直接写名字 （例如：fs,  path,  http）

- [x] 自定义模块： 写模块文件路径（例如： ./utils.js）

```javascript
const baseURL = 'http://hmajax.itheima.net'
const getArraySum = arr => arr.reduce((sum,val)=>sum+=val,0)

module.exports = {
    对外属性1:baseURL,
    对外属性2:getArraySum
}

const obj = require('模块名或路径')
// obj 等于 module.exports 导出的对象
```

总结：

1. Node.js 中什么是模块化?

   每个文件都是独立的模块

2. 模块之间如何联系？

   使用特定的语法，导出和导入使用

3. CommonJS 标准规定如何导出和导入模块？

   导出： module.exports = {}

   导入： require('模块名或路径')

4. 模块名/路径如何选择？

   内置模块，直接写名字，例如：fs ,path, http 等

   自定义模块，写模块文件路径，例如：./utils.js

### ECMAScript 标准 - 默认到处导入

> 封装并导出基地址和求数组元素和的函数

默认标准使用：

1. 导出： export default()
2. 导入：import 变量名 from '模块名或路径'

注意： Node.js 默认支持 CommonJS 标准语法。 如需使用ECMAScript标准语法，在运行模块所在文件夹新建 `package.json` 文件，并设置 `{'type':'module'}`

```javascript
const baseURL = 'http://hmajax.itheima.net'
const getArraySum = arr=>{
    arr.reduce((sum,val)=> sum+=val,0)
}
// 导出
export default {
    对外属性1:baseURL,
    对外属性2:getArraySum
}
// 导入
import obj from '模块名或路径'
// obj 等于 export default 导出对象
```

总结：

1. ECMAScript 标准规定 默认到处和导入模块

   导出：export defalut{}

   导入： import 变量名 from ' 模块名或路径 '

2. 如何让Node.js 切换模块为ECMAScript? 

   运行模块所在文件夹，新建 package.json并设置

   `{"type":"module"}`

### ECMAScript 标准 - 命名导出和导入

> 封装并导出基地址和求数组元素和的函数

命名标准使用

1. 导出： export修饰定义语句
2. 导入：import (同名变量) from '模块名和路径'

如何选择命名/默认导出导入

- 按需加载，使用命名导出和导入
- 全部加载，使用默认导出导入

```javascript
export const baseURL = 'http://hmajax.itheima.net'
export const getArraySum = arr => arr.reduce((sum,val)=>sum+=val,0)

import {baseURL, getArraySum} from '模块名或路径'

```

总结：

1. Node.js 支持两种模块化辨准

   CommonJS 标准语法 (默认)

   ECMAScript 标准语法

2. ECEAScript 标准， 命名导出和导入的语法

   导出： export 修饰定义的语句

   导入： import { 同名变量 } from '模块名或路径'

3. ECEAScript 标准，默认导出和导入语法

   导出：export default {}

   导入：import 变量名 from '模块名或路径'

# 包

> 包：将模块，代码，其他资料聚合成一个文件夹

### 1. 包分类

- 项目包 ： 主要用于编写项目和业务逻辑
- 软件包： 封装工具和方法进行使用

要求： 根目录中，必须有package.json文件 （记录包的清单信息）

注意： 导入软件包时，引入的默认是 index.js 模块文件/ main 属性指定的模块文件 （utils 工具包的唯一出口，作用：把所有工具模块方法集中起来，统一向外暴露）

>  放入视频，因为老师有一些文件结构，我没有截图

总结：

1. 什么是包？

   将模块，代码，其他资料聚合成的文件夹。文件我们称之为模块

2. 包分为2类

   项目包： 编写项目代码的文件夹

   软件包： 封装工具和方法

3. package.json 文件的作用？

   记录了包的信息/作者/名字/入口信息

4. 导入一个包文件夹的时候，默认导入index.js 文件或package main属性指定的文件

# npm 

> npm 是Node.js 标准的软件包管理器，作为下载和管理 Node.js 包依赖的方式

##1 .npm 软件包 使用

1. 初始化清单文件： `npm init -y` （得到package.json 文件，可以记录当前项目中，下载了多少软件包） 
2. 下载软件包： `npm i 软件包名称`
3. 使用软件包

### 2. 使用案例

- 图解

![image-20240402001555040](/img/Javascript/image-20240402001555040.png)

总结：

1. npm软件包管理器作用？

   下载软件包以及管理版本

2. 初始化项目清单文件 `package.json `命令

   `npm init -y`

3. 下载软件包的命令？

   `npm i 软件包名字`

4. 下载的包 存放地址

   当前项目下的`node_modules`中，并记录`package.json`中

## 2. npm - 安装所有依赖

- 若收到项目文件中不包含node_modules 是否能正常运行？

  不能，缺少依赖的本地软件包

  原因： 因为自己用 npm下载依赖比磁盘传递拷贝要快得多

- __解决方案: __

  项目终端输入命令： `npm i`

  下载`package.json` 中记录的所有软件包

## 3. npm - 全局软件包 nodemon

### 软件包区别

- 本地软件包：当前项目内使用，封装属性和方法，存在于`node_modules`
- 全局软件包：本机所有项目使用，封装命令和工具，存在于系统设置的位置

nodemon作用：代替node命令，检测代码更改，自动重启程序

### nodemon使用

1. 安装 `npm i nodemon -g` (-g 代表安装到全局环境中)
2. 运行 `nodemon` 待执行的目标 js 文件

总结：

1. 本地软件包和全局软件包区别

   本地软件包，作用与当前项目，封装属性与方法

   全局软件包，本机所有项目使用，封装命令和工具

2. nodemon 全局软件包的作用

   替代node命令，检测代码更改，自动重启程序

3. nodemon怎么用？

   先确保安装 npm i nodemon -g （只有是命令和工具的软件包才安装到全局）

   使用 nodemon 执行目标js文件

# Node.js 总结

## Node.js 模块化 

概念： 每个文件当做一个模块，独立作用域，按需加载

使用： 采用特点的标准语法导出和导入进行使用

- CommonJS 标准

  导出：`module.exports = {}`

  导入：`require('模块名或路径')`

- ECMAScript标准

  默认模式：

  导出：`export default {}`

  导入：`import 变量名 from '模块化路径'`

  命名模式:

  导出：`export 修饰定义语句`

  导入：`import {同名变量} from'模块化路径' `

CommonJS 标准：一般应用在Node.js 项目环境中

ECMAScript标准：一般应用在前端工程化项目中

## Node.js 包

> 把模块文件，代码文件，其他资料聚合成一个文件夹

项目包：编写项目需求和业务逻辑文件夹

软件包：封装工具和方法进行使用的文件夹 (一般使用npm管理)

- 本地软件包： dayjs, loads, … 

  作用当前项目，一般封装的属性/方法，供项目调用编写业务需求

- 全局软件包:    nodemon

  作用在所有项目，一般封装的命令/工具，支撑项目运行

### Node.js 常用命令

| 功能                 | 命令              |
| -------------------- | ----------------- |
| 执行js文件           | node index.js     |
| 初始化 packpage.json | npm init -y       |
| 下载本地软件包       | npm i 软件包名    |
| 下载全局软件包       | npm i 软件包名 -g |
| 删除软件包           | npm uni 软件包名  |

# Webpack 引入

## 1. 定义

> 本质上， webpack是一个用于现代 JavaScript 应用程序的 静态模块打包工具，当webpack处理应用程序时，它会在内部从一个或多个入口点构建一个依赖图 (dependency graph), 然后将你的项目中所需要的每一个模块组合成一个或多个 bundles，它们均为静态资源，用于展示你的内容

静态模块： 指的是编写代码过程中的 `html`, `css`,`js`,`图片`等固定内容的文件

打包：把静态模块内容 压缩，整合，转译等等 （前端工程化）

- 把 less/sass 转换成 css代码
- 把 ES6+ 降级到 ES5
- 支持多种模块标准语法

关于vite (另一种打包工具)，很多项目还是基于webpack构建，也为Vue, React脚手架使用做铺垫

## 2. 执行步骤

1. 准备项目和源代码

2. 准备 webpack 打包的环境

   新建自定义配置

   ```json
   // 导入/导出标准
   "type": "module",
   // 添加自定义命令，调用build，使用webpack
     "scripts": {
       "test": "echo \"Error: no test specified\" && exit 1",
       "build": "webpack"
     }
   ```

3. 运行自定义命令打包观察效果 

   `npm run 自定义命令`

   出现 dist 文件夹

# Webpack 打包入口和出口修改

## 1. 默认值

- 默认打包入口： `src/index.js`
- 默认打包出口：`dist/main.js`

步骤：

1. 项目根目录，新建 `webpack.config.js` 配置文件
2. 导出配置对象，配置入口，出口文件的路径
3. 重新打包观察

__注意__:  只有和入口产生直接/简介的引入关系，才会被打包

```javascript
const path = require('path')

module.exports = {
    entry: path.resolve(__dirname, 'src/login/index.js'),
    output:{
        path: path.resolve(__dirname, 'dist'),
        filename: './login/index.js',
        clean: true 
        // 生成打包内容后，清空输出目录，只在webpack 5以上的版本才能使用
    }
}
```



## 2. Webpack的官方网址

目前b站教的是webpack5 `webpack.docschina.org/concepts`

## 3. Webpack 修改入口 (entry)

在 `webpack configuration`中配置`entry`属性，来指定一个或多个不同的入口起点

文件夹-> 项目根目录中的`webpack.config.js`

```javascript
module.exports = {
    entry: './path/file.js'
};
```

## 4. Webpack 修改出口 (output)

在 `webpack configuration.js`中配置`output`属性，表明webpack在哪里输出创建的`bundle`

文件夹-> 项目根目录中的`webpack.config.js`

```javascript
const path = require('path');
module.exports = {
    entry: './path/file.js',
    output: {
        // 输出路径
        path: path.resolve(__dirname,'dist')
        // 打包后文件的名字
        filename:'my-first-webpack.bundle.js'
    }
}
```

## 5. 案例 用户登录

前端工程化思路： Webpack打包后的代码，在前端页面中的使用

![image-20240402170606972](/img/Javascript/image-20240402170606972.png)

步骤：

1. 准备用户登录页面
2. 编写核心JS逻辑代码
3. 打包手动复制网页到dist下，引入打包后的js，运行

## 6. Webpack 自动生成html文件

> 前情提要： 之前打包后我们将原始的html文件，手动添加至输出文件夹，这回我们让webpack自动找到对应的html文件

### 1. Html-wabpack-plugin 插件

`HtmlWebpackPlugin`简化了HTML文件的创建，以便为webpack包提供服务，这对于文件名中包含哈希值，并且哈希值会随着每次编译而改变的webpack包非常有用。可以让该插件为用户生成HTML 文件，使用lodash提供模版，或者使用自己的loader

### 安装

`npm install --save-dev html-webpack-plugin`

--sav-dev 表示只在开发环境中使用

### 基本用法及步骤

> 无论是什么功能都是 找包-> 下包-> 配置包

1. 下载 Html-wabpack-plugin 本地软件包

   该插件将为你生成一个HTML5文件，在body中使用script变迁引入你所有webpack生成的bundle，只需添加该插件到你的webpack配置中

```javascript
const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');

module.exports = {
    entry: index.js,
    output:{
        path: path.resolve(__dirname, './dist'),
        // 输出文件
        filename: 'index_bundle.js',
    },
    //这个位置
    plugins: [new HtmlWepackPlugin()],
};
```

2. 配置webpack.config.js 让 Webpack 拥有插件功能

   - 会在`dist`文件下生成`index.html`， 如果有多个webpack入口，都会在已生成`HTML`文件中的`<script>`标签内引入。

   - 如果在webpack的输出中有任何css资源 (例如，使用MiniCssExtractPlugin提取的CSS)，那么这些资源也会在HTML文件`<head>`元素中的`<link>`标签内引入

   - 更多配置可以自行添加 webpack.config.js

   ```javascript
   {
     "entry": "index.js",
     "output": {
       "path": __dirname + "/dist",
       "filename": "index_bundle,js"
     },
         // new 一个对应的插件对象
     "plugins": [
     new HtmlWebpackPlugin({
         // html 标题
         "title": "My App",
         "filename": "assets/admin.html"
       })
     ]
   }
   ```

## 7. Webpack打包css代码

> Webpack 默认只识别 js代码， 加载器可以让webpack识别更多类型的模块文件

加载器的官方文档： webpack.docschina.org/loaders/

加载器 `css-loader`:  解析css代码

加载器`style-loader `: 将解析后的css代码插入到DOM 

### 1. 安装 css-loader

 `npm install --save-dev css-loader`

### 2. file.js

`import css from "file.css";`

css 文件与入口文件产生引入关系，webpack打包时会先找到入口，分析在入口中引入了其他的一些文件，然后将文件内容一起打包

### 3. 将loader引用到webpak的配置中

`webpack.config.js`

```javascript
module.exports = {
    module: {
        rules: [
            {
                test: /\.css$i,
                // 不区分大小写的，以css结尾的文件
                user:["style-loader","css-loader"],
        // 使用加载器的顺序是从后向前使用
            }
        ]
    }
};
```

### 步骤

1. 准备 css 文件代码引入到 `src/login/index.js`（压缩转译处理等）
2. 下载 `css-loader` 和 `style-loader` 本地软件包
3. 配置`webpack.config.js` 让`Webpack`拥有该加载器功能

## 8. 优化 - 提取 css 代码

> 上节课学会了如何打包 css 代码，但是是融合在 .js 文件中的。这次将css 代码单独提取出来

好处： css文件可以被浏览器缓存，减少 .JS 文件体积， 可以让浏览器加载更快，浏览器可以并行下载 css/js 这两个文件的代码，使网页尽快展给用户。

### 1. 使用 MiniCssExtractPlugin插件步骤

1. 下载插件

   `npm install --save.dev mini-css-extract-plugin`

   建议 `mini-css-extract-plugin` 与 `css-loader`一起使用，但是不能与 `style-loader`一起使用!!

2. 配置插件

```javascript
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
    plugins: [new MiniCssExtractPlugin()]
    module: {
        rules: [
            {
                test: /\.css$i,
                // 不区分大小写的，以css结尾的文件
                user:[MiniCssExtractPlugin,"css-loader"],
        // 使用加载器的顺序是从后向前使用
            }
        ]
    }
};
```

## 9. 优化 - 提取 css 代码的压缩

> css 代码提取后并没有压缩， 再次使用插件解决。
>
> 找包下包配置包

### css-minimizer-webpack-plugin 插件

1. 找包

2. 下包

   `npm install css-minimizer-webpack-plugin`

3. 配置包

```javascript
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const CssMinimizerPlugin = require('css-minimizeer-webpacke-plugin')

module.exports = {
    // ...
    // 优化
            optimization:{
                minimizer:[
                    // 在webpack@5中可以使用 ... 语法来扩展现有的minimizer (即 terser-webpack-plugin)，将下一行取消注释 (保证JS代码还能被压缩处理)
                    ...,
                    new CssMinimizerPlugin(), 
                ]
            }
};
```

## 10. Webpack 打包 less

### 1. less-loader

> 将Less编译为CSS的loader

1. 找包

2. 下包

   `npm install less less-loader --save-dev`

3. 配置包

```javascript
module.exports = {
    module: {
        rules: [
            {
                test: /\.less$i,
                // 不区分大小写的，以css结尾的文件
               use: [
                'style-loader',
                'css-loader',
                'less-loader',
                ]
        // 从后向前使用
            }
        ]
    }
};
```

### 步骤

1. 新建 less 代码 （设置背景图）并引入到 `src/login/index.js`
2. 下载 less 和 less-loader 本地软件包，因为less-loader需要配合less软件包使用
3. 配置 webpack.config.js 

## 11. Webpack资源模块

> 资源模块 （asset module）是一种模块类型，允许使用资源文件 (字体，图标等）而无需配置额外 loader

资源模块类型 (asset module type), 通过添加4种新的模块类型，替换所有loader

- `asset/resource` 发送一个单独文件并导出URL，之前通过使用`file-loader`实现。<i>针对图片/文件</i>i
- `asset/inline` 导出一个资源的data URI, 之前通过使用`url-loader`实现
- `asset/source` 导出资源的源代码。之前通过使用`raw-loader`实现。<i>针对txt文本，使用场景不多</i>
- `asset` 在导出一个data URI 和发送一个单独文件之间自动选择。之前通过使用`url-loader`，并且配置资源体积限制实现。文件大于8kb使用`asset/resource`，小于8kb使用`assest/inline`

当在webpack5中使用旧日的assets loader (如 file-loader/url-loader/raw-loader 等)和asset模块时，你可能想停止当前 asset模块的处理，并再次启动处理，这可能会导致 asset重复，你可以通过将 asset模块的类型设置为 `javascript/auto`来解决

### 1. 打包图片

资源模块： Webpack5 内置资源模块 (字体/图片等) 打包，无需额外loader

步骤：

1. 配置 `webpack.config.js` 让Webpack拥有打包图片功能

   - 占位符 [ hash ] 对模块内容做算法计算，得到映射的数字字母组合的字符串
   - 占位符 [ext] 使用当前模块原本的占位符，例如：.png/.jpg等字符串
   - 占位符 [query] 保留引入文件时代码中查询参数 (只有URL下生效)

   注意：判断临界值默认为 8kb

   - 大于8kb文件：发送一个单独的文件并导出URL地址

   - 小于8kb文件：导出一个data URI （base64字符串）

```javascript
module.exports = {
    // ...
    module:{
        rules:[
            // ...
            {
                test: /\.(png|jpg|jpeg|gif)$/i,
                type:'asset',
                generator:{
                    // 默认以output path作为路径
                    filename: 'assets/[hash][ext][query]'
                }
            }
        ]
    }
}
```

## 12. webpack热更新环境搭建

> 之前改代码，需要重新打包才能运行查看，效率很低

### 1. 开发环境

 配置webpack-dev-server 快速开发应用程序

- 开发环境： 开发 `mode: 'development'`
- 生产环境：用户看到的页面` mode: 'production'`

作用：启动Web服务，自动检测代码变化，热更新到网页

注意：dist 目录和打包内容存在内存里 （更新快）

### 2. 下包 Webpackp-dev-server

`npm install --save-dev webpack-dev-server`

### 3. 配置包

- 设置模式为开发模式
- 自定义命令
- 使用 `npm run dev`来启动开发服务器，试试热更新效果

```json
// package.json 设置自定义命令
scripts: {
    "build": "webpack",
    "dev":"webpack server --open" //自动弹出浏览器
}

module.exports = {
    mode: 'development',
    entry:{
        index: './src/index.js',
        print:'./src/print.js'
    },
    devtool: 'inline-source-map',
    devServer:{
        static:'/dist'
    }
    
}
```

以上配置表示

- `webpack-dev-server` 借助 http模块创建8080默认web服务，将`dist`目录下的文件serve到`localhost:8080`下。（serve 将资源作为server可访问的文件 ），如果不设置`static`属性，默认使用`public`文件夹的内容渲染页面
- `webpack-dev-server`根据配置，打包相关代码在内存当中，意味着不会生成新的文件，开发者肉眼不可见。以`output.path`的值作为服务器根目录，可以直接自己拼接访问dist目录下内容

## 13. Webpack 打包模式

### 1. 打包模式

>  告知Webpack使用相应模式的内置优化

### 2. 分类

开发模式，生产模式

| 模式名称 | 模式名字    | 特点                           | 场景     |
| -------- | ----------- | ------------------------------ | -------- |
| 开发模式 | development | 调试代码，实时加载，模块热替换 | 本地开发 |
| 生产模式 | production  | 压缩代码，资源优化，更轻量     | 打包上线 |

### 3. 设置方式

- 方式1:   在webpack.config.js 配置文件设置mode选项

```javascript
module.exports = {
    // ... 
    mode: 'production'
}
```



- 方式2：在package.json命令行设置mode参数 【优先级高于配置文件，会覆盖优先级】

```json
"scripts":{
    "build":"webpack --mode=production",
    "dev":"webpack serve --mode=development"
},
```

### 4. 打包模式的应用

需求：

- 在开发模式下用 `style-loader`内嵌更快
- 在生产模式下提取`css`代码，为了在用户的电脑上并行加载 css 和 js 的代码

方案1: `webpack.config.js`配置导出函数，但是局限性很大（因为只接收生产模式和开发模式）

方案2: 借助 `cross-env`（跨平台通用）包命令，设置参数区分环境

1. 下载 cross-env 软件包到当前项目
2. 配置自定义命令，传入参数名和值 (会绑定到process.nev对象下)
3. 在webpack.conifg.js 区分不同环境使用不同配置
4. 重新打包观察两种配置区别

```json
"script":{
    "test":"echo \"Error: no test specified\"&& exit 1",
    "build":"cross-env NODE_ENV=production webpack --mode=production",
    "dev":"cross-env NODE_ENV=development webpack serve --open --mode=development"
}
```

方案3: 配置不同的webpack.config.js （适用于多种模式差异性较大情况）

## 14. 前端-注入环境变量

> 前端项目中，开发模式下打印语句生效，生产模式下打印语句失效

`cross-env`设置只能在`Node.js`环境生效，打包后代码作用在浏览器，前端代码无法访问 `process.env.NODE_ENV`

>  解决方法依然是 找包掉包配置包 `DefinePlugin`插件 （内置插件无需下载）

```javascript
const webpack = require('webpack')
module.exports = {
    // ...
    plugins: [
        // ...
        // 在编译时，将前端代码中匹配的变量名，替换为值或表达式
        new webpack.DefinePlugin({
            // key 是诸如到打包后的前端 JS 代码中作为全局变量
            // value 是变量对应的值(在cross-env诸如在node.js中的环境变量字符串)
            'process.env.NODE_ENV':JSON.stringfy(process.env.NODE_ENV)
        })
    ]
}
```

## 15. 开发环境调错 -source map

代码被压缩和混淆，无法正且定位源代码位置（行数和列数）

source map: 可以准切追踪error和warning 在原始代码的位置

设置: web pack.config.js 配置devtool选项

```javascript
module.exports = {
    devtool:'inline-source-map'
};
```

`inline-source-map`：把源码的位置信息一起打包js文件内

注意： source map仅仅是用于开发环境，不要在生产环境使用 (防止被轻易查看源码位置)

## 16. 解析别名 alias

配置模块如何解析，创建import引入路径的别名，来确保模块引入变得更简单，例如原来路径长且相对路径不安全

```javascript
// @ 代表绝对路径
import {checkPhone, checkCode} from '@/utils/check.js'
```

```javascript
const config = {
    resolve:{
        alias:{
            '@':path.resolve(__dirname,'src')
        }
    }
}
```

