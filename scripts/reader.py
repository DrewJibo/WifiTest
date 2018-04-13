#!/usr/bin/env python3
import os, sys
import json
import paramiko


def print_signals():
	path = sys.argv[1]
	target_ssid = sys.argv[2]

	with open(path, 'r') as file:
		data = json.load(file)

	for scan in data:
		if scan == 'ethtool_statistics':
			print('\n\n****** Ethtool Statistics ******\n\n')

			print(data[scan]['cmd'])
			print('\n')
			print(data[scan]['signal'])

		elif scan == 'wifi_station_dump':
			print('\n\n****** Wifi Station Dump ******\n\n')

			print(data[scan]['cmd'])
			print('\n')
			print(data[scan]['signal'])

		elif scan == 'iw_scan':
			print('\n\n****** IW Scan ******\n\n')

			print(data[scan]['cmd'])
			print('\n')

			for bss in data[scan]['bss_objects']:
				ssid = bss['ssid']
				if ssid == target_ssid:
					print("\nbssid: " + str(bss['bssid']))
					print(bss['signal'])

		elif scan == 'link_info':
			print('\n\n****** Link Info ******\n\n')
			print(data[scan]['cmd'])
			print('\n')
			print(data[scan]['signal'])
			print('\n')


if __name__ == "__main__":
	print_signals()