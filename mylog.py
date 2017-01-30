import sys
import os
import inspect
import time

class Log:
	def __init__(self, to_syslog=True, to_file=False, filename=time.strftime('%d_%M_%Y'), filedir=None):
		# Logger Initialization
		self.to_syslog = to_syslog
		self.to_file = to_file
		self.filename = filename if '.log' in filename else filename + '.log'
		self.SEVERITY_TO_COLOR_MAP = {'DEBUG':'0;37', 'INFO':'32', 'WARN':'33', 'ERROR':'31', 'FATAL':'31', 'UNKNOWN':'37'}
		if (not self.to_syslog) and (not self.to_file):
			raise Exception("I don't see any use of initializing me!")
		if self.to_file and self.filename:
			self.filename = filename
			self.filedir = os.path.dirname(filedir) if filedir else os.path.dirname(__file__)
			if not os.path.exists(self.filedir):
				try:
					os.makedirs(self.filedir)
				except Exception as direrror:
					raise Exception(direrror.strerror)
					sys.exit(1)

			self.filepath = os.path.join(self.filedir,self.filename)
			self.keeper = open(self.filepath,"a", 0)
		

	def write(self, msg, purpose):
		self.keeper.write(time.ctime()+': %s - %s.\n'%(purpose.upper(),msg))

	def info(self, msg, linenumber=False):
		(frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
		if linenumber: line_number = linenumber
		self.log(msg, "INFO", frame, filename, line_number, function_name, lines, index)

	def debug(self, msg, linenumber=False):
		(frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
		if linenumber: line_number = linenumber
		self.log(msg, "DEBUG", frame, filename, line_number, function_name, lines, index)

	def warn(self, msg, linenumber=False):
		(frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
		if linenumber: line_number = linenumber
		self.log(msg, "WARN", frame, filename, line_number, function_name, lines, index)

	def error(self, msg, linenumber=False):
		(frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
		if linenumber: line_number = linenumber
		self.log(msg, "ERROR", frame, filename, line_number, function_name, lines, index)

	def fatal(self, msg, linenumber=False):
		(frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
		if linenumber: line_number = linenumber
		self.log(msg, "FATAL", frame, filename, line_number, function_name, lines, index)

	def log(self, msg, severity, frame, filename, line_number, function_name, lines, index):
		if not severity: severity="UNKNOWN"
		callee = str(filename)+'#'+str(function_name)+':'+str(line_number)

		formatted_time = time.ctime()
		color = self.SEVERITY_TO_COLOR_MAP[severity]
		formatted_severity = severity

		info_to_write = "\033[0;37m{}\033[0m [\033[{}m{}\033[0m] \033[0;36m{}\033[0m \033[0;{}m{}\033[0m\n".format(formatted_time,color,formatted_severity,callee,color,msg)
		if self.to_syslog:	sys.stdout.write(info_to_write)
		if self.to_file: self.keeper.write(info_to_write)
