from QLPrinter import QLPrinter
from QLPrinter import QLPrinter_Button
from ELKApiClient import ELKApiClient
from AWSMqtt import AWSMqtt
import time

class Thermoprintmanager():
    def __init__(self):
        self.while_param = True
        self.print_try_count = 0
        self.printer_wakeup_pin = 21
        self.printer_name = "termo_printer_1"
        self.client = AWSMqtt("AWSTestConnection1", "******.iot.us-east-2.amazonaws.com", 8883,
                    "./ssl/AmazonRootCA1.pem", "./ssl/893e9ca39a-certificate.pem.crt", "./ssl/893e9ca39a-private.pem.key")
        self.client.subscribe("/devices/" + self.printer_name)
        self.client.publish("Thermoprinter manager connected ")

        self.client.loop()
        while self.while_param:
            time.sleep(5)
            if str(self.client.message()) == "update":
                self.core()

    def core(self):
        button = QLPrinter_Button(self.printer_wakeup_pin)
        check = ELKApiClient(self.printer_name)
        model, port = check.printer_info()
        if model != None or port != None:
            ql_printer = QLPrinter(model, port)
            button.wakeup()
            api = ELKApiClient(self.printer_name)
            api.saveimage()
            if ql_printer.print("62", str(api.image_name()), True) == 0:
                api.jobcomplete(True)
                self.core()
            else:
                if self.print_try_count != 5:
                    print("Повторная попытка печати")
                    self.print_try_count += 1
                    time.sleep(3)
                    self.core()
                else:
                    print("Не удается распечатать изображение, оно будет удалено из очереди")
                    api.jobcomplete(True)
                    self.print_try_count = 0
                    self.core()
        else:
            print("Очередь печати пуста.")
            button.shutdown()

if __name__ == "__main__":
        Thermoprintmanager()
