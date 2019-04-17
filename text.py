import tkinter
import time
# wuya = tkinter.Tk()
# wuya.title("wuya")
# wuya.geometry("1000x900+100+200")

def get_text(father_form, width, height, place):
    # 创建滚动条
    # scroll = tkinter.Scrollbar()
    # 创建文本框text，设置宽度100，high不是高度，是文本显示的行数设置为3行
    text = tkinter.Text(father_form, width=width, height=height)
    text.place(x=place[0], y=place[1])
    # 将滚动条填充
    # scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y) # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
    text.pack(side=tkinter.LEFT,fill=tkinter.Y) # 将文本框填充进wuya窗口的左侧，
    # 将滚动条与文本框关联
    # scroll.config(command=text.yview) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
    # text.config(yscrollcommand=scroll.set) # 将滚动条关联到文本框
    return text

# def generator():
#     for i in range(10000000):
#         yield i
# text = get_text(wuya, 1000, 10, (0, 0))
# # for i in generator():
# #     text.insert('insert', '%d\n'%i)
# #     text.update()
# #     wuya.after(10)
# wuya.mainloop()
