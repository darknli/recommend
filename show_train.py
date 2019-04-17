import tkinter as tk
from text import get_text
import threading
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


class show_train():
    def __init__(self, window):
        self.window_train = tk.Toplevel(window, bg='pink')
        self.window_train.geometry('300x250')
        self.window_train.title('训 练 界 面')
        btn_tag = tk.Button(self.window_train, bg='Light blue',
                              text='训 练 模 型 1',
                              command=lambda :self.run(self.tag_LFM, "算法1"))
        btn_tag.place(x=100, y=50)

        btn_prob = tk.Button(self.window_train, bg='Light blue',
                              text='训 练 模 型 2',
                              command=lambda :self.run(self.prob_FM, "算法2"))
        btn_prob.place(x=100, y=100)

        btn_cs = tk.Button(self.window_train, bg='Light blue',
                              text='训 练 模 型 3',
                              command=lambda :self.run(self.coldstart, "算法1"))
        btn_cs.place(x=100, y=150)

    def run(self, function, name="算法"):
        train = threading.Thread(target=function, name=name)
        train.start()

    def tag_LFM(self):
        from tag_LFM import RLTMF
        tk.messagebox.showinfo('提示', message='已选择算法1进行训练！')
        self.show_info =  tk.Toplevel(self.window_train, bg='pink')
        self.show_info.geometry('300x250')
        self.show_info.title('训 练')
        text = get_text(self.show_info, 100, 10, (200, 200))
        text.insert('insert', '    算法1 训练信息\n')
        text.update()
        text.pack()
        model = RLTMF(2, 2)
        model.InitList_movielens('jester_ratings.csv')
        x = []
        y = []
        for epoch_info in model.fit():
            if not isinstance(epoch_info, tuple):
                text.insert('insert', epoch_info)
                break
            x.append(epoch_info[0])
            y.append(epoch_info[1])
            text.insert('insert', " %3d epoch :MAE is %f\n" % epoch_info)
            text.update()
        model.setEvalPara(10)
        cover = model.Coverage()
        pre_rec = model.PrecisionRecall()

        diver = model.Diversity()

        tk.messagebox.showinfo('模型性能评测', cover+pre_rec+diver)
        plt.plot(x,y)
        plt.savefig('train.jpg')
        self.plot_train()

    def prob_FM(self):
        from prob_lfm import BLFM
        tk.messagebox.showinfo('提示', message='已选择算法2进行训练！')
        self.show_info =  tk.Toplevel(self.window_train, bg='pink')
        self.show_info.geometry('300x250')
        self.show_info.title('训 练')
        text = get_text(self.show_info, 100, 10, (200, 200))
        text.insert('insert', '    算法2 训练信息\n')
        text.update()
        text.pack()
        model = BLFM('jester_ratings.csv', 25)
        for epoch_info in model.fit():
            text.insert('insert', " %3d epoch :MAE is %f\n" % epoch_info)
            text.update()
        self.plot_train()

    def coldstart(self):
        from cold_net import Data_coldStart, cold_model
        tk.messagebox.showinfo('提示', message='已选择算法3进行训练！')
        self.show_info = tk.Toplevel(self.window_train, bg='pink')
        self.show_info.geometry('300x250')
        self.show_info.title('训 练')
        text = get_text(self.show_info, 100, 10, (200, 200))
        text.insert('insert', '    算法2 训练信息\n')
        text.update()
        text.pack()

        datapath = r'C:\Users\Darkn\python\recommender\hetrec2011-movielens-2k-v2'
        dim = 10
        data = Data_coldStart()
        data.get_actor(datapath + r'\movie_actors.dat', weight=20)
        data.get_country(datapath + r'\movie_countries.dat')
        data.get_director(datapath + r'\movie_directors.dat')
        data.get_genres(datapath + r'\movie_genres.dat', weight=30)
        # data.get_data(DATAPATH + r'\user_ratedmovies.dat')
        data.read_data()
        actor_num, country_num, director_num, genre_num = data.size()
        CM = cold_model(actor_num, country_num, director_num, genre_num, data.train.users, dim)
        for epoch_info in CM.fit(30, data):
            text.insert('insert', " %3d epoch :MAE is %f\n" % epoch_info)
            text.update()
        self.plot_train()


    def plot_train(self):
        win_img = tk.Toplevel(self.window_train)
        win_img.title('迭代折线图')
        img = Image.open('train.jpg')
        img = ImageTk.PhotoImage(img)
        tk.Label(win_img, image=img).pack()
