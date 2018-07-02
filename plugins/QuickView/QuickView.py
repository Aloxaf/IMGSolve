# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk

# TODO: PIL与tkinter都包含Image, 冲突
from PIL import Image, ImageTk

from basic.stegcore import StegImage


def init(_top):
    global top
    top = _top

def get_menus():

    return [{'type': 'command', 'command': quick_view, 'label': '快速预览'}]

class quick_viewer:

    def __init__(self, top):
        self.Fpreview = ttk.Frame(top)
        self.Fpreview.grid(row=0, column=0)

        self.Sright = ttk.Scrollbar(self.Fpreview)
        self.Sright.grid(row=0, column=1, sticky=N+S)

        self.Ccanvas = Canvas(self.Fpreview,
                              width=800,
                              height=1600,
                              yscrollcommand=self.Sright.set,
                              xscrollcommand=self.Sright.set)
        self.Ccanvas.grid(row=0, column=0, sticky=N+S+E+W)

        self.image = self.Ccanvas.create_image(0, 0, anchor=NW, image=None)

        self.Ccanvas.config(scrollregion=self.Ccanvas.bbox("all"))



def quick_view():
    global top, viewer_window

    if not top.img:
        return

    img = Image.new('L', (200 * 4, 200 * 8), 255)

    for i in range(4):
         for j in range(8):
            bit_img = top.stegimg.getbit(i * 8 + j)
            scale = min(200 / bit_img.size[0], 200 / bit_img.size[1])
            bit_img = bit_img.resize([round(scale * x) for x in bit_img.size], Image.ANTIALIAS)
            img.paste(bit_img, (200 * i, 200 * j))

    root = Toplevel()
    root.title('快速预览')

    viewer_window = quick_viewer(root)
    viewer_window.tkimg = ImageTk.PhotoImage(img)
    viewer_window.Ccanvas.itemconfig(viewer_window.image, image=viewer_window.tkimg)
    viewer_window.Ccanvas.config(scrollregion=viewer_window.Ccanvas.bbox("all"))

    root.mainloop()
