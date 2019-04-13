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
    def Mix_recd(self):
        window_recd = tk.Toplevel(self.window_main, bg='Light blue')
        window_recd.geometry('300x250')
        window_recd.title('混 合 推 荐')

        def recds_1():
            recd_1 = filedialog.askopenfilename(title=u'选择文件',
                                                #                                          initialdir=(os.path.expanduser(default_dir)),
                                                filetypes=[('', '*.py'), ('All Files', '*')])
            tk.messagebox.showinfo('运行', message='开始计算')
            recd_1_out = os.popen('python ' + str(recd_1))
            result = open('result.txt', 'w')
            result.write(recd_1_out.read())
            result.close()
            tk.messagebox.showinfo('完成', message='完成推荐！')

        def Result_recd():
            l_recd = tk.Label(window_recd,
                              text='推荐结果',
                              bg='white',
                              width=12)
            l_recd.pack()
            var_recd = tk.StringVar()
            #            str_temp = ''
            #            with open('result.txt', 'r') as show:
            #                 for line in show:
            #                     str_temp =  str_temp + line
            str_out = ['物品  评分', '203  4.99', '44  4.74', '931  4.60', '711  4.58',
                       '1033  4.57', '192  4.57', '200  4.51', '505  5.43', '776  5.12', '854  5.08']
            var_recd.set(str_out)
            lb_recd = tk.Listbox(window_recd,
                                 listvariable=var_recd)
            lb_recd.pack()

        recd_alg_1 = tk.Button(window_recd, bg='Light blue',
                               text='执 行 推 荐 算 法',
                               command=recds_1)
        recd_alg_1.place(x=100, y=50)

        recd_result = tk.Button(window_recd, bg='Light blue',
                                text='显 示 推 荐 结 果',
                                command=Result_recd)
        recd_result.place(x=100, y=120)

