# -*- coding: utf-8 -*-
import shared as g
from matplotlib import dates
from matplotlib import pyplot as plt

class ChatPlotter:


	# TO DO: manter um arquivo com datas especificas associadas a um label, ai pode passar conjunto de labels pra essas funções pra plotar essas datas em uma cor especifica(especificado no arquivo) e mostrar legenda
	def __init__(self, chatobj):
		self.chatobj = chatobj
		
	def _genXY(self, vetor):
		X = []
		Y = []
		
		for (a1, a2) in vetor:
			X.append(a1)
			Y.append(a2)
		
		return (X, Y)
		
		
	# Plota ocorrencias de um chat todo ou de um sender especifico
	def plot_occurs_line(self, sender = None, regex = None, cores = None)
	
		if not cores:
			cores = "brgcmykw"
		
		senders = [sender]
		if sender == None:
			senders = self.chatobj.users
			
		re_label = "ALL"
		if regex:
			re_label = regex		
			
		for i in range(senders):
			Xd, Y = self._genXY(self.chatobj.countbydays(regex, senders[i]))
			X = dates.date2num(Xd)
			
			plt.plot_date(X, Y, '%s-' % cores[i], linewidth = 0.5, label="%s(%s)" % (re_label, senders[i][i]))		

		plt.title("Ocorrencias/dia")
		plt.ylabel("Ocorrencias")
		plt.xlabel("Dia")
	
	#Mostra na tela o plot configurado
	def display(self):
		plt.legend()
		plt.show()
	
	# todo: pra esparsos colocar numero em cima, ou outro jeito de ficar mais visivel
	# graph_lines: tuplas (chatobj, nome = None(todos senders), regex = None(todas palavras/linhas), color)
	def plot_daily_count(self, graph_lines):
		
		cores = "brgcmykw"
		
		for i in range(len(self.chatobj.users)):
			Xd, Y = self._genXY(self.chatobj.countbydays(regex, self.chatobj.users[i]))
			X = dates.date2num(Xd)
			
			plt.plot_date(X, Y, '%s-' % cores[i], linewidth = 0.5, label=self.chatobj.users[i])
		
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