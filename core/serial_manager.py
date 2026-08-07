from PySide6.QtCore import QObject, Signal
import serial
import json
import time
import logging


class SerialManager(QObject):

    packetReceived = Signal(dict)

    connected = Signal()
    disconnected = Signal()
    error = Signal(str)

    def __init__(self):
        super().__init__()

        self.ser = None

        self.running = False

        self.port = None
        self.baudrate = None

        self._connected = False

    def open(self, port, baudrate):

        self.port = port
        self.baudrate = baudrate

        self.running = True

    def _connect(self):

        if self.ser and self.ser.is_open:
            return True

        try:

            logging.info(f"Connecting {self.port} ...")
            print(f"Connecting {self.port} ...")

            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=0.1,
            )
            
            time.sleep(2)

            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()

            # ESP32 biasanya reset ketika serial dibuka
            time.sleep(2)

            self._connected = True

            logging.info("Serial Connected")
            print("Serial Connected")

            self.connected.emit()

            return True

        except Exception as e:

            if self._connected:
                self._connected = False
                self.disconnected.emit()

            print("CONNECT ERROR :", e)

            self.error.emit(str(e))

            self.ser = None

            return False

    def start(self):

        while self.running:

            # Belum connect
            if self.ser is None:

                if not self._connect():

                    time.sleep(2)

                    continue

            try:

                if self.ser.in_waiting == 0:

                    time.sleep(0.01)

                    continue

                line = self.ser.readline().decode(
                    "utf-8",
                    errors="ignore"
                ).strip()

                if not line:
                    continue

                try:

                    packet = json.loads(line)

                    self.packetReceived.emit(packet)

                except json.JSONDecodeError:

                    logging.info("Invalid JSON : %s", line)
                    print("Invalid JSON :", line)

            except serial.SerialException as e:

                logging.info("Serial Error :", e)
                print("Serial Error :", e)

                self.error.emit(str(e))

                try:
                    self.ser.close()
                except:
                    pass

                self.ser = None

                if self._connected:

                    self._connected = False

                    self.disconnected.emit()

                time.sleep(2)

            except Exception as e:

                logging.info("Error :", e)
                print("Error :", e)

                self.error.emit(str(e))

                time.sleep(1)

    def disconnect(self):

        self.running = False

        if self.ser:

            try:
                self.ser.close()
            except:
                pass

        self.ser = None

        if self._connected:

            self._connected = False

            self.disconnected.emit()

    def send(self, packet: dict):

        if not self.ser or not self.ser.is_open:

            self.error.emit("Serial belum terhubung")

            return False

        try:

            message = json.dumps(packet) + "\n"

            self.ser.write(message.encode("utf-8"))

            self.ser.flush()

            return True

        except Exception as e:

            self.error.emit(str(e))

            try:
                self.ser.close()
            except:
                pass

            self.ser = None

            if self._connected:

                self._connected = False

                self.disconnected.emit()

            return False
