import os, sys
import time
import utils

def main():
	ssid = sys.argv[1]
	robot_name = get_robot_name()

	path = os.path.expanduser('~/jibo/WifiTest/logs/{}'.format(robot_name))
	
	if not os.path.exists(path):
		os.makedirs(path)

	files = os.listdir(path)
	file_count = len(files)

	filename = 'wifi-scan-{}.json'.format(file_count)
	path_json = '{}/{}'.format(path, filename)

	run_tool(path_json, robot_name)
	print_signals(path_json, ssid, path)


if __name__ == "__main__":
	main()