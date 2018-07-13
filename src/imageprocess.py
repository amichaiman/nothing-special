import pytesseract
import pyscreenshot
from PIL import ImageFilter

def get_image_text(img):
    pix = img.load()
    w, h = img.size
    threshold = 80
    for i in range(0, w):
        for j in range(0, h):
            try:
                r, g, b = img.getpixel((i, j))
                if r > threshold or g > threshold or b > threshold:
                    pix[i, j] = (255, 255, 255)
            except:
                return "nope"
    # img.show()
    return pytesseract.image_to_string(img, lang="heb")


def get_image_text_question(img):
    pix = img.load()
    w, h = img.size
    threshold = 210
    for i in range(0, w):
        for j in range(0, h):
            try:
                r, g, b = img.getpixel((i, j))
                if r < threshold or g < threshold or b < threshold:
                    pix[i, j] = (0, 0, 0)
            except:
                return "nope"
    # img.show()
    return pytesseract.image_to_string(img, lang="heb")


def get_question_and_answers():
    question = get_image_text_question(pre_process_image(pyscreenshot.grab(bbox=(50, 440, 400, 540))))
    answers = {
        0: get_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 557, 350, 595)))),
        1: get_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 610, 350, 650)))),
        2: get_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 665, 350, 700))))
    }
    return question, answers


def pre_process_image(img):
    img = img.filter(ImageFilter.SMOOTH_MORE)
    return img


def get_question_and_answers_quick():
    question = get_image_text_question(pyscreenshot.grab(bbox=(50, 400, 400, 480)))
    answers = {
        0: get_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 505, 350, 540)))),
        1: get_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 560, 350, 595)))),
        2: get_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 610, 350, 645)))),
        3: get_image_text(pre_process_image(pyscreenshot.grab(bbox=(110, 665, 350, 700))))
    }

    return question, answers
