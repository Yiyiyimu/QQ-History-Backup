# qqmessageoutput
安卓QQ聊天记录导出

```python
q=QQoutput('yourdb.db','yourkey')
test=q.message(yourfriendqq)
q.output(yourfriendqq)
for msg in test:
    print(msg)
```

