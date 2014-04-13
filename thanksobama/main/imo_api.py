import socket
import struct
import json
from time import sleep

class IMOInterface(object):
	def __init__(self):
		self.sock = socket.create_connection(('66.252.70.188', 42011))
		self.sock.setblocking(1)
		self.orgID = 'd03b26e60936db9f'
		self.expiry_workaround = True

	def get_imo_from_query(self, query):
		self.sock.send("search^1|0|2|1^%s^%s\n" % (query, self.orgID))
		sleep(0.25)
		L = struct.unpack('!I', self.sock.recv(4))[0]
		data = self.sock.recv(L)
		data = json.loads(data)
		if self.expiry_workaround and len(data['data']['items']):
			data['data']['items'] = data['data']['items'][1:]
		if len(data['data']['items']):
			x = data['data']['items'][0]
			return x['title']
		else:
			return None

