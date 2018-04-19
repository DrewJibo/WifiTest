import os, sys
import json
import paramiko
import time
from prettytable import PrettyTable

"""
	Grabs bssid's and signals from json file.
	Creates a new json file with those key-values.
"""
def print_signals(path, target_ssid, new_path):
	new_path = '{}.json'.format(new_path)
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


def main():

	path_dir = sys.argv[1]
	ssid = sys.argv[2]	
	
	path_b = os.path.expanduser('~/jibo/wifi_testing/{}/before.json'.format(path_dir))
	path_save_b = os.path.expanduser('~/jibo/wifi_testing/{}/b_report'.format(path_dir))

	path_a = os.path.expanduser('~/jibo/wifi_testing/{}/after.json'.format(path_dir))
	path_save_a = os.path.expanduser('~/jibo/wifi_testing/{}/a_report'.format(path_dir))

	print_signals(path_b, ssid, path_save_b)
	time.sleep(3)
	print_signals(path_a, ssid, path_save_a)


if __name__ == "__main__":
	main()
