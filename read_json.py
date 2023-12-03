import json

# Kan läsa både inventory.json och orders.json
with open("orders.json", "r") as file:
    file_content = json.load(file)
    for order in range(len(file_content)):
        order_string = str(file_content[order])
        if "Green" in order_string:
            color = "green"
            color_quantity = order_string[-3:-2]

        if "Blue" in order_string:
            color = "blue"
            color_quantity = order_string[-3:-2]

        if "Yellow" in order_string:
            color = "yellow"
            color_quantity = order_string[-3:-2]

        if "Red" in order_string:
            color = "red"
            color_quantity = order_string[-3:-2]

        print([color, color_quantity])
