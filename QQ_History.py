from _overlapped import NULL
import hashlib
import sqlite3
import time
import traceback

class QQoutput():
    def __init__(self,db,key,mode,s):
        self.key=key    #解密用的密钥
        self.c=sqlite3.connect(db).cursor()
        self.mode=mode
        self.s=s
        
    def fix(self,data,mode):
        #msgdata mode=0
        #other mode=1
        if(mode==0):
            rowbyte=[]
            for i in range(0,len(data)):
                rowbyte.append(data[i]^ord(self.key[i%len(self.key)]))
            rowbyte=bytes(rowbyte)
            try:
                msg=rowbyte.decode(encoding="utf-8")
            except:
                msg=NULL
            return msg
        elif(mode==1):
            str=""
            try:
                for i in range(0,len(data)):
                    str+=chr(ord(data[i])^ord(self.key[i%len(self.key)]))
            except:
                str=NULL
            return str
    def decode(self, cursor):
        for row in cursor:
            continue
        data = row[0]
        MsgEnc = self.s.encode(encoding="utf-8")
        KeySet = ""
        #for i in range(0,min(len(MsgEnc), len(data))):
        for i in range(0,len(MsgEnc)):
            KeySet+=chr(data[i]^MsgEnc[i])
        #TO AVOID LOOP
        RealKey, restKey = "", ""
        for i in range(4, len(KeySet)):
            '''
            bug WARNING!!
            Assuming Key should be longer than 5 digits
            To Prevent string loop in single key
            Like "121212456"
            '''
            RealKey, nextKey, restKey = KeySet[0:i], KeySet[i:2*i], KeySet[2*i:len(KeySet)]
            KeyLen = len(RealKey)
            flagLoop = True
            for j in range(KeyLen):
                if((j < len(nextKey) and RealKey[j] != nextKey[j]) or (j < len(restKey) and RealKey[j] != restKey[j])):
                    flagLoop = False
                    break
            if(flagLoop and j == KeyLen-1):
                break
        return RealKey
    def AddEmoji(self, msg):
        pos = msg.find('\x14')
        while(pos != -1):
            lastpos = pos
            num = ord(msg[pos+1])
            msg = msg.replace(msg[pos:pos+2], "<img src='./gif/"+str(num)+".gif' alt="+str(num)+">")
            pos = msg.find('\x14')
            if(pos == lastpos):
                break
        return msg
    def message(self,num,mode):
        #mode=1 friend
        #mode=2 troop
        num=str(num).encode("utf-8")
        md5num=hashlib.md5(num).hexdigest().upper()
        if(mode==1):
            execute="select msgData,senderuin,time from mr_friend_{md5num}_New".format(md5num=md5num)
        elif(mode==2):
            execute="select msgData,senderuin,time from mr_troop_{md5num}_New".format(md5num=md5num)
        else:
            print("error mode")
            exit(1)
        #try:
        cursor = self.c.execute(execute)
        #except:
        #    raise ValueError("QQ号/db地址错误")
        if(self.key == "" and len(self.s)>=5):
            self.key = self.decode(cursor)
        cursor = self.c.execute(execute)
        allmsg=[]
        for row in cursor:
            msgdata= row[0]
            if(not msgdata):
                continue
            uin=row[1]
            ltime=time.localtime(row[2])
            
            sendtime=time.strftime("%Y-%m-%d %H:%M:%S",ltime)
            msg=self.fix(msgdata,0)
            senderuin=self.fix(uin, 1)
            
            amsg=[]
            amsg.append(sendtime)
            amsg.append(senderuin)
            amsg.append(msg)
            allmsg.append(amsg)
        return allmsg    
    def output(self,num,mode,n1,n2):
        first = str(num)[0]
        name1 = n1 if n1 != "" else "我"
        name2 = n2 if n2 != "" else str(num)
        file=str(num)+".html"
        f2 = open(file,"w",encoding="utf-8")
        f2.write("<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head>")
        allmsg=self.message(num,mode)
        f2.write("<div style='white-space: pre-line'>")
        for msg in allmsg:
            try:
                if(msg[1][0]==first):
                    f2.write("<p align='left'>")
                    f2.write("<font color=\"blue\"><b>")
                    f2.write(name2)
                    f2.write("</b></font>-----<font color=\"green\">")
                    f2.write(msg[0])
                    f2.write("</font></br>")
                else:
                    f2.write("<p align='right'>")
                    f2.write("<font color=\"green\">")
                    f2.write(msg[0])                    
                    f2.write("</font>-----<font color=\"blue\"><b>")
                    f2.write(name1)
                    f2.write("</font></b></br>")
                f2.write(self.AddEmoji(msg[2]))
                f2.write("</br></br>")
                f2.write("</p>")               
            except:
                pass
        f2.write("</div>")
        return self.key

def main(db, qq, key, msg, n1, n2):
    try:
        mode = 1
        q=QQoutput(db,key,mode,msg)
        return q.output(qq, mode, n1, n2)
    except Exception as e:
        with open('log.txt', 'w') as f:
            f.write(str(e))
            f.write(traceback.format_exc())

        err_info = repr(e).split(":")[0] == "OperationalError('no such table"
        print(err_info)
        print(repr(e).split(":")[0])
        if(err_info):
            raise ValueError("QQ号/db地址错误")
'''
db = "C:/Users/30857/Desktop/QQ_History/slowtable_2289785930.db"
qq = "1962662168"
key = "02:00:00:00:00:00"
msg = "不用回这条消息"
main(db, qq, key, msg, "", "")
'''