# ------------------------------------------
# --- Author: Chanthujan Chandrakumar
# --- Date: 7th July 2023
# --- Python Ver: 3.8
# ------------------------------------------
import sys
# Make sure python-socketio is installed with a version that starts with `4`.
# E.g. version `4.6.1`
from datetime import datetime, time
import socketio
import time as t
import requests
import _thread
import json
import socket as s


ip = "169.254.88.193" #input("Sensor IP (without port): ")
port_x =  "8002" #input("Datastream port (8000, 8002, 8004): ")
port_y = "8004"
port_z = "8000"

SERVER_IP = "10.241.144.172"
SERVER_PORT = 2098

# We need to send a post request to this url before the
# server will agree to connect
r = requests.post(f"http://{ip}/view/autostart.php")
print(r.status_code)
print(r.headers)


sio_x = socketio.Client()
sio_y = socketio.Client()
sio_z = socketio.Client()

instance = datetime.now().strftime("%Y%m%d_%H%M%S")
outdir = "out/"  # Output directory for the received data and logs
serverLogDir = "P_alert_logs/"  # Output directory for the server logs

log_x= f"{outdir}{serverLogDir}client_log_x.txt"  # Log file for the server
log_y= f"{outdir}{serverLogDir}client_log_y.txt"  # Log file for the server
log_z= f"{outdir}{serverLogDir}client_log_z.txt"  # Log file for the server

log_dir = "logs"

def decimate_array(array, decimation_factor):
    return array[::decimation_factor]
def to_array_func(data_string):
    data_string = str(data_string)
    data_string = data_string.replace("{'date': '400,", "")
    data_string = data_string.rstrip("'}")
    data_list = data_string.split(",")  # Split the string into individual values
    decimation_factor = 4
    downsampled_array = decimate_array(data_list, decimation_factor)
    # Convert each value in the downsampled array to float
    downsampled_array = [float(value) for value in downsampled_array]
    return downsampled_array

def log(logFilePath, logString, threadID):
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    #print(f"{timestamp} \tThread: {threadID} \t{logString}")
    writeToFile(logFilePath, f"{timestamp} \tThread: {threadID} \t{logString}")

def writeToFile(filePath, data):
    with open(filePath, "a") as file:
        file.write(f"{data}\r")

def check_dir():
    import os
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(outdir + serverLogDir):
        os.makedirs(outdir + serverLogDir)


udp_soc = s.socket(s.AF_INET,  s.SOCK_DGRAM)
def udp_Sender(channel, timestamp, data): #this function sends data to the server for live graphs
    # print("Sending data to server...")
    # Make it look like raspberry shake data
    formatted_message = f"{{'{channel}', {str(timestamp)}, {', '.join([str(s) for s in to_array_func(data)])}}}"
    # Convert to binary
    message_binary = formatted_message.encode('utf-8')
    udp_soc.sendto(message_binary, (SERVER_IP, SERVER_PORT))


@sio_x.event
def connect():
    print('Connection established with X axis of the sensor')
    # print the time now when the data is recieved


@sio_x.event
def date(data):
    current_datetime = datetime.now()
    timestamp = current_datetime.timestamp()
    udp_Sender("ENN", timestamp, data)



@sio_x.event
def disconnect():
    print('Disconnected from X AXIS sensor')

@sio_y.event
def connect():
    print('Connection established with Y axis of the sensor')
    # print the time now when the data is recieved


@sio_y.event
def date(data):
    current_datetime = datetime.now()
    timestamp = current_datetime.timestamp()
    udp_Sender("ENE", timestamp, data)



@sio_y.event
def disconnect():
    print('Disconnected from Y AXIS sensor')

@sio_z.event
def connect():
    print('Connection established with Z axis of the sensor')
    # print the time now when the data is recieved

@sio_z.event
def date(data):
    current_datetime = datetime.now()
    timestamp = current_datetime.timestamp()
    udp_Sender("ENZ", timestamp, data)


@sio_z.event
def disconnect():
    print('Disconnected from Z AXIS sensor')



def connect_port_x(ip, port):
    while True:
        try:
            sio_x.connect(f"http://{ip}:{port}")
            sio_x.wait()
        except (ConnectionError, socketio.exceptions.ConnectionError):
            print('Connection to X axis sensor failed. Retrying...')
            time.sleep(2)
        except KeyboardInterrupt:
            print("Keyboard interrupt. Exiting...")
            sys.exit()
def connect_port_y(ip, port):
    while True:
        try:
            sio_y.connect(f"http://{ip}:{port}")
            sio_y.wait()
        except (ConnectionError, socketio.exceptions.ConnectionError):
            print('Connection to Y axis sensor failed. Retrying...')
            time.sleep(2)
        except KeyboardInterrupt:
            print("Keyboard interrupt. Exiting...")
            sys.exit()
def connect_port_z(ip, port):
    while True:
        try:
            sio_z.connect(f"http://{ip}:{port}")
            sio_z.wait()
        except (ConnectionError, socketio.exceptions.ConnectionError):
            print('Connection to Z axis sensor failed. Retrying...')
            time.sleep(2)
        except KeyboardInterrupt:
            print("Keyboard interrupt. Exiting...")
            sys.exit()

if __name__ == "__main__":
    check_dir()
    while True:
        try:
            _thread.start_new_thread(connect_port_x, (ip, port_x))
            _thread.start_new_thread(connect_port_y, (ip, port_y))
            _thread.start_new_thread(connect_port_z, (ip, port_z))
            while True:
                pass
        except KeyboardInterrupt:
            print("Keyboard interrupt. Exiting...")
            tsc_soc.close()
            sys.exit(0)
        except Exception as e:
            print("Exception: ", e)
            tsc_soc.close()
            if failure_start_time is None:
                failure_start_time = time.time()
            elif time.time() - failure_start_time > 10:
                print("Rebooting the sensor...")
                t.sleep(60)  # Wait for the sensor to reboot
            t.sleep(2)
