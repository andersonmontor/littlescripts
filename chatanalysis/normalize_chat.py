# -*- coding: utf-8 -*-
import re
from datetime import datetime as dt
import chatclasses as cc

# TODO: checagem de se log nao quebra ordem, se as datas estão sequenciais
# pra casos em que dei join repetido sem querer


path_chatfile = "../data/tay_whatsapp_all.txt"

reg1 = r"^(\d{1,2})/(\d{1,2})/(\d{1,4}), (\d{2}):(\d{2}) - (.+): (.+$)"
reg2 = r"^(\d{4})\.(\d{2}).(\d{2}) - (\d{2}):(\d{2}):(\d{2}); (.+): (.+)$"
reg3 = cc.ChatLog.reg # formato output

f = open(path_chatfile)

output_lines = []
newlineobj = None

counts = [0, 0, 0, 0, 0]
for line in f.readlines():
	if re.search(reg1, line):
		g = re.search(reg1, line).groups()
		#                (mes,       dia,       ano,       hora,      minuto,    nome, mensagem)
		newlineobj = cc.Line(int(g[1]), int(g[0]), int(g[2]), int(g[3]), int(g[4]), g[5], g[6])
		output_lines.append(newlineobj)
		
		counts[0] += 1
	elif re.search(reg2, line):
		g = re.search(reg2, line).groups()
		#                (dia,       mes,       ano,       hora,      minuto,    nome, mensagem)
		newlineobj = cc.Line(int(g[2]), int(g[1]), int(g[0]), int(g[3]), int(g[4]), g[6], g[7], int(g[5]))
		output_lines.append(newlineobj)
	
		counts[1] += 1
	elif re.search(reg3, line):
		g = re.search(reg3, line).groups()
		#                (dia,       mes,       ano,       hora,      minuto,    nome, mensagem)
		newlineobj = cc.Line(int(g[2]), int(g[1]), int(g[0]), int(g[3]), int(g[4]), g[6], g[7], int(g[5]))
		output_lines.append(newlineobj)
	
		counts[2] += 1
	elif newlineobj:
		newlineobj.mensagem += cc.Line.DELIM + line.strip()
		counts[3] += 1
	else:
		# Nao deve acontecer num formato correto de arquivo de chat
		raw_input("ERROR: invalid first line(%s)" % line.strip())
		counts[4] += 1
		
	if len(output_lines) >= 2:		
		if output_lines[-2].dt > output_lines[-1].dt:
			date_difference = (output_lines[-2].dt - output_lines[-1].dt).seconds
			print "WARNING: inconsistent date sequence((%d) %s)" % (date_difference, line.strip())
		

f.close()

print counts

fout = open("../data/normalized_chat.txt", 'w')

for lineobj in output_lines:
	try:
		fout.write(str(lineobj))
	except:
		print lineobj.mensagem.strip()
		raw_input()

fout.close()






