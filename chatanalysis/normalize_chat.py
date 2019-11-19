# -*- coding: utf-8 -*-
import re
from datetime import datetime as dt
import chat as cc
import shared as g
from shared import print_verbose
from sys import argv, exit

# TODO: normalizar pra uma db sqlite, manter opção de passar pra um arquivo de saida

if len(argv) < 2:
	print_verbose("Escolha o arquivo a ser normalizado da pasta ../data/", g.QUIET)
	exit(1)
	
path_chatfile = "../data/%s" % argv[1]

# Formatos de export que ja vi em logs de whatsapp
regs = (r"^(\d{4})\.(\d{2}).(\d{2}) - (\d{2}):(\d{2}):(\d{2}); (.+?): (.+)$",
		r"^(\d{1,2})/(\d{1,2})/(\d{1,4}), (\d{2}):(\d{2}) - (.+?): (.+$)$",
		r"^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2});(.+?): (.*)$",
		r"^(\d{1,2})/(\d{1,2})/(\d{1,4}) (\d{2}):(\d{2}) - (.+?): (.+$)$",
		r"^(\d{1,2})/(\d{1,2})/(\d{1,4}), (\d{1,2}):(\d{1,2}) (AM|PM) - (.+?): (.+$)$"
)

regs_evals = ("cc.Line(int(gp[2]), int(gp[1]), int(gp[0]), int(gp[3]), int(gp[4]), gp[6], gp[7], int(gp[5]))",
			  "cc.Line(int(gp[1]), int(gp[0]), int(gp[2]), int(gp[3]), int(gp[4]), gp[5], gp[6])",
			  "cc.Line(int(gp[2]), int(gp[1]), int(gp[0]), int(gp[3]), int(gp[4]), gp[6], gp[7], int(gp[5]))",
			  "cc.Line(int(gp[1]), int(gp[0]), int(gp[2]), int(gp[3]), int(gp[4]), gp[5], gp[6])",
			  "cc.Line(int(gp[1]), int(gp[0]), int(gp[2]), int(gp[3]), int(gp[4]), gp[6], gp[7], am_pm = gp[5])"
)

regs_readable = (r"YYYY.MM.DD - HH:MM:SS; NOME: MSG",
		r"MM/DD/YYYY, HH:MM - NOME: MSG",
		r"YYYY-MM-DD HH:MM:SS;NOME: MSG",
		r"MM/DD/YYYY HH:MM - NOME: MSG",
		r"MM/DD/YY, HH:MM AM|PM - NOME: MSG"
)

f = open(path_chatfile)

newlineobj = None
chatobj = cc.ChatLog()

counts = {"newline": 0, "inconsistent_date": 0}
for r in regs:
	counts[r] = 0
	
for line in f.readlines():

	flag_done = False
	for i in range(len(regs)):
		if re.search(regs[i], line):
			gp = re.search(regs[i], line).groups()
			newlineobj = eval(regs_evals[i])
			chatobj.add_line(newlineobj)
			
			counts[regs[i]] += 1
			flag_done = True
			break
			
	if not flag_done:
		if newlineobj:
			newlineobj.mensagem += cc.Line.DELIM + line.strip()
			counts["newline"] += 1
		else:
			# Nao deve acontecer num formato correto de arquivo de chat
			raw_input("ERROR: invalid first line(%s)" % line.strip())
			
	if len(chatobj.lines) >= 2:		
		if chatobj.lines[-2].dt > chatobj.lines[-1].dt:
			date_difference = (chatobj.lines[-2].dt - chatobj.lines[-1].dt).seconds
			print_verbose("WARNING: inconsistent date sequence((%d) %s)" % (date_difference, line.strip()), g.VERBOSE)
			counts["inconsistent_date"] += 1
			
f.close()

print_verbose('\n', g.NORMAL)
for i in range(len(regs)):
	print_verbose("%s: %d" % (regs_readable[i], counts[regs[i]]), g.NORMAL)
print_verbose("NEWLINE(other): %d" % counts["newline"], g.NORMAL)
print_verbose("Inconsistent dates: %d" % counts["inconsistent_date"], g.NORMAL)

og_filename = re.search(r".*/(.+)\.txt", path_chatfile).groups()[0]

out_choice = raw_input("Output em sqlite3 db(1) ou txt file(2): ")

if out_choice == '1':
	chatobj.export_sqlite("../data/normalized_%s.db" % og_filename)
elif out_choice == '2':
	chatobj.export_textfile("../data/normalized_%s.txt" % og_filename)
else:
	print "Opcao invalida"