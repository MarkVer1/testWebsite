import base64
from io import BytesIO
from PIL import Image


def im_2_b64(image):
    buff = BytesIO()
    image.save(buff, format="JPEG")
    img_str = base64.b64encode(buff.getvalue())
    return img_str


def main():
    #img = Image.open("imgs/abstract.jpg")
    #print(im_2_b64(img).decode())
    v = '/'
    print(v[1:] + ";")


if __name__ == '__main__':
    main()