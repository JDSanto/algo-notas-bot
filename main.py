#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telegram
import listener
from telegram.ext import Updater
from telegram.ext import CommandHandler
import database
import sched, time
import pprint
import json
import threading
import os

s = sched.scheduler(time.time, time.sleep)
updater = Updater(token=os.environ['TOKEN_TELEGRAM_BOT'])

def start(bot, update):
	print update
	bot.send_message(chat_id=update.message.chat_id, text="Usar el comando /link junto a un link del sistema para notificar notas.")


def add_link(bot, update):
	link = update.message.text.split("/link ")[1]
	database.delete_user(update.message.chat_id)
	grades = listener.get_grades(link)
	if len(grades) > 0:
		database.insert_user(update.message.chat_id, str(grades), link)
		bot.send_message(update.message.chat_id, text="Link verificado. \n" + str(grades))
	else:
		bot.send_message(update.message.chat_id, text="Link erroneo.")


def show_grades(bot, update):
	user = database.get_single_user(update.message.chat_id)
	if user == None:
		updater.bot.send_message(chat_id=update.message.chat_id, text="No se encontraron datos (utilizar el comando /link).")
	else:
		grades = user['previous_data']
		updater.bot.send_message(chat_id=update.message.chat_id, 
			text='\n'.join('{}: {}'.format(k.encode('utf-8'),v.encode('utf-8')) for k,v in grades.items()))


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('link', add_link))
updater.dispatcher.add_handler(CommandHandler('vernotas', show_grades))

updater.start_polling()


def check_data(sc):
	try:
		users = database.get_users()
		for user in users:
			new_grades = json.loads(listener.get_grades(user['link']))
			diff = dict()
			for key, value in new_grades.iteritems():
				if key not in user['grades'] or user['grades'][key] != new_grades[key]:
					diff[key] = new_grades[key]
			if len(diff) > 0:
				updater.bot.send_message(chat_id=user['chat'], 
					text='\n'.join('{}: {}'.format(k.encode('utf-8'),v.encode('utf-8')) for k,v in diff.items()))
				database.update_user(user['chat'], json.dumps(new_grades), user['link'])
	except BaseException as e:
		print e

	s.enter(time=900, priority=1, action=check_data, kwargs=(sc,))

def new_task():
	s.enter(time=5, priority=1, action=check_data, kwargs=(s,))
	s.run()

t = threading.Thread(target=new_task, args=()).start()