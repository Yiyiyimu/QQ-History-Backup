import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from icon import ico, github_mark
import base64
import QQ_History
import os
import webbrowser


def Enter():
    dir, qq_self, qq = e1.get(), e2.get(), e3.get()
    group = 1 if e4.get() == '私聊' else 2
    if (dir == "" or qq_self == "" or qq == ""):
        info.set("信息不完整！")
        return ()
    info.set("开始导出")
    try:
        QQ_History.main(dir, qq_self, qq, group)
    except Exception as e:
        info.set(repr(e))
        return ()


def SelectPath():
    dir = filedialog.askdirectory()
    pathGet.set(dir)


def url():
    webbrowser.open_new("https://github.com/Yiyiyimu/QQ_History_Backup")


root = tk.Tk()
pathGet, keyGet, info = tk.StringVar(), tk.StringVar(), tk.StringVar()

tmp = open("tmp.ico", "wb+")
tmp.write(base64.b64decode(ico))
tmp.close()
root.iconbitmap("tmp.ico")
os.remove("tmp.ico")

root.title("QQ聊天记录导出")

ttk.Label(root, text="*com.tencent.mobileqq：").grid(row=0, column=0, sticky="e")
e1 = ttk.Entry(root, textvariable=pathGet)
e1.grid(row=0, column=1)
ttk.Button(root, text="选择", command=SelectPath, width=5).grid(row=0, column=3)

ttk.Label(root, text="*自己QQ号：").grid(row=1, column=0, sticky="e")
e2 = ttk.Entry(root)
e2.grid(row=1, column=1, columnspan=3, sticky="ew", pady=3)

ttk.Label(root, text="*QQ号/群号：").grid(row=2, column=0, sticky="e")
e3 = ttk.Entry(root)
e3.grid(row=2, column=1, columnspan=3, sticky="ew", pady=3)

ttk.Label(root, text="私聊/群聊：").grid(row=3, column=0, sticky="e")
e4 = ttk.Combobox(root)
e4['values'] = ('私聊', '群聊')
e4.current(0)
e4.grid(row=3, column=1, columnspan=3, sticky="ew", pady=3)

root.grid_columnconfigure(2, weight=1)

ttk.Button(root, text="确认", command=Enter).grid(row=4, column=1)
l1 = ttk.Label(root, textvariable=info)
l1.grid(row=4, column=1)

tmp = open("tmp.png", "wb+")
tmp.write(base64.b64decode(github_mark))
tmp.close()
github = tk.PhotoImage(file='tmp.png')
os.remove("tmp.png")

button_img = tk.Button(root, image=github, text='b', command=url, bd=0)
button_img.grid(row=6, rowspan=7, column=0, sticky="ws")

root.mainloop()

# pyinstaller -F -w -i icon.ico GUI.py
