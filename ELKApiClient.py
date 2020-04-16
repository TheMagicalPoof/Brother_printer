#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import os


class ELKApiClient():
    """Class on requests to the https://elksale.xyz/"""
    def __init__(self, printer_id):
        request_json_get = requests.get("https://elksale.xyz/devicemessages.php?action=queuelist&deviceid=" +printer_id)
        self.json_content = json.loads(request_json_get.text)
        if self.json_content == []:
            print("Отсутствуют задачи для исполнения.")
            self.printer_usb_adr = None
            self.model = None
            return
        else:
            job = json.dumps(self.json_content[0]["id"])
            self.job = job[1:-1]
            self.job_content = "https://elksale.xyz/devicemessages.php?action=downloadjob&job=" + str(self.job)

            payload = json.dumps(self.json_content[0]["payload"])

            payload = json.loads(payload)
            payload = json.loads(payload)
            # print(payload)

            self.model = json.dumps(payload["printer_model"])
            self.model = self.model[1:-1]

            self.printer_usb_adr = json.dumps(payload['printer_usb_adr'])
            self.printer_usb_adr = self.printer_usb_adr[1:-1]

    def printer_info(self, info=False):
        """Method for get printer id of JSON"""
        if info:
            print('Модель устройства: "' + self.model + '" с адрессом "' + self.printer_usb_adr + '"')
            return
        return self.model, self.printer_usb_adr

    def image_name(self, info=False):
        """Method for get image name"""
        if info:
            print('Название картинки: "' + self.job + '.png"')
            return
        return self.job + ".png"

    def saveimage(self, info=False):
        """Method for get name of image of JSON and saving it to a file"""
        request_image_content = requests.get(self.job_content)
        if request_image_content.status_code == 404:
            print("Нет подключения к https://elksale.xyz/")
            return

        with open(self.job + ".png", "wb") as file:
            file.write(request_image_content.content)
            file.close()
        if info:
            print('Сохранение: "' + self.image_name() + '" завершено.')
            return

    def removeimage(self, info=False):
        """Remove the image file"""
        os.remove(self.image_name())
        if info:
            print('Удаление "' + self.image_name() + '" - завершено.')
            return

    def print_queue(self, info=False):
        """Number of sticker queue"""
        if info:
            print('Длина очереди составляет ' + str(len(self.json_content)) + ' картинок.')
        return len(self.json_content)

    def jobcomplete(self, info=False):
        """Need to be called after printing"""
        requests.get("https://elksale.xyz/devicemessages.php?action=jobcompleted&job=" + self.job)

        if info:
            if self.print_queue() - 1 == 0:
                print('Наклейка "' + str(self.job) + '" удалена из очереди.')
            else:
                print('Наклейка "' + str(self.job) + '" удалена из очереди, осталось еще ' + str(self.print_queue()-1))
        self.removeimage()
        return 0



# q = ELKApiClient("termo_printer_1")
# qtt = q.printer()
# ttq = q.saveimage()
# q.print_queue(True)
# q.printer_info(True)
# q.jobcomplite()
#
# # print(qtt)
# # print(ttq)
