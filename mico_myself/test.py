import os
import time
import re
import tkinter as tk

window =tk.Tk()
window.title("my window")
window.geometry('300x500')

var = tk.StringVar()
l=tk.Label(window,textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
l.pack()

on_hit = False
def hit_me():
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set('you hit me')
    else:
        on_hit = False
        var.set('')

b = tk.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, command=hit_me)
b.pack()
e = tk.Entry(window, show=None, font=('Arial', 14))   # 显示成密文形式
e.pack()

def insert_point():  # 在鼠标焦点处插入输入内容
    var = e.get()
    t.insert('insert', var)


def insert_end():  # 在文本框内容最后接着插入输入内容
    var = e.get()
    t.insert('end', var)


# 第6步，创建并放置两个按钮分别触发两种情况
b1 = tk.Button(window, text='insert point', width=10,height=2, command=insert_point)
b1.pack()
b2 = tk.Button(window, text='insert end', width=10,height=2, command=insert_end)
b2.pack()

# 第7步，创建并放置一个多行文本框text用以显示，指定height=3为文本框是三个字符高度
t = tk.Text(window, height=3)
t.pack()



window.mainloop()