#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import stdout
from os import _exit
from atexit import register
from threading import Thread
from socket import error
from platform import system
import api.moubot
import api.functions

def printc(text, color='default'):
	'''output with colors'''
	colortable = {
		'black':		'0;30',		'bright gray':	'0;37',
		'blue':			'1;34',		'white':		'1;37',
		'green':		'1;32',		'red':			'1;31',
		'purple':		'1;35',		'yellow':		'0;33',
		'default':		'0'}
	if (system() != 'Windows'):
		stdout.write("\033[%sm%s\033[0m" % (colortable[color], text))
	else:
		stdout.write(text)#I didn't implemented windows terminal colors for windows sorry

def clean_exit():
	'''just close the socket and kill threads before quitting'''
	printc("\n[*] quitting\n", "purple")
	try:
		del bot
	except NameError:
		pass
	printc("Done!\n")
	_exit(0)


def ircloop():
	'''
	loop which wait data and execute functions
	you must declare a global bot before with api.moubot.moubot'''
	while (True):
		try:
			bot.get()
			message = bot.get_message()
		except error:
			return 1
		if bot.data == '':
			return 1
		printc("\r%s <%s> %s\n" % (bot.get_channel(), message[0], message[1]), "blue")
		printc("~> ", "red")
		stdout.flush()
		#here you can launch bot functions
		api.functions.basic_options(bot)
	return 0

def main():
	global bot

	bot = api.moubot.moubot()
	register(clean_exit)

	while True:
		try:
			printc("~> ", "red")
			command = raw_input()
		except (KeyboardInterrupt, EOFError):
			clean_exit()

		try:
			com = command.split("&")
			print(getattr(bot, com[0])(*com[1:]))
		except (AttributeError, TypeError, error):
			if (command == 'exit'):
				clean_exit()

			elif (command.split("&")[0] == 'server'):
				bot.connect(*command.split("&")[1:])
				Thread(target=(ircloop)).start()

			elif (command == 'help'):
				help(api.moubot.moubot)
				print("Example:\nserver&irc.server.com\njoin&#channel\nsay&hi\nreset\nnick&nickname")

			else:
				if (hasattr(bot, com[0])):
					printc("More arguments needed.\n", "blue")
				else:
					try:    
						bot.say(command)
					except error:
						printc("Connect yourself to a server or a channel, type help for help\n")
	return 0

if __name__ == '__main__':
	printc("MOUBOT & MOUCLIENT VERSION BETA 1.0\ntype help for help :)\n%s\n" % ("-"*50), "green")
	main()
