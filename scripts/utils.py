import os, sys
import json
import paramiko
import time
from prettytable import PrettyTable


"""
	Grabs default robot name from jibo-cli
"""
def get_robot_name():
	robot_name = os.popen("jibo robot-list | grep '*'").read().rstrip()
	robot_name = robot_name.split(' ')[-1]
	return robot_name


"""
	Uses ssh connection to run wifi tool on robot.
	Copies output.json from robot to local machine.
"""
def run_tool(path, robot_name):
	username = 'root'
	password = 'jibo'
	src = '/opt/.spooky_spy_stuff/robot_wifi_info.json'

	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=robot_name, username=username, password=password)

	scan_wifi = 'python /opt/jibo/wifi-util/robot_wifi_info.py'
	ssh_client.exec_command(scan_wifi)

	time.sleep(3)
	copy_file = 'sshpass -p "{}" rsync -auv {}@{}:{} {}'.format(password, username, robot_name, src, path)
	os.system(copy_file)


"""
	Grabs bssid's and signals from json file.
"""
def print_signals(path, target_ssid):
	with open(path, 'r') as file:
		data = json.load(file)

	for scan in data:
		if scan == 'ethtool_statistics':
			table = PrettyTable(['BSSID', 'Signal'])
			signal = data[scan]['signal']
			cmd = data[scan]['cmd']

			print('\n\n****** Ethtool Statistics ******')
			print(cmd)
			print('\n')
			table.add_row(['N/a', signal])
			print(table)

		elif scan == 'wifi_station_dump':
			table = PrettyTable(['BSSID', 'Signal'])
			cmd = data[scan]['cmd']
			bssid = data[scan]['bssid']
			signal = data[scan]['signal']

			print('\n\n****** Wifi Station Dump ******')

			print(cmd)
			print('\n')
			table.add_row([bssid, signal])
			print(table)

		elif scan == 'iw_scan':
			table = PrettyTable(['BSSID', 'Signal'])
			cmd = data[scan]['cmd']


			print('\n\n****** IW Scan ******')

			print(cmd)
			print('\n')

			for bss in data[scan]['bss_objects']:
				ssid = bss['ssid']
				if ssid == target_ssid:
					signal = bss['signal']
					bssid = bss['bssid']
					table.add_row([bssid, signal])
			print(table)

		elif scan == 'link_info':
			table = PrettyTable(['BSSID', 'Signal'])
			cmd = data[scan]['cmd']
			bssid = data[scan]['bssid']
			signal = data[scan]['signal']

			print('\n\n****** Link Info ******')
			print(cmd)
			print('\n')
			table.add_row([bssid, signal])
			print(table)
			print('\n')


def main():
	path = sys.argv[1]
	ssid = sys.argv[2]

	if not os.path.exists(path):
		os.system('mkdir logs')

	robot_name = get_robot_name()
	run_tool(path, robot_name)
	print_signals(path, ssid)


if __name__ == "__main__":
	main()
