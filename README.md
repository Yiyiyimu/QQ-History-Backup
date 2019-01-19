# qqmessageoutput
安卓QQ聊天记录导出/安卓QQ数据库解密

```python
q=QQoutput('yourdb.db','yourkey')
test=q.message(yourfriendqq)
q.output(yourfriendqq)
for msg in test:
    print(msg)
```

获取db文件首先手机要root

```
data\data\com.tencent.mobileqq\databases\你的QQ.db
```

yourkey是解密的密钥，一般是手机序列号，拨号键盘下输入*#06#

手机QQ的db文件加密方式是异或加密，如果找不到自己的key可以反向破解