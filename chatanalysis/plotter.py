# -*- coding: utf-8 -*-
import shared as g
import datetime as dt
from matplotlib import dates
from matplotlib import pyplot as plt

class ChatPlotter:


	# TODO: manter um arquivo com datas especificas associadas a um label, ai pode passar conjunto de labels pra essas funções pra plotar essas datas em uma cor especifica(especificado no arquivo) e mostrar legenda
	
	# TODO: mostrar no grafico periodos faltando dados (a partir de alguns dias, talvez uns 5 dias)
	def __init__(self, chatobj):
		self.chatobj = chatobj
		
	def _genXY(self, vetor):
		X = []
		Y = []
		
		for (a1, a2) in vetor:
			X.append(a1)
			Y.append(a2)
		
		return (X, Y)
		
	# ver se ja existe automatico no plotting em tools mais avançadas de data visualization
	# dias_count: (tupla(dia, count): quantas ocorrencias por dia
	def _bin_intervals(self, dias_count, k):
	
		if k == 1:
			return dias_count			
		else:
			interval = dt.timedelta(days = k)
			
			# WIP
			i = 0
			binned_dias_count = []
			while i < len(dias_count):
				curr_date = dias_count[i][0]
				curr_datetime = dt.combine(curr_date, dt.time())
				end_date = curr_datetime + interval
				avg_date = curr_datetime + interval/2
				sum_occurs = 0.
				n_occurs = 0.
				while curr_datetime <= end_date:
					sum_occurs += dias_count[i][1]
					i += 1
					n_occurs += 1
				
				avg_occurs = sum_occurs/n_occurs
				binned_dias_count.append((avg_date.date(), avg_occurs))
				
			return binned_dias_count
			
			
	# Plota ocorrencias de um chat todo ou de um sender especifico
	# TODO: ao invés de um só dia, deixa escolher o intervalo de dias, ver se fica uma visualização melhor
	def plot_occurs_line(self, sender = None, regex = None, cores = None, k = 1):
	
		if not cores:
			cores = "brgcmykw"
		
		senders = [sender]
		if sender == None:
			senders = self.chatobj.users
			
		re_label = "ALL"
		if regex:
			re_label = regex		
			
		for i in range(len(senders)):
			bin_diascount = self._bin_intervals(self.chatobj.countbydays(regex, senders[i]), k)
			Xd, Y = self._genXY(bin_diascount)
			X = dates.date2num(Xd)
			
			plt.plot_date(X, Y, '%s-' % cores[i], linewidth = 0.5, label="%s(%s)" % (re_label, senders[i]))		

		plt.title("Occurences/day")
		plt.ylabel("Occurences")
		plt.xlabel("Day")
	
	#Mostra na tela o plot configurado
	def display(self, show_legend = True):
		if show_legend:
			plt.legend()
		plt.show()
	
	# todo: pra esparsos colocar numero em cima, ou outro jeito de ficar mais visivel
	# graph_lines: tuplas (chatobj, nome = None(todos senders), regex = None(todas palavras/linhas), color)
	def plot_daily_count(self, graph_lines):
		
		cores = "brgcmykw"
		
		for i in range(len(self.chatobj.users)):
			Xd, Y = self._genXY(self.chatobj.countbydays(regex, self.chatobj.users[i]))
			X = dates.date2num(Xd)
			
			plt.plot_date(X, Y, '.-', color=cores[i], linewidth = 0.5, label=self.chatobj.users[i])
		
		if regex:
			plt.title("Ocorrencias/dia: (%s)" % regex)
			plt.ylabel("Ocorrencias")
		else:
			plt.title("Palavras/dia")
			plt.ylabel("Palavras")
		plt.xlabel("Dia")
		
	# TODO: recebe um vetor de (nome, regex, color = None) e plota no mesmo grafico, ou adiciona essa função na daily count mesmo
	# ou as vezes ate mixar varios chats
	def multi_daily_count(self, nomes_regexes):
		pass
		
	def plot_response_times(self):
		pass
		
	def plot_regex_ocurrences(self, regexes):
		pass
		
	# Pega o self.chatobj + os do parametro e plota os daily msgs
	# ver se da pra generalizar depois pra poder misturar chats com qualquer funcao
	# melhor: sempre passar o conjunto de chats como parametro pra essa classe, ao invés de ficar atrelada a um unico
	def plot_daily_multichats(self, otherchats):
		pass
		
	# mistura os Y de 2 plots diferentes fazendo operacao bit a bit
	def arithmetic_plot(Xa, Xb, operacao):
	
		assert (len(Xa) == len (Xb))
		pass
		#TODO
		
	def plot_nomessages_interval(self, min_days):
		days = self.chatobj.getUniqueDays()
		#TODO
	