import os, sys
import shutil


def setup():
	venv_path = os.path.expanduser('~/jibo/WifiTest/venv')
	activate_file = os.path.expanduser('~/jibo/WifiTest/venv/bin/activate_this.py')

	print('\n**** WARNING ****')
	print('This script will overwrite current virtual environment (venv) within this directory.')
	answer = raw_input('Continue? (y/n): ')

	if answer is not 'y':
		print('Quitting...\n')
		sys.exit(0)

	print('\n**** Updating repo ****')
	os.system('git pull origin master')
	print('completed.\n')


	if os.path.exists(venv_path):
		print('\n**** Removing Venv ****')
		shutil.rmtree(venv_path)
		print('completed.\n')

	try:
		print('\n**** Installing Virtualenv ****')
		os.system('pip3 install virtualenv')
		print('completed.\n')
	except:
		print("Error: Could not install virtualenv.\n")

	print('\n**** Creating Venv ****')
	os.system('virtualenv -p python3 venv')
	print('completed.\n')

	print('\n**** Installing Required Packages ****')
	os.system('source venv/bin/activate; pip install -r requirements.txt')
	print('completed.\n')

	print('\n**** Activate Virtualenv ****')
	print('NOTE: press CTRL+D to exit bash.\n')
	os.system('/bin/bash --rcfile venv/bin/activate')


if __name__ == "__main__":
	setup()