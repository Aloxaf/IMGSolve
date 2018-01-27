# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
import platform


def ReadOnlyText(title, text):

    root = Tk()
    root.title(title)

    if platform.system() == 'Linux':
        font = ('Droid Sans Mono', 10)
    else:
        font = ('Consolas', 10)

    # self.title('扫描结果')

    root.text = Text(root, font=font)
    root.text.insert(END, ''.join(text))

    root.scbar = ttk.Scrollbar(root, command=root.text.yview)
    root.text.configure(yscrollcommand=root.scbar.set)
    root.scbar.pack(side=RIGHT, fill=Y)

    root.text.pack(side=LEFT, fill=BOTH)
    root.mainloop()

