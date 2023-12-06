import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import RPi.GPIO as GPIO
import time
import json
from time import sleep
from lib.dobot import Dobot
bot = Dobot('/dev/ttyS0')

target_x = 241.89479064941406
target_y = -76.48391723632812
target_z = 11.184303283691406
target = [target_x, target_y, target_z]

blue_x = 116.79029083251953
blue_y = -176.5496063232422
blue_z = -47.93147277832031
blue = [blue_x, blue_y, blue_z]

red_x = 116.35862731933594
red_y = -238.92129516601562
red_z = -48.053924560546875
red = [red_x, red_y, red_z]

green_x = 117.26726531982422
green_y = -266.2510986328125
green_z = -46.561439514160156
green = [green_x, green_y, green_z]

yellow_x = 115.96161651611328
yellow_y = -209.32736206054688
yellow_z = -49.54224395751953
yellow = [yellow_x, yellow_y, yellow_z]

curr_x = 0
curr_y = 0
curr_z = 0
curr = [curr_x, curr_y, curr_z]

buffer = 30
plockade = 0

bot.interface.set_point_to_point_coordinate_params(300,300,300,300)
bot.interface.set_ir_switch(2, 1, 2, 1)

def get_curr_pos():
    pos = bot.get_pose()
    curr_x = pos[0]
    curr_y = pos[1]
    curr_z = pos[2]
    curr = [curr_x, curr_y, curr_z]
    return curr

def take_cube(color, column, dest):
    to_cube(color, column)
    from_cube(dest, column)
    
def deliver_cube(color, column):
    to_target_from_cube(target)
    bot.interface.set_end_effector_suction_cup(1, 1)
    to_cube(color, column)
    bot.interface.set_end_effector_suction_cup(1, 0)
    
def distance(dest):
    curr_pos = get_curr_pos()
    distance_x = dest[0] - curr_pos[0]
    distance_y = dest[1] - curr_pos[1]
    distance_z = dest[2] - curr_pos[2]
    distance = [distance_x, distance_y, distance_z]
    return distance

def to_cube(color, column, inlevutlev, plockade):
    status = inlevutlev
    curr_pos = get_curr_pos()
    bot.move_to_relative(0, 0, 5, 0)
    if color == red or color == green:
        bot.move_to_relative(0, (color[1]-curr_pos[1])/2, 0, 0)
        bot.move_to_relative((color[0]-curr_pos[0]-buffer*column)/2, 0, 0, 0)
        bot.move_to_relative(0, (color[1]-curr_pos[1])/2, 0, 0)
        bot.move_to_relative((color[0]-curr_pos[0]-buffer*column)/2, 0, 0, 0)
        
    else:
        bot.move_to_relative(0, color[1]-curr_pos[1], 0, 0)
        bot.move_to_relative(color[0]-curr_pos[0]-buffer*column, 0, 0, 0)
    
    bot.move_to_relative(0, 0, color[2]-curr_pos[2]-5, 0)
    if status == "inlev":
        bot.interface.set_end_effector_suction_cup(1, 0)
    else:
        bot.interface.set_end_effector_suction_cup(1, 1)
    
    #from cube
    
    curr_pos = get_curr_pos()
    bot.move_to_relative(0, 0, target[2]-curr_pos[2]+10, 0)
        
    if color == red or color == green:
        bot.move_to_relative(0, (target[1]-curr_pos[1])/3, 0, 0)
        bot.move_to_relative(target[0]-curr_pos[0], 0, 0, 0)
        bot.move_to_relative(0, (target[1]-curr_pos[1])*2/3-buffer*plockade, 0, 0)
    else:
        bot.move_to_relative(target[0]-curr_pos[0], 0, 0, 0)
        bot.move_to_relative(0, target[1]-curr_pos[1]-buffer*plockade, 0, 0)
    
    if status == "utlev":
        bot.move_to_relative(0, 0, -10, 0)
        bot.interface.set_end_effector_suction_cup(1, 0)
    
def to_target(dest):
    curr_pos = get_curr_pos()
    bot.move_to_relative(0, dest[1]-curr_pos[1], 0, 0)
    bot.move_to_relative(dest[0]-curr_pos[0], 0, 0, 0)
    bot.move_to_relative(0, 0, dest[2]-curr_pos[2], 0)
    
def to_target_from_cube(dest):
        
    curr_pos = get_curr_pos()
    bot.move_to_relative(0, 0, (dest[2]-curr_pos[2])+20, 0)
    bot.move_to_relative(dest[0]-curr_pos[0], 0, 0, 0)
    bot.move_to_relative(0, (dest[1]-curr_pos[1]), 0, 0)
        
    #bot.move_to_relative(0, 0, -20, 0)


