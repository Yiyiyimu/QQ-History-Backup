from _overlapped import NULL
import hashlib
import sqlite3
import time


class QQoutput():
    def __init__(self,db,key):
        self.key=key    #解密用的密钥
        self.c=sqlite3.connect(db).cursor()
        
    def fix(self,data,mode):
        #msgdata mode=0
        #other mode=1
        if(mode==0):
            rowbyte=[]
            for i in range(0,len(data)):
                rowbyte.append(data[i]^ord(self.key[i%len(self.key)]))
            rowbyte=bytes(rowbyte)
            try:
                msg=rowbyte.decode(encoding='utf-8')
            except:
                msg=NULL
            return msg
        elif(mode==1):
            str=''
            try:
                for i in range(0,len(data)):
                    str+=chr(ord(data[i])^ord(self.key[i%len(self.key)]))
            except:
                str=NULL
            return str         
    
    def message(self,num):
        num=str(num).encode('utf-8')
        md5num=hashlib.md5(num).hexdigest().upper()
        execute="select msgData,senderuin,time from mr_friend_{md5num}_New".format(md5num=md5num)
        cursor = self.c.execute(execute)
        allmsg=[]
        for row in cursor:
            msgdata= row[0]
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
            
    def output(self,num):
        file=str(num)+".html"
        f2 = open(file,'w',encoding="utf-8")
        f2.write("<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head>")
        allmsg=self.message(num)
        for msg in allmsg:
            try:
                f2.write("<font color=\"blue\">")
                f2.write(msg[0])
                f2.write("</font>-----<font color=\"green\">")
                f2.write(msg[1])
                f2.write("</font></br>")
                f2.write(msg[2])
                f2.write("</br></br>")               
            except:
                pass    
   
