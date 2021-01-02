from _overlapped import NULL
import hashlib
import sqlite3
import time
import os
import traceback


class QQoutput():
    def __init__(self, dir, qq_self, qq_oppo, mode):
        self.key = get_key(dir)  # 解密用的密钥
        db = os.path.join(dir, "db", qq_self + ".db")
        self.c = sqlite3.connect(db).cursor()
        self.qq_self = qq_self
        self.qq = qq_oppo
        self.mode = mode
        self.num_to_name = {}

    def decrypt(self, data):
        if type(data) == bytes:
            msg = b''
            try:
                for i in range(0, len(data)):
                    msg += bytes([data[i] ^ ord(self.key[i % len(self.key)])])
            except:
                msg = NULL
            return msg.decode(encoding="utf-8")
        elif type(data) == str:
            msg = ""
            try:
                for i in range(0, len(data)):
                    msg += chr(ord(data[i]) ^ ord(self.key[i % len(self.key)]))
            except:
                msg = NULL
            return msg
        return NULL

    def add_emoji(self, msg):
        pos = msg.find('\x14')
        while (pos != -1):
            lastpos = pos
            num = ord(msg[pos + 1])
            msg = msg.replace(
                msg[pos:pos + 2],
                "<img src='./gif/" + str(num) + ".gif' alt=" + str(num) + ">")
            pos = msg.find('\x14')
            if (pos == lastpos):
                break
        return msg

    def message(self):
        # mode=1 friend
        # mode=2 troop
        num = self.qq.encode("utf-8")
        md5num = hashlib.md5(num).hexdigest().upper()
        if (self.mode == 1):
            execute = "select msgData,senderuin,time from mr_friend_{md5num}_New".format(
                md5num=md5num)
        else:
            execute = "select msgData,senderuin,time from mr_troop_{md5num}_New".format(
                md5num=md5num)

        cursor = self.c.execute(execute)
        allmsg = []
        for row in cursor:
            msgdata = row[0]
            if (not msgdata):
                continue
            uin = row[1]
            ltime = time.localtime(row[2])

            sendtime = time.strftime("%Y-%m-%d %H:%M:%S", ltime)

            amsg = []
            amsg.append(sendtime)
            amsg.append(self.decrypt(uin))
            amsg.append(self.decrypt(msgdata))
            allmsg.append(amsg)
        return allmsg

    def get_name(self):
        exe = "select uin,remark from Friends"
        cursor = self.c.execute(exe)
        for row in cursor:
            num = self.decrypt(row[0])
            name = self.decrypt(row[1])
            self.num_to_name[num] = name

    def output(self):
        name1 = "我"
        file = str(self.qq) + ".html"
        self.get_name()
        f2 = open(file, "w", encoding="utf-8")
        f2.write(
            "<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head>"
        )
        allmsg = self.message()
        f2.write("<div style='white-space: pre-line'>")
        for msg in allmsg:
            try:
                if (msg[1] == str(self.qq_self)):
                    f2.write("<p align='right'>")
                    f2.write("<font color=\"green\">")
                    f2.write(msg[0])
                    f2.write("</font>-----<font color=\"blue\"><b>")
                    f2.write(name1)
                    f2.write("</font></b></br>")
                else:
                    f2.write("<p align='left'>")
                    f2.write("<font color=\"blue\"><b>")
                    f2.write(self.num_to_name.get(msg[1]) or msg[1])
                    f2.write("</b></font>-----<font color=\"green\">")
                    f2.write(msg[0])
                    f2.write("</font></br>")
                f2.write(self.add_emoji(msg[2]))
                f2.write("</br></br>")
                f2.write("</p>")
            except:
                pass
        f2.write("</div>")


def get_key(dir):
    kc_path = os.path.join(dir, "f", "kc")
    kc_file = open(kc_path, "r")
    return kc_file.read()


def main(dir, qq_self, qq_oppo, mode):
    try:
        q = QQoutput(dir, qq_self, qq_oppo, mode)
        q.output()
    except Exception as e:
        with open('log.txt', 'w') as f:
            f.write(str(e))
            f.write(traceback.format_exc())

        err_info = repr(e).split(":")[0] == "OperationalError('no such table"
        print(traceback.format_exc())
        if (err_info):
            raise ValueError("QQ号/私聊群聊选择/db地址/错误")


dir = "C:/Users/30857/Desktop/QQ_History/qq/apps/com.tencent.mobileqq"
qq_self = "308571034"
qq_oppo = "584740257"
#qq = "939840382"
key = "361910168"
#msg = "还是在试表情"
msg = ""
main(dir, qq_self, qq_oppo, 1)
