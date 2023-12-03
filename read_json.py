import json


def update_inventory(color, quantity, operation):
    file = open("inventory.json", "r")
    data = json.load(file)
    file.close()
    old_string = str(data[order])
    old_quantity = int(old_string[-3])
    if operation == "add": #if inleverans
        new_quantity = str(old_quantity + quantity)
    if operation == "sub": #if packning
        new_quantity = str(old_quantity - quantity)

    if int(new_quantity) > 9:
        print("Inventory full")

    if int(new_quantity) < 0:
        print("Invalid quantity")
    new_string = {"Name": "" + color + "", "Quantity": "" + new_quantity + ""}
    data[order] = new_string
    file = open("inventory.json", "w+")
    file.write(json.dumps(data))
    file.close()


# Kan läsa både inventory.json och orders.json
with open("orders.json", "r") as file:
    file_content = json.load(file)
    for order in range(len(file_content)):
        order_string = str(file_content[order])
        if "Green" in order_string:
            color = "Green Cube"
            color_quantity = int(order_string[-3])
            update_inventory(color, color_quantity, "sub")

        if "Blue" in order_string:
            color = "Blue Cube"
            color_quantity = int(order_string[-3])
            update_inventory(color, color_quantity, "add")

        if "Yellow" in order_string:
            color = "Yellow Cube"
            color_quantity = int(order_string[-3])
            update_inventory(color, color_quantity, "add")

        if "Red" in order_string:
            color = "Red Cube"
            color_quantity = int(order_string[-3])
            update_inventory(color, color_quantity, "add")

        #print([color, color_quantity])

