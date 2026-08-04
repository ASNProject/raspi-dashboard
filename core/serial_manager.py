import serial
import json


class SerialManager:

    def __init__(self):

        self.ser = None

    def connect(self, port, baudrate):

        self.ser = serial.Serial(
            port,
            baudrate,
            timeout=1,
        )

    def send(self, data):

        if self.ser is None:
            print("Serial belum connect")
            return

        message = json.dumps(data)

        self.ser.write(
            (message + "\n").encode()
        )