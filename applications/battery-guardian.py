#!/usr/bin/env python3

import re
import subprocess
from argparse import ArgumentParser

MINUTES_TO_FORCE_SHUTDOWN = 3


class BatteryStatus:
	PERCENTAGE_REGEX = re.compile('percentage:\s+(?P<percentage>\d{1,3})%')
	CHARGING_REGEX = re.compile('state:\s+(charging|fully\\-charged)')

	LEVEL_LOW = 20
	LEVEL_HIGH = 98

	def __init__(self, percentage, charging):
		self.percentage = percentage
		self.charging = charging

	def is_low(self):
		return (self.percentage <= BatteryStatus.LEVEL_LOW) and (not self.charging)

	def is_almost_charged(self):
		return (self.percentage >= BatteryStatus.LEVEL_HIGH) and self.charging

	@staticmethod
	def parse(output):
		percentage = int(BatteryStatus.PERCENTAGE_REGEX.search(output).group('percentage'))
		charging = BatteryStatus.CHARGING_REGEX.search(output) is not None

		return BatteryStatus(percentage, charging)


def parse_arguments(parser):
	parser.add_argument('-F', '--force', action='store_true',
		help='enforce computer shutdown once battery level is too low')

	return parser.parse_args()


def read_battery_status():
	upower = subprocess.run(['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'], stdout=subprocess.PIPE)
	output = upower.stdout.decode()

	return BatteryStatus.parse(output)


def send_battery_notification(message, critical=False):
	command = ['notify-send']
	if critical:
		command.extend(['-u', 'critical'])
	command.extend(['Battery Guardian', message])

	subprocess.run(command)


def turn_off_computer():
	subprocess.run(['shutdown', '-P', '+' + str(MINUTES_TO_FORCE_SHUTDOWN)])


def main():
	description = '''Check battery level and notify if it is too low (<={}%) or too high (>={}%)'''.format(
		BatteryStatus.LEVEL_LOW, BatteryStatus.LEVEL_HIGH)
	args = parse_arguments(ArgumentParser(description=description))

	battery = read_battery_status()

	if battery.is_low():
		if args.force:
			send_battery_notification('Battery level is too low: {}%. Computer will be shutdown in {} minutes.'.format(
				battery.percentage, MINUTES_TO_FORCE_SHUTDOWN), critical=True)
			turn_off_computer()
		else:
			send_battery_notification('Battery level is getting low: {}%'.format(battery.percentage), critical=True)

	elif battery.is_almost_charged():
		send_battery_notification('Battery level is almost full: {}%. Please turn off charging.'.format(
			battery.percentage))


if __name__ == '__main__':
	main()
