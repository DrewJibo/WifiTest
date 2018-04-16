import os
import json
import paramiko
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
	Copies robot_wifi_info.json from robot to local machine.
"""
def run_tool_robot(path, robot_name):
	username = 'root'
	password = 'jibo'
	src = '/opt/.spooky_spy_stuff/robot_wifi_info.json'

	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=robot_name, username=username, password=password)

	scan_wifi = 'python /opt/jibo/wifi-util/robot_wifi_info.py'
	stdin, stdout, stderr = ssh_client.exec_command(scan_wifi)

	exit_status = stdout.channel.recv_exit_status()
	if exit_status == 0:
		print("Scanning complete.")
		ftp_client = ssh_client.open_sftp()
		ftp_client.get(src, path)
		ftp_client.close()
	else:
		print("Error", exit_status)

	ssh_client.close()


"""
	Runs local wifi tool.
	Copies robot_wifi_info.json from output directory into logs
"""
def run_tool_local(path):
	src = '~/jibo/utilities/output/robot_wifi_info.json'

	scan_wifi = 'python ~/jibo/utilities/src/robot_wifi_info.py'
	os.system(scan_wifi)

	copy = 'cp {} {}'.format(src, path)
	os.system(copy)


"""
	Grabs bssid's and signals from json file.
	Creates a new json file with those key-values.
"""
def get_signals(path, target_ssid, new_path):
	new_path = '{}/test.json'.format(new_path)
	new_data = {}

	with open(path, 'r') as file:
		data = json.load(file)

	for scan in data:
		if scan == 'ethtool_statistics':
			table = PrettyTable(['BSSID', 'Signal'])
			signal = data[scan]['signal']
			cmd = data[scan]['cmd']
			bssid = None

			print('\n\n****** Ethtool Statistics ******')
			print(cmd)
			print('\n')
			table.add_row([bssid, signal])
			print(table)

			new_data[scan] = {"cmd": cmd, "bssid": bssid, "signal": signal}

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

			new_data[scan] = {"cmd": cmd, "bssid": bssid, "signal": signal}

		elif scan == 'iw_scan':
			table = PrettyTable(['BSSID', 'Signal'])
			cmd = data[scan]['cmd']


			print('\n\n****** IW Scan ******')

			print(cmd)
			print('\n')

			new_data[scan] = {"cmd": cmd, "bss_objects": []}

			for bss in data[scan]['bss_objects']:
				ssid = bss['ssid']
				if ssid == target_ssid:
					signal = bss['signal']
					bssid = bss['bssid']
					table.add_row([bssid, signal])

					new_data[scan]['bss_objects'].append({"bssid": bssid, "signal": signal})

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

			new_data[scan] = {"cmd": cmd, "bssid": bssid, "signal": signal}

		with open(new_path, 'w') as file:
			json.dump(new_data, file, indent=4)
