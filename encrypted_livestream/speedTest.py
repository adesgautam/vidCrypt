import os
import re
import subprocess
import time
import socket

class SpeedTestResults:
	def __init__(self):
		self.ping = 0
		self.download = 0
		self.upload = 0

	def check_conn(self):
		try:
			socket.create_connection(("www.google.com", 80))
			return True
		except OSError:
			pass
		return False

	def get_results(self):
		if self.check_conn():
			response = str(subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read())
			ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
			download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
			upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

			self.ping = ping[0].replace(',', '.')
			self.download = download[0].replace(',', '.')
			self.upload = upload[0].replace(',', '.')

			# print('{},{},{},{},{}'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping[0], download[0], upload[0]))
			return str(float(self.download)/8), str(float(self.upload)/8), str(float(self.ping)/8)
		else:
			print("No Internet Connection!")
			return _, _, _


# c = SpeedTestResults()
# print(c.get_results())

# import speedtest

# class TestResults:
# 	def __init__(self):
# 		self.ping = 0
# 		self.upload = 0
# 		self.download = 0
# 		self.s = speedtest.Speedtest()


# 	def get_results(self):
# 		self.s.get_best_server()
# 		all_res = self.s.results.dict()
		
# 		self.ping = all_res['ping']
# 		self.download = all_res['download']
# 		self.upload = all_res['upload']

# 		# return self.download, self.upload, self.ping
# 		return all_res

# c = TestResults()
# print(c.get_results()