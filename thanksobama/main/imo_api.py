import socket
import struct
import json
from lxml import html
import requests
from time import sleep

class IMOInterface(object):
	def __init__(self):
		self.sock = socket.create_connection(('66.252.70.188', 42011))
		self.sock.settimeout(2)
		self.orgID = 'd03b26e60936db9f'
		self.expiry_workaround = True

	def get_imo_from_icd10(self, icd10_code):
		self.sock.send("search^1|0|2|1^%s^%s\n" % (icd10_code, self.orgID))
		sleep(0.25)
		L = struct.unpack('!I', self.sock.recv(4))[0]
		data = self.sock.recv(L)
		data = json.loads(data)
		if self.expiry_workaround and len(data['data']['items']):
			data['data']['items'] = data['data']['items'][1:]
		if len(data['data']['items']):
			return data['data']['items'][0]['title']
		else:
			return None
