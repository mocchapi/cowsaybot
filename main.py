import discord
import configparser
import csv
import time
import subprocess
import random
import updater

$updater.update()

bot_config = configparser.ConfigParser()
bot_config.read('bot.secret')

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

def filter_text(text):
	return text.replace("```","").replace('-','').replace('\n','')

def cowsay(message):
	test = subprocess.Popen(['cowsay',remove_prefix(message)], stdout=subprocess.PIPE)
	cowsay_output = test.communicate()[0]
	cowsay_output = str(cowsay_output).replace("\\n",'\n').replace("\\\\","\\")[2:-1]
	cowsay_output = "```"+cowsay_output+"```"
	return cowsay_output

def command_cow(message):
	try:
		filtered_text = filter_text(message)
		cowsay_output = cowsay(filtered_text)
		if len(cowsay_output) <1999:
			print(cowsay_output)
			log_this(True,"said: "+remove_prefix(message.content))
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
		blacklist = str(bot_config.get('Options','blacklist'))

		await message.channel.send(command_cow(remove_prefix(message.content)))
		log_this(True,"from: "+message.author.name+"#"+message.author.discriminator+" with message: "+str(message.content))





try:
	client.run(bot_config.get('Tokens','bot'))
except BaseException as e:
	report_this(False,e)
