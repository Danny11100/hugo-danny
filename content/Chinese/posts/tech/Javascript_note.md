---
title : '学习: JavaScript 基础篇'
date : 2024-02-24
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
summary: "开始学习JavaScript!! 课程来自于 Udemy+Bilibili"

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

## JavaScript输入输出

```javascript
alert('comment') //浏览器弹出
prompt('comment:') //用户输入
console.log() //写出在控制台
document.write()
```

## Varible 变量 

1. let 不允许==多次声明==一个变量， 和python不一样

   ```let age = 18 ```

    ```age = 19 ```

2. let 可以一次声明多个变量:

   ```let age = 18, uname = 'Ali'	```


## Array 数组

1. 数组的声明方式，数组有序

   可以存储任意类型数据

   ```javascript
   let arr1 = [1,2,3,4,5,6]
   let arr2 = ['Mon','Tue','Wed']
   ```

2. 数组索引方式

   ```javascript
   console.log(arr[0])
   ```

3. 数组长度

   ```javascript
   console.log(arr.length)
   ```

## Const 常量

```javascript
const PI = 3.14
```

1. 常量不可以改变，不可以复制，像是Java中的final static的性质。
2. 常量声明的时候必须赋值。
3. 常量命名最好大写。

## Data type 数据类型 

JavaScript 松散、弱数据类型语言

> Java

```java
int num = 10;
```

>  JavaScript: 只有赋值之后才知道类型

```javascript
let num = '二'
```

### 基本数据类型：

#### 1. number

+ 可以是整数、小数、正数、负数

+ 算数运算符：  +  - *   /  % 

+ NaN 数据类型的出现，表示计算错误，或计算机无法理解的结果。黏性属性，任何对NaN的操作返回都是NaN

#### 2. string

+ \+ 数字相加，字符相连

  ```javascript
  console.log("pink"+'color'+num)
  ```

+ 模版字符串

  语法： 

  1. `` (反引号)

  2. 内容拼接变量时，用`${}`包含变量

     ```javascript
     let age = 18
     document.write(`${age}岁`)
     ```


####  3. boolean

+ true
+ false

#### 4. undefined

+ 只声明不赋值，变量默认值undefined
+ 使用场景：开发时声明一个变量，接受数据，如果不确定数据是否传输成功，检测变量是否为undefined

#### 5. null

​	null 和 undefined 的区别：

+ undefined 表示没有赋值

+ null 表示赋值了，内容为空

  ```javascript
  console.log(undefined + 1) //Nan
  console.log(null + 1 ) // 1
  ```


使用场景： 

+ null作为尚未创建的对象。

+ 将变量里面存放一个对象，但对象还没创建好，先给null

### 检测数据类型

#### typeof

+ typeof 变量名
+ typeof (变量名)

### 引用数据类型

## 类型转换

#### 1. 隐式转换

+ +号两边只要有一个字符串，两边都会转成字符串
+ 除了+号以外的算术运算符，都会把数据转成数字类型
+ +号作为正号解析可以转换为数字型
+ 任何数据和字符串相加结果都是字符串

![image-20240224102913057](/Users/jingyiwu/Library/Application Support/typora-user-images/image-20240224102913057.png)

 

#### 2. 显示转换

```javascript
Number(data) // 转化数字型 NaN也是number类型，代表非数字
ParseInt(data) // 只保留整数，不会四舍五入
ParseFloat(data) // 可以保留小数

```

# Day 2

### 运算符

#### 1. 一元运算符

一元运算符 ---> 自增运算、正负号

+ 前后置自增：

  在独立使用时两者没区别，但是运算时有区别。

  后置i++使用的比较多

  ```javascript
  let num = 10
  num +=1
  ++ num //前置自增
  console.log(++i + 1) //3
  // i先自加1，变成2之后，与后面的1相加
  num ++ //后置自增
  console.log(i++ + 1) //2 后置自增先运算 再++
  // 先和1相加，先运算输出完毕后，i再自加
  ```

#### 2. 二元运算符

需要两个操作数称为二元运算符

#### 3. 比较运算符

```javascript
	> 
    < 
    >=
    <=
    ==  //左右两边值是否相等 
        console.log(2=='2') true
    === //左右两边是否类型和值都相等，强烈建议使用
        console.log(2==='2') false
    !== //左右两边是否不全等
    
```

