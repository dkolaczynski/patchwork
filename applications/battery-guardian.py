#!/usr/bin/env python3

import re
import subprocess
from argparse import ArgumentParser


class BatteryStatus:
	PERCENTAGE_REGEX = re.compile('percentage:\s+(?P<level>\d{1,3})%')
	CHARGING_REGEX = re.compile('state:\s+charging')

	def __init__(self, percentage, charging):
		self.percentage = percentage
		self.charging = charging

	@staticmethod
	def parse(output):
		# parse percentage
		battery_percentage = BatteryStatus.PERCENTAGE_REGEX.search(output).group('level')
		percentage = int(battery_percentage)

		# parse charging
		charging = BatteryStatus.CHARGING_REGEX.search(output) is not None

		return BatteryStatus(percentage, charging)


def parse_arguments(parser):
	parser.add_argument('-F', '--force', action='store_true', help='TODO')
	return parser.parse_args()


def read_battery_status():
	command = ['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0']
	completed_process = subprocess.run(command, stdout=subprocess.PIPE)
	completed_process_output = completed_process.stdout.decode()

	return BatteryStatus.parse(completed_process_output)


def send_battery_notification(message, critical=False):
	command = ['notify-send']
	if critical:
		command.extend(['-u', 'critical'])
	command.extend(['Battery Guardian', message])

	subprocess.run(command)


def turn_off_computer():
	pass


def main():
	args = parse_arguments(ArgumentParser(description=''))
	battery = read_battery_status()
	if battery.percentage < 21 and not battery.charging:
		send_battery_notification('Battery is getting low: {}'.format(battery.percentage), critical=True)
		if battery.percentage < 16 and args.force:
			turn_off_computer()
	elif battery.percentage >= 98 and battery.charging:
		send_battery_notification('Battery is almost full: {}. Please turn off charging'.format(battery.percentage))


if __name__ == '__main__':
	main()
