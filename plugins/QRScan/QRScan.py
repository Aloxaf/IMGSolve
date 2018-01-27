# -*- coding: utf-8 -*-

from pyzbar import pyzbar
from PIL import Image, ImageDraw
from tkinter import Menu

from basicWindow import ReadOnlyText

try:
    from plugins.QRScan.Cdenoise import denoise
except ImportError:
    from plugins.QRScan.denoise import denoise

def init(_top):
    global top
    top = _top


def get_menus():

    global menu

    menu = Menu(tearoff=False)
    menu.add_command(command=lambda: scan(True), label='扫描全图')
    menu.add_command(command=lambda: scan(False), label='扫描指定区域(更准确)')

    return [{'type': 'cascade', 'menu': menu, 'label': '扫描二维码'}]


def scan(scan_whole):
    """扫描二维码, scan_whole决定是否扫描整张图片"""
    global top

    if not top.img:
        return

    rect = []
    select = None

    # 实现框选效果
    def start_select(event):
        nonlocal rect, select
        # print(event)
        select = top.Ccanvas.create_rectangle(event.x, event.y, event.x, event.y)
        rect.extend((event.x, event.y))

    def mouse_move(event):
        # print(event)
        top.Ccanvas.coords(select, rect[0], rect[1], event.x, event.y)
        pass

    def end_select(event):
        nonlocal rect

        top.Ccanvas.delete(select)
        top.Ccanvas.configure(cursor='left_ptr')
        top.Ccanvas.unbind('<B1-Motion>')
        top.Ccanvas.unbind('<Button-1>')
        top.Ccanvas.unbind('<ButtonRelease-1>')

        img = top.img

        # rect.extend((event.x, event.y))

        # 调整截图区域大小, 截到外面
        rect.append(
            (event.x if event.x > 0 else 0) if event.x < img.size[0] else img.size[0]
        )
        rect.append(
            (event.y if event.y > 0 else 0) if event.y < img.size[1] else img.size[1]
        )

        # 排序以保证左上角坐标在前面
        rect.sort()

        img = img.crop(rect)

        decode(img)

    def decode(img):
        # 用新的白底画布存放二维码来提高识别率
        qr_code = Image.new("L", (img.size[0] + 60, img.size[1] + 60), (255,))
        qr_code.paste(img, (30, 30))

        # 调用pyzbar识别二维码, 不成功则降噪再识别
        # 这个地方cython版的速度大概是python版的30+倍
        data = pyzbar.decode(qr_code)
        if len(data) == 0:

            # 降噪
            qr_code_dn = denoise(qr_code, 50, 4, 1)
            # qr_code.save('02.png')
            data = pyzbar.decode(qr_code_dn)

            # 如果还没成功, 就减少黑色杂色后再识别
            if len(data) == 0:
                # 减少黑色杂色
                qr_code = denoise(qr_code, 50, 4, 1, 0)
                # qr_code.save('01.png')

                # 降噪
                qr_code = denoise(qr_code, 50, 4, 1)
                # qr_code.save('02.png')
                data = pyzbar.decode(qr_code)


        result = ['{}\t{}\n'.format(x.type, x.data) for x in data]

        # 显示结果
        ReadOnlyText('扫描结果', ''.join(result))

    if scan_whole:
        decode(top.img)
    else:
        top.Ccanvas.configure(cursor='cross')
        top.Ccanvas.bind('<B1-Motion>', mouse_move)
        top.Ccanvas.bind('<Button-1>', start_select)
        top.Ccanvas.bind('<ButtonRelease-1>', end_select)