+ 字符串比较按照ASCII值，从左至右依次比较，如果第一位一样再比较第二位，以此类推

  `console.log('a'<'b') //true`

+ NaN不等于任何值，包括它本身。涉及到 "NaN"都是false

+ 不同类型之间比较会发生隐式转换

  最终把数据隐士转换变成number类型再比较

  所以开发中，如果准确比较喜欢`==`或者`!==`

+ 比较运算符的结果返回true和false

#### 4. 逻辑运算符

| 符号 | 名称   | 特点           |
| ---- | ------ | -------------- |
| &&   | 逻辑与 | 一假则假       |
| \|\| | 逻辑或 | 一真则真       |
| !    | 取反   | 真变假，假变真 |



#### 5. 运算符优先级

优先级一致，从左至右运算

| 优先级 | 运算符     | 顺序           |
| ------ | ---------- | -------------- |
| 1      | 小括号     | （）           |
| 2      | 一元运算符 | ++ -- ！       |
| 3      | 算数运算符 | 先*/% 后+-     |
| 4      | 关系运算符 | \> >= < <=     |
| 5      | 相等运算符 | == != \=== !== |
| 6      | 逻辑运算符 | 先&&后\|\|     |
| 7      | 赋值运算符 | =              |
| 8      | 逗号运算符 | ,              |

+ 一元运算符的逻辑非优先级很高
+ 逻辑与比逻辑或优先级

### 分支语句

#### 1. 表达式

表达式是可以被求值的代码，JavaScript会计算出一个结果 

>  因为表达式可以被求值，所以它可以写在赋值语句的右侧`num=3+4`

#### 2. 语句

语句是一段可以执行的代码

> prompt() 可以弹出一个输入框，还有 if 语句 for循环语句

> 而语句不一定有值，所以alert(), for, break等语句不能被用于赋值

>  `alert()` 弹出对话框

> `console.log()` 控制台打印输出

#### 3. 程序三大流程控制语句

+ 顺序结构：从上至下
+ 分支结构（条件判断）
+ 循环结构

#### 4. 分支语句

1. 种类：单分支、双分支、多分支

   只有一条分支会被执行

2. 使用方法

   ```javascript
   if (condition 1){
       .....
       code block
       .....
   } else if (condition 2){
       .....
       code block
       .....
   } else if (condition 2){
       .....
       code block
       .....
   }
   else {
       // 不满足条件执行的代码
       .....
       code block
       .....
   }
   ```

   a.  括号内条件为true时，进入大括号执行代码

   + 除了 ==0== 之外的其余数字都是true
   + 除了 ==' '==  所有的字符串都是true 

   b.  小括号内的结果若不是布尔类型时，会发生隐式转换为布尔类型

   c.  如果大括号只有一个语句，大括号可以省略

   d.  先判断条件1，若满足条件1就执行代码1，其他不执行。若不满足则向下判断条件2，满足条件2 执行代码2，爱他不执行。若依然不满足继续向下判断，以此类推。若以上条件都不满足，执行else里面的代码。

#### 三元运算符

>  if 双分支的简洁版本

condition 满足 执行code1，不满足code2

```javascript
condition ? code1 :code2 
3>5 ? alert("真的"):alert("假的")
```

#### switch语句

Keopoints:

+ 找到小括号里面数据==全等==的case值，并执行里面对应的代码
+ 若没有全等 ===\=\===的值，则执行defalut里面的代码
+ switch case语句一般用于等值判断，不适用于区间判断
+ switch case一般需要配合break关键词使用，没有break会造成case穿透

```javascript
switch(数据){
    case value1:
        //code
        break
    case value2:
        //code
        break
    case valueN:
        //code
        break
    default:
        //code
        break
}
```

# Day3

## 循环语句

### while循环

#### 语法

```javascript
while(condition){//执行条件
    // code
    // 循环体
}
```

+ 满足括号里面的条件true才会进入循环体执行代码
+ while大括号里代码执行完毕后不会跳出，而是继续回到小括号里面判断条件是否满足，若满足又执行大括号里的代码，然后再回到小括号里面判断条件，直到括号内条件不满足，跳出循环

#### 三要素

+ 变量起始值
+ 终止条件（木有终止条件，循环会一直执行，造成死循环）
+ 变量变化量（用自增或自减）

```javascript
let i = 1
while (i <= 3){
    document.write('循环三次')
}
```

#### break & continue

