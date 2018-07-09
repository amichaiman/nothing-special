import pytesseract
from PIL import ImageOps,ImageEnhance
import pyscreenshot


def get_image_text(img):
    pix = img.load()
    w, h = img.size
    threshold = 160
    for i in range(0, w):
        for j in range(0, h):
            try:
                r, g, b = img.getpixel((i, j))
                if r < threshold or g < threshold or b < threshold:
                    pix[i, j] = (0, 0, 0)
            except:
                return "nope"
    return pytesseract.image_to_string(img, lang="heb")


def get_question_and_answers():
    question = get_image_text(pyscreenshot.grab(bbox=(50, 440, 400, 540)))
    answers = {
        0: get_image_text(pyscreenshot.grab(bbox=(136, 557, 350, 595))),
        1: get_image_text(pyscreenshot.grab(bbox=(136, 608, 350, 650))),
        2: get_image_text(pyscreenshot.grab(bbox=(136, 660, 350, 700)))
    }
    return question, answers


def get_question_and_answers_quick():
    question = get_image_text(pyscreenshot.grab(bbox=(50, 400, 400, 480)))
    answers = {
        0: get_image_text(pyscreenshot.grab(bbox=(136, 505, 350, 545))),
        1: get_image_text(pyscreenshot.grab(bbox=(136, 560, 350, 595))),
        2: get_image_text(pyscreenshot.grab(bbox=(136, 610, 350, 645))),
        3: get_image_text(pyscreenshot.grab(bbox=(136, 665, 350, 700)))
    }

    return question, answers
