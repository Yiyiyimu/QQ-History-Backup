# QQ聊天记录导出

可执行文件[Github下载链接](https://github.com/Yiyiyimu/QQ_History_Backup/releases/download/v2.0/QQ_History_Backup-v2.0.zip)，[百度网盘下载链接](https://pan.baidu.com/s/1nbJcP5RVc1ID1IFGsN1-yQw)(i4cv) ，可直接运行。

## 简介

本项目 fork 自大佬的项目[roadwide/qqmessageoutput](https://github.com/roadwide/qqmessageoutput) 在此非常感谢。因为改动较多，不再作为 fork 分支开发

在之前版本的基础上完成了自动提取密钥解密的方法，自动填入备注/昵称，添加了QQ表情的一并导出，并制作了GUI方便使用

## 获取聊天记录文件夹方法

如果root了，直接在以下地址就可以找到。建议压缩文件夹后复制导出。

```
data\data\com.tencent.mobileqq
```

如果没有root，可以通过手机自带的备份工具备份整个QQ软件，具体方法可以参见

> 怎样导出手机中的QQ聊天记录？ - 益新软件的回答 - 知乎
> https://www.zhihu.com/question/28574047/answer/964813560


## GUI使用方法

![GUI_image](./img/GUI.png)

com.tencent.mobileqq：选择备份后的相应文件夹，一般为`apps/com.tencent.mobileqq`

## 输出截图

为了方便离线查看，qq表情gif选择保存在本地，注意移动聊天记录的时候需要同时移动gif文件

![screenshot](./img/screenshot.png)

有bug的话提issue，记得附上log.txt里的内容

## v2.0 更新
- 直接从 `files/kc` 提取明文的密钥，不用再手动输入或解密
- 支持群聊记录导出
- 支持 私聊/群聊 的 备注/昵称 自动填入
- 支持 slowtable 的直接整合

## TODO
- [x] support troop message output
- [x] use com.tencent.mobileqq/f/kc as key
- [x] decode friend/troop name, to use in result
- [x] auto-combine db and slow-table
- [ ] update to new qq emoji
- [ ] add desensitization data to create e2e test
- [ ] add Makefile, to run build/test
- [ ] use pic in mobile folder, to better present result
