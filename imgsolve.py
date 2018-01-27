#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk


# http://effbot.org/zone/tkinter-autoscrollbar.htm
class AutoScrollbar(ttk.Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise(TclError, "cannot use pack with this widget")
    def place(self, **kw):
        raise(TclError, "cannot use place with this widget")


class MainWindow:

    def __init__(self, top: Tk=None):

        # top.geometry('430x170+200+200')

        # 创建菜单, tearoff=False禁止该菜单分离(为什么加进这种奇怪的功能...)
        self.Mmenubar = Menu(top)

        self.Mfile = Menu(top, tearoff=False)
        self.Mfile.add_command(command=support.openFile, label='打开')
        self.Mfile.add_command(command=support.saveAs, label='另存为')
        self.Mfile.add_separator()
        self.Mfile.add_command(command=support.exitProgram, label='退出')
        self.Mmenubar.add_cascade(menu=self.Mfile, label='文件')

        # self.Medit = Menu(top, tearoff=False)
        # self.Medit.add_command(command=support.scanQRC, label='扫描二维码')
        # self.Medit.add_command(command=support.viewHex, label='Hex视图')
        # self.Mmenubar.add_cascade(menu=self.Medit, label='编辑')

        self.Mplugins = Menu(top, tearoff=False)
        self.Mmenubar.add_cascade(menu=self.Mplugins, label='插件')

        self.Mhelp = Menu(top, tearoff=False)
        self.Mhelp.add_command(command=support.about, label='关于')
        self.Mmenubar.add_cascade(menu=self.Mhelp, label='帮助')

        # 创建提示文字-第一行
        self.Lnow = ttk.Label(top)
        self.Lnow.grid(row=0, column=1)

        self.BlastFrame = ttk.Button(top, command=lambda: support.setFrame(-1), text='上一帧')
        self.BlastFrame.grid(row=0, column=0)

        self.BnextFrame = ttk.Button(top, command=lambda: support.setFrame(1), text='下一帧')
        self.BnextFrame.grid(row=0, column=2)

        # 创建滚动画布-第二行
        self.Fpreview = ttk.Frame(top)
        self.Fpreview.grid(row=1, column=0, columnspan=4)

        self.Sright = AutoScrollbar(self.Fpreview)
        self.Sright.grid(row=0, column=1, sticky=N+S)
        self.Sbuttom = AutoScrollbar(self.Fpreview, orient=HORIZONTAL)
        self.Sbuttom.grid(row=1, column=0, sticky=E+W)

        self.Ccanvas = Canvas(self.Fpreview,
                              yscrollcommand=self.Sright.set,
                              xscrollcommand=self.Sbuttom.set)
        self.Ccanvas.grid(row=0, column=0, sticky=N+S+E+W)

        self.Sright.config(command=self.Ccanvas.yview)
        self.Sbuttom.config(command=self.Ccanvas.xview)

        # print(self.Sright.winfo_width())

        # 让画布可扩展
        self.Fpreview.grid_rowconfigure(0, weight=1)
        self.Fpreview.grid_columnconfigure(0, weight=1)

        # 创建图片预览Label
        # self.Lpreview = ttk.Label(self.Ccanvas)
        # self.Lpreview.grid(row=0, column=0)
        # NW表示左上角, 非常重要, 不然0, 0会位于图片中间(什么鬼)
        self.image = self.Ccanvas.create_image(0, 0, anchor=NW, image=None)
        # self.Ccanvas.create_window(0, 0, anchor=NW, window=self.Lpreview)
        # self.Ccanvas.update_idletasks()
        self.Ccanvas.config(scrollregion=self.Ccanvas.bbox("all"))

        # 创建前进/后退按钮-第三行
        self.Blast = ttk.Button(top, command=lambda: support.setBit(-1), text='<')
        self.Blast.grid(row=2, column=0)

        self.Bnext = ttk.Button(top, command=lambda: support.setBit(1), text='>')
        self.Bnext.grid(row=2, column=2)

        # 创建下拉菜单-第三行
        self.Cviews = ttk.Combobox(top)
        self.Cviews['values'] = support.viewnames
        self.Cviews.bind('<<ComboboxSelected>>', support.selectView)
        self.Cviews.grid(row=2, column=1)

        # top.bind("<Configure>", support.on_resize)
        self.img = None

        top.configure(menu=self.Mmenubar)


if __name__ == '__main__':
    import UI_support as support

    root = Tk()
    root.title('IMG Stego')

    top = MainWindow(root)

    support.init(root, top)

    root.mainloop()
