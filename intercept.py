import RPi.GPIO as GPIO
import time


class Intercept:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(1, GPIO.IN)
        GPIO.setup(19, GPIO.OUT)
        GPIO.output(19, GPIO.LOW)

    def run(self):
        print('\nIntercept Started ...\n')
        GPIO.output(19, GPIO.HIGH)
        start_time = time.time()
        flag = False
        while time.time() - start_time < 60:
            if GPIO.input(1):
                flag = True
                print('Stream Found')
                with open("/home/esset/FTP/files/intercept/stream.bin", "w") as file:
                    file.write(hex(1))
                break
        if not flag:
            print('Stream Not Found')
            with open("/home/esset/FTP/files/intercept/stream.bin", "w") as file:
                file.write(hex(0))

        print('\nIntercept Finished ...\n')
