#basic irc functions are defined here
#when the first arguement is 'irc' its means you must open a irc socket before and set it as arguement

def get_data(irc, read_buffer=4096):
	return irc.recv(read_buffer)

def catch_host(data):
	return [data[data.find(":")+1:data.find("!")],data[data.find("@"):data.find(" ")]]

def catch_channel_by_message(data):
	return data[data.find(" #")+1:data.find(" :")]

def get_nick(data):
	return data[1:data.find('!')]

def get_message(data):
	return data[data.find(' :')+2:].replace("\r\n", "")

def catch(data, to_catch):
	to_catch = to_catch.upper()
	if (to_catch in ['NICK', 'JOIN', 'PART']):
		return [data[get_nick(data):data.find("!")], data[data.find(to_catch)+len(to_catch)+1:].replace("\r\n","")]
	return ''
#######################################################################################

def mode(irc, mode, channel, nick=''):
	irc.send('MODE %s %s %s\r\n' % (channel, mode, nick))

def kick(irc, name, channel, why='killed'):
	irc.send('KICK %s %s :%s\r\n' % (channel, name, why))

def topic(irc, topic, channel):
	irc.send("TOPIC %s :%s" % (channel, topic))

def part(irc, channel):
	irc.send('PART %s :part\r\n' % (channel))

def send_raw(irc, raw):
	irc.send(raw)

def nick(irc, nick):
	irc.send('NICK %s\r\n' % nick)

def join(irc, channel):
	irc.send('JOIN %s\r\n' % channel)

def msg(irc, who, message):
	irc.send("PRIVMSG %s :%s\r\n" % (who, message))
