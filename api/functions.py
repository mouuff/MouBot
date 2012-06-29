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

def printc(text, color='default'):
	'''output with colors'''
	colortable = {
		'black':		'0;30',		'bright gray':	'0;37',
		'blue':			'1;34',		'white':		'1;37',
		'green':		'1;32',		'red':			'1;31',
		'purple':		'1;35',		'yellow':		'0;33',
		'default':		'0'}
	if system != 'Windows':
		stdout.write("\033[%sm%s\033[0m" % (colortable[color], text))
	else:
		stdout.write(text)#I didn't implemented windows terminal colors for windows sorry
