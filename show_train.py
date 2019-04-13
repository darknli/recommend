import tkinter as tk
from text import get_text

class show_train():
    def __init__(self, window):
        self.window_train = tk.Toplevel(window, bg='pink')
        self.window_train.geometry('300x250')
        self.window_train.title('主 界 面')
        btn_tag = tk.Button(self.window_train, bg='Light blue',
                              text='打 开 算 法 1',
                              command=self.tag_LFM)
        btn_tag.place(x=100, y=50)

        btn_prob = tk.Button(self.window_train, bg='Light blue',
                              text='打 开 算 法 2',
                              command=self.prob_FM)
        btn_prob.place(x=100, y=100)

        btn_cs = tk.Button(self.window_train, bg='Light blue',
                              text='打 开 算 法 3',
                              command=self.coldstart)
        btn_cs.place(x=100, y=150)

    def tag_LFM(self):
        from tag_LFM import RLTMF
        self.show_info = tk.Toplevel(self.window_train)
        self.show_info.geometry('300x250')
        self.show_info.title('训 练')
        text = get_text(self.show_info, 100, 10, (200, 200))
        text.insert('insert', '    算法1 训练信息\n')
        text.update()
        text.pack()
        self.model = RLTMF(40)
        self.model.InitList_movielens('jester_ratings.csv')
        for epoch_info in self.model.fit():
            text.insert('insert', epoch_info)
            text.update()

    def prob_FM(self):
        from prob_lfm import BLFM
        self.show_info = tk.Toplevel(self.window_train)
        self.show_info.geometry('300x250')
        self.show_info.title('训 练')
        text = get_text(self.show_info, 100, 10, (200, 200))
        text.insert('insert', '    算法2 训练信息\n')
        text.update()
        text.pack()
        model = BLFM('jester_ratings.csv', 25)
        for epoch_info in model.fit():
            text.insert('insert', epoch_info)
            text.update()

    def coldstart(self):
        from cold_net import Data_coldStart, cold_model
        self.show_info = tk.Toplevel(self.window_train)
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
            text.insert('insert', epoch_info)
            text.update()


