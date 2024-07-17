import RPi.GPIO as GPIO
import time
import json

class Fuzzing:
    def __init__(self):
        # Define the list of GPIO pins to use as inputs
        self.input_data = [2, 3, 4, 17, 27, 22, 10, 9]  # GPIO2 ---> LSB, GPIO9 ---> MSB
        self.output_data = [14, 15, 18, 23, 24, 25, 8, 7]  # GPIO14 ---> LSB, GPIO7 ---> MSB
        self.is_reading = True
        self.response = ""
        self.initialize_port()

    def run(self):
        self.read_fuzzing_data_file()
        self.send_fuzzing_data()
        self.write_responses()

    def initialize_port(self):
        GPIO.setmode(GPIO.BCM)

        # Sniffing:
        # fpga sending status (DV)  -----> it will be asserted after fpga send a byte in sniffing mode
        GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # set pin 23 (GPIO11) as input and pull down

        # rasberry receiving data from fpga (ack) in sniffing mode ---> it will be asserted after receiving each byte
        GPIO.setup(16, GPIO.OUT)  # set pin 36 (GPIO16) as output
        GPIO.output(16, GPIO.LOW)

        # Fuzzing:
        # fpga transmitter status (ack) ---> it will be asserted when fpga send the byte in fuzzing mode  (Ack come from UART TX for example)
        GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # set pin 31 (GPIO6) as Input

        # rasberry sending data to fpga (DV) in fuzzing mode   -------> it will be asserted after sending each byte (DV Tx Uart)
        GPIO.setup(13, GPIO.OUT)  # set pin 33 (GPIO13) as output
        GPIO.output(13, GPIO.LOW)

        #  message sent (DV) ---> it will be asserted after sending 4 bytes for example # Start Sniffing Signal
        GPIO.setup(19, GPIO.OUT)  # set pin 35 (GPIO19) as output
        GPIO.output(19, GPIO.LOW)


        # Set up GPIO pins as inputs for receiving data from fpga
        for pin in self.input_data:
            GPIO.setup(pin, GPIO.IN)

        # Set up GPIO pins as output for sending data to fpga
        for pin in self.output_data:
            GPIO.setup(pin, GPIO.OUT)

    def write_byte(self, byte_value):
        # Convert byte_value to binary string with leading zeros
        binary_string = format(byte_value, '08b')
        # Iterate over the GPIO pins and set the output according to the binary string
        for index, pin in enumerate(self.output_data):
            GPIO.output(pin, int(binary_string[7 - index]))

    def receive_sniffed_data(self,message):
        # Record the start time
        self.response = ""
        start_time = time.time()     
        while time.time() - start_time < 20:
            self.data = 0
    
            if GPIO.input(11) and self.is_reading:
                # GPIO.output(16, GPIO.HIGH)
                self.is_reading = False
                for index, pin in enumerate(self.input_data):
                    pin_state = GPIO.input(pin)
                    self.data |= (pin_state << index)
                # if self.data == 255:
                #     continue

                print(self.data)
                self.response += str(hex(self.data))
                start_time = time.time()   # reset timer
                GPIO.output(16, GPIO.HIGH) # send ack to fpga
                # GPIO.output(16, GPIO.LOW)
            if not GPIO.input(11):
                # clear ack
                GPIO.output(16, GPIO.LOW)
                self.is_reading = True
        print("the response is: ",self.response)
        self.fuzzing_data[message] = self.response

    def write_responses(self):
        with open("/home/esset/FTP/files/fuzzing/fuzzing_data.json", 'w') as json_file:
            json.dump(self.fuzzing_data, json_file, indent=4)

    def send_fuzzing_data(self):
        # Iterate over the messages
        for message in self.fuzzing_data.keys():
            GPIO.output(19, GPIO.LOW)  # reset signal
            bytes_list = message.split('0x')[1:]
            for byte in bytes_list:
                print("byte in fuzzing data is: ",byte)
                self.write_byte(int(byte,16))
                GPIO.output(13, GPIO.HIGH ) #send DV to fpga
                GPIO.output(13, GPIO.LOW) #reset DV'
                while GPIO.input(6) == 0:  # wait until fpga send data
                    pass
            print("message sent")        
            GPIO.output(19, GPIO.HIGH) # message sent status
            # fpga will start sniffing after receiveng a message ( 4 bytes)
            self.receive_sniffed_data(message)

    def read_fuzzing_data_file(self):
        with open("/home/esset/FTP/files/fuzzing/fuzzing_data.json", 'r') as json_file:
            self.fuzzing_data = json.load(json_file)
