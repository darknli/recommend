import tkinter as tk
from show_train import show_train
from mix_recommend import mix_re


class MainPage():
    def __init__(self, window):
        self.window_main = tk.Toplevel(window, bg='pink')
        self.window_main.geometry('300x250')
        self.window_main.title('主 界 面')
        btn_train = tk.Button(self.window_main, bg='Light blue', text='训 练 模 型',
                              command=self.start_train)
        btn_train.place(x=100, y=50)
        btn_recd = tk.Button(self.window_main, bg='Light blue', text='混 合 推 荐',
                             command=self.start_recommend)
        btn_recd.place(x=100, y=120)


    def start_train(self):
        self.train_model = show_train(self.window_main)

    def start_recommend(self):
        self.recommend = mix_re(self.window_main)
    # ------------混合推荐 界面--------------#