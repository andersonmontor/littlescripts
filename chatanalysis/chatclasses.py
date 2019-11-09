from datetime import datetime as dt
import re

# TODO: suporte a chats de grupo

class Line:

	DELIM = " "
	
	def __init__(self, dia, mes, ano, hora, minuto, nome, mensagem, segundos = 0):
		if ano < 1000:
			ano += 2000
		self.dt = dt(ano, mes, dia, hora, minuto)
		self.nome = nome
		self.mensagem = mensagem
		
	def __str__(self):
		str_dt = self.dt.strftime("%m/%d/%Y, %H:%M")
		return "%s - %s: %s\n" % (str_dt, self.nome, self.mensagem)
		
		
class ChatLog:

	reg = r"^(\d{1,2})/(\d{1,2})/(\d{1,4}), (\d{2}):(\d{2}) - (.+): (.+$)"
	
	def __init__(self, path = None):
		if path:
			self.load_from_file(path)
	
	def load_from_file(self, path):
		self.lines = []
		line_errors = 0
		
		try:
			f = open(path)
		except:
			return -1
		
		for line in f.readlines():
			line = line.strip()
			if re.search(self.reg, line):
				g = re.search(self.reg, line).groups()
				newlineobj = Line(int(g[1]), int(g[0]), int(g[2]), int(g[3]), int(g[4]), g[5], g[6])
				self.lines.append(newlineobj)
			else:
				line_errors += 1
		
		f.close()
		
		return line_errors
		
	def len(self):
		return len(self.lines)
		

class ChatPlotter:

	def __init__(self, chatobj):
		self.chatobj = chatobj
		
	def plot_daily_count(self):
		pass
		
	def plot_response_times(self):
		pass
		
	def plot_regex_ocurrences(self, regexes):
		pass
		