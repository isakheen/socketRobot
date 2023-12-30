from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("e-web-7c05b-39c461a6e3ef.json")
firebase_admin.initialize_app(cred)
# used to help action_text_box, [delivery, packing], 0 = no, 1 = yes
action_status = [0, 0]


# writes to our client log file
def client_file_writer(string_to_write):
    # current date and time
    now = datetime.now()

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    with open("client_log_file.txt", "a") as file:
        file.write(dt_string + "\n" + string_to_write + "\n\n")
    file.close()


def set_restock(number):
    action_status[0] = number


def get_delivery():
    return action_status[0]


def set_packing(number):
    action_status[1] = number


def get_packing():
    return action_status[1]


def list_to_string(list_to_convert):
    return_string = "["
    for i in range(len(list_to_convert)):
        if i != 3:
            return_string += str(list_to_convert[i]) + ","
        else:
            return_string += str(list_to_convert[i]) + "]"
    return return_string


# takes a list [r,g,b,y] and updates the inventory accordingly
def set_inventory(new_values):
    db = firestore.client()
    color = db.collection(u'inventory').document(u'red')
    color.set({
        u'quantity': new_values[0]
    })

    db = firestore.client()
    color = db.collection(u'inventory').document(u'green')
    color.set({
        u'quantity': new_values[1]
    })

    db = firestore.client()
    color = db.collection(u'inventory').document(u'blue')
    color.set({
        u'quantity': new_values[2]
    })

    db = firestore.client()
    color = db.collection(u'inventory').document(u'yellow')
    color.set({
        u'quantity': new_values[3]
    })


# retrieves the inventory and returns it in a list
def get_inventory():
    inv_list = [0, 0, 0, 0]
    db = firestore.client()
    # gets specified document
    color = db.collection(u'inventory').document(u'red').get()
    color_string = str(color.to_dict())
    # saves the specific index with the quantity in the list
    inv_list[0] = int(color_string[-2])

    db = firestore.client()
    color = db.collection(u'inventory').document(u'green').get()
    color_string = str(color.to_dict())
    inv_list[1] = int(color_string[-2])

    db = firestore.client()
    color = db.collection(u'inventory').document(u'blue').get()
    color_string = str(color.to_dict())
    inv_list[2] = int(color_string[-2])

    db = firestore.client()
    color = db.collection(u'inventory').document(u'yellow').get()
    color_string = str(color.to_dict())
    inv_list[3] = int(color_string[-2])

    return inv_list


# gets the earliest order from the database and adds it to a list, which is returned
def get_order():
    # flag to indicate if the inventory is insufficient or not
    inv_flag = 0
    order_list = [0, 0, 0, 0]
    db = firestore.client()
    orders = db.collection(u'orders').get()
    document_name = orders[0].id

    orders = db.collection(u'orders').document(document_name).get()
    order_data = orders.to_dict()
    order_items = order_data.get('items', [])

    # iterates trough items in the order and adds the quantity of each item to the list
    for item in order_items:
        item_name = (item.get('name') or '').lower()
        item_qty = (item.get('item') or '')
        if item_name == "red":
            order_list[0] = int(order_list[0]) + item_qty
        if item_name == "green":
            order_list[1] = int(order_list[1]) + item_qty
        if item_name == "blue":
            order_list[2] = int(order_list[2]) + item_qty
        if item_name == "yellow":
            order_list[3] = int(order_list[3]) + item_qty

    for i in range(len(order_list)):
        if get_inventory()[i] < int(order_list[i]):
            inv_flag = 1

    if inv_flag == 0:
        # delete order from database
        db.collection(u'orders').document(document_name).delete()
        return order_list

    return "Insufficient inventory"
