#! /usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as paho
import ssl


class AWSMqtt():
    def __init__(self, client_name, endpoint, port, caPath, certPath, keyPath):
        """constructor"""
        self.Mqttclient = paho.Client(client_name)
        self.Mqttclient.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED,
                       tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.Mqttclient.connect(endpoint, port, keepalive=60)
        self.Mqttclient.on_connect = self.on_connect
        self.Mqttclient.on_message = self.on_message

    message_content = ""

    def on_connect(self, client, userdata, flags, rc):
        """Callback индикатор подключения к серверу"""
        if rc == 0:
            print("Подключено к Mqtt")
        else:
            print("Подключение к Mqtt серверу не удалось")

    def on_message(self, client, userdata, msg, info=False):
        """Callback прием сообщений"""
        self.message_content = msg.payload.decode("utf-8")

    def subscribe(self, broker_topic, info=False):
        """Функция подписки на топик"""
        self.broker_topic = broker_topic
        self.Mqttclient.subscribe(broker_topic, qos=0)
        if info:
            print('Произведена подписка на канал: "' + broker_topic + '".')

    def publish(self, message, info=False):
        """Функция публикации на топик"""
        self.Mqttclient.publish(self.broker_topic, str(message), qos=0)
        if info:
            print('Сообщение: "' + message + '" опубликованно на канале "' + self.broker_topic + '".')

    def loop(self):
        """Функция для запуска буфера ожидания приема сообщений, нужно запускать в while"""
        self.Mqttclient.loop_start()

    def loop_stop(self):
        """Функция для остановки буфера ожидания """
        self.Mqttclient.loop_stop()

    def message(self, info=False):
        """Функция приема сообщений"""
        content = self.message_content
        self.message_content = ""
        if info:
            print('На брокер поступило сообщение: "' + content + '" в канал "' + self.broker_topic + '".')
        return content


# q = AWSMqtt("AWSTestConnection", "a27pzrjkz8wf5r-ats.iot.us-east-2.amazonaws.com", 8883, "ssl/AmazonRootCA1.pem", "ssl/893e9ca39a-certificate.pem.crt", "ssl/893e9ca39a-private.pem.key")
# q.subscribe("top")
# q.publish("test")
# while True:
#     time.sleep(2)
#     q.loop()
#     if str(q.message()) == "privet":
#         print("DOROY")