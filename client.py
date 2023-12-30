import socket

from guizero import App, TextBox, PushButton
from client_functions import *


def client_program():
    # same ip address as the server
    host = "127.0.0.1"
    # same port as the server
    port = 5000
    client_file_writer("starting client")
    client_socket = socket.socket()
    # connect to the server
    client_file_writer("connecting to server")
    client_socket.connect((host, port))

    def start_belt_button_action():
        color_reset()
        start_belt_button.text_color = "blue"
        client_socket.send("set_belt(\"on\")".encode())
        client_file_writer("starting belt")

    def restock_button_action():
        color_reset()
        delivery_button.text_color = "blue"
        send_string = "start_restock(" + str(get_inventory()) + ")"
        set_restock(1)
        client_file_writer("starting restock")
        action_text_box_action(1)
        client_socket.send(send_string.encode())
        client_file_writer("waiting for server to finish restocking")
        data = ""
        while not data.__contains__("done"):
            data = client_socket.recv(1024).decode()
        set_restock(0)
        client_file_writer("restocking finished")
        action_text_box_action(1)
        inventory_text_box_action()
        return_list = [int(data[5]), int(data[6]), int(data[7]), int(data[8])]
        set_inventory(return_list)
        client_file_writer("Received from server: " + data)

    def stop_belt_button_action():
        color_reset()
        stop_belt_button.text_color = "blue"
        client_socket.send("set_belt(\"off\")".encode())
        client_file_writer("stopping belt")
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
        client_file_writer("Received from server: " + data)

    def left_button_action():
        color_reset()
        left_button.text_color = "blue"
        client_socket.send("set_belt(\"left\")".encode())
        client_file_writer("changing belt direction to left")
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
        client_file_writer("Received from server: " + data)

    def pack_button_action():
        color_reset()
        pack_button.text_color = "blue"
        order_list = get_order()
        if order_list != "Insufficient inventory":
            inventory_list = get_inventory()
            order_string = "move_cube(" + list_to_string(inventory_list) + "," + list_to_string(order_list) + ")"
            print(order_string)
            set_packing(1)
            client_file_writer("starting packing")
            action_text_box_action(1)
            client_socket.send(order_string.encode())
            data = ""
            client_file_writer("waiting for server to finish packing")
            while not data.__contains__("done"):
                data = client_socket.recv(1024).decode()
            set_packing(0)
            client_file_writer("packing finished")
            action_text_box_action(1)
            inventory_text_box_action()
            data = client_socket.recv(1024).decode()  # receive response
            print('Received from server: ' + data)  # show in terminal
            client_file_writer("Received from server: " + data)

        else:
            action_text_box_action(2)
            client_file_writer("Insufficient inventory")

    def right_button_action():
        color_reset()
        right_button.text_color = "blue"
        client_socket.send("set_belt(\"right\")".encode())
        client_file_writer("changing belt direction to right")
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal

    def action_text_box_action(number):
        action_text_box.clear()
        if number == 1:
            action_text_box.append("Action performed\n" + action_status())

        if number == 2:
            action_text_box.append(
                "Action performed\n" + action_status() + "\n" + "Insufficient inventory,\nperform delivery")

    def inventory_text_box_action():
        inventory_text_box.clear()
        inventory_text_box.append("Inventory\nRed:" + str(get_inventory()[0]) +
                                  "          Green:" + str(get_inventory()[1]) + "\nBlue:" + str(
            get_inventory()[2]) + "         Yellow:" +
                                  str(get_inventory()[3]))

    def color_reset():
        app.text_color = "black"

    def action_status():
        if get_packing() == 1:
            return "Packing"
        elif get_delivery() == 1:
            return "Delivering"
        else:
            return "Standby"

    app = App(title="Packningsrobot", layout="grid", width=500, height=350)
    start_belt_button = PushButton(app, width=10, height=4, text="START", grid=[0, 0], command=start_belt_button_action)
    delivery_button = PushButton(app, width=10, height=4, text="START DELIVERY", grid=[0, 1],
                                 command=restock_button_action)

    stop_belt_button = PushButton(app, width=10, height=4, text="STOP", grid=[1, 0], command=stop_belt_button_action)
    pack_button = PushButton(app, width=10, height=4, text="PACK ORDER", grid=[1, 1], command=pack_button_action)
    left_button = PushButton(app, width=10, height=4, text="<", grid=[0, 2], command=left_button_action)
    right_button = PushButton(app, width=10, height=4, text=">", grid=[1, 2], command=right_button_action)
    action_text_box = TextBox(app, width=40, height=8, multiline=True, text="\nAction performed\n" + action_status(),
                              grid=[2, 0])

    inventory_text_box = TextBox(app, width=40, height=8, multiline=True, text="\nInventory\nRed:" +
                                                                               str(get_inventory()[
                                                                                       0]) + "          Green:" + str(
        get_inventory()[1]) + "\nBlue:" + str(get_inventory()[2]) +
                                                                               "         Yellow:" + str(
        get_inventory()[3]), grid=[2, 1])

    app.display()


if __name__ == '__main__':
    client_program()
