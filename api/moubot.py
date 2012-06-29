from mouirc import *
from socket import socket, error, AF_INET, SOCK_STREAM


class moubot:
	def __init__(self):
		self.irc = socket(AF_INET, SOCK_STREAM)
		self.focused_channel = ''
		self.connecte = False
		self.muted = False
		self.actives_channels = []
		self.nick = "moubot"

	def __del__(self):
		self.irc.close()
		self.connecte = False

	def connect(self, address, port=6667):
		'''connect to the server'''
		try:
			self.irc.connect((address, int(port)))
			self.connecte = True
			nick(self.irc, self.nick)
			send_raw(self.irc, 'USER MOU raps mouu :Python IRC bot\r\n')
		except (error):
			self.connecte = False

	def reset(self):
		try:
			self.irc.close()
		except error:
			pass
		self.irc = socket(AF_INET, SOCK_STREAM)
		self.actives_channels = []
		self.focused_channel = ''

	def get(self):
		try:
			self.data = get_data(self.irc)
		except (error):
			self.irc.close()
		if self.data[:4] == 'PING':
			send_raw(self.irc, 'PONG %s\r\n' % self.data[5:])
		else:
			return self.data

	def cycle(self, channel):
		self.part(channel)
		self.join(channel)

	def join(self, channel):
		self.focused_channel = channel
		if channel not in self.actives_channels:
			join(self.irc, channel)
			self.actives_channels.append(channel)
	
	def part(self, channel):
		if channel in self.actives_channels:
			part(self.irc, channel)
			self.actives_channels.remove(channel)

	def reply(self, message):
		if not self.muted:
			send_message(self.irc, message, catch_channel_by_message(self.data))

	def say(self, message_to_send):
		'''Send a message to the focused channel'''
		if not self.muted:
			send_message(self.irc, message_to_send, self.focused_channel)
	
	def mute(self):
		self.muted = True
	
	def unmute(self):
		self.muted = False

	def nick(self, nick):
		'''Change nickname'''
		self.nick = nick
		nick(self.irc, nick)
	
	def raw(self, raw):
		send_raw(self.irc, raw)
	
	def topic(self, topic):
		topic(self.irc, topic, self.focused_channel)
		
	def kick(self, nick, why='stfu', channel=''):
		if channel == '':
			channel = self.focused_channel
		kick(self.irc, nick, channel, why)
	
	def mode(self, mode, channel='', nick=''):
		if channel == '':
			channel = self.focused_channel
		if nick != '':
			nick = ' '+nick
		mode(self.irc, mode, channel, nick)
	
	def get_nick(self):
		return get_nick(self.data)
	
	def get_message(self):
		return [get_nick(self.data), get_message(self.data)]
		
	def catch_host(self, nick):
		return catch_host(self.data)

if __name__ == '__main__':
	'''simple example of this lib'''
	xbot = moubot()
	server = raw_input("server: ")
	channel = "#" + raw_input("channel #")
	xbot.connect(server)
	xbot.join(channel)
	while 1:
		xbot.get()
		nick, message = xbot.get_message()
		print(nick+" : "+message)
