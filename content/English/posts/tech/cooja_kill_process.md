---
title : 'Solution: Cooja Displays Resource Busy'
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
summary: "When running cooja for port listening, there will be two processes. We must kill one, then cooja run successfully."

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

# Kill process in shell

## 1. Check for Zombie Processes

 Use the ps command to check for zombie processes.
> `ps aux | grep 'Z'`

## 2. Check Port Usage
 Use lsof or netstat to check if the port is still being used and by which process

> `sudo lsof -i :60001`

 This is show all of 60001 ports processes, you can check the PID in there.

## 3. Kill process by PID
> `kill [PID]`
> `kill -9 [PID]` 

  This means force to stop process

## 4. Check the current process again
> The problem I met is my computer always had two processes, one from <strong>Java<strong>, one from <strong>sudo<strong>. So I need to kill the sudo, because cooja run in Java.

