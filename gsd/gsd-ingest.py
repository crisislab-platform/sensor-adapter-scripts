import sys
from obspy.clients.seedlink.easyseedlink import create_client
import socket as s
from datetime import datetime,timezone

SENSOR_HOST = "gsd.local"
SEEDLINK_PORT = "18000"
NETWORK_ID="GS"
STATION_ID = "MASB"
CHANNEL_SELECTOR = 'HN?'

SERVER_IP = "10.241.144.172"
SERVER_PORT = 2098

udp_soc = s.socket(s.AF_INET, s.SOCK_DGRAM)
print("UDP opened", flush=True)

counter = 0
def udp_sender(channel, timestamp, data):
	global counter
	# This function sends data to the server for live graphs

	# Make it look like raspberry shake data
	formatted_message = f"{{'{channel}', {str(timestamp)}, {', '.join([str(s) for s in data])}}}"
	# Convert to binary
	message_binary = formatted_message.encode('utf-8')
	udp_soc.sendto(message_binary, (SERVER_IP, SERVER_PORT))
	counter += 1
	if counter >= 100:
		counter = 0
		print(f"[{datetime.now(timezone.utc)}] Sent data to server. Packet sample: {formatted_message}", flush=True)

def on_data(trace):
	udp_sender(trace.stats.channel, trace.stats.starttime.timestamp, trace.data)


# Define the SeedLink server parameters
if __name__ == "__main__":
	try:
		# Create a SeedLink client instance
		client = create_client(f"{SENSOR_HOST}:{SEEDLINK_PORT}", on_data=on_data)

		streams_xml = client.get_info('STREAMS')
		print(streams_xml, flush=True)
		# Start the connection to the SeedLink server
		client.select_stream(NETWORK_ID, STATION_ID, CHANNEL_SELECTOR)
		client.run()

	except KeyboardInterrupt:
		print("Keyboard interrupt. Exiting...", flush=True)
		sys.exit()

	except Exception as e:
		print("An error occurred:", str(e), flush=True)
		print("Restarting...", flush=True)