def from_cube(dest, column):
    curr_pos = get_curr_pos()
    bot.move_to_relative(0, 0, dest[2]-curr_pos[2]+10, 0)
    
    if column != 0:
        bot.move_to_relative(buffer*column, 0, 0, 0)

    bot.move_to_relative(dest[0]-curr_pos[0], 0, 0, 0)

    bot.move_to_relative(dest[0]-curr_pos[0]-buffer*column, 0, 0, 0)
        
    bot.move_to_relative(0, 0, -10, 0)
    
    bot.interface.set_end_effector_suction_cup(1, 0)
    
################Funktioner för band############################################# 
    
def change_values(status):
    status_value = status
    
    if status_value == "on":
        GPIO.setup(12, GPIO.OUT)
    if status_value == "off":
        GPIO.setup(12, GPIO.IN)
    if status_value == "left":
        GPIO.output(16, GPIO.HIGH)
    if status_value == "right":
        GPIO.output(16, GPIO.LOW)
        
def check_ir():
    status = 0
    start_time = time.time()
    change_values("on")
    
    while True:
        end_time = time.time()
        if end_time - start_time > 10:
            status = 1
            change_values("off")
            break
        
        printa = bot.interface.send1([0xaa,0xaa,0x04,0x8a,0x00,0x02,0x00,0x74])
        if printa[0] == 1:
            change_values("off")
            break
    return status
        
################Funktioner för RPI#############################################        
    
def starta_inlev(antal_av_varje):
    colors = ["blue", "yellow", "red", "green"]
    color = ["Blue Cube", "Yellow Cube", "Red Cube", "Green Cube"]
    bot.move_to_relative(1, 1, 1, 0)
    to_target(target)
    bot.move_to_relative(0, 0, 10, 0)
    i = 0
    while True:
        if check_ir() == 1:
            break
        bot.move_to_relative(0, 0, -10, 0)
        bot.interface.set_end_effector_suction_cup(1, 1)
        column = check_inv(colors[i])
        update_inventory(color[i], colors[i], 1, "add", plockade)
        column = check_inv(colors[i])
        if column == antal_av_varje:
            i += 1
            column = 0
            
def plocka_kub(color, column):
    to_cube(color, column, "utlev")
    
################Funktioner för läsning/uppdatering av fil################################### 
def check_inv(color):
    if color == "blue":
        index = 0
    if color == "yellow":
        index = 1
    if color == "red":
        index = 2
    if color == "green":
        index = 3
        
    file = open("inventory.json", "r")
    data = json.load(file)
    file.close()
    
    inv_string = str(data[index])
    inv_quantity = int(inv_string[-3])
    return inv_quantity

def update_inventory(cube_color, color, quantity, operation, plockade):
    if color == "blue":
        color = blue
        index = 0
    if color == "yellow":
        color = yellow
        index = 1
    if color == "red":
        color = red
        index = 2
    if color == "green":
        color = green
        index = 3
        
    file = open("inventory.json", "r")
    data = json.load(file)
    file.close()
    old_string = str(data[index])
    old_quantity = int(old_string[-3])
    if operation == "add": #if inleverans
        to_cube(color,old_quantity,"inlev", plockade)
        new_quantity = str(old_quantity + quantity)
        
    if operation == "sub": #if packning
        for i in range(quantity):
            to_cube(color,old_quantity-i-1,"utlev", plockade)
        new_quantity = str(old_quantity - quantity)

    if int(new_quantity) > 9:
        print("Inventory full")

    if int(new_quantity) < 0:
        print("Invalid quantity")
        
    new_string = {"Name": "" + cube_color + "", "Quantity": "" + new_quantity + ""}
    data[index] = new_string
    file = open("inventory.json", "w+")
    file.write(json.dumps(data))
    file.close()
    
def read_order():
    plockade = 0
    with open("orders.json", "r") as file:
        file_content = json.load(file)
        for i in range(len(file_content)):
            order_string = str(file_content[i])
            
            if "Green" in order_string:
                update_inventory("Green Cube", "green", int(order_string[-3]), "sub", plockade)

            if "Blue" in order_string:
                update_inventory("Blue Cube", "blue", int(order_string[-3]), "sub", plockade)

            if "Yellow" in order_string:
                update_inventory("Yellow Cube", "yellow", int(order_string[-3]), "sub", plockade)

            if "Red" in order_string:
                update_inventory("Red Cube", "red", int(order_string[-3]), "sub", plockade)
                
            plockade += 1
    bot.move_to_relative(0, 0, 10, 0)
