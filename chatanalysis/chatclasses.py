# -*- coding: utf-8 -*-
from datetime import datetime as dt
from datetime import date as dtdate
from matplotlib import dates
from matplotlib import pyplot as plt
import re

# TODO: suporte a chats de grupo

class Line:

	DELIM = " "
	
	def __init__(self, dia, mes, ano, hora, minuto, nome, mensagem, segundos = 0):
		if ano < 100:
			ano += 2000
		self.dt = dt(ano, mes, dia, hora, minuto)
		self.nome = nome
		self.mensagem = mensagem
		
	def __str__(self):
		str_dt = self.dt.strftime("%Y/%m/%d, %H:%M")
		return "%s - %s: %s\n" % (str_dt, self.nome, self.mensagem)
		
		
class ChatLog:

	reg = r"^(\d{4})/(\d{1,2})/(\d{1,2}), (\d{2}):(\d{2}) - (.+): (.+$)"
	
	def __init__(self, path = None):
		if path:
			self.load_from_file(path)
	
	# Retorno(int): -1 se deu erro, se nao numero de erros de inconsistencia de formato(0 se foi perfeito)
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
				#                (dia,       mes,       ano,       hora,      minuto,    nome, mensagem)
				newlineobj = Line(int(g[2]), int(g[1]), int(g[0]), int(g[3]), int(g[4]), g[5], g[6])
				self.lines.append(newlineobj)
			else:
				line_errors += 1
		
		f.close()
		
		return line_errors
		
	# Retorno(int): numero de mensagens do chat
	# nome: se quer filtrar por nome
	def len(self, nome = None):
		count = 0
		if nome:
			for line in self.lines:
				if line.nome == nome:
					count += 1
		else:
			count = len(self.lines)
			
		return count
		
	# Retorno(obj datetime): datas das linhas do chat
	def get_datetimes(self):
		dts = []
		for lineobj in self.lines:
			dts.append(lineobj.dt)
			
		return dts
		
	# Retorno(obj date): dias distintos do chat
	def getUniqueDays(self):
		days = []
		dtdates = []
		for data in self.get_datetimes():
			dia = (data.day, data.month, data.year)
			if dia not in days:
				days.append(dia)
				dtdates.append(dtdate(dia[2], dia[1], dia[0]))
			
		return dtdates
		
	# Retorno(tupla(dia, linhas)): agrupa linhas do chat pra cada dia distinto
	def groupbydays(self):
		days = {}

		for lineobj in self.lines:
			dia = lineobj.dt.date()
			if dia in days:
				days[dia].append(lineobj)
			else:
				days[dia] = [lineobj]
				
		return days
			
	# Retorno(string): converte o chat todo pra uma string unica(parecido com o conteudo do input file)
	def get_full_string(self):
		full_string = ""
		
		for line in self.lines:
			full_string += str(line)
			
		return full_string
		
	# Retorna(tupla(dia, count): quantas ocorrencias por dia
	# regex: filtra pra uma ocorrencia de uma regex especifica ao invés da linha toda
	# nome: filtra pra um remetente especifico
	# count_type: se quer contar por linhas ou por palavras
	def countbydays(self, regex = None, nome = None, count_type = "BY_LINE"):
		dias_count = []
		
		dias_linhas = self.groupbydays()
		for dia in dias_linhas.keys():
			occurs = 0
			for linha in dias_linhas[dia]:
				if (nome == None) or (linha.nome == nome):				
					if regex:
						if count_type == "BY_LINE" and re.search(regex, linha.mensagem):
							occurs += 1
						elif count_type == "BY_WORDS":
							occurs += len(re.findall(regex, linha.mensagem))
					else:
						if count_type == "BY_LINE":
							occurs += 1
						elif count_type == "BY_WORDS":
							occurs += len(linha.mensagem.strip().split())
							
			dias_count.append((dia, occurs))
			
		return dias_count
		
		
class ChatPlotter:


	# TO DO: manter um arquivo com datas especificas associadas a um label, ai pode passar conjunto de labels pra essas funções pra plotar essas datas em uma cor especifica(especificado no arquivo) e mostrar legenda
	def __init__(self, chatobj):
		self.chatobj = chatobj
		
		
	def _gen_X(self):
		datas = self.chatobj.get_datetimes()
		return dates.date2num(datas)
		
	
		
		
	def plot_daily_count(self):
		pass
		
	def plot_response_times(self):
		pass
		
	def plot_regex_ocurrences(self, regexes):
		pass
		