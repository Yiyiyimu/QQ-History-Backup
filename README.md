# QQ聊天记录导出

可执行文件[下载链接](https://github.com/Yiyiyimu/QQ_History_Backup/releases/download/v1.0/QQ_History_Backup-v1.1.zip)

## 简介

本项目 fork 自大佬的项目[roadwide/qqmessageoutput](https://github.com/roadwide/qqmessageoutput) 在此非常感谢

在之前版本的基础上完成了原作者提到的无需密钥解密的方法，添加了QQ表情的一并导出，并制作了GUI方便使用

## 获取db文件方法

如果root了，直接在以下地址就可以找到

```
data\data\com.tencent.mobileqq\databases\你的QQ.db 和 slowtable_你的QQ.db
```



如果没有root，可以通过手机自带的备份工具备份整个QQ软件，具体方法可以参见

> 怎样导出手机中的QQ聊天记录？ - 益新软件的回答 - 知乎
> https://www.zhihu.com/question/28574047/answer/964813560

导出之前建议发给对方一句话（至少六个汉字），后面解密用

## GUI使用方法

![GUI_image](./img/GUI.png)

db文件地址（必填）：选择对应的 qq号.db ，如果不全再选择slowtable_qq号.db

对方QQ号（必填）

手机识别码（二选一填入）：理论上是用手机识别码（MEID）作为聊天记录数据库的密钥，获取方法为在电话界面输入“*#06#”。但试了两个人的手机都不能用这个识别码作为密钥，可能QQ换了什么加密方式。。。

最后一次聊天记录（二选一填入，**推荐**）：因为测试所用两部手机密钥分别为9位和14位，一个汉字对应三个utf-8码，所以避免更长的密钥推荐使用至少六个汉字。可以在导出之前给对方发一句话过去。

最后一次聊天记录（二选一填入，**推荐**）：因为测试所用两部手机密钥分别为9位和14位，一个汉字对应三个utf-8码，所以避免更长的密钥推荐使用至少六个汉字。可以在导出之前给对方发一句话过去。

我的名字（选填）：默认为“我”，填入进行替换

对方名字（选填）：默认为对方QQ号，填入进行替换

## 输出截图

为了方便离线查看，qq表情gif选择保存在本地，注意移动聊天记录的时候需要同时移动gif文件

![screenshot](./img/screenshot.png)