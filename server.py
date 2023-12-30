import socket
import sys
import os

sys.path.insert(0, os.path.abspath('.'))
from lib.dobot import Dobot
import RPi.GPIO as GPIO
from server_functions import *

bot = Dobot('/dev/ttyS0')
# changing robot speed
bot.interface.set_point_to_point_coordinate_params(300, 300, 300, 300)
# setting ports for sensors to be able to read them
bot.interface.set_ir_switch(2, 1, 2, 1)
bot.interface.set_color_sensor(2, 1, 1, 1)

# setting up conveyor belt
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# PWM pin
GPIO.setup(12, GPIO.OUT)
# conveyor belt direction pin
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.HIGH)
pi_pwm = GPIO.PWM(12, 400)
pi_pwm.start(0)
pi_pwm.ChangeDutyCycle(50)
# turning pwm pin "off" to stop belt from moving immediately
GPIO.setup(12, GPIO.IN)


def server_program():
    # ip address of this device
    host = "192.168.26.250"
    # same on server and client
    port = 1234

    server_socket = socket.socket()
    # bind host address and port together
    server_socket.bind((host, port))
    print("starting server")
    server_file_writer("Starting server")
    # configure how many clients the server can listen simultaneously
    server_socket.listen(5)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    server_file_writer("Client connected to the server")
    while True:
        # receive data stream. it won't accept data packets greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break

        print("from connected user: " + str(data))
        server_file_writer("from connected user: " + str(data))
        if data.__contains__("("):
            exec(data)
            data = "done " + list_to_string(get_cube_list())

        elif data == "hearbeat":
            data = "alive"

        else:
            data = "message received"

        conn.send(data.encode())

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
