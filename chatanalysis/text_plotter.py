# -*- coding: utf-8 -*-
import shared as g

# TODO: uma versao textual do plotter, com a ideia de extrair os dados em forma de texto pra ser lido ou usado em outra ferramenta


class TextPlotter:


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
		
	# TODO
	def plot_daily_count(self, regex = None):
		
		for i in range(len(X)):
			print Xd[i], Y[i]
			
		print "%d: %d" % (len(X), len(Y))
		
	def plot_response_times(self):
		pass
		
	def plot_regex_ocurrences(self, regexes):
		pass
		
	# Pega o self.chatobj + os do parametro e plota os daily msgs
	# ver se da pra generalizar depois pra poder misturar chats com qualquer funcao
	def plot_daily_multichats(self, otherchats):
		pass