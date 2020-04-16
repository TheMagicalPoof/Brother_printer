#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from PIL import Image
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

class QLPrinter():
    """The selection of the print settings, and print images"""
    def __init__(self, model, port):
        """Initiate print connection"""
        os.environ["BROTHER_QL_PRINTER"] = port
        os.environ["BROTHER_QL_MODEL"] = model

    def print(self, label, img, cut=True, info=False):
        """Initiate printing option"""

        label_sizes = (["12", 106, 0], ["29", 306, 0], ["38", 413, 0], ["50", 554, 0], ["54", 590, 0]
                            , ["62", 696, 0], ["102", 1164, 0], ["17x54", 165, 566], ["17x87", 165, 956]
                            , ["23x23", 202, 202], ["29x42", 306, 425], ["29x90", 306, 991], ["39x90", 413, 991]
                            , ["39x48", 425, 495], ["52x29", 578, 271], ["62x29", 696, 271], ["62x100", 696, 1109]
                            , ["102x51", 1164, 526], ["102x152", 1164, 1660], ["d12", 94, 94], ["d24", 236, 236]
                            , ["d58", 618, 618])

        label_px_size_width = ""
        label_px_size_height = ""
        width = ""
        height = ""
        wrong_label_format = True
        wrong_image_size = True
        wrong_image_directory = False
        print_function_cut = "" if cut is True else "--no-cut "
        for sizes in label_sizes:
            if sizes[0] == label:
                wrong_label_format = False
                label_px_size_width = sizes[1]
                label_px_size_height = sizes[2]
                break
        if wrong_label_format:
            print("Неверный формат бумаги")
            return 1

        try:
            label_size = Image.open(str(img))
            (width, height) = label_size.size
            if str(label_px_size_width) == str(width) and (str(label_px_size_height) == str(height) or str(label_px_size_height) == str(0)):
                wrong_image_size = False
        except:
            wrong_image_directory = True

        if wrong_image_directory:
            print("Неверная директория изображения")
            return 1

        if wrong_image_size:
            print("Неверный размер изображения")
            return 1
        print_function = os.system("brother_ql print " + print_function_cut + "-l " + str(label) + " " + img)

        if print_function == 0:
                print('Печать изображения: "' + img + '"  завершена')
                return 0
        else:
            print("Соединение с принтером потеряно")
            return 1

class QLPrinter_Button():
    def __init__(self, pinNum):
        self.pinNum = pinNum

    def wakeup(self, info=False):
        """Turn (on) the printer through digital pin HIGH value"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinNum, GPIO.OUT)
        GPIO.output(self.pinNum, GPIO.LOW)
        GPIO.output(self.pinNum, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.pinNum, GPIO.LOW)
        GPIO.cleanup()
        if info:
            print("Включение принтера по цифровому выводу: " + str(self.pinNum) + ".")

    def shutdown(self, info=False):
        """Turn (off) the printer through digital pin HIGH value"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinNum, GPIO.OUT)
        GPIO.output(self.pinNum, GPIO.LOW)
        time.sleep(1)
        GPIO.output(self.pinNum, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.pinNum, GPIO.LOW)
        GPIO.cleanup()
        if info:
            print("Выключение принтера по цифровому выводу: " + str(self.pinNum) + ".")


# q = QLPrinter("QL-700", "usb://04f9:2042", 21)
# q.wakeup(21)
# q.print("62", "16148_1_sticker.png", True)
# q.shutdown()