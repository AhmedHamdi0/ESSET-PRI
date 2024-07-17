import RPi.GPIO as GPIO
import time
import struct


class Sniffing:

    def __init__(self):
        self.gpio_pins = [2, 3, 4, 17, 27, 22, 10, 9]
        self.is_reading = True
        self.data_list = []

        self.initialize_port()

    def initialize_port(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        for pin in self.gpio_pins:
            GPIO.setup(pin, GPIO.IN)
        GPIO.setup(19, GPIO.OUT)
        GPIO.output(19, GPIO.LOW)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(16, GPIO.LOW)

    def run(self, sniffing_time):
        print("\n\nSniffing Started ...\n")
        GPIO.output(19, GPIO.HIGH)
        start_time = time.time()
        while time.time() - start_time < sniffing_time:
            data = 0
            if GPIO.input(11) and self.is_reading:
                self.is_reading = False
                for index, pin in enumerate(self.gpio_pins):
                    pin_state = GPIO.input(pin)
                    data |= (pin_state << index)
                self.data_list.append(data)
                GPIO.output(16, GPIO.HIGH)
                print("Byte Received: ", data)
            
            if not GPIO.input(11):
                GPIO.output(16, GPIO.LOW)
                self.is_reading = True
        self.store_in_file()
        GPIO.output(19, GPIO.LOW)
        print("\nSniffing Finished ...\n")

    def store_in_file(self):
        with open("/home/esset/FTP/files/sniffing/data.bin", "w") as file:
            for byte in self.data_list:
                file.write(hex(byte))
