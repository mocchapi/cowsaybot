import discord
import configparser
import csv
import time
import subprocess
import random

bot_token = configparser.ConfigParser()
bot_token.read('bot.secret')

client = discord.Client()

def report_this(success,note):
	with open('log.csv', 'a', newline='') as logcache:
		#time shenanigans
		date = time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")
		wr = csv.writer(logcache, delimiter=',')
		#check if its an error or not (False = error)
		if success == True:
			succeeded = "[ OK ]"
		elif success == False:
			succeeded = "[EROR]"
		#prints & logs the things
		print('<REPORT> [',date,']',succeeded,str(note))
		wr.writerow([date, succeeded,note])
	logcache.close()

def log_this(success,note):
	date = time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")
	if success == True:
		succeeded = "[ OK ]"
	elif success == False:
		succeeded = "[EROR]"
	print('[',date,']',succeeded,str(note))

def remove_prefix(text):
	if text.startswith("cow "):
		return text[len("cow "):]
	else:
		return text

@client.event
async def on_ready():
	log_this(True,"Cow time :)")


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('cow ') or random.randint(1,501) == 1:
		

		test = subprocess.Popen(['cowsay',remove_prefix(message.content)], stdout=subprocess.PIPE)
		cowsay_output = test.communicate()[0]
		#cowsay_output = cow.cowsay(remove_prefix(message.content))
		cowsay_output = str(cowsay_output).replace("\\n",'\n').replace("\\\\","\\")[2:-1]
		if len(cowsay_output) <1992:
			print(cowsay_output)
			await message.channel.send("```"+cowsay_output+"```")
			log_this(True,"said: "+remove_prefix(message.content))
		else:
			await message.channel.send("too long")





try:
	client.run(bot_token.get('Tokens','bot'))
except BaseException as e:
	log_this(False,e)