+ 循环里面遇到break直接退出循环
+ 循环里面遇到continue，重新开始新的循环，原来continue之后的语句不再执行

### 3. for 循环

优点： 声明起始值、循环条件、变化值写到一起

#### 语法

```javascript
for (变量起始值; 终止条件; 变量变化量){
    //循环体
}
```

#### 循环嵌套

+ 双重for循环

```javascript
for (outside_start; condition; change_value){
    for(inside_start; condition; change_value){
        //code body
    }
}
```



### 4.无限循环：

+ while(true) 使用break中断循环
+ for(;;) 使用break中断循环

#### 5. while和for的区别

+ 明确循环次数使用for
+ 不明确循环次数，推荐使用while

## 数组

> Array是一种按顺序保存数据的数据类型， 每个数据都有索引

### 1. 声明语法

```javascript
// 1. 字面量声明数组
let arr = [1,2,'pink','true']
// 2. 使用new Array构造函数声明
let arr = new Array(1,2,3,4)
```

### 2. 取值语法

```javascript
let names = ['hams','jams','lily','lake','tom']
names[0] // hams
names[1] // jams

names.length //获得数组长度
```

### 3. 数组操作

- 增 

  ```javascript
  arr.push(元素1,...,元素n) 
  // 将一个或多个元素添加到数组末尾，并返回该数组的新长度[!important]
  arr.unshift(元素1,...,元素n)
  // 将一个或多个元素添加到数组开头，并返回该数组的新长度
  ```

- 删 

  ```javascript
  arr.pop() // 从数组数组中删除最后一个元素，并返回该元素的值
  arr.shift() //删除第一个元素
  arr.splice(start, deleteCount) 
  // 删除指定元素
  // arr.splice(起始位置, 删除几个元素) 
  // 如果没有指定deldeteCount,会默认从起始位置删除到数组最后
  ```

- 改 —> 数组[下标] = value

- 查 —> 数组下标

# Day4

## 函数使用

## 函数声明

```javascript
function funcName(){
    console.log('声明函数')
}
```

+ 尽量小驼峰命名法
+ 前缀应该为动词
+ 命名建议：常用动词约定

| 动词 | 含义                   |
| ---- | ---------------------- |
| can  | 判断是否可执行某个动作 |
| has  | 判断是否含有某个值     |
| is   | 判断是否为某个值       |
| get  | 获取某个值             |
| set  | 设置某个值             |
| load | 加载某些数据           |

## 函数调用

`函数名( ) `

函数与循环的不同：

+ 循环代码写完即执行，不能很方便控制执行位置
+ 随时调用，随时执行，可重复掉用

## 函数传参

```javascript
function funName(parameter...){
    code body
}

function getSum(num1,num2){
    document.write(num1+num2)
}
```

### 参数列表

+ 传入数据列表
+ 声明这个函数需要传入几个数据
+ 多个数据用逗号隔开

### 参数默认值

+ 如果用户不给形参对应的实参，结果为<b>==undefined==</b>
+ undefined + undefined == NaN
+ 增加代码健壮性，用户不输入实参，可以给形参默认值
+ 默认值只会在缺少实参参数时才会被执行
+ 参数也可以是变量

```javascript
function getSum(x = 0, y = 0){
    document.write(x+y)
}
getSum() //结果是0，而不是NaN
getSum(1,2) //结果是3
```

## 函数返回值

> 函数返回执行结果对整个程序的扩展性更高，可以让其他程序使用此结果

### Keypoints

+ return 会立刻结束当前函数，后面的代码块不会执行
+ 如果函数没有return, 则此函数默认返回值为undefined
+ return多个值，使用`return[max, min]`, 返回一个数组

```javascript
function getMaxMinValue(arr = []) {
  let max = arr[0]
  let min = arr[0]
  for (let i = 1; i < arr.length; i++) {
    if (max < arr[i]) {
      max = arr[i]
    }
  }

  for (let i = 1; i < arr.length; i++) {
    if (min > arr[i]) {
      min = arr[i]
    }
  }
  return [max, min]
}
```

## 函数细节

+ 同一个作用域，两个相同名字的函数，后面的函数会覆盖前面的函数

+ return 会结束函数，所以return后面不再有语句

  >break VS return
  >
  >break -> 结束循环或switch
  >
  >return -> 结束函数

+ 参数不匹配

  > 实参比形参多，剩余实参不参与运算
  >
  > 实参比形参少，1 + undefined == NaN

  ```javascript
  function fn(a,b){
      return a+b
  }
  
  fn(1,2,100) // return 3
  fn(1) //NaN
  ```

