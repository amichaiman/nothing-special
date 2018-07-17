import pytesseract
import pyscreenshot
import numpy
from PIL import ImageFilter, Image
import cv2


def get_image_text(img):
    img = img.resize((img.size[0] * 2, img.size[1] * 2), Image.ANTIALIAS)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    thresh = 120
    img = img.convert('L').point(lambda x: 255 if x > thresh else 0, mode='1')
    # img.show()
    return pytesseract.image_to_string(img, lang="heb")


def get_image_text_question(img):
    img = img.resize((img.size[0] * 2, img.size[1] * 2), Image.ANTIALIAS)
    thresh = 180
    img = img.convert('L').point(lambda x: 255 if x > thresh else 0, mode='1')
    # img.show()
    return pytesseract.image_to_string(img, lang="heb")


def get_question_and_answers():
    question = get_image_text_question(pre_process_image(pyscreenshot.grab(bbox=(50, 440, 400, 540))))
    answers = {
        0: get_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 562, 350, 595)))),
        1: get_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 615, 350, 650)))),
        2: get_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 665, 350, 700))))
    }

    return question, answers


def pre_process_image(img):
    # img = img.filter(ImageFilter.SMOOTH_MORE)
    return img


def get_quick_image_text(img):
    img = img.resize((img.size[0] * 2, img.size[1] * 2), Image.ANTIALIAS)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    thresh = 100
    img = img.convert('L').point(lambda x: 255 if x > thresh else 0, mode='1')
    # img.show()
    return pytesseract.image_to_string(img, lang="heb")


def get_question_and_answers_quick():
    question = get_image_text_question(pyscreenshot.grab(bbox=(50, 400, 400, 480)))
    answers = {
        0: get_quick_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 505, 350, 540)))),
        1: get_quick_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 560, 350, 595)))),
        2: get_quick_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 610, 350, 645)))),
        3: get_quick_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 665, 350, 700))))
    }
    return question, answers
