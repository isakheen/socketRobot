import serial
import threading

from lib.message import *


class Interface:
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()

        self.serial = serial.Serial(
            port=port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        
    def sendColor(self, message):
        self.lock.acquire()
        self.serial.write(message)
        self.serial.flush()
        response = Message.readColor(self.serial)
        self.lock.release()
        return response

        
    def sendIR(self, message):
        self.lock.acquire()
        self.serial.write(message)
        self.serial.flush()
        response = Message.read(self.serial)
        self.lock.release()
        return response.params

    def send(self, message):
        self.lock.acquire()
        self.serial.write(message.package())
        self.serial.flush()
        response = Message.read(self.serial)
        self.lock.release()
        return response.params

    def get_pose(self):
        request = Message([0xAA, 0xAA], 2, 10, False, False, [], direction='out')
        return self.send(request)

    def get_homing_paramaters(self):
        request = Message([0xAA, 0xAA], 2, 30, False, False, [], direction='out')
        return self.send(request)

    def set_homing_parameters(self, x, y, z, r, queue=True):
        request = Message([0xAA, 0xAA], 2, 30, True, queue, [x, y, z, r], direction='out')
        return self.send(request)

    def set_homing_command(self, command, queue=True):
        request = Message([0xAA, 0xAA], 2, 31, True, queue, [command], direction='out')
        return self.send(request)

    def get_end_effector_suction_cup(self):
        request = Message([0xAA, 0xAA], 2, 62, False, False, [], direction='out')
        return self.send(request)

    def set_end_effector_suction_cup(self, enable_control, enable_suction, queue=True):
        request = Message([0xAA, 0xAA], 2, 62, True, queue, [enable_control, enable_suction], direction='out')
        return self.send(request)

    def get_point_to_point_joint_params(self):
        request = Message([0xAA, 0xAA], 2, 80, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_joint_params(self, velocity, acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 80, True, queue, velocity + acceleration, direction='out')
        return self.send(request)

    def get_point_to_point_coordinate_params(self):
        request = Message([0xAA, 0xAA], 2, 81, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_coordinate_params(self, coordinate_velocity, effector_velocity, coordinate_acceleration, effector_acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 81, True, queue, [coordinate_velocity, effector_velocity, coordinate_acceleration, effector_acceleration], direction='out')
        return self.send(request)

    def set_extended_motor_velocity(self, index, enable, speed, queue=True):
        request = Message([0xAA, 0xAA], 2, 135, True, queue, [index, enable, speed], direction='out')
        return self.send(request)

    def get_color_sensor(self, index):
        request = Message([0xAA, 0xAA], 2, 137, False, False, [], direction='out')
        return self.send(request)

    def set_color_sensor(self, index, enable, port, version, queue=True):
        request = Message([0xAA, 0xAA], 2, 137, True, queue, [enable, port, version], direction='out')
        return self.send(request)

    def get_ir_switch(self,index):
        request = Message([0xAA, 0xAA], 2, 138, False, False,[], direction='out')
        return self.send(request)

    def set_ir_switch(self, index, enable, port, version, queue=True):
        request = Message([0xAA, 0xAA], 2, 138, True, queue, [enable, port, version], direction='out')
        return self.send(request)

    def start_queue(self):
        request = Message([0xAA, 0xAA], 2, 240, True, False, [], direction='out')
        return self.send(request)

    def stop_queue(self, force=False):
        request = Message([0xAA, 0xAA], 2, 242 if force else 241, True, False, [], direction='out')
        return self.send(request)

    def start_queue_download(self, total_loop, line_per_loop):
        request = Message([0xAA, 0xAA], 2, 243, True, False, [total_loop, line_per_loop], direction='out')
        return self.send(request)

    def stop_queue_download(self):
        request = Message([0xAA, 0xAA], 2, 244, True, False, [], direction='out')
        return self.send(request)

    def clear_queue(self):
        request = Message([0xAA, 0xAA], 2, 245, True, False, [], direction='out')
        return self.send(request)

    def get_current_queue_index(self):
        request = Message([0xAA, 0xAA], 2, 246, True, False, [], direction='out')
        return self.send(request)

