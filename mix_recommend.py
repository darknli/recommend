import tkinter as tk
from text import get_text
from tqdm import tqdm
from tag_LFM import RLTMF
class mix_re():
    def __init__(self, window):
        self.data = []
        self.users = set()
        self.items = set()
        self.flag = True

        self.read_data('ratings.dat')
        self.load_model()
        self.mix_recommend = tk.Toplevel(window, bg='pink')
        self.mix_recommend.geometry('300x300')
        self.mix_recommend.title('混合推荐')

        show_user = tk.Button(self.mix_recommend, bg='Light blue', text='显示所有用户',
                              command=self.show_users)
        show_user.place(x=100, y=20)

        tk.Label(self.mix_recommend, bg='Light blue', text='推荐长度：').place(x=20, y=60)
        int_n = tk.IntVar()
        int_n.set(10)
        self.recommend_n = tk.Entry(self.mix_recommend, textvariable=int_n)
        self.recommend_n.place(x=80, y=60)

        tk.Label(self.mix_recommend, bg='Light blue', text='用户名：').place(x=20, y=100)
        var_user_name = tk.StringVar()
        self.entry_user_name = tk.Entry(self.mix_recommend, textvariable=var_user_name)
        self.entry_user_name.place(x=80, y=100)

        to_rec = tk.Button(self.mix_recommend, text='进行推荐', command=self.push_top_N)
        to_rec.place(x=80, y=150)

    def read_data(self, filename):
        # with open(filename) as f:
        #     pstr = f.read()
        #     self.test = eval(pstr)
        with open(filename) as f:
            token = ','
            if '.dat' in filename:
                token = '::'
            lines = f.readlines()[1:]
            pbar = tqdm(total=len(lines))
            for line in lines:
                fields = line.strip().split(token)
                # print(fields)
                self.users.add(fields[0])
                self.items.add(fields[1])
                self.data.append(fields[:3])
                pbar.update(1)
            pbar.close()
        self.users = sorted(self.users)
        self.items = sorted(self.items)
        tk.messagebox.showinfo('提示', message='数据读取成功')


    def load_model(self):
        self.model = RLTMF(10, 10)
        self.model.ReadModel(setTrain=True)
        # self.model.setEvalPara(10)
        tk.messagebox.showinfo('提示', message='模型加载完毕')

    def show_users(self):
        self.all_user = tk.Toplevel(self.mix_recommend, bg='pink')
        self.all_user.geometry('600x600')
        self.all_user.title('所有用户')
        self.text = get_text(self.all_user, 200, 100, (200, 200))
        self.text.insert('insert', '    用户列表\n')
        self.text.update()
        self.text.pack()
        num_users = len(self.users)
        for index in range(0, num_users, 10):
            self.text.insert('insert', ' '.join(['%6s' % user for user in self.users[index:index+8]])+'\n')
            self.text.update()

    def push_top_N(self):
        user = self.entry_user_name.get()
        top_n = self.recommend_n.get()
        try:
            top_n = int(top_n)
        except BaseException:
            tk.messagebox.showinfo('错误', message='输入列表长度必须是数字格式!')
            return
        if top_n > 100:
            tk.messagebox.showinfo('错误', message='推荐列表长度设置过大!')
            return
        self.model.setEvalPara(int(top_n))
        # if not self.flag:
        #     self.text.pack_forget()
        rec_list = self.model.TopN(user, choice="RATING")
        if rec_list is None:
            tk.messagebox.showinfo('错误', message='系统中没有该用户id，请查看【所有用户】!')
            return
        push_win = tk.Toplevel(self.mix_recommend, bg='pink')
        push_win.geometry('200x400')
        push_win.title('所有用户')
        text = get_text(push_win, 200, 100, (200, 400))
        text.insert('insert', '%s %s %s\n' % ('行号', '物品id', '预测评分'))
        text.insert('insert', '\n'.join(['%3d %7s  %.3f'%(i, item, rating) for i, (item, rating) in enumerate(rec_list)]))