## 作用域

> 变量名的有效范围称为作用域

### 全局作用域

> 全局有效
>
> 作用于所有代码执行环境（整个script标签内部或独立js文件）

### 局部作用域

> 局部有效
>
> 作用域函数内的代码环境，因为与函数有关系，也称为函数作用域

### 全局变量

> 全局变量在任何区域都可以访问和修改

+ 如果函数内部，变量没有声明，直接赋值，也当作==全局变量==， 黑户一样的存在，不太规范。
+ 函数的形参看作局部变量

### 局部变量

> 局部变量只能在当前函数内部访问修改

### 变量的访问原则

+ 只要是代码，就至少有一个作用域
+ 写在函数内部的是局部作用域
+ 如果函数中还有函数（嵌套），那么在这个作用域中又诞生一个作用域
+ <b>==访问原则：在能够访问到的情况下，先局部，局部没有再找全局==</b>
+ 作用域链：采取==就近原则==的方式查找变量的最终值

## 匿名函数

> 没有名字的函数，无法直接使用

### 使用方式

#### 函数表达式

> 将匿名函数赋值给一个变量，通过变量名称进行调用，我们将这个称为函数表达式

```javascript
let fn = function(){
    //code body
    condole.log('hi')
}
//调用方式

fn() //还是要加（）
```

##### 函数表达式和具名函数的区别

+ 具名函数的调用可以写在任何位置
+ 匿名函数需要先声明函数表达式再使用

```javascript
let btn = document.querySelector('button')
btn.onclick = function(){
    alert('我是匿名函数')
}
```

#### 立即执行函数

> 场景介绍：避免全局变量之间的污染

```javascript
// 方式一
(function(){})(); 
//必须加;不然函数不停止
//第二个()本质是调用函数 fn();可以加实参
(function(a+b){console.log(a+b)})(1,2);

// 方式二
(function (){}());
(function(a+b){return a+b}(2,3));
//不需要调用，立刻执行
```

总结： 

+ 立即执行函数主要作用是防止变量污染
+ 立即执行函数无需调用，立即执行；多个立即执行函数用;隔开

## 逻辑中断

```javascript
function fn(x,y){
    x = x||0
    y = y||0
    //逻辑中断
}
```

### 逻辑运算符里的短路



+ 短路：只存在于&&和||之间，当满足一定条件会让右边代码不执行

  | 符号 | 短路条件          |
  | ---- | ----------------- |
  | &&   | 左边为false就短路 |
  | \|\| | 左边为true就短路  |

+ 通过左边能得到整个式子的结果，没必要判断右边

+ 运算结果：

  无论&&还是||，运算结果都是最后被执行的表达式值，一般用在变量赋值

```javascript
console.log(false && 3+5) //false 

let age = 18
console.log(false && age++) 
//age还是18，因为左边为false，所以age++不能执行
console.log(age);

console.log(11||age++)
//age还是18,因为11判断为true,后面age++不执行
console.log(age)

//如果表达式两侧都为真，则返回最后一个值
console.log(11&22) //return 22
```

### 转换为Boolean型

#### 显式转换：

​	Boolean( 数据 )

​	`'', 0, undefined, null, false, NaN`

​	转换为布尔值都是false，其余为true

```javascript
console.log(false && 20)  //false
console.log(5<3 && 20) // false
console.log(undefined && 20) //undefined
console.log(null && 20) // null
console.log(0 && 20) // 0
console.log(10 && 20) //20
```

```javascript
console.log(false || 20) //20
console.log(5<3 || 20)   //20
console.log(undefined || 20) //20
console.log(null || 20)  //20
console.log(0 || 20)  //20
console.log(10 || 20) //10
```

#### 隐式转换

1. 有字符串的加法 `"" + 1`，结果是 “1”

2. 减法 - ，只能用于数字，会使空字符串""转换为 0

3. null 经过数字转换后会变成 0

4. undefined 经过数字转换后会变成NaN 

   ``null == undefined //true``

   ``null === undefined //false``

```javascript
console.log(''-1)    //-1
console.log('pink老师' -1)  //NaN
console.log(null + 1) // 1
console.log(undefined + 1) //NaN
// undefined 无论 + - * / 都是NaN
console.log(NaN + 1) //NaN
// NaN做任何的操作都是NaN，NaN也不等于NaN
```

