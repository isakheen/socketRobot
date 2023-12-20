import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import RPi.GPIO as GPIO
import time
import json
from time import sleep
from lib.dobot import Dobot
bot = Dobot('/dev/ttyS0')

target_x = 243.64430236816406
target_y = -79.6631088256836
target_z = 10.834213256835938
target = [target_x, target_y, target_z]

belt_x = 242.2924346923828
belt_y = -161.6956329345703
belt_z = 11.776344299316406
belt = [belt_x, belt_y, belt_z]

colorSens_x = 162.2412109375
colorSens_y = -163.2942352294922
colorSens_z = 16.308555603027344
colorSens = [colorSens_x, colorSens_y, colorSens_z]

blue_x = 116.79029083251953
blue_y = -185
blue_z = -47.93147277832031
blue = [blue_x, blue_y, blue_z]

yellow_x = 116.79029083251953
yellow_y = -220
yellow_z = -47.93147277832031
yellow = [yellow_x, yellow_y, yellow_z]

red_x = 116.79029083251953
red_y = -255
red_z = -47.93147277832031
red = [red_x, red_y, red_z]

green_x = 116.79029083251953
green_y = -290
green_z = -47.93147277832031
green = [green_x, green_y, green_z]

curr_x = 0
curr_y = 0
curr_z = 0
curr = [curr_x, curr_y, curr_z]

buffer = 30
plockade = 0

cube_list = [0,0,0,0]

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
        if status == "utlev":
            if plockade == 3:
                bot.move_to_relative(0, (color[1]-curr_pos[1])/3, 0, 0)
                bot.move_to_relative((color[0]-curr_pos[0])-buffer*column, 0, 0, 0)
                bot.move_to_relative(0, (color[1]-curr_pos[1])*2/3, 0, 0)
            
            else:
                bot.move_to_relative(0, (color[1]-curr_pos[1])*2/3+buffer*plockade, 0, 0)
                bot.move_to_relative((color[0]-curr_pos[0]-buffer*column)*3/4, 0, 0, 0)
                bot.move_to_relative(0, (color[1]-curr_pos[1])/3-buffer*plockade, 0, 0)
                bot.move_to_relative((color[0]-curr_pos[0]-buffer*column)/4, 0, 0, 0)
            
        else:
            bot.move_to_relative((color[0]-curr_pos[0]-buffer*column)/3, 0, 0, 0)
            bot.move_to_relative(0, (color[1]-curr_pos[1])/2, 0, 0)
            bot.move_to_relative((color[0]-curr_pos[0]-buffer*column)/3, 0, 0, 0)
            bot.move_to_relative(0, (color[1]-curr_pos[1])/2, 0, 0)
            bot.move_to_relative((color[0]-curr_pos[0]-buffer*column)/3, 0, 0, 0)
            
    elif color == yellow:
        bot.move_to_relative(0, (color[1]-curr_pos[1])/2, 0, 0)
        bot.move_to_relative((color[0]-curr_pos[0])/2, 0, 0, 0)
        bot.move_to_relative(0, (color[1]-curr_pos[1])/2, 0, 0)
        bot.move_to_relative((color[0]-curr_pos[0])/2-buffer*column, 0, 0, 0)
        
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
    if plockade == 3:
        bot.move_to_relative(0, 0, 20, 0)
    bot.move_to_relative(0, 0, target[2]-curr_pos[2]+10, 0)
        
    if color == red or color == green:
        bot.move_to_relative(0, (target[1]-curr_pos[1])/3, 0, 0)
        bot.move_to_relative((target[0]-curr_pos[0])/2, 0, 0, 0)
        bot.move_to_relative(0, (target[1]-curr_pos[1])/3, 0, 0)
        bot.move_to_relative((target[0]-curr_pos[0])/2, 0, 0, 0)
        bot.move_to_relative(0, (target[1]-curr_pos[1])/3-buffer*plockade, 0, 0)
    
    elif color == yellow:
        bot.move_to_relative((target[0]-curr_pos[0])/2, 0, 0, 0)
        bot.move_to_relative(0, (target[1]-curr_pos[1])/3, 0, 0)
        bot.move_to_relative((target[0]-curr_pos[0])/2, 0, 0, 0)
        bot.move_to_relative(0, (target[1]-curr_pos[1])*2/3-buffer*plockade, 0, 0)
        
    else:
        bot.move_to_relative(target[0]-curr_pos[0], 0, 0, 0)
        bot.move_to_relative(0, target[1]-curr_pos[1]-buffer*plockade, 0, 0)
    
    if status == "utlev":
        if plockade == 3:
            bot.move_to_relative(0, 0, -30, 0)
        
        else:
            bot.move_to_relative(0, 0, -10, 0)
            
        bot.interface.set_end_effector_suction_cup(1, 0)
    
def to_target(dest):
    bot.move_to_relative(0, 0, 10, 0)
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
def move_belt(seconds):
    start_time = time.time()
    change_values("on")
    
    while True:
        end_time = time.time()
        if end_time - start_time > seconds:
            change_values("off")
            break

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
        
        printa = bot.interface.sendIR([0xaa,0xaa,0x04,0x8a,0x00,0x02,0x00,0x74])
        if printa[0] == 1:
            change_values("off")
            break
    return status
        
################Funktioner för RPI#############################################        
def check_color():
    status = bot.interface.sendColor([0xaa,0xaa,0x03,0x89,0x00,0x01,0x76])
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
    
