import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath('.'))
import RPi.GPIO as GPIO
from time import sleep, time
from lib.dobot import Dobot

bot = Dobot('/dev/ttyS0')

# coordinates for cube detected by IR-sensor
ir_sens_x = 243.64430236816406
ir_sens_y = -79.6631088256836
ir_sens_z = 10.834213256835938
ir_sens = [ir_sens_x, ir_sens_y, ir_sens_z]

# where we put a scanned cube when our warehouse is full
belt_x = 242.2924346923828
belt_y = -161.6956329345703
belt_z = 11.776344299316406
belt = [belt_x, belt_y, belt_z]

# coordinates for the color sensor
color_sens_x = 162.2412109375
color_sens_y = -163.2942352294922
color_sens_z = 16.308555603027344
color_sens = [color_sens_x, color_sens_y, color_sens_z]

# coordinates for the first column of the cubes, the rest are placed according to buffer below
red_x = 116.79029083251953
red_y = -255
red_z = -47.93147277832031
red = [red_x, red_y, red_z]

green_x = 116.79029083251953
green_y = -290
green_z = -47.93147277832031
green = [green_x, green_y, green_z]

blue_x = 116.79029083251953
blue_y = -185
blue_z = -47.93147277832031
blue = [blue_x, blue_y, blue_z]

yellow_x = 116.79029083251953
yellow_y = -220
yellow_z = -47.93147277832031
yellow = [yellow_x, yellow_y, yellow_z]

# distance between center of cubes when placed next to each other
buffer = 30

# list to keep track of number of cubes delivered
cube_list = [0, 0, 0, 0]


# writes to our server log file
def server_file_writer(string_to_write):
    # current date and time
    now = datetime.now()

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    with open("server_log_file.txt", "a") as file:
        file.write(dt_string + "\n" + string_to_write + "\n\n")
    file.close()


# suction cub on/off
def set_suction(value):
    bot.interface.set_end_effector_suction_cup(1, value)


# functions for moving the robot arm in different directions
def move_arm_x(distance):
    bot.move_to_relative(distance, 0, 0, 0)


def move_arm_y(distance):
    bot.move_to_relative(0, distance, 0, 0)


def move_arm_z(distance):
    bot.move_to_relative(0, 0, distance, 0)


def get_curr_pos():
    pos = bot.get_pose()
    curr_x = pos[0]
    curr_y = pos[1]
    curr_z = pos[2]
    curr = [curr_x, curr_y, curr_z]
    return curr


def packing_threshold(packed):
    if packed >= 4:
        move_arm_z(5)
        run_belt(3)
        packed = 0
        bot.move_to_relative(1, 1, 1, 0)
        move_arm_to(ir_sens)
    return packed


# helps the restock function
def restock_color(color):
    color_inv_full = 0
    if color == "red":
        index = 0
        color_read = red

    elif color == "green":
        index = 1
        color_read = green

    elif color == "blue":
        index = 2
        color_read = blue

    else:
        index = 3
        color_read = yellow

    # 8 cubes maximum in each row
    if get_cube_list()[index] < 8:
        set_cube_list(index)
    else:
        color_inv_full = 1

    return index, color_read, color_inv_full


# moves cubes depending on color and if we are restocking or packing an order
def move_cube(color, column, action, packed):
    status = action
    curr_pos = get_curr_pos()
    move_arm_z(5)
    # the reach the cubes further away we have to change the movement
    if color == blue or color == yellow:
        if status == "packing":
            if packed == 3:
                move_arm_y((color[1] - curr_pos[1]) / 3)
                move_arm_x((color[0] - curr_pos[0]) - buffer * column)
                move_arm_y((color[1] - curr_pos[1]) * 2 / 3)

            else:
                move_arm_y((color[1] - curr_pos[1]) * 2 / 3 + buffer * packed)
                move_arm_x((color[0] - curr_pos[0] - buffer * column) * 3 / 4)
                move_arm_y((color[1] - curr_pos[1]) / 3 - buffer * packed)
                move_arm_x((color[0] - curr_pos[0] - buffer * column) / 4)

        else:
            move_arm_x((color[0] - curr_pos[0] - buffer * column) / 3)
            move_arm_y((color[1] - curr_pos[1]) / 2)
            move_arm_x((color[0] - curr_pos[0] - buffer * column) / 3)
            move_arm_y((color[1] - curr_pos[1]) / 2)
            move_arm_x((color[0] - curr_pos[0] - buffer * column) / 3)

    elif color == green:
        move_arm_y((color[1] - curr_pos[1]) / 2)
        move_arm_x((color[0] - curr_pos[0]) / 2)
        move_arm_y((color[1] - curr_pos[1]) / 2)
        move_arm_x((color[0] - curr_pos[0]) / 2 - buffer * column)

    else:
        move_arm_y(color[1] - curr_pos[1])
        move_arm_x(color[0] - curr_pos[0] - buffer * column)

    move_arm_z(color[2] - curr_pos[2] - 5)

    if status == "restock":
        set_suction(0)
    else:
        set_suction(1)

    # from cube

    curr_pos = get_curr_pos()
    if packed == 3:
        move_arm_z(20)
    move_arm_z(ir_sens[2] - curr_pos[2] + 10)

    if color == red or color == green:
        move_arm_y((ir_sens[1] - curr_pos[1]) / 3)
        move_arm_x((ir_sens[0] - curr_pos[0]) / 2)
        move_arm_y((ir_sens[1] - curr_pos[1]) / 3)
        move_arm_x((ir_sens[0] - curr_pos[0]) / 2)
        move_arm_y((ir_sens[1] - curr_pos[1]) / 3 - buffer * packed)

    elif color == yellow:
        move_arm_x((ir_sens[0] - curr_pos[0]) / 2)
        move_arm_y((ir_sens[1] - curr_pos[1]) / 3)
        move_arm_x((ir_sens[0] - curr_pos[0]) / 2)
        move_arm_y((ir_sens[1] - curr_pos[1]) * 2 / 3 - buffer * packed)

    else:
        move_arm_x(ir_sens[0] - curr_pos[0])
        move_arm_y(ir_sens[1] - curr_pos[1] - buffer * packed)

    if status == "packing":
        if packed == 3:
            move_arm_z(-30)

        else:
            move_arm_z(-10)

        set_suction(0)