# Day5

## 对象(object)

> JavaScript里面的一种数据类型
>
> 可以理解为一种无序的数据集合，数组是有序的数据集合
>
> 用来描述某事物

```javascript
let obj = {
    uname: 'xx',
    age: 18,
    gender: '女'
}
```

###属性与方法

### 声明方式

```javascript
let objectName1  = {}
let objectName2  = new Object()
```

### 属性

+ 属性： 信息或特征 (名词)   尺寸、颜色、重量
+ 方法：功能或行为  (动词)   打电话、发短信、玩游戏

```javascript
let goods = {
    name: '小米10青春版',
    num: 100012816024,
    weight: '0.55kg',
    'current-address': '中国大陆'
}
```

+ 属性都是成对出现，包括属性名和值，用英文 `:`  分隔
+ 多个属性之间用英文 `, `分隔

#### 增删改查

#### 查

```javascript
console.log(goods.name)
console.log(goods.price)
//第二种方法
goods['current-address']
```

#### 改

```javascript
obj.gender = '男'
```

#### 增

```javascript
obj.hobby = '足球'    //直接新增一个属性
```

#### 删

```javascript
delete obj.hobby
```

### 方法

+ 方法由方法名和函数两部分构成，使用`:`分隔
+ 多个属性之间使用`,`分隔
+ 方法是依附在对象中的函数
+ 方法名可以使用引号，一般情况省略，除非遇到特殊符号
+ 可以添加实参和形参

```javascript
let obj = {
    uname : '刘德华',
    
    //匿名函数
    song : function(){
        console.log('冰雨')
    },
    addNum : function(x,y){
        console.log(x+y)
    }
}
obj.addNum(1,2)
```

+ 后追加

```javascript
obj.hobby = '足球' //注意后追加变成了 = 号
obj.move = function(){
    //code body//
}
```

### 遍历对象

+ ==for k in obj== 的索引是字符串，适合遍历对象 

> javascript的对象有点像字典， k->key

```javascript
let obj = {
    uname : 'pink',
    age : 18,
    gender: '男'
}
// 遍历对象
for (let k in obj){
    console.log(k) //输出 'uname'
    console.log(obj[k])
}
```

+ 一般不使用for k in obj这种方式遍历数组，主要是用来遍历对象
+ for in 语法中的 k是一个变量，在循环过程中依次代表对象的属性名
+ 由于k是字符串变量，所以需要使用 `[ ]` 语法解析
+ ==k==是获得对象的属性名，==obj [k]== 是获得属性值

### 内置对象

> JavaScript内部提供的对象，包含各种属性和方法给开发者调用
>
> + console.log() 
> + document.write()

#### Math

> 提供了一系列的数学运算的方法

##### 包含方法

+ random-> 生成0-1之间的随机数 （包0不包1）

+ ceil -> 向上取整

+ floor -> 向下取整 

  有点像parseInt( )

+ round -> 四舍五入

+ max -> 找最大数

+ min-> 找最小数

+ pow-> 幂运算

+ abs-> 绝对值

##### Math.random()

```javascript
// 向下取整
Math.floor(Math.random()*(10+1))

//随机抽取数组
let arr = ['red','green','blue']
let random = Math.floor(Math.random()*arr.length)

//生成N-M之间的随机数
Math.floor(Math.random()*(M-N+1))+N

//如何生成5-10之间的随机数
Math.floor(Math.random()*(5+1))+5
```

```javascript
//抽奖游戏，抽中的人在列表中删除

let name_arr = ['赵云', '黄忠', '关羽', '张飞']
while (name_arr.length > 0) {
  let random_index = Math.floor(Math.random() * name_arr.length)
  document.write(name_arr.splice(random_index, 1))
}

//数组删除数据方式
splice(起始位置,删除几个元素)
```

## 数据类型

### 基本数据类型

> 又称为值类型，在存储变量中，存储的值本身
>
> + string, number, boolean, undefined, null

### 引用数据类型

> 复杂数据类型，在存储变量时是地址（引用）
>
> + 通过new关键创造的对象 Object, Array, Data

### 栈堆

![image-20240227220622098](/Users/jingyiwu/Library/Application Support/typora-user-images/image-20240227220622098.png)

![image-20240227220658528](/Users/jingyiwu/Library/Application Support/typora-user-images/image-20240227220658528.png)

















