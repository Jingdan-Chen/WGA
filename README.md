# WGA

---

## 简介

由于武汉大学各个学院的综测/保研各有院内细则，规则十分复杂，且教务系统做的十分拉稀，不具备处理此类复杂功能的能力，因此在进行奖学金/保研评定是往往需要学生干部进行大量手工计算。WGA是为缓解此情况而出现的

WGA(**W**hu **G**rade **A**ssistant) 目前是由本人独立开发的针对武汉大学化学与分子科学学院，进行自动：*毕业审核/GPA计算/平均分计算/综合素质测评F2项计算/保研绩点计算* 的Python程序。可以处理包括A班加权在内的稍复杂的设置。使用者可以通过直接传入从教务系统导出的成绩文件，更改设置文件(./config.txt)完成不同任务和设置微调，不必更改源码，因此原则上不需要编程能力。

## 文件扼要说明

./config.txt: 程序运行的设置

./email.ipynb: 是笔者实现自动给每个同学发送成绩的小notebook

./configReadin.py: 包含读取config.txt的组件

./infoReadin.py: 用于读取成绩文件，进行运算处理

./task.py: 定义包括 毕业审核/GPA计算/平均分计算/综合素质测评F2项计算/保研绩点计算 的多种任务

./main.py: 主程序

RawData/: 放入成绩文件

personal/: 生成个人细则

ConfigData/: 是config.txt 的补充，包含了如保研考察课程列表等文件，可更改

cache/: 缓存文件

## 更多说明

笔者随缘update(毕业之前应该会写上，嗯)

