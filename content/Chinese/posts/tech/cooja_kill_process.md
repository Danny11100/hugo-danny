---
title : '解决: Cooja 端口显示资源繁忙'
date : 2024-02-15
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
summary: "每次运行Cooja的端口监听，显示资源繁忙，可能是端口已经被占用，只要给其中一个进程干掉就好."

categories: 
- tech

tags:
- Cooja
- VUB

keywords:
- cooja
- resource busy
- MacBook Pro


cover:
    image: ""
    caption: "" #图片底部描述
    alt: ""
    relative: true
---

# 在终端中干掉进程

## 1. 检查有没有僵尸进程

 在终端中使用👇的语句.
> `ps aux | grep 'Z'`

## 2. 检查端口的使用情况
 在终端中使用👇的语句.

> `sudo lsof -i :60001`

 60001 是端口名称, 输入一下语句之后，就能看到进程的ID了. (方便直接干掉它)

## 3. 关键一步：干掉进程
> `kill [PID]`
> `kill -9 [PID]` 

  最后一个 -9 是强制停止

## 4. 再检查一遍端口的使用情况
> 我遇到的问题是我的计算机总是有两个进程，一个来自 <strong>Java<strong>，一个来自 <strong>sudo<strong>。所以我需要杀死 sudo，因为 cooja 在 Java 中运行. 如果kill进程失败了, 尝试使用sudo kill [PID]

