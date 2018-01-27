"""LSB Tool核心, 利用cython提供对图片的高速处理(??)"""

from PIL import Image, ImageSequence, ImageDraw

class StegImage:

    def __init__(self, filename):

        self.raw = Image.open(filename)

        if self.raw.format == 'GIF':
            self.gif = [x.copy() for x in ImageSequence.Iterator(self.raw)]
            self.setframe(0)
        else:
            self.img = self.raw.convert('RGBA')

            pix = self.img.getdata()

            self.data = [x[0] << 24 | x[1] << 16 | x[2] << 8 | x[3] for x in pix]

    def getbit(self, nbit):

        pix = [((i >> nbit) & 1) * 255 for i in self.data]

        img = Image.new('L', self.img.size)
        img.putdata(pix)

        return img

    def getchannel(self, n):

        pix = self.img.getdata()
        data = [x[n] for x in pix]

        img = Image.new('L', self.img.size)
        img.putdata(data)
        return img

    def getrawimg(self):
        return self.img

    def setframe(self, n):
        self.img = self.gif[n].convert('RGBA')
        pix = self.img.getdata()

        self.data = [x[0] << 24 | x[1] << 16 | x[2] << 8 | x[3] for x in pix]

    def close(self):
        self.img.close()
