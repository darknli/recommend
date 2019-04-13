import tkinter as tk
from text import get_text
from tqdm import tqdm

class mix_re():
    def __init__(self, window):
        self.mix_recommend = tk.Toplevel(window, bg='pink')
        self.mix_recommend.geometry('300x600')
        self.mix_recommend.title('混合推荐')

        show_user = tk.Button(self.mix_recommend, bg='Light blue', text='显示所有用户',
                              command=self.show_users)
        show_user.place(x=100, y=20)


        tk.Label(self.mix_recommend, bg='Light blue', text='用户名：').place(x=20, y=100)

        var_user_name = tk.StringVar()
        entry_user_name = tk.Entry(self.mix_recommend, textvariable=var_user_name)
        entry_user_name.place(x=80, y=100)

        to_rec = tk.Button(self.mix_recommend, text='进行推荐', command=self.wind)
        to_rec.place(x=80, y=150)
        self.data = []
        self.users = set()
        self.items = set()
        self.read_data('ratings.dat')

    def read_data(self, filename):
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
                # if fields[0] not in self.users:
                #     self.users.append(fields[0])
                # if fields[1] not in self.items:
                #     self.items.append(fields[1])
                self.data.append(fields[:3])
                pbar.update(1)
            pbar.close()
        self.users = sorted(self.users)
        self.items = sorted(self.items)

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

    def wind(self):
        pass

