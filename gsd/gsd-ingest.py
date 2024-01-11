import sys
from obspy.clients.seedlink.easyseedlink import EasySeedLinkClient
import socket as s

#ethernet port settings for pi
# interface eth0
# metric 302
# static ip_address=192.168.100.3/24
# #static ip6_address=fd51:42f8:caae:d92e::ff/64
# static routers=192.168.100.1
# static domain_name_servers=192.168.100.1
# #8.8.8.8 fd51:42f8:caae:d92e::1
#
# interface eth1

SERVER_IP = "10.241.144.172"
SERVER_PORT = 2098

global timestamp

class MyClient(EasySeedLinkClient):
	def __init__(self, connection_address):
		print("Constructor called!")
		self.udp_soc = s.socket(s.AF_INET, s.SOCK_DGRAM)
		print("UDP opened")
		
		super().__init__(connection_address)
		print("SEEDLINK connected")

	def udp_sender(self, channel, timestamp, data):
		#this function sends data to the server for live graphs
		# print("Sending data to server...")
		# Make it look like raspberry shake data
		formatted_message = f"{{'{channel}', {str(timestamp)}, {', '.join([str(s) for s in data])}}}"
		# Convert to binary
		message_binary = formatted_message.encode('utf-8')
		self.udp_soc.sendto(message_binary, (SERVER_IP, SERVER_PORT))
	# Implement the on_data callback
	def on_data(self, trace):
		global timestamp
		# print("STATS of the data: " + str(trace.stats))
		# convert the timestamp to UTC format
		# only get the timestamp for the first data
		timestamp = trace.stats.starttime
		# flag = False
		# print the length of the data
		# print("Original data: " + str(trace.data))
		# if(len(trace.data) == 200):
		#	 data_todb = data_message("CSI", "CS001", timestamp, trace.stats.channel, trace.data)
		#	 tcp_Sender(data_todb)
		# else:
		# print("Data length is not 200")
		# data = data_process(trace)
		# if(len(data) == 200):
		self.udp_sender(trace.stats.channel, timestamp.timestamp, trace.data)
	def on_seedlink_error(self):
		print('Received an error from the SeedLink server')
	def on_info(self, msgtype, content):
		print('Received info message:')
		print(content)
	def close(self):
		print('Connection closed')


# Define the SeedLink server parameters
if __name__ == "__main__":
	try:
		# Create a SeedLink client instance
		client = MyClient('gsd.local:18000')

		# Define the desired station, network, location, and channel codes
		station = 'ABC'  # Replace with the desired station code
		network = 'XY'  # Replace with the desired network code
		location = ''  # Replace with the desired location code
		channel = 'EHZ'  # Replace with the desired channel code

		streams_xml = client.get_info('STREAMS')
		print(streams_xml)
		# Start the connection to the SeedLink server
		# Netowrk code, station code, channel codes
		client.select_stream("GS", "MASB", "HN?")
		client.run()

	except KeyboardInterrupt:
		print("Keyboard interrupt. Exiting...")
		sys.exit()

	except Exception as e:
		print("An error occurred:", str(e))
		print("Restarting the code...")