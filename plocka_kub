import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import math
from time import sleep
from lib.dobot import Dobot

targetx = 170.3140869140625
targety = -2.0460288524627686
targetz = 12.809982299804688
target = [targetx, targety, targetz]

blåx = 53.722923278808594
blåy = -182.7084503173828
blåz = -45.676734924316406
blå = [blåx, blåy, blåz]

rödx = 18.134769439697266
rödy = -184.5638885498047
rödz = -47.45319366455078
röd = [rödx, rödy, rödz]

grönx = -13.706839561462402
gröny = -185.08853149414062
grönz = -46.922271728515625
grön = [grönx, gröny, grönz]

gulx = -47.065704345703125
guly = -185.0820770263672
gulz = -46.32207489013672
gul = [gulx, guly, gulz]

currx = 0
curry = 0
currz = 0
curr = [currx, curry, currz]

buffer = 40


bot = Dobot('/dev/ttyS0')
bot.interface.set_point_to_point_coordinate_params(300,300,300,300)
bot.interface.set_ir_switch(2, 1, 2, 1)

printa = bot.interface.send1([0xaa,0xaa,0x04,0x8a,0x00,0x02,0x00,0x74])
print(printa)
printa2 = bot.interface.send1([0xaa,0xaa,0x02,0x89,0x00,0x00,0x00,0x77])
print(printa2)
#bot.home()

def getcurrpos():
    pos = bot.get_pose()
    currx = pos[0]
    curry = pos[1]
    currz = pos[2]
    curr = [currx, curry, currz]
    return curr

def flyttakub(färg, col, dest):
    tillkub(färg, col)
    frånkub(dest, col)

def tillkub(färg, col):
    currpos = getcurrpos()
    bot.move_to_relative(0, 0, 10, 0)


    bot.move_to_relative(0, färg[1]-currpos[1], 0, 0)
    bot.move_to_relative(färg[0]-currpos[0], 0, 0, 0)
    bot.move_to_relative(0, 0, färg[2]-currpos[2], 0)
    
    if col != 0:
        bot.move_to_relative(0, -buffer*col, 0, 0)
    
    bot.move_to_relative(0, 0, -10, 0)
    
    bot.interface.set_end_effector_suction_cup(1, 1)

def frånkub(dest, col):
    currpos = getcurrpos()
    bot.move_to_relative(0, 0, dest[2]-currpos[2]+30, 0)
    
    if col != 0:
        bot.move_to_relative(0, buffer*col, 0, 0)

    bot.move_to_relative(dest[0]-currpos[0], 0, 0, 0)

    bot.move_to_relative(0, dest[1]-currpos[1]-buffer*col, 0, 0)
        
    bot.move_to_relative(0, 0, -30, 0)
    
    bot.interface.set_end_effector_suction_cup(1, 0)
    
    bot.move_to_relative(0, 0, 30, 0)
    
#flyttakub(target, 0, blå)



