import pytesseract
from PIL import Image, ImageFilter, ImageEnhance, ImageOps


def get_question_and_answers():
    img_path = "/home/amichai/PycharmProjects/q/src/"
    img_extension = ".jpeg"
    img = Image.open(img_path + "image" + img_extension)
    img = ImageOps.invert(img)
    pix = img.load()
    w, h = img.size
    ImageOps.solarize(img,10)
    threshold = 30

    for i in range(0, w):
        for j in range(600, h):
            r, g, b = img.getpixel((i, j))
            if r > threshold or g > threshold or b > threshold:
                pix[i, j] = (255, 255, 255)

    img.save(img_path + "blackwhite" + img_extension)

    img.crop((0, 700, w, h - 450)).save(img_path + "question" + img_extension)
    img.crop((150, 1000, w, h - 300)).save(img_path + "answer0" + img_extension)
    img.crop((0, 1150, w, h - 160)).save(img_path + "answer1" + img_extension)
    img.crop((0, 1300, w, h - 30)).save(img_path + "answer2" + img_extension)

    # img.crop((0, 900, w, h - 450)).save(img_path + "question" + img_extension)
    # img.crop((0, 1170, w, h - 320)).save(img_path + "answer0" + img_extension)
    # img.crop((0, 1300, w, h - 190)).save(img_path + "answer1" + img_extension)
    # img.crop((0, 1430, w, h - 55)).save(img_path + "answer2" + img_extension)

    answers = {
        0: pytesseract.image_to_string(Image.open(img_path + "answer0" + img_extension), lang="heb"),
        1: pytesseract.image_to_string(Image.open(img_path + "answer1" + img_extension), lang="heb"),
        2: pytesseract.image_to_string(Image.open(img_path + "answer2" + img_extension), lang="heb")
    }

    question = pytesseract.image_to_string(Image.open(img_path + "question" + img_extension), lang="heb")
    return question, answers
