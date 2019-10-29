import urllib.request
import configparser
import sys


def update(manualupdate=False):
	try:
		config = configparser.ConfigParser()
		config.read('updater.config')
		gitUrl = config.get('Updater','githubraw')
		localfile = config.get('Updater','localfile')
		autoupdate = config.get('Updater','autoupdate')
	except BaseException as e:
		print(e)
		print("generating config file...")
		CreateConfig = open('updater.config','w')
		CreateConfig.write('[Updater]\n')
		CreateConfig.write('githubraw = https://raw.githubusercontent.com/mocchapi/cowsaybot/master/main.py\n')
		CreateConfig.write('localfile = main.py\n')
		CreateConfig.write('autoupdate = True\n')
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
				print("Local - Github mismatch!")
				if autoupdate == "True" or manualupdate:
					print('autoupdate enabled')
					print("updating...")
					localNew = open(localfile,'w')
					localNew.write(GitCode)
					sys.exit()
				elif autoupdate == "False":
					print('autoupdate disabled')
					print('continueing as usual...')
				else:
					print('autoupdate option unrecognizeable, set to '+autoupdate)
					print('continueing as usual...')
		elif LocalCode == GitCode:
			print("up to date!")
		else:
			print("what the fuck")
	except BaseException as e:
		print(e)

if __name__ == "__main__":
	print('starting manual update')
	update(manualupdate=True)
