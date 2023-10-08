import threading
import socket
import pandas as pd
import pythonosc.parsing.osc_types
from pythonosc import udp_client, dispatcher, osc_server, parsing, osc_message_builder, osc_message
import time
import random

# csv path
csv_path = "gigante roja_Cap4.png.csv"
# Multi Threading declarations
num_quadrants = 4
num_features = 7
num_sections = 25
num_threads = num_quadrants * num_features


# num_iterations is the number of sections (how many times its column changes)
def worker(thread_id, num_iterations, x_index, y_index, df, strip_id, plugin_id, parameter_id):
    acum = 0
    for i in range(0, num_iterations):
        print()
        base_value = df[x_index][y_index + acum]
        # scale_factor = random.uniform(1, 50)
        scale_factor = 35
        new_value = base_value / scale_factor
        new_value = min(10, new_value)
        ardour_client.send_message("/strip/plugin/parameter", [strip_id, plugin_id, parameter_id,
                                                               new_value])
        acum += 1

        print(f"Thread: {thread_id}: strip_id: {strip_id}, plugin_id {plugin_id}, parameter_id: {parameter_id}")
        time.sleep(0.5)


dataframe = pd.read_csv(csv_path, header=None, index_col=None)

# Set up a UDP socket to listen for replies from Ardour
udp_socket_address = ("127.0.0.1", 8000)  # Adjust port as needed
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(udp_socket_address)

# Create a dispatcher to handle OSC messages
dispatcher_instance = dispatcher.Dispatcher()
dispatcher_instance.map("/strip/list", print)  # You can replace 'print' with your own callback function


def run_udp_socket():
    try:
        while True:
            data, client_address = udp_socket.recvfrom(1024)
            # print(f"Received raw data from Ardour: {data}")

            # print(len(data))
            index = 0
            reply = []
            while index < len(data) - 1:
                try:
                    data_decoded = pythonosc.parsing.osc_types.get_string(data, index)
                except Exception as e:
                    # print(f"Error decoding OSC message: {e}")
                    break  # Break out of the loop if an error occurs

                index = data_decoded[1]
                reply.append(data_decoded[0])

            # print(reply[len(reply)-1])
            print(reply)
    except KeyboardInterrupt:
        pass
    finally:
        udp_socket.close()


# Start the UDP socket in a separate thread
udp_socket_thread = threading.Thread(target=run_udp_socket)
udp_socket_thread.start()

# Set up the Ardour OSC client
ardour_client = udp_client.SimpleUDPClient("127.0.0.1", 3819)  # Adjust port as needed

# Example: Send an OSC message to query Ardour
ardour_client.send_message("/strip/list", None)
ardour_client.send_message("/strip/plugin/list", 1)
ardour_client.send_message("/strip/plugin/descriptor", [1, 1])

print(dataframe)

threads = []
strip_id = 1
parameter_id = 1
parameters_per_strip = 4

threads_ids = 1
for i in range(0, num_quadrants * num_sections, num_sections):
    for j in range(2, num_features+2):
        thread = threading.Thread(target=worker, args=(threads_ids, num_sections, j, i, dataframe, strip_id, 1, parameter_id))
        threads.append(thread)
        thread.start()
        if parameter_id == parameters_per_strip:
            parameter_id = 0
            strip_id += 1
        parameter_id += 1
        time.sleep(0.25)
        threads_ids += 1


# acum = 0
# while True:
#
#     if acum < 10:
#         acum += 0.1
#     else:
#         acum = 0
#
#     ardour_client.send_message("/strip/plugin/parameter", [1,1,1,acum])
#     time.sleep(0.25)

# Optionally, wait for a response (this is just an example, you may handle replies in a more sophisticated way)
time.sleep(1)

# Stop the UDP socket when done
udp_socket_thread.join()

# Wait for all threads to complete
for thread in threads:
    thread.join()
