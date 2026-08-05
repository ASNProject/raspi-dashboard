from PySide6.QtCore import QObject, Signal, QThread, QMetaObject, Qt
import serial
import json
import time


class SerialManager(QObject):

    packetReceived = Signal(dict)

    connected = Signal()
    disconnected = Signal()
    error = Signal(str)

    def __init__(self):
        super().__init__()

        self.ser = None
        self.running = False

    def open(self, port, baudrate):

        print("OPEN:", port, baudrate)

        try:

            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=0.1,
            )

            print("OPEN BERHASIL")

            self.running = True

            self.connected.emit()

        except Exception as e:

            self.running = False

            self.ser = None

            self.error.emit(str(e))

    def start(self):

        while self.running:

            # Menunggu sampai connect()
            if not self.running:

                time.sleep(0.2)

                continue

            # Serial belum dibuka
            if self.ser is None:

                time.sleep(0.2)

                continue

            try:

                # Tidak ada data
                if self.ser.in_waiting == 0:

                    time.sleep(0.01)

                    continue

                # Baca satu baris JSON
                line = self.ser.readline().decode(
                    "utf-8",
                    errors="ignore"
                ).strip()

                if line == "":
                    continue

                # Parse JSON
                data = json.loads(line)

                # Kirim ke Dashboard
                self.packetReceived.emit(data)

            except json.JSONDecodeError:

                print("Invalid JSON :", line)

            except serial.SerialException as e:

                print("Serial Error :", e)

                self.running = False

                if self.ser:

                    try:
                        self.ser.close()
                    except:
                        pass

                self.ser = None

                self.disconnected.emit()

            except Exception as e:

                print("Error :", e)

                self.error.emit(str(e))

                time.sleep(0.1)

    def disconnect(self):

        self.running = False

        if self.ser:

            try:
                self.ser.close()
            except:
                pass

        self.ser = None

        self.disconnected.emit()