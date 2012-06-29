#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import stdout
from os import _exit
from atexit import register
from threading import Thread
from socket import error
import api.moubot
import api.functions

def clean_exit():
	'''just close the socket and kill threads before quitting'''
	api.functions.printc("\n[*] quitting\n", "purple")
	try:
		del bot
	except NameError:
		pass
	api.functions.printc("Done!\n")
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
		api.functions.printc("\r<%s> %s\n" % (message[0], message[1]), "blue")
		api.functions.printc("command~> ", "red")
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
			api.functions.printc("command~> ", "red")
			command = raw_input()
		except (KeyboardInterrupt, EOFError):
			clean_exit()

		try:
			com = command.split("&")
			print(getattr(bot, com[0])(*com[1:]))
		except (AttributeError, TypeError):
			if (command == 'exit'):
				clean_exit()

			elif (command.split("&")[0] == 'server'):
				bot.connect(*command.split("&")[1:])
				Thread(target=(ircloop)).start()

			elif (command == 'help'):
				help(api.moubot.moubot)
				print("Example:\nserver&irc.server.com\njoin&#channel\nsay&hi\n&reset&nick nickname")

			else:
				print("[*] command not found try 'help'")
	return 0

if __name__ == '__main__':
	api.functions.printc("MOUBOT & MOUCLIENT VERSION BETA 1.0\ntype help for help :)\n%s\n" % ("-"*50), "green")
	main()
