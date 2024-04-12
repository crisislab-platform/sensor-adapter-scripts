import sys
from obspy.clients.seedlink.easyseedlink import create_client
import socket as s

SENSOR_IP = "169.254.139.7"
SEEDLINK_PORT = "18000"
NETWORK_ID="SS"
STATION_ID = "DEM2"
CHANNEL_SELECTOR = 'HN?'

SERVER_IP = "10.241.144.172"
SERVER_PORT = 2098

udp_soc = s.socket(s.AF_INET, s.SOCK_DGRAM)
print("UDP opened")

def udp_sender(self, channel, timestamp, data):
	#this function sends data to the server for live graphs
	# print("Sending data to server...")
	# Make it look like raspberry shake data
	formatted_message = f"{{'{channel}', {str(timestamp)}, {', '.join([str(s) for s in data])}}}"
	# Convert to binary
	message_binary = formatted_message.encode('utf-8')
	udp_soc.sendto(message_binary, (SERVER_IP, SERVER_PORT))

def on_data(self, trace):
	self.udp_sender(trace.stats.channel, trace.stats.starttime.timestamp, trace.data)


# Define the SeedLink server parameters
if __name__ == "__main__":
	try:
		# Create a SeedLink client instance
		client = create_client(f"{SENSOR_IP}:{SEEDLINK_PORT}", on_data=on_data)

		streams_xml = client.get_info('STREAMS')
		print(streams_xml)
		# Start the connection to the SeedLink server
		client.select_stream(NETWORK_ID, STATION_ID, CHANNEL_SELECTOR)
		client.run()

	except KeyboardInterrupt:
		print("Keyboard interrupt. Exiting...")
		sys.exit()

	except Exception as e:
		print("An error occurred:", str(e))
		print("Restarting...")