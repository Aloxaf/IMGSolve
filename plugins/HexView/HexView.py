# -*- coding: utf-8 -*-


from basicWindow import ReadOnlyText


def init(_top):
    global top

    top = _top


def get_menus():
    return [{'type': 'command', 'command': view_hex, 'label': 'Hex视图'}]


def view_hex():
    global top

    if not top.img:
        return

    img = top.img

    text = hex_dump(img.tobytes())

    ReadOnlyText('Hex View', text)


# https://gist.github.com/sbz/1080258
def hex_dump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in range(0, len(src), length):
        chars = src[c:c + length]
        hexs = ' '.join(["{:0>2X}".format(x) for x in chars])
        printable = ''.join(["{}".format((x <= 127 and FILTER[x]) or '.') for x in chars])
        lines.append("{:0>8X}:  {:<{}}  |{}|\n".format(c, hexs, length*3, printable))
    return ''.join(lines)
