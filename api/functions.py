
from sys import stdout
from platform import system

def basic_options(bot):
	'''Simple example of implementation of fonctions for moubot'''
	nick, message = bot.get_message()
	if (message[:6] == '!ascii'):
		try:
			bot.reply(message[7:].encode("hex"))
		except TypeError:
			bot.reply("Error")
	elif (message[:4] == '!hex'):
		try:
			bot.reply(message[5:].replace(" ", "").decode("hex"))
		except TypeError:
			bot.reply("Error")
	else:
		pass
