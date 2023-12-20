import time
import serial
import json
import socket

SERIAL_PORT = "/dev/cu.usbserial-110"

SERVER_IP = ""
SERVER_PORT = ""


while True:
    try:
        print("opening udp")
        udp_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("done with opening udp")

        def send_data_to_server(channel: str, data: list[int]):
            print("Sending data to server...")
            # Make it look like raspberry shake data
            formatted_message = f"{{'{channel}', {str(time.time())}, {', '.join([str(s) for s in data])}}}"
            # Convert to binary
            message_binary = formatted_message.encode('utf-8')
            udp_soc.sendto(message_binary, (SERVER_IP, SERVER_PORT))

        print(f"connecting to serial port {SERIAL_PORT}")
        ser = serial.Serial(SERIAL_PORT, 9600)
        print(f"done connecting to serial port")

        lines_so_far = 0
        while True:
            line = ser.readline().decode('ascii')
            print(f"Serial line:{line}")

            if lines_so_far < 2:
                lines_so_far+=1
                ser.write("no_wifi_pls".encode('ascii'))

            try:
                data = json.loads(line)
                if "x" in data:
                    send_data_to_server("CLX", data["x"])
                    
                if "y" in data:
                    send_data_to_server("CLY", data["y"])
                    
                if "z" in data:
                    send_data_to_server("CLZ", data["z"])
                
            except Exception as err:
                print(err)
                print("oh well. reading next line anyway")
            
    except Exception as err:
        print(err)
        print("oh well. starting over in 5s")
        time.sleep(5)
