#basic irc functions are defined here
#when the first arguement is 'irc' its means you must open a irc socket before and set it as arguement

def get_data(irc, read_buffer=4096):
	'''Wait data from the server'''
	return irc.recv(read_buffer)

def catch_host(data):
	'''Get the ip or hashed ip by the last message'''
	return [data[data.find(":")+1:data.find("!")],data[data.find("@"):data.find(" ")]]

def catch_channel_by_message(data):
	'''Get the channel where the last message was sent'''
	return data[data.find(" #")+1:data.find(" :")]

def get_nick(data):
	'''get the nickname or the person by message'''
	return data[1:data.find('!')]

def get_message(data):
	'''Get message by last data received'''
	return data[data.find(' :')+2:].replace("\r\n", "")

def catch(data, to_catch):
	'''see if people in channel actions
	like nick change or join and part
	example:
	catch('NICK')'''
	to_catch = to_catch.upper()
	if (to_catch in ['NICK', 'JOIN', 'PART']):
		return [data[get_nick(data):data.find("!")], data[data.find(to_catch)+len(to_catch)+1:].replace("\r\n","")]
	return ''
#######################################################################################

def mode(irc, mode, channel, nick=''):
	'''Set modes'''
	irc.send('MODE %s %s %s\r\n' % (channel, mode, nick))

def kick(irc, name, channel, why='killed'):
	'''kick somebody'''
	irc.send('KICK %s %s :%s\r\n' % (channel, name, why))

def topic(irc, topic, channel):
	'''Set channel topic'''
	irc.send("TOPIC %s :%s" % (channel, topic))

def part(irc, channel):
	'''Quit the channel'''
	irc.send('PART %s :part\r\n' % (channel))

def send_raw(irc, raw):
	'''send raw data to the server'''
	irc.send(raw)

def nick(irc, nick):
	'''Change nickname'''
	irc.send('NICK %s\r\n' % nick)

def join(irc, channel):
	'''Join a channel'''
	irc.send('JOIN %s\r\n' % channel)

def send_message(irc, message_to_send, channel):
	'''Send a message to the channel'''
	irc.send('PRIVMSG %s :%s\r\n' % (channel, message_to_send))
