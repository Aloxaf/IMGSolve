#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 参考了http://dream-people.iteye.com/blog/379064
# G 二值化阈值
# N 降噪率
# Z 降噪次数
# 由于最低位通常都是充满了噪点, 而二维码理想的识别环境是白色
# 通过调整ignore=0可以强行忽略白色噪点, 纯化背景, 但这样就无法起到降噪作用
def denoise(img, G, N, Z, ignore=-1):

    # 聪明的方法
    # https://stackoverflow.com/questions/1109422/getting-list-of-pixel-values-from-pil
    pixels = list(img.getdata())
    width, height = img.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    new_pixels = pixels[:]
    new_img = img.copy()

    # 二值化的降噪
    def denoise_pixel(x, y):
        # print(x, y, len(pixels), len(pixels[0]))
        L = pixels[x][y]

        L = True if L > G else False

        # 因为这个地方的遍历包括了自身, which一定是True, 所以nearDots = -1来保证结果正确
        nearDots = -1
        for _x in range(x - 1, x + 2):
            for _y in range(y - 1, y + 2):
                if L == (pixels[_x][_y] > G):
                    nearDots += 1

        # TODO: 这个地方直接返回上一个像素感觉不妥
        if nearDots < N:
            return pixels[x][y - 1]
        else:
            return ignore

    for i in range(0, Z):
        for x in range(1, height - 1):
            for y in range(1, width - 1):
                color = denoise_pixel(x, y)
                # color = pixels[x][y]
                # print(x, y, len(pixels), len(pixels[0]))
                if color != ignore:
                    pixels[x][y] = color

    pixels = [x for y in pixels for x in y]

    new_img.putdata(pixels)

    return new_img
