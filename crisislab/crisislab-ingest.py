import time
import serial
import json
import socket

SERIAL_PORT = "/dev/ttyUSB0"

SERVER_IP = "10.241.144.172"
SERVER_PORT = 2098


while True:
    try:
        print("Opening udp...")
        udp_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Done opening udp")

        def send_data_to_server(channel: str, data: list[int]):
            # Make it look like raspberry shake data
            formatted_message = f"{{'{channel}', {str(time.time())}, {', '.join([str(s) for s in data])}}}"
            # Convert to binary
            message_binary = formatted_message.encode('utf-8')
            udp_soc.sendto(message_binary, (SERVER_IP, SERVER_PORT))

        print(f"Connecting to serial port {SERIAL_PORT}...")
        ser = serial.Serial(SERIAL_PORT, 9600)
        ser.close()
        print("Half way there...")
        # We need to close and reopen for the sensor to cooperate
        time.sleep(1)
        ser = serial.Serial(SERIAL_PORT, 9600)
        print("Done connecting to serial port")

        lines_so_far = 0
        while True:
            line = ser.readline().decode('ascii')
            # print(">"+line.replace("\n", ">\n").strip())

            # Send dummy wifi name & password
            if lines_so_far < 2:
                lines_so_far+=1
                ser.write("no_wifi_pls".encode('ascii'))
                continue

            # parse data packets
            try:
                data = json.loads(line)
                if "x" in data:
                    # Crisis Lab X-axis
                    send_data_to_server("CLX", data["x"])
                    
                if "y" in data:
                    # Crisis Lab Y-axis
                    send_data_to_server("CLY", data["y"])
                    
                if "z" in data:
                    # Crisis Lab Z-axis
                    send_data_to_server("CLZ", data["z"])
                
            except Exception as err:
                pass
            
    except Exception as err:
        print(err)
        print("Oh well. Starting over in 5s")
        time.sleep(5)
