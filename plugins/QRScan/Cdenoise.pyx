#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cpython cimport array
# import array

cdef array.array pixels
cdef int G, N, ignore, width, height


# 二值化的降噪
cdef int denoise_pixel(int x, int y):
    cdef bint L
    cdef int nearDots, _x, _y

    L = True if pixels.data.as_ints[x * width + y] > G else False

    # 因为这个地方的遍历包括了自身, which一定是True, 所以nearDots = -1来保证结果正确
    nearDots = -1
    for _x in range(x - 1, x + 2):
        for _y in range(y - 1, y + 2):
            if L == (pixels.data.as_ints[_x * width + _y] > G):
                nearDots += 1

    # TODO: 这个地方直接返回上一个像素感觉不妥
    return pixels.data.as_ints[x * width + y - 1] if nearDots < N else ignore


# 参考了http://dream-people.iteye.com/blog/379064
# G 二值化阈值
# N 降噪率
# Z 降噪次数
# 由于最低位通常都是充满了噪点, 而二维码理想的识别环境是白色
# 通过调整ignore=0可以强行忽略白色噪点, 纯化背景, 但这样就无法起到降噪作用
def denoise(img, int _G, int _N, int Z, int _ignore=-1):
    global pixels, G, N, ignore, width, height
    G = _G
    N = _N
    ignore = _ignore

    cdef int i, x, y, color

    width, height = img.size

    pixels = array.array('i', list(img.getdata()))

    new_img = img.copy()


    for i in range(0, Z):
        for x in range(1, height - 1):
            for y in range(1, width - 1):
                color = denoise_pixel(x, y)
                if color != ignore:
                    pixels.data.as_ints[x * width + y] = color


    new_img.putdata(list(pixels))

    return new_img
