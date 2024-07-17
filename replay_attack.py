import RPi.GPIO as GPIO


class ReplayAttack:
    def __init__(self):
        self.output_data = [14, 15, 18, 23, 24, 25, 8, 7]  # GPIO14 ---> LSB, GPIO7 ---> MSB
        self.initialize_port()

    def run(self):
        self.read_replay_attack_data_file()
        self.send_replay_attack_data()

    def initialize_port(self):
        GPIO.setmode(GPIO.BCM)
        # fpga transmitter status (ack) ---> it will be asserted when fpga send the byte
        GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # set pin 31 (GPIO6) as Input

        # it will be asserted after sending each byte (DV Tx Uart)
        GPIO.setup(13, GPIO.OUT)  # set pin 33 (GPIO13) as output
        GPIO.output(13, GPIO.LOW)

        # Set up GPIO pins as output for sending data to fpga
        for pin in self.output_data:
            GPIO.setup(pin, GPIO.OUT)

    def write_byte(self, byte_value):
        # Convert byte_value to binary string with leading zeros
        binary_string = format(byte_value, '08b')
        # Iterate over the GPIO pins and set the output according to the binary string
        for index, pin in enumerate(self.output_data):
            GPIO.output(pin, int(binary_string[7 - index]))

    def send_replay_attack_data(self):
        print("\nReplay Attack Started ...\n")
        bytes_list = self.replay_attack_data.split('0x')[1:]
        for byte in bytes_list:
            print("byte in replay attack data is: ",byte)
            self.write_byte(int(byte, 16))
            GPIO.output(13, GPIO.HIGH ) #send DV to fpga
            GPIO.output(13, GPIO.LOW)   #reset DV'
            while GPIO.input(6) == 0:   # wait until fpga send data
                pass
        print("\nReplay Attack Finished ...\n")

    def read_replay_attack_data_file(self):
        with open("/home/esset/FTP/files/replay_attack/data.bin", 'r') as file:
            self.replay_attack_data = file.read()
