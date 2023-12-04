import json


def check_inv(color):
    if color == blue:
        index = 0
    if color == yellow:
        index = 1
    if color == red:
        index = 2
    if color == green:
        index = 3
        
    file = open("inventory.json", "r")
    data = json.load(file)
    file.close()
    
    inv_string = str(data[index])
    inv_quantity = int(inv_string[-3])
    return inv_quantity

def update_inventory(cube_color, color, quantity, operation, order):
    if color == blue:
        index = 0
    if color == yellow:
        index = 1
    if color == red:
        index = 2
    if color == green:
        index = 3
        
    file = open("inventory.json", "r")
    data = json.load(file)
    file.close()
    old_string = str(data[index])
    old_quantity = int(old_string[-3])
    loop_range = old_quantity - quantity-1
    print(loop_range)
    if operation == "add": #if inleverans
        for i in range(loop_range):
            to_cube(color,old_quantity-i,"inlev")
        new_quantity = str(old_quantity + quantity)
        
    if operation == "sub": #if packning
        for i in range(loop_range):
            to_cube(color,old_quantity-i-1,"utlev")
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
    with open("orders.json", "r") as file:
        file_content = json.load(file)
        for order in range(len(file_content)):
            order_string = str(file_content[order])
            
            if "Green" in order_string:
                update_inventory("Green Cube", green, int(order_string[-3]), "sub", order)

            if "Blue" in order_string:
                update_inventory("Blue Cube", blue, int(order_string[-3]), "sub", order)

            if "Yellow" in order_string:
                update_inventory("Yellow Cube", yellow, int(order_string[-3]), "sub", order)

            if "Red" in order_string:
                update_inventory("Red Cube", red, int(order_string[-3]), "sub", order)
