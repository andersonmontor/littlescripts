# -*- coding: utf-8 -*-
from time import sleep
import os
from datetime import datetime as dt
from datetime import timedelta
from sys import platform

# TODO: opcao de debug: salvar ultima hora que inseriu e perguntar se é ela, ajuda quando to rodando varias vezes pra testar se ta rodando bonitinho
# TODO: jeito de calcular comeup com mais acuracia, e talvez nao-fixo(tolerancia vai aumentando etc)
# TODO: quando o tempo acabar, avisar o user e mostrar quanto tempo ele ta de "overtime"
# TODO: opcao de settar tempo que fez o setup pra estudar(chegou na biblioteca por ex)
# TODO: opcao de considerar comeup ou nao(pra quando nao tomou nada), se sim, mostrar barra pós-comeup com porcentagem ajustada
# TODO: opção de settar um alarme pra daqui x tempo, pra lembrar a pessoa de voltar a produção(usar push notifications e maybe som)
# TODO: função pomodoro(usar push notifications e maybe som)
# TODO: alguma metrica pra testar eficacia, ai fazer regressao linear pra mostrar o % de eficacia atual
# TODO: overlay no desktop(linux e windows) mostrando format string combinando valores atuais(duracao, duracao_comeup, duracao_percent, restante, end_time, etc), also uma forma de mostrar intensidade atual
# TODO: ver se é possivel pegar a duracao automaticamente do celular(ou algo com o datacollector.py)

COMEUP_SECONDS = 2 * 3600. # 2 horas

# Platform variables
ON_LINUX = platform.startswith("linux")
ON_WINDOWS = platform.startswith("win")

def progress_bar(total_length, total, completed, text = '', cmup_percent = None):
	percent = completed.total_seconds()/float(total.total_seconds())
	bar_length = int(total_length - (len(text) + 4 + len(str(int(percent*100)))))
	n_bars = int(percent * bar_length)
	p_bar_str = "%s[%s%s] %d%%" % (text, 'X' * n_bars, '-' * (bar_length - n_bars), int(percent*100))
	if cmup_percent == None:
		return p_bar_str
	else:		
		cmup_marker_str = ' ' * (int(len(text) + 1 + cmup_percent * bar_length) - 1) + '^'		
		return p_bar_str + '\n' + cmup_marker_str

	# TODO: fazer o comeup de outro cor, ou indicar com um ^ embaixo(mais simples)(feito, deixar aqui pro find_TODOs.py pegar depois)
	
def clear_screen():
	if ON_WINDOWS:
		os.system("cls")
	elif ON_LINUX:
		os.system("clear")
		
def get_terminal_width():
	if ON_LINUX:
		return int(os.popen('stty size', 'r').read().split()[1])
	else:
		return 80 #TODO: arrumar
		
def str_timedelta(td):
	total_secs = td.total_seconds()
	h, m, s = total_secs / 3600, (total_secs % 3600) / 60, (total_secs % 3600) % 60
	return "%02d:%02d:%02d" % (h, m, s)
	
# TODO: quando tem comeup mas nao end_time, ver todas combinacoes
def print_stopwatch(start_time, end_time = None, comeup_duration = None):
	passed = dt.now() - start_time
	
	if comeup_duration != None:
		if (passed - comeup_duration).total_seconds() > 0:
			aftercomeup_passed = (passed - comeup_duration)
		else:
			aftercomeup_passed = timedelta(seconds = 0)
			
		print("Duracao:  %s (%s)" % (str_timedelta(passed), str_timedelta(aftercomeup_passed)))
	else:
		print("Duracao:  %s" % (str_timedelta(passed)))
		
	if end_time != None:
		remaining = end_time - dt.now()
		total_duration = end_time - start_time
		percent_comeup = comeup_duration.total_seconds()/total_duration.total_seconds()
		print("Restante: %s (%s)" % (str_timedelta(remaining), end_time.strftime("%H:%M:%S")))
		print("Porcentagem comeup: %d%%" % (percent_comeup * 100))
		print(progress_bar(get_terminal_width(), total_duration, passed, 'Duracao: ', percent_comeup))
		
	
def main():
	print("Horario atual: %02d:%02d:%02d" % (dt.now().hour, dt.now().minute, dt.now().second))
	choice = input("Duracao inicial(hh, mm, ss), enter se comeca agora: ")
	if choice == '':
		passed = timedelta(seconds = 0)
	else:
		h, m, s = eval(choice)
		passed = timedelta(hours = h, minutes = m, seconds = s)
		
	start_time = dt.now() - passed

	choice_pb = input("Ate que horas(hh, mm, ss), enter pra nao ter progress bar: ")
	if choice_pb != '':
		h2, m2, s2 = eval(choice_pb)
		end_time = dt.now().replace(hour = h2, minute = m2, second = s2)
		comeup_duration = timedelta(seconds = COMEUP_SECONDS)

	while True:
		clear_screen()
		if choice_pb != '':
			print_stopwatch(start_time, end_time, comeup_duration)
		else:
			print_stopwatch(start_time)
		sleep(1)

if __name__ == '__main__':
	main()


