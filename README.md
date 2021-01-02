# QQ聊天记录导出

可执行文件[Github下载链接](https://github.com/Yiyiyimu/QQ_History_Backup/releases/download/v1.41/QQ_History_Backup-v1.41.zip)，[百度网盘下载链接](https://pan.baidu.com/s/1FRcqKiYho-DoDU-RC_uRkw)(sqhc) ，可直接运行。

## 简介

本项目 fork 自大佬的项目[roadwide/qqmessageoutput](https://github.com/roadwide/qqmessageoutput) 在此非常感谢。因为改动较多不再作为 fork 分支开发

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
  
手机识别码（待自动填入，供slowtable使用）：
1.Android Q及以上（19年以后的系统）限制了id获取权限，无法使用手机识别码（IMEI/MEID）作为聊天记录数据库的密钥，只能通过最后一次聊天记录计算key。在导出slowtable里的内容时默认使用前一步输出的手机识别码作为密钥。

最后一次聊天记录（非slowtable**必填**）：  
因为测试所用两部手机密钥分别为9位和14位，一个汉字对应三个utf-8码，为了避免更长的密钥推荐使用至少六个汉字符号。可以在导出之前给对方发一句话过去。

我的名字（选填）：默认为“我”，填入进行替换

对方名字（选填）：默认为对方QQ号，填入进行替换

私聊/群聊

2.root以后可以通过查看/data/data/com.tencent.mobileqq/files/kc来直接获取
  Termux可以使用以下命令：
  ```Bash
  cat /data/data/com.tencent.mobileqq/files/kc
  ```
  输出的那串数字即为该数据库的识别码。
## 输出截图

为了方便离线查看，qq表情gif选择保存在本地，注意移动聊天记录的时候需要同时移动gif文件

![screenshot](./img/screenshot.png)

有bug的话记得附上log.txt里的内容

## TODO
- [x] support troop message output
- [ ] use com.tencent.mobileqq/f/kc as key
- [ ] decode friend/troop name, to use in result
- [ ] add desensitization data to create e2e test
- [ ] add Makefile, to run build/test
- [ ] use pic in mobile folder, to better present result
