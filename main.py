import discord
import configparser
import csv
import time
import subprocess
import random
import sys
from updater import update

#update()

try:
	bot_config = configparser.ConfigParser()
	bot_config.read('bot.secret')
	blacklist = str(bot_config.get('Options','blacklist'))
except BaseException as e:
	print(e)
	sys.exit()

client = discord.Client()

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

def filter_text(text):
	filtered_text =text.replace("```","").replace('-','').replace('\n','').replace('\\n','')
	if filtered_text == '' or filtered_text == None:
		return "No valid input"
	return filtered_text

def cowsay(message, username=None):
	test = subprocess.Popen(['cowsay',remove_prefix(message)], stdout=subprocess.PIPE)
	cowsay_output = test.communicate()[0]
	cowsay_output = str(cowsay_output).replace("\\n",'\n').replace("\\\\","\\")[2:-1]
	if username == None:
		cowsay_output = "```%s```" % (cowsay_output)
	else:
		cowsay_output = "```%s says:\n%s```" % (username, cowsay_output)
	return cowsay_output

def command_cow(message, username=None):
	try:
		filtered_text = filter_text(message)
		cowsay_output = cowsay(filtered_text, username=username)
		if len(cowsay_output) <1999:
			return cowsay_output
		else:
			return cowsay("Too long")
	except BaseException as e:
		return cowsay("error: "+str(e))




@client.event
async def on_ready():
	print('total guilds:'+str(len(client.guilds)))
	for index,val in enumerate(client.guilds):
		print('['+str(index)+']'+val.name+"\nID:"+str(val.id)+"\n")


@client.event
async def on_message(message):
	if message.author == client.user or message.author.bot:
		return

	if str(message.guild.id) in blacklist:
		print("guild "+message.guild.name+" in blacklist, leaving guild.")
		await message.guild.leave()
		return

	if message.content.startswith('cow ') or random.randint(1,501) == 1:
		log_this(True,"from: "+message.author.name+"#"+message.author.discriminator+" with message: "+str(message.content))
		inputstr =remove_prefix(str(message.content))
		try:
			await message.delete()
		except BaseException as e:
			print(e)
		await message.channel.send(command_cow(inputstr, username=message.author.nick))
		log_this(True,"said: "+command_cow(inputstr))


try:
	client.run(bot_config.get('Tokens','bot'))
except BaseException as e:
	print("[!!!] FATAL ERROR: %s" % e)
