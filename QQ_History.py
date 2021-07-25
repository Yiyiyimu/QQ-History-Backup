import hashlib
import sqlite3
import time
import os
import traceback
import json
import base64
from proto.RichMsg_pb2 import PicRec
from proto.RichMsg_pb2 import Elem

_crc64_init = False
_crc64_table = [0] * 256


def crc64(s):
    global _crc64_init
    if not _crc64_init:
        for i in range(256):
            bf = i
            for j in range(8):
                if bf & 1 != 0:
                    bf = bf >> 1 ^ -7661587058870466123
                else:
                    bf >>= 1
            _crc64_table[i] = bf
        _crc64_init = True
    v = -1
    for i in range(len(s)):
        v = _crc64_table[(ord(s[i]) ^ v) & 255] ^ v >> 8
    return v


class QQoutput():
    def __init__(self, path, qq_self, qq, mode, emoji, with_img, combine_img):
        self.db_path = path
        self.key = self.get_key()  # 解密用的密钥
        db = os.path.join(path, "databases", qq_self + ".db")
        self.c1 = sqlite3.connect(db).cursor()
        db = os.path.join(path, "databases", "slowtable_" + qq_self + ".db")
        self.c2 = sqlite3.connect(db).cursor()

        self.qq_self = qq_self
        self.qq = qq
        self.mode = mode
        self.emoji = emoji
        self.with_img = with_img
        self.combine_img = combine_img

        self.num_to_name = {}
        self.emoji_map = self.map_new_emoji()

    def decrypt(self, data, msg_type=-1000):
        msg = b''
        if type(data) == bytes:
            msg = b''
            for i in range(0, len(data)):
                msg += bytes([data[i] ^ ord(self.key[i % len(self.key)])])
        elif type(data) == str:
            msg = ''
            for i in range(0, len(data)):
                msg += chr(ord(data[i]) ^ ord(self.key[i % len(self.key)]))
            return msg

        if msg_type == -1000 or msg_type == -1049 or msg_type == -1051:
            try:
                return msg.decode('utf-8')
            except:
                # print(msg)
                pass
                return '[decode error]'

        if not self.with_img:
            return None
        elif msg_type == -2000:
            return self.decode_pic(msg)
        elif msg_type == -1035:
            return self.decode_mix_msg(msg)
        elif msg_type == -5008:
            return self.decode_share_url(msg)
        elif msg_type == -5012 or msg_type == -5018:
            return '[戳一戳]'
        # for debug
        # return '[unknown msg_type {}]'.format(msg_type)
        return None

    def add_emoji(self, msg):
        pos = msg.find('\x14')
        while pos != -1:
            lastpos = pos
            num = ord(msg[pos + 1])
            if str(num) in self.emoji_map:
                index = self.emoji_map[str(num)]

                if self.emoji == 1:
                    filename = "new/s" + index + ".png"
                else:
                    filename = "old/" + index + ".gif"

                emoticon_path = os.path.join('emoticon', filename)
                if self.combine_img:
                    emoticon_path = self.get_base64_from_pic(emoticon_path)

                msg = msg.replace(
                    msg[pos:pos + 2], '<img src="{}" alt="{}" />'.format(emoticon_path, index))
            else:
                msg = msg.replace(msg[pos:pos + 2],
                                  '[emoji:{}]'.format(str(num)))
            pos = msg.find('\x14')
            if pos == lastpos:
                break
        return msg

    def message(self):
        # mode=1 friend
        # mode=2 troop
        num = self.qq.encode("utf-8")
        md5num = hashlib.md5(num).hexdigest().upper()
        if self.mode == 1:
            cmd = "select msgData,senderuin,time,msgtype from mr_friend_{}_New order by time".format(
                md5num)
            self.get_friends()
        else:
            cmd = "select msgData,senderuin,time,msgtype from mr_troop_{}_New order by time".format(
                md5num)
            # print('Groups {} -> {}'.format(num, md5num))
            self.get_troop_members()

        cursors = self.fill_cursors(cmd)
        allmsg = []
        for cs in cursors:
            for row in cs:
                msgdata = row[0]
                if not msgdata:
                    continue
                uin = row[1]
                ltime = time.localtime(row[2])
                sendtime = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
                msg_type = row[3]
                msg_final = self.decrypt(msgdata, msg_type)
                if msg_final is None:
                    continue

                allmsg.append(
                    [sendtime, msg_type, self.decrypt(uin), msg_final])
        return allmsg

    def get_friends(self):
        cmd = "SELECT uin, remark FROM Friends"
        cursors = self.fill_cursors(cmd)
        for cs in cursors:
            for row in cs:
                num = self.decrypt(row[0])
                name = self.decrypt(row[1])
                self.num_to_name[num] = name

    def get_troop_members(self):
        cmd = "SELECT troopuin, memberuin, friendnick, troopnick FROM TroopMemberInfo"
        cursors = self.fill_cursors(cmd)
        for cs in cursors:
            for row in cs:
                if self.decrypt(row[0]) != self.qq:
                    continue
                num = self.decrypt(row[1])
                name = self.decrypt(row[3]) or self.decrypt(row[2])
                self.num_to_name[num] = name

    def fill_cursors(self, cmd):
        cursors = []
        # slowtable might not contain related message, so just skip it
        try:
            cursors.append(self.c2.execute(cmd))
        except:
            pass
        cursors.append(self.c1.execute(cmd))
        return cursors

    def output(self):
        name1 = "我"
        file = str(self.qq) + ".html"
        f2 = open(file, "w", encoding="utf-8")
        f2.write(
            "<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head>"
        )
        allmsg = self.message()
        f2.write("<div style='white-space: pre-line'>")
        for ts, _, uid, msg in allmsg:
            if not msg:
                continue
            if uid == str(self.qq_self):
                f2.write("<p align='right'>")
                f2.write("<font color=\"green\">")
                f2.write(ts)
                f2.write("</font>-----<font color=\"blue\"><b>")
                f2.write(name1)
                f2.write("</font></b></br>")
            else:
                f2.write("<p align='left'>")
                f2.write("<font color=\"blue\"><b>")
                f2.write(self.num_to_name.get(uid) or uid)
                f2.write("</b></font>-----<font color=\"green\">")
                f2.write(ts)
                f2.write("</font></br>")
            f2.write(self.add_emoji(msg))
            f2.write("</br></br>")
            f2.write("</p>")
        f2.write("</div>")

    def get_key(self):
        self.unify_path()
        kc_path = os.path.join(self.db_path, "files", "kc")
        kc_file = open(kc_path, "r")
        return kc_file.read()

    # unify databases path of different phones
    def unify_path(self):
        if os.path.isdir(os.path.join(self.db_path, "f")):
            os.rename(os.path.join(self.db_path, "f"),
                      os.path.join(self.db_path, "files"))
        if os.path.isdir(os.path.join(self.db_path, "db")):
            os.rename(os.path.join(self.db_path, "db"),
                      os.path.join(self.db_path, "databases"))
        if not os.path.isfile(os.path.join(self.db_path, "files", "kc")):
            raise OSError(
                "File not found. Please report your directory layout.")

    def map_new_emoji(self):
        with open('./emoticon/face_config.json', encoding='utf-8') as f:
            emojis = json.load(f)
        new_emoji_map = {}

        for e in emojis['sysface']:
            if self.emoji == 1:
                new_emoji_map[e["AQLid"]] = e["QSid"]
            else:
                if len(e["EMCode"]) == 3:
                    new_emoji_map[e["AQLid"]] = str(int(e["EMCode"]) - 100)
        return new_emoji_map

    def get_base64_from_pic(self, path):
        with open(path, "rb") as image_file:
            return (b'data:image/png;base64,' + base64.b64encode(image_file.read())).decode("utf-8")

    def decode_pic(self, data):
        try:
            doc = PicRec()
            doc.ParseFromString(data)
            url = 'chatimg:' + doc.md5
            filename = hex(crc64(url))
            filename = 'Cache_' + filename.replace('0x', '')
            rel_path = os.path.join("./chatimg/", filename[-3:], filename)
            if os.path.exists(rel_path):
                w = 'auto' if doc.uint32_thumb_width == 0 else str(
                    doc.uint32_thumb_width)
                h = 'auto' if doc.uint32_thumb_height == 0 else str(
                    doc.uint32_thumb_height)
                if self.combine_img:
                    rel_path = self.get_base64_from_pic(rel_path)
                return '<img src="{}" width="{}" height="{}" />'.format(rel_path, w, h)
        except:
            pass
        return '[图片]'

    def decode_mix_msg(self, data):
        try:
            doc = Elem()
            doc.ParseFromString(data)
            img_src = ''
            if doc.picMsg:
                img_src = self.decode_pic(doc.picMsg)
            return img_src + doc.textMsg.decode('utf-8')
        except:
            pass
        return '[混合消息]'

    def decode_share_url(self, msg):
        # TODO
        return '[分享卡片]'


def main(db_path, qq_self, qq, mode, emoji, with_img, combine_img):
    try:
        q = QQoutput(db_path, qq_self, qq, mode, emoji, with_img, combine_img)
        q.output()
    except Exception as e:
        with open('log.txt', 'w') as f:
            f.write(repr(e))
            f.write(traceback.format_exc())

        print(traceback.format_exc())
        if repr(e).split(":")[0] == "OperationalError('no such table":
            raise ValueError("信息填入错误")
        else:
            raise BaseException("Error! See log.txt")
