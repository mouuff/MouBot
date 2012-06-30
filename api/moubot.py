from mouirc import *
from socket import socket, error, AF_INET, SOCK_STREAM


class moubot:
	def __init__(self):
		self.irc = socket(AF_INET, SOCK_STREAM)
		self.focused_channel = ''
		self.connecte = False
		self.muted = False
		self.actives_channels = []
		self.xnick = "moubot"

	def __del__(self):
		self.irc.close()
		self.connecte = False

	def connect(self, address, port=6667):
		'''connect to the server'''
		try:
			self.irc.connect((address, int(port)))
			self.connecte = True
			nick(self.irc, self.xnick)
			send_raw(self.irc, 'USER MOU raps mouu :Python IRC bot\r\n')
		except (error):
			self.connecte = False

	def reset(self):
		'''use that when you get connection errors or if you just want to switch server'''
		try:
			self.irc.close()
		except error:
			pass
		self.irc = socket(AF_INET, SOCK_STREAM)
		self.actives_channels = []
		self.focused_channel = ''

	def get(self):
		'''Get data and manage it'''
		try:
			self.data = get_data(self.irc)
		except (error):
			self.data = ''
			self.irc.close()
		if self.data[:4] == 'PING':
			send_raw(self.irc, 'PONG %s\r\n' % self.data[5:])
		else:
			return self.data

	def cycle(self, channel):
		'''cycle a channel'''
		self.part(channel)
		self.join(channel)
	
	def msg(self, to, message):
		'''send a message'''
		msg(self.irc, to, message)

	def join(self, channel):
		'''join a channel, it will focus on it if you already joinned it'''
		self.focused_channel = channel
		if channel not in self.actives_channels:
			join(self.irc, channel)
			self.actives_channels.append(channel)
	
	def part(self, channel):
		'''part a channel'''
		if channel in self.actives_channels:
			part(self.irc, channel)
			self.actives_channels.remove(channel)
		if channel == self.focused_channel:
			self.focused_channel = ''

	def reply(self, message):
		'''just reply a message'''
		if not self.muted:
			msg(self.irc, catch_channel_by_message(self.data), message)

	def say(self, message_to_send):
		'''Send a message to the focused channel
		tips: to focus a channel just join one'''
		if not self.muted:
			msg(self.irc, self.focused_channel, message_to_send)
	
	def mute(self):
		'''mute the bot'''
		self.muted = True
	
	def unmute(self):
		'''unmute the bot'''
		self.muted = False

	def nick(self, xnick):
		'''Change nickname'''
		self.xnick = xnick
		nick(self.irc, self.xnick)

	def raw(self, raw):
		'''send raw data to the server'''
		send_raw(self.irc, raw)

	def topic(self, topic, channel=''):
		'''set topic'''
		if channel == '':
			channel = self.focused_channel
		topic(self.irc, topic, channel)

	def kick(self, nick, why='stfu', channel=''):
		'''kick somebody'''
		if channel == '':
			channel = self.focused_channel
		kick(self.irc, nick, channel, why)

	def mode(self, mode, channel='', nick=''):
		'''set channel and users modes'''
		if channel == '':
			channel = self.focused_channel
		if nick != '':
			nick = ' '+nick
		mode(self.irc, mode, channel, nick)
	
	def get_channel(self):
		return catch_channel_by_message(self.data)

	def get_nick(self):
		'''returns the nick of the message'''
		return get_nick(self.data)
	
	def get_message(self):
		'''returns the last message and the nick in a list'''
		return [get_nick(self.data), get_message(self.data)]
		
	def catch_host(self):
		'''get the hostname of the data nick'''
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
