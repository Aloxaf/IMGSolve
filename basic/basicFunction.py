#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox, Tk, ttk, Text
from operator import methodcaller
import os
import sys
import tkinter
import platform

from .stegcore import StegImage
from imgsolve import MainWindow
from pyzbar import pyzbar
import imgsolve

root: Tk = None
top: MainWindow = None
stegimg: StegImage = None
nbit: int = 0
nframe: int = 0

viewnames = ["原图", "R通道", "G通道", "B通道", "Alpha通道"]
viewnames.extend(f'{c}{i}' for c in ['Alpha', 'G', 'B', 'R',] for i in range(8))

methods = [['getrawimg']]
methods.extend(['getchannel', i] for i in range(4))
methods.extend(['getbit', i] for i in range(32))

def openFile():
    global top, stegimg, nbit, nframe

    if stegimg:
        stegimg.close()

    filename = filedialog.askopenfilename(filetypes=[('任何图片', '.*')])

    if not filename:
        return

    stegimg = StegImage(filename)
    nbit = nframe = 0

    # 窗口大小调整&居中

    # 屏幕大小
    scrw = root.winfo_screenwidth()
    scrh = root.winfo_screenheight()

    # 画布的最大大小, +5防止出现微小的滚动条
    width = (round(scrw * 0.8) if stegimg.img.size[0] > round(scrw * 0.8) else stegimg.img.size[0]) + 5
    height = (round(scrh * 0.8) if stegimg.img.size[1] > round(scrh * 0.8) else stegimg.img.size[1]) + 5

    # 似乎第一次获取的top.Sright.winfo_width()是1, 干脆不获取
    size = (width + 25, height + top.Bnext.winfo_height() + 55)

    # root.update_idletasks()
    scrw = root.winfo_screenwidth()
    scrh = root.winfo_screenheight()
    x = scrw // 2 - size[0] // 2
    y = scrh // 2 - size[1] // 2
    root.geometry("%dx%d+%d+%d" % (size + (x, y)))

    # 切换提示
    top.Lnow.configure(text='原图')
    top.img = stegimg.img
    top.stegimg = stegimg

    top.tkimg = ImageTk.PhotoImage(top.img)
    # 更新图像
    top.Ccanvas.configure(width=width, height=height)

    # top.Lpreview.configure(image=top.img)
    top.Ccanvas.itemconfig(top.image, image=top.tkimg)
    # top.Ccanvas.create_rectangle(0, 0, 100, 100, outline="black", fill="red")

    # 更新完Lpreview需要执行下面这句, 否则没有滚动条
    top.Ccanvas.config(scrollregion=top.Ccanvas.bbox("all"))


def saveAs():

    if not stegimg:
        return

    filename = filedialog.asksaveasfilename(filetypes=[('PNG', '.png'), ('BMP', '.bmp'), ('JPEG', '.jpg')])

    if filename:
        top.img.save(filename)


def exitProgram():

    stegimg.close()

    root.quit()


def setBit(n):
    "取下1位/上1位, 取决于n的值"
    if not stegimg:
        return

    global nbit

    nbit += n

    if nbit >= len(viewnames) or nbit < -1 * len(viewnames):
        nbit = 0

    changeView(nbit)


def setFrame(n):
    global nframe

    if not stegimg:
        return

    nframe += n

    if stegimg.raw.format == 'GIF':
        if nframe >= len(stegimg.gif) or nframe < -1 * len(stegimg.gif):
            nframe = 0

        stegimg.setframe(nframe)
        nbit = 0
        changeView(0)


def changeView(n):
    global top

    if not stegimg:
        return

    top.Lnow.configure(text=viewnames[n])
    top.img = methodcaller(*methods[n])(stegimg)
    top.tkimg = ImageTk.PhotoImage(top.img)
    top.Ccanvas.itemconfig(top.image, image=top.tkimg)


def selectView(event):
    global top, nbit

    nbit = viewnames.index(top.Cviews.get())

    changeView(nbit)


def about():
    messagebox.showinfo(title='关于', message='IMG Solve\n图片隐写分析工具\n项目主页:\nhttps://github.com/YinTianliang/IMGSolve')


def init(_root, _top):
    global root, top
    root = _root
    top = _top

    for plugin in os.listdir(sys.path[0] + '/plugins'):
        pg = __import__('plugins.' + plugin)
        pg = getattr(pg, plugin)
        pg.init(top)

        for menu in pg.get_menus():
            if menu['type'] == 'command':
                top.Mplugins.add_command(command=menu['command'], label=menu['label'])
            elif menu['type'] == 'cascade':
                top.Mplugins.add_cascade(menu=menu['menu'], label=menu['label'])
