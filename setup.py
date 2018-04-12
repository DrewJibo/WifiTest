import os, sys
import shutil


def setup():
	venv_path = os.path.expanduser('~/jibo/WifiTest/venv')

	os.system('git pull origin master')

	if os.path.exists(venv_path):
		print('removing previous venv...')
		shutil.rmtree(venv_path)

	try:
		os.system('pip3 install virtualenv')
	except:
		print("Could not install virtualenv")

	os.system('virtualenv -p python3 venv')
	os.system('source venv/bin/activate; pip install -r requirements.txt')


if __name__ == "__main__":
	setup()