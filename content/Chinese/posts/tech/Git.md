---
title : '学习：Git '
date : 2024-04-05
Lastmod: 
draft : false
author : "Jingyi Wu"
comments: true #是否展示评论
showToc: true # 显示目录
TocOpen: false # 自动展开目录
hidemeta: false # 是否隐藏文章的元信息，如发布日期、作者等

## disableShare: true # 底部不显示分享栏

Showbreadcrumbs: true #顶部显示当前路径
ShowShareButtons: true
ShowReadingTime: true
ShowWordCounts: true
ShowPageViews: true
ShowLastMod: true #显示文章更新时间
hasCJKLanguage: true
summary: Git basic operation

categories: 

- tech

tags:

- Git
- VUB
- Frontend

keywords:

- Git

cover:
    image: ""
    caption: "" #图片底部描述
    alt: ""
    relative: true
---

# Git

> 分布式代码版本控制系统，帮助开发团队维护代码。实现记录代码内容，切换代码版本，多人开发时高效合并代码内容

![image-20240404212226415](/img/Javascript/image-20240404212226415.png)

## 安装及配置

### 1.如何判断安装成功？

1. 打开bash终端 (git专用)
2. 命令：`git-v` 查看版本号

### 2. Git 配置用户信息

用户名`git config --global user.name "用户名"`

邮箱 `git config --global user.email "@gamil"`

## Git 仓库

Git 仓库 (repository): 记录文件状态内容的地方，存储修改历史记录

![image-20240404213144948](/img/Javascript/image-20240404213144948.png)

如何创建：

1. 把本地文件夹转换成Git仓库： `git init`
2. 从其他服务器上克隆Git仓库

## Git 三个区域

- 工作区：实际开发时操作的文件夹
- 暂存区：保存之前的准备区域（暂存改动的文件） .git/index
- 版本库： 提交并保存暂存去中的内容，产生一个版本快照 .git/objects

![image-20240404214549241](/img/Javascript/image-20240404214549241.png)

| 命令                     | 作用                     |
| ------------------------ | ------------------------ |
| git add 文件名           | 暂存指定文件             |
| git add .                | 暂存所有改动文件         |
| git commit -m "注释说明" | 提交并保存，产生版本快照 |
| git ls-files             | 看看暂存区有啥文件       |
| git status -s            | 查看文件状态，并最终提交 |

## Git文件状态

- 未跟踪： 新文件，从未被Git管理过
- 已跟踪：Git已经知道和管理文件

使用： 修改文件-> 暂存-> 提交保存记录

| 文件状态     | 概念            | 场景                 |
| ------------ | --------------- | -------------------- |
| 未跟踪 (U)   | 从未被Git管理过 | 新文件               |
| 新添加 (A)   | 第一次被Git暂存 | 之前版本记录无此文件 |
| 未修改 (' ') | 三个区域统一    | 提交保存后           |
| 已修改 (M)   | 工作区内容变化  | 修改了内容产生       |

`git status -s`

- 第一列是暂存区的状态
- 第二列是工作区的状态

## Git 暂存区使用

> 暂时存储，可以临时恢复代码内容，与版本库解藕

- 暂存区 -> 覆盖 -> 工作区 `git restore 目标文件`  (注意：完全确认覆盖时使用)
- 从暂存区移除文件 `git rm --cached 目标文件`

![image-20240404220949930](/img/Javascript/image-20240404220949930.png)

## Git 回退版本

> 把版本库某个版本对应的内容快照，恢复到工作区/暂存区

查看提交历史 ： `git log --oneline`

查看完整日志： `git reflog --online`

__回退命令： git reset --soft 版本号 (其他文件未跟踪)__

> 会尽可能保留 暂存区和工作区 里面的内容，都会变为未被 git 跟踪的状态

![image-20240404223530621](/img/Javascript/image-20240404223530621.png)

__回退命令： git reset --hard 版本号，只会看到回退的文件，其他全部删除__

![image-20240404223810396](/img/Javascript/image-20240404223810396.png)

__回退命令： git reset --mixed 版本号 (git reset 默认模式)，暂存区只会看到回退的文件， 但是工作区会保留__

![image-20240404223944859](/img/Javascript/image-20240404223944859.png)

总结：

1. 什么是Git回退版本？

   将版本库某个版本对应的内容快照，回复到工作区/暂存区

2. 强制覆盖暂存区和工作区命令？

   `git reset --hard 版本号`

3. 如何查看提交历史

   `git log --oneline`

   `git reflog --oneline`

## Git 删除文件

- 方法一

  手动在工作区中删除 -> `git add . 至暂存区` -> `git commite -m""`

- 方法二

  手动在工作区中删除 -> `git rm --cached 目标文件` -> `git commite -m""`

## Git 忽略文件

> .gitignore 文件可以让 git 彻底忽略跟踪指定文件

目的： 让git仓库更小更快，避免重复无意义的文件管理。

- 系统或软件自动生成的文件
- 编译产生的结果文件
- 运行时生成的日志文件，缓存文件，临时文件
- 涉密文件，密码，秘钥等文件

创建步骤：

- 项目__根目录__新建 .gitignore 文件
- 填入相应配置来忽略指定文件

```javascript
# 忽略 npm 下载的第三方包
node_modules
# 忽略分发 文件夹
dist
# 忽略 VSCode 配置文件
.vscode
# 忽略秘钥文件
*.pem
*.cer
# 忽略日志文件
*.log
```

## Git 分支

> 本质是 指向提交节点的可变指针， 默认名字是master/main

注意： HEAD指针影响工作区/暂存区的代码状态

### 场景

- 开发新需求/修复Bug，保证主线代码随时可用，多人协助

![image-20240404230422064](/img/Javascript/image-20240404230422064.png)

