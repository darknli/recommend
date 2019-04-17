# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 16:45:05 2019

@author: Administrator
"""

# ------------登录窗口的实现（Frame）--------------#

import matplotlib.pyplot as plt
from PIL import Image
import os
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
import pickle
from mainPage import *

# ------------登录和注册按钮--------------#
def user_login(window):
    user_name = var_user_name.get()
    user_pwd = var_user_pwd.get()

    try:
        with open('user_info.pickle', 'rb') as user_file:
            user_info = pickle.load(user_file)

    except FileNotFoundError:
        with open('user_info.pickle', 'wb') as user_file:
            user_info = {'admin': 'admin'}
            pickle.dump(user_info, user_file)

    if user_name in user_info:
        if user_pwd == user_info[user_name]:
            tk.messagebox.showinfo(title = 'Welcome', message = 'Hello ' + user_name)
            mp = MainPage(window)
            pass
        else:
            tk.messagebox.showerror(message='您输入的密码错误！请重试。')
    else:
        is_sign_up = tk.messagebox.askyesno('您还未注册，现在注册吗？')
        if is_sign_up:
            user_sign_up()


def user_sign_up():
    def sign_to_Python():
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()

        with open('user_info.pickle', 'rb') as user_file:
            exist_user_info = pickle.load(user_file)

        if np != npf:
            tk.messagebox.showerror('密码和确认密码必须一致！')
        elif nn in exist_user_info:
            tk.messagebox.showerror('此用户名已被注册过。')
        else:
            exist_user_info[nn] = np
            with open('user_info.pickle', 'wb') as user_file:
                pickle.dump(exist_user_info, user_file)
            tk.messagebox.showinfo('', message="注册成功！")
            window_sign_up.destroy()

    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('Sign up window')

    new_name = tk.StringVar()
    # new_name.set('1')
    tk.Label(window_sign_up, bg='Light blue', text='用户名:').place(x=10, y=10)
    entry_user_name = tk.Entry(window_sign_up, textvariable=new_name)
    entry_user_name.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, bg='Light blue', text='密码:').place(x=10, y=50)
    entry_user_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_user_pwd.place(x=150, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, bg='Light blue', text='确认密码:').place(x=10, y=90)
    entry_user_pwd = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_user_pwd.place(x=150, y=90)

    btn_confirm_sign_up = tk.Button(window_sign_up, text='注册', command=sign_to_Python)
    btn_confirm_sign_up.place(x=150, y=130)



if __name__ == '__main__':

    window = tk.Tk()
    window.title("登录界面")
    window.geometry('442x400')  # 此处的x是英文字母小写x，不是字符*

    # ------------加载登录界面图片（Welcome image）--------------#
    canvas = tk.Canvas(window,
                       height=200,
                       width=500)

    image_file = tk.PhotoImage(file='welcome.jpg')  # 加载图片失败
    canvas.create_image(0, 0, anchor='nw', image=image_file)
    canvas.pack(side='top')

    # ------------登录界面的用户和密码信息--------------#
    tk.Label(window, bg='Light blue', text='用户名：').place(x=50, y=200)
    tk.Label(window, bg='Light blue', text='密码：').place(x=50, y=240)

    # ------------用于用户名输入的文本框--------------#
    var_user_name = tk.StringVar()
    var_user_name.set('darkn')

    entry_user_name = tk.Entry(window, textvariable=var_user_name)
    entry_user_name.place(x=160, y=200)

    # ------------用于密码输入的文本框--------------#
    var_user_pwd = tk.StringVar()
    var_user_pwd.set('1')
    entry_user_pwd = tk.Entry(window, textvariable=var_user_pwd, show='*')
    entry_user_pwd.place(x=160, y=240)

    btn_login = tk.Button(window, text='登 录', command=lambda :user_login(window))
    btn_login.place(x=170, y=280)

    btn_sign_up = tk.Button(window, text='注 册', command=user_sign_up)
    btn_sign_up.place(x=230, y=280)
    window.mainloop()




# ------------加载登录界面图片（Welcome image）--------------#


