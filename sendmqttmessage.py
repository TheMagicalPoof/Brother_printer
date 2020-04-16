import paho.mqtt.client as paho
import time
import ssl
import sys


class sendmqttmessage():
    def __init__(self, broker_topic, message):
        self.message_container = message
        self.broker_topic = broker_topic
        self.while_param = True
        self.client = paho.Client("ELKPrinterServer")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        broker_address = "********.iot.us-east-2.amazonaws.com"  # Endpoint
        port = 8883  # Port no.
        caPath = "ssl/AmazonRootCA1.pem"  # Root_CA_Certificate_Name
        certPath = "ssl/26a6a76ddd-certificate.pem.crt"  # <Thing_Name>.cert.pem
        keyPath = "ssl/26a6a76ddd-private.pem.key"  # <Thing_Name>.private.key
        self.client.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED,
                       tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.client.connect(broker_address, port, keepalive=5)
        self.client.subscribe(broker_topic, qos=0)
        while self.while_param:
            self.client.loop_start()
            time.sleep(1)

    def on_connect(self, client, userdata, flags, rc):
        """Callback индикатор подключения к серверу"""
        if rc == 0:
            client.publish(self.broker_topic, str(self.message_container), qos=0)
        else:
            print("Connection Error")

    def on_message(self, client, userdata, msg):
        """Проверка доставки сообщения"""
        msg = msg.payload.decode("utf-8")
        if msg == self.message_container:
            print('Message: "' + self.message_container + '" delivered')
            self.client.loop_stop()
            self.while_param = False
        else:
            print("Message delivery Error")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        sendmqttmessage(sys.argv[1], sys.argv[2])
    else:
        print("Parameter Error")
    # sendmqttmessage("top", "printer_1")