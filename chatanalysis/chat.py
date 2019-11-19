# -*- coding: utf-8 -*-
import shared as g
from datetime import datetime as dt
from datetime import date as dtdate
import sqlite3
import re


# TODO: suporte a chats de grupo

class Line:

	DELIM = " "
	
	def __init__(self, dia, mes, ano, hora, minuto, nome, mensagem, segundos = 0, am_pm = None):
		if ano < 100:
			ano += 2000
		
		if am_pm:
			hora, minuto, segundos = g.convert12hto24h(hora, minuto, segundos, am_pm)
			
		self.dt = dt(ano, mes, dia, hora, minuto, segundos)
		self.nome = re.sub(r'\W+', '', nome)
		self.mensagem = mensagem
		
	def __str__(self):
		#"YYYY.MM.DD - HH:MM:SS; NOME: MSG"
		str_dt = self.dt.strftime("%Y.%m.%d - %H:%M:%S")
		msg = self.mensagem
		if msg == '':
			msg = "<Media omitted>"
		return "%s; %s: %s\n" % (str_dt, self.nome, msg)
		
		
class ChatLog:

	reg = r"^(\d{4})\.(\d{2}).(\d{2}) - (\d{2}):(\d{2}):(\d{2}); (.+?): (.+)$"
	
	def __init__(self, path = None):
		self.users = []
		self.lines = []
		if path != None:
			self.load_from_file(path)

	def add_line(self, lineobj):
		if lineobj.nome not in self.users:
			self.users.append(lineobj.nome)

		self.lines.append(lineobj)
	
	# Retorno(int): -1 se deu erro, se nao numero de erros de inconsistencia de formato(0 se foi perfeito)
	def load_from_file(self, path):
		line_errors = 0
		
		try:
			f = open(path)
		except:
			print "Erro ao abrir o arquivo..."
			return -1			
		
		for line in f.readlines():
			if re.search(self.reg, line, re.IGNORECASE):
				gp = re.search(self.reg, line, re.IGNORECASE).groups()
				#                (dia,        mes,        ano,        hora,       minuto,     nome,  msg,   segundos)
				newlineobj = Line(int(gp[2]), int(gp[1]), int(gp[0]), int(gp[3]), int(gp[4]), gp[6], gp[7], int(gp[5]))
				self.add_line(newlineobj)
			else:
				line_errors += 1
				raw_input(line)
		
		f.close()
		
		return line_errors

	def load_from_db(self, db_filename):
		pass
		
	def export_textfile(self, filename):

		fout = open(filename, 'w')

		for lineobj in self.lines:
			try:
				fout.write(str(lineobj))
			except:
				print lineobj.mensagem.strip()
				raw_input()

		fout.close()

	def export_sqlite(self, db_filename):
		conn = sqlite3.connect(db_filename)

		c = conn.cursor()
		c.execute('''CREATE TABLE chatlog
		             (date_time datetime, sender text, msg text)''')

		for lineobj in self.lines:
			c.execute("INSERT INTO chatlog VALUES (?, ?, ?)", (lineobj.dt, unicode(lineobj.nome), unicode(lineobj.mensagem)))


		conn.commit()
		conn.close()

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
	def countbydays(self, regex = None, nome = None, count_type = "BY_WORDS"):
		dias_count = []
		
		dias_linhas = self.groupbydays()
		for dia in dias_linhas.keys():
			occurs = 0
			for linha in dias_linhas[dia]:
				if (nome == None) or (linha.nome == nome):				
					if regex:
						if count_type == "BY_LINE" and re.search(regex, linha.mensagem, re.IGNORECASE):
							occurs += 1
						elif count_type == "BY_WORDS":
							occurs += len(re.findall(regex, linha.mensagem, re.IGNORECASE))
					else:
						if count_type == "BY_LINE":
							occurs += 1
						elif count_type == "BY_WORDS":
							occurs += len(linha.mensagem.strip().split())
							
			dias_count.append((dia, occurs))
			
		return g.sort_by_kelement(dias_count, 1)