- 保证主线业务的同时，新增content分支，继续增加新功能，但不影响主分支master的功能
- 在新分支中修复bug

![image-20240404230742486](/img/Javascript/image-20240404230742486.png)

### 步骤&命令

1. 创建分支 `git branch 分支名`

2. 切换分支 `git checkout 分支名`

3. 查看分支 `git branch`

   就是将 HEAD 指针指向 新的分支

   ![image-20240404231035481](/img/Javascript/image-20240404231035481.png)

总结：

1. 什么是Git分支？

   指针，指向提交记录

2. HEAD 指针的作用？

   影响暂存区和工作区的代码

3. 如何创建和切换指针？

   `git branch 分支名`

   `git checkout 分支名`

## Git 分支 - 合并与删除

> 把分支合并回`master，并删除分支

1. 切换回要合入的分支，如果要合并至master: `git checkout master`
2. `git merge 要合并的分支`

![image-20240405001220514](/img/Javascript/image-20240405001220514.png)

3. 删除合并后的分支指针： `git branch -d 已合并的分支`

## Git 分支 - 合并与提交

> 发生于原分支产生了新的提交记录后，再合并回去时发生，自动使用多个快照记录合并后产生一次新的提交

![image-20240405001859735](/img/Javascript/image-20240405001859735.png)

1. 切回到要合入的分支 `git checkout master`
2. 合并其他分支 `git merge content`
3. 删除合并后的分支 `git branch -d content`

## Git 分支 - 合并冲突

> 在不同的分支中，对同一个文件的同一部分修改，Git无法干净的合并，产生合并冲突

1. 打开VSCode找到冲突文件并手动解决
2. 解决后需要提交暂存，再次提交一次至版本库
3. 删除合并后的分支 

## Git 常用命令总结

| 命令                   | 作用                                 | 注意                                     |
| ---------------------- | ------------------------------------ | ---------------------------------------- |
| git -v                 | 查看git版本                          |                                          |
| git init               | 初始化git仓库                        |                                          |
| git add '文件标识'     | 暂存某个文件                         | 文件标识以终端为起始的相对路径           |
| git add .              | 暂存所有文件                         |                                          |
| git commit -m '...'    | 提交产生版本记录                     | 每次提供，把暂存区内容快照一份           |
| git status             | 查看文件状态 - 详细信息              |                                          |
| git status -s          | 查看文件状态 - 简略信息              | 第一列是暂存区状态，第二列是工作区状态   |
| git ls-files           | 查看暂存区文件列表                   |                                          |
| git restore '文件标识' | 从暂存区恢复到工作区                 | 如果文件标识为，则恢复所有文件           |
| git rm --cached        | 从暂存区移除文件                     | 不让git跟踪文件变化                      |
| git log                | 查看提交记录- 详细                   |                                          |
| git log --oneline      | 查看提交记录- 简略信息               | 版本号 分支指针 提交时说明注释           |
| git relog --oneline    | 查看完整历史 -简略消息               | 包括提交，切换，回退等所有记录           |
| git reset 版本号       | 切换版本代码到暂存区和工作区         |                                          |
| git branch 分支名      | 创建分支                             |                                          |
| git branch             | 查看本地分支                         |                                          |
| git branch -d 分支名   | 删除分支                             | 确保记录已经合并到别的分支下，再删除分支 |
| git checkout 分支名    | 切换分支                             |                                          |
| git checkout -b 分支名 | 创建并立刻切换分支                   |                                          |
| git merge 分支名       | 把分支提交历史记录合并到当前所在分支 |                                          |

## Git 远程仓库

> 托管在网络中的项目版本库

__作用：__ 保存版本库的历史记录，多人协作

__创建：__ 公司自己的服务器/第三方托管平台 (Github)

![image-20240405014842128](/img/Javascript/image-20240405014842128.png)

### 推送步骤 

1. 注册第三方平台账号(创建repo)

2. 新建仓库得到远程仓库 Git 地址

3. 本地 Git 仓库添加远程仓库原点地址

   `git remote add origin 仓库地址`

4. 本地Git 仓库推送版本记录到远程残酷

   `git push -u 远程仓库别名 本地和远程分支名`

   `git push -u origin master`

   完整写法 `git push --set-upstream origin master:master`

5. 如果添加错了远程仓库，如何移除？

   `git remote remove origin`


### 克隆 clone

1. 命令： `git clone 'url'`
2. 会在运行命令的文件夹生成项目文件夹（包含版本库，并映射到暂存区和工作区）

注意：

1. Git本地仓库已经建立好和远程仓库的连接，再次推送无需push

### 更新本地代码 pull

1.多人协同工作步骤

+ A 开发代码 -> 工作区 -> 暂存区 -> 提交 -> 拉取 (可选) -> 推送
+ B -> 拉取（后续也可以开发代码 -> ... -> 推送）

2.命令 

`git pull 远程仓库别名 本地和远程分支名 ` 

`git pull origin/maste`

`git pull rebase prigin master` 强制合并 

### Git 远程仓库常用命令

| 命令                                     | 作用             | 注意                       |
| ---------------------------------------- | ---------------- | -------------------------- |
| git remote add 远程仓库别名 远程仓库地址 | 添加远程仓库地址 | 别名唯一                   |
| git remote -v                            | 查看远程仓库地址 |                            |
| git remote remove 远程仓库别名           | 删除远程仓库地址 |                            |
| git pull 远程仓库别名 远程仓库地址       | 拉去             | 等于 git fetch + git merge |
| git push                                 | 推送             |                            |
| git pull --rebase 远程仓库别名 分支名    | 拉取合并         | 合并没有关系的记录         |
| git clone 远程仓库地址                   | 克隆             |                            |



