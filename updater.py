import urllib
import requests
import configparser
import sys


def update():
	try:
		config = configparser.ConfigParser()
		config.read('updater.config')
		gitUrl = config.get('Updater','githubraw')
		localfile = config.get('Updater','localfile')
	except BaseException as e:
		print(e)
		print("generating config file...")
		CreateConfig = open('updater.config','w')
		CreateConfig.write('[Updater]\n')
		CreateConfig.write('githubraw = \n')
		CreateConfig.write('localfile = \n')
		CreateConfig.close()
		sys.exit()

	try:
		try:
			with urllib.request.urlopen(gitUrl) as url:
				GitRaw = url.read()
				GitCode = GitRaw.decode("utf-8").rstrip()
		except BaseException as e:
			print(e)
		try:
			with open(localfile,'r') as LocalRaw:
				LocalCode = LocalRaw.read()
		except BaseException as e:
			print(e)

		if LocalCode != GitCode:
			with open(localfile,'w') as LocalNew:
				print("Local - Github mismatch!")
				print("updating...")
				LocalNew.write(GitCode)
				sys.exit()
		elif LocalCode == GitCode:
			print("up to date!")
		else:
			print("what the fuck")
	except BaseException as e:
		print(e)