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
		
	def plot_daily_count(self, regex = None):
		
		cores = "brgcmykw"
		
		for i in range(len(self.chatobj.users)):
			Xd, Y = self._genXY(self.chatobj.countbydays(regex, self.chatobj.users[i]))
			X = dates.date2num(Xd)
			
			plt.plot_date(X, Y, '%s-' % cores[i], linewidth = 0.5, label=self.chatobj.users[i])
		
		
		
		# for i in range(len(X)):
			# print Xd[i], Y[i]
		# print len(X), len(Y)
		
		
		if regex:
			plt.title("Ocorrencias/dia: (%s)" % regex)
			plt.ylabel("Ocorrencias")
		else:
			plt.title("Palavras/dia")
			plt.ylabel("Palavras")
		plt.xlabel("Dia")
		plt.legend()
		#plt.scatter(X, Y)
		plt.show()
		
	def plot_response_times(self):
		pass
		
	def plot_regex_ocurrences(self, regexes):
		pass
		
	# Pega o self.chatobj + os do parametro e plota os daily msgs
	# ver se da pra generalizar depois pra poder misturar chats com qualquer funcao
	def plot_daily_multichats(self, otherchats):
		pass