def move_arm_to(destination):
    move_arm_z(10)
    curr_pos = get_curr_pos()
    move_arm_y(destination[1] - curr_pos[1])
    move_arm_x(destination[0] - curr_pos[0])
    move_arm_z(destination[2] - curr_pos[2])


def run_belt(seconds):
    start_time = time.time()
    set_belt("on")

    while True:
        end_time = time.time()
        if end_time - start_time > seconds:
            set_belt("off")
            break


# start, stop or change directions for the conveyor belt
def set_belt(status):
    status_value = status

    if status_value == "on":
        GPIO.setup(12, GPIO.OUT)
    if status_value == "off":
        GPIO.setup(12, GPIO.IN)
    if status_value == "left":
        GPIO.output(16, GPIO.HIGH)
    if status_value == "right":
        GPIO.output(16, GPIO.LOW)


# starts the belt and ultimately stops it when a cube is detected
def check_ir():
    time_limit = 0
    start_time = time.time()
    set_belt("on")

    while True:
        end_time = time.time()
        # if 10 seconds pass without a cube the belt is stopped
        if end_time - start_time > 10:
            time_limit = 1
            set_belt("off")
            break

        # keeps reading ir-sensor until a cube appears
        cube_detection = bot.interface.sendIR([0xaa, 0xaa, 0x04, 0x8a, 0x00, 0x02, 0x00, 0x74])
        if cube_detection[0] == 1:
            set_belt("off")
            break
    return time_limit


# reads color sensor and return the color
def check_color():
    status = bot.interface.sendColor([0xaa, 0xaa, 0x03, 0x89, 0x00, 0x01, 0x76])
    if status[0] == 1:
        return "red"
    elif status[1] == 1:
        return "green"
    elif status[2] == 1:
        return "blue"
    else:
        return "yellow"


def set_cube_list(index):
    cube_list[index] = int(cube_list[index]) + 1


def get_cube_list():
    return cube_list


def list_to_string(lista):
    return_string = ""

    for i in range(4):
        return_string += str(lista[i])

    return return_string


# restocks the inventory until it's full or no cube is detected by the sensor
def start_restock(current_inventory):
    for i in range(4):
        cube_list[i] = current_inventory[i]

    bot.move_to_relative(1, 1, 1, 0)
    move_arm_to(ir_sens)
    move_arm_z(10)

    while True:
        color_inv_full = 0
        cube_sum = 0

        # check if inventory is full
        for i in get_cube_list():
            cube_sum += i
        if cube_sum >= 32:
            break

        # if there are no cubes detected for 10 seconds, break
        if check_ir() == 1:
            break

        move_arm_z(-10)
        set_suction(1)

        move_arm_to(color_sens)
        sleep(1)

        function_returns = restock_color(check_color())
        index = function_returns[0]
        color_read = function_returns[1]
        color_inv_full = function_returns[2]

        # if row not full, add the cube
        if color_inv_full == 0:
            column = get_cube_list()[index]
            move_cube(color_read, column, "restock", 0)

        # else put it back on the belt
        else:
            move_arm_to(belt)
            set_suction(0)
            move_arm_to(ir_sens)
            move_arm_z(10)


def packing_color(order_list, inventory_list, color, packed):
    if color == red:
        index = 0
    elif color == green:
        index = 1
    elif color == blue:
        index = 2
    else:
        index = 3

    for i in range(order_list[index]):
        # if the order is larger than 4 cubes, and we have packed 4 of them already, move the belt a bit and reset
        # this is to prevent the arm from reaching too far
        packed = packing_threshold(packed)

        move_cube(color, inventory_list[index], "packing", packed)
        move_arm_z(5)
        # decrease local inventory list and order list to keep track
        inventory_list[index] = inventory_list[index] - 1
        order_list[index] = order_list[index] - 1
        packed += 1

    return packed


# pack the order received by the client
def pack_order(inventory, order):
    packed = 0
    inventory_list = [0, 0, 0, 0]
    order_list = [0, 0, 0, 0]

    for i in range(4):
        inventory_list[i] = inventory[i]
        order_list[i] = order[i]

    # as long as the given color is actually ordered, we pack it
    if order_list[0] != 0:
        packed = packing_color(order_list, inventory_list, red, packed)

    if order_list[1] != 0:
        packed = packing_color(order_list, inventory_list, green, packed)

    if order_list[2] != 0:
        packed = packing_color(order_list, inventory_list, blue, packed)

    if order_list[3] != 0:
        packing_color(order_list, inventory_list, yellow, packed)

    # when the entire order is packed, move the belt, then move arm back to starting pos
    if order_list == [0, 0, 0, 0]:
        move_arm_z(10)
        run_belt(3)
        bot.move_to_relative(1, 1, 1, 0)
        move_arm_to(ir_sens)
