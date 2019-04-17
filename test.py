from PIL import Image,ImageTk
import tkinter as tk

# 简单插入显示
def show_jpg():
    root = tk.Tk()
    im=Image.open("train.jpg")
    img=ImageTk.PhotoImage(im)
    tk.Label(root,image=img).pack()
    root.mainloop()

if __name__ == '__main__':
    show_jpg()
