import time
import serial
import json
import socket

# Change this to your serial port, e.g. COM3
SERIAL_PORT = "/dev/tty.usbserial-10"

SERVER_IP = "10.241.144.172"
SERVER_PORT = 2098

BAUD_RATE = 115200

# We buffer ~100 data points before sending to the server
buffers = {
    "x": [],
    "y": [],
    "z": []
}

while True:
    try:
        print("Opening udp...")
        udp_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Done opening udp")

        def send_data_to_server(channel: str, data: list[str]):
            # Make it look like raspberry shake data
            formatted_message = f"{{'{channel}', {str(time.time())}, {', '.join(data)}}}"
            # Convert to binary
            message_binary = formatted_message.encode('utf-8')
            udp_soc.sendto(message_binary, (SERVER_IP, SERVER_PORT))

        print(f"Connecting to serial port {SERIAL_PORT}...")
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        ser.close()
        print("Half way there...")
        # We need to close and reopen for the sensor to cooperate
        time.sleep(1)
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        print("Done connecting to serial port")

        # lines_so_far = 0
        while True:
            try:
                line = ser.readline().decode('ascii')
                x, y, z = line.strip().split(",")
                buffers["x"].append(x)
                buffers["y"].append(y)
                buffers["z"].append(z)

                # We buffer 10 samples before sending it off
                if len(buffers["x"]) >= 10:
                    print(x,y,z)
                    try:
                        send_data_to_server("x", buffers["x"])
                        send_data_to_server("y", buffers["y"])
                        send_data_to_server("z", buffers["z"])
                        print("Sent data to server")
                    except Exception as err:
                        print("Error sending data: ",err)
                        
                    buffers["x"] = []
                    buffers["y"] = []
                    buffers["z"] = []

            except Exception as err:
                print("Error reading line: ",err)
       
            
    except Exception as err:
        print(err)
        print("Oh well. Starting over in 5s")
        time.sleep(5)