def starta_inlev(lista):
    for i in range(4):
        cube_list[i] = lista[i]
    
    print(get_cube_list())
    #color = ["Blue Cube", "Yellow Cube", "Red Cube", "Green Cube"]
    bot.move_to_relative(1, 1, 1, 0)
    to_target(target)
    bot.move_to_relative(0, 0, 10, 0)
    
    while True:
        inv_full = 0
        color_inv_full = 0
        cube_sum = 0
        
        for i in get_cube_list():
            cube_sum += i
            
        print(cube_sum)
        if cube_sum >= 32:
            break
        
        if check_ir() == 1:
            break
        bot.move_to_relative(0, 0, -10, 0)
        bot.interface.set_end_effector_suction_cup(1, 1)
        to_target(colorSens)
        sleep(1)
        colorRead = check_color()
        print(colorRead)
        if colorRead == "red":
            colorRead = red
            index = 0
            if get_cube_list()[index] < 8:
                set_cube_list(0)
            else:
                color_inv_full = 1
                
        if colorRead == "green":
            colorRead = green
            index = 1
            if get_cube_list()[index] < 8:
                set_cube_list(1)
            else:
                color_inv_full = 1
                
        if colorRead == "blue":
            colorRead = blue
            index = 2
            if get_cube_list()[index] < 8:
                set_cube_list(2)
            else:
                color_inv_full = 1
                
        if colorRead == "yellow":
            colorRead = yellow
            index = 3
            if get_cube_list()[index] < 8:
                set_cube_list(3)
            else:
                color_inv_full = 1
        
        if color_inv_full == 0:
            column = get_cube_list()[index]
            to_cube(colorRead,column,"inlev",0)
            
        else:
            to_target(belt)
            bot.interface.set_end_effector_suction_cup(1, 0)
            to_target(target)
            bot.move_to_relative(0, 0, 10, 0)
            
    data = "klar " + list_to_string(get_cube_list())
        
def pack_order(inventory, order):
    plockade = 0
    inventory_list = [0,0,0,0]
    order_list = [0,0,0,0]
    for i in range(4):
        inventory_list[i] = inventory[i]
        order_list[i] = order[i]
    
    if order_list[0] != 0:
        for i in range(order_list[0]):
            
            if plockade >= 4:
                bot.move_to_relative(0, 0, 5, 0)
                move_belt(3)
                plockade = 0
                bot.move_to_relative(1, 1, 1, 0)
                to_target(target)
                
            to_cube(red, inventory_list[0], "utlev", plockade)
            bot.move_to_relative(0, 0, 5, 0)
            inventory_list[0] = inventory_list[0]-1
            order_list[0] = order_list[0]-1
            print(order_list)
            plockade += 1
            
    if order_list[1] != 0:
        for i in range(order_list[1]):
            
            if plockade >= 4:
                bot.move_to_relative(0, 0, 5, 0)
                move_belt(3)
                plockade = 0
                bot.move_to_relative(1, 1, 1, 0)
                to_target(target)
                
            to_cube(green, inventory_list[1], "utlev", plockade)
            bot.move_to_relative(0, 0, 5, 0)
            inventory_list[1] = inventory_list[1]-1
            order_list[1] = order_list[1]-1
            print(order_list)
            plockade += 1
            
    if order_list[2] != 0:
        for i in range(order_list[2]):
            
            if plockade >= 4:
                bot.move_to_relative(0, 0, 5, 0)
                move_belt(3)
                plockade = 0
                bot.move_to_relative(1, 1, 1, 0)
                to_target(target)
                
            to_cube(blue, inventory_list[2], "utlev", plockade)
            bot.move_to_relative(0, 0, 5, 0)
            inventory_list[2] = inventory_list[2]-1
            order_list[2] = order_list[2]-1
            print(order_list)
            plockade += 1
            
    if order_list[3] != 0:
        for i in range(order_list[3]):
            
            if plockade >= 4:
                bot.move_to_relative(0, 0, 5, 0)
                move_belt(3)
                plockade = 0
                bot.move_to_relative(1, 1, 1, 0)
                to_target(target)
                
            to_cube(yellow, inventory_list[3], "utlev", plockade)
            bot.move_to_relative(0, 0, 5, 0)
            inventory_list[3] = inventory_list[3]-1
            order_list[3] = order_list[3]-1
            print(order_list)
            plockade += 1
    
    if order_list == [0,0,0,0]:
        bot.move_to_relative(0, 0, 10, 0)        
        move_belt(3)
        bot.move_to_relative(1, 1, 1, 0)
        to_target(target)
    
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
        
    #file = open("inventory.json", "r")
    #data = json.load(file)
    #file.close()
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
        
    #ew_string = {"Name": "" + cube_color + "", "Quantity": "" + new_quantity + ""}
    #data[index] = new_string
    #file = open("inventory.json", "w+")
    #file.write(json.dumps(data))
    #file.close()
    
def read_order(color, quantity, operation, plockade):
    plockade = 0
    
    if operation == "add": #if inleverans
        to_cube(color,old_quantity,"inlev", plockade)
        new_quantity = str(old_quantity + quantity)
        
    if operation == "sub": #if packning
        for i in range(quantity):
            to_cube(color,old_quantity-i-1,"utlev", plockade)
            new_quantity = str(old_quantity - quantity)
        
            
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
