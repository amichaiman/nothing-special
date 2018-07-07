import pytesseract
from PIL import Image, ImageFilter, ImageEnhance, ImageOps


def get_question_and_answers():
    img = Image.open("/home/amichai/PycharmProjects/q/src/image.jpeg")
    img = img.convert('P')
    # img = ImageOps.grayscale(img)
    img = ImageOps.invert(img)
    img.filter(ImageFilter.DETAIL)
    img.filter(ImageFilter.SHARPEN)
    img = ImageOps.autocontrast(img)

    img.save("/home/amichai/PycharmProjects/q/src/blackwhite.jpeg")
    w, h = img.size
    img.crop((0, 900, w, h - 450)).save("/home/amichai/PycharmProjects/q/src/question.jpeg")
    img.crop((0, 1170, w, h - 320)).save("/home/amichai/PycharmProjects/q/src/answer0.jpeg")
    img.crop((0, 1300, w, h - 190)).save("/home/amichai/PycharmProjects/q/src/answer1.jpeg")
    img.crop((0, 1430, w, h - 55)).save("/home/amichai/PycharmProjects/q/src/answer2.jpeg")

    answers = {
        0: pytesseract.image_to_string(Image.open("/home/amichai/PycharmProjects/q/src/answer0.jpeg"), lang="heb"),
        1: pytesseract.image_to_string(Image.open("/home/amichai/PycharmProjects/q/src/answer1.jpeg"), lang="heb"),
        2: pytesseract.image_to_string(Image.open("/home/amichai/PycharmProjects/q/src/answer2.jpeg"), lang="heb")
    }

    for answer in answers:
        if answer is "":
            answers.__delitem__(answer)

    question = pytesseract.image_to_string(Image.open("/home/amichai/PycharmProjects/q/src/question.jpeg"), lang="heb")
    return question, answers
