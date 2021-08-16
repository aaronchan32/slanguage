from PIL import Image

def resize(im):
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            (r,g,b,a) = im.getpixel((x//2, y//2))
            pic2.putpixel((x,y) ,(r,g,b))

pic1 = Image.open('homer.png')
pic2 = Image.open('homer.png')
resize(pic1)
pic2.show()