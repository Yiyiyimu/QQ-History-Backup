import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from icon import ico, github_mark
import base64
import QQ_History
import os
import webbrowser


def Enter():
    db_path, qq_self, qq, img_path = e1.get(), e2.get(), e3.get(), e6.get()
    group = 1 if e4.get() == '私聊' else 2
    emoji = 1 if e5.get() == '新' else 2
    if (db_path == "" or qq_self == "" or qq == ""):
        info.set("信息不完整！")
        return ()
    info.set("开始导出")
    try:
        QQ_History.main(db_path, qq_self, qq, group, emoji, img_path)
        info.set("完成")
    except Exception as e:
        info.set(repr(e))
    return ()


def SelectDBPath():
    dir = filedialog.askdirectory()
    db_path_get.set(dir)


def SelectImgPath():
    dir = filedialog.askdirectory()
    img_path_get.set(dir)


def url():
    webbrowser.open_new("https://github.com/Yiyiyimu/QQ_History_Backup")


root = tk.Tk()
db_path_get, img_path_get, key_get, info = tk.StringVar(
), tk.StringVar(), tk.StringVar(), tk.StringVar()

tmp = open("tmp.ico", "wb+")
tmp.write(base64.b64decode(ico))
tmp.close()
root.iconbitmap("tmp.ico")
os.remove("tmp.ico")

root.title("QQ聊天记录导出")

ttk.Label(root, text="*com.tencent.mobileqq：").grid(row=0, column=0, sticky="e")
e1 = ttk.Entry(root, textvariable=db_path_get)
e1.grid(row=0, column=1, columnspan=2, sticky="ew", pady=3)
ttk.Button(root, text="选择", command=SelectDBPath,
           width=5).grid(row=0, column=3)

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

ttk.Label(root, text="表情版本：").grid(row=4, column=0, sticky="e")
e5 = ttk.Combobox(root)
e5['values'] = ('新', '旧')
e5.current(0)
e5.grid(row=4, column=1, columnspan=3, sticky="ew", pady=3)

ttk.Label(root, text="chatimg：").grid(row=5, column=0, sticky="e")
e6 = ttk.Entry(root, textvariable=img_path_get)
e6.grid(row=5, column=1, columnspan=2, sticky="ew", pady=3)
ttk.Button(root, text="选择", command=SelectImgPath,
           width=5).grid(row=5, column=3)

root.grid_columnconfigure(2, weight=1)
info.set("开始")
ttk.Button(root, textvariable=info, command=Enter).grid(row=6, column=1)

tmp = open("tmp.png", "wb+")
tmp.write(base64.b64decode(github_mark))
tmp.close()
github = tk.PhotoImage(file='tmp.png')
os.remove("tmp.png")

button_img = tk.Button(root, image=github, text='b', command=url, bd=0)
button_img.grid(row=6, rowspan=7, column=0, sticky="ws")

root.mainloop()
