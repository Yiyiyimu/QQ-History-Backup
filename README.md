# qqmessageoutput
安卓QQ聊天记录导出/安卓QQ数据库解密

[2019-10-02]新增了QQ群的消息记录导出，mode=1是好友，2是群

```python
q=QQoutput('yourdb.db','yourkey',mode)
test=q.message(yourfriendqq,mode)
q.output(yourfriendqq,mode)
for msg in test:
    print(msg)
```

获取db文件首先手机要root

```
data\data\com.tencent.mobileqq\databases\你的QQ.db
```
另外我还发现，如果聊天记录过多，会将较早的聊天记录存入以下数据库
```
data\data\com.tencent.mobileqq\databases\slowtable_你的QQ.db
```

yourkey是解密的密钥，一般是手机序列号，拨号键盘下输入*#06#

手机QQ的db文件加密方式是异或加密，如果找不到自己的key可以反向破解


