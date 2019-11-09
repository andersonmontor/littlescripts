from datetime import datetime as dt


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