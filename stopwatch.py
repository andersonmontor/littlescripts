# -*- coding: utf-8 -*-
from time import sleep
import os
from datetime import datetime as dt
from datetime import timedelta
from sys import platform

COMEUP_TIME = 2 * 3600. # 2 horas

# Platform variables
ON_LINUX = platform.startswith("linux")
ON_WINDOWS = platform.startswith("win")

def progress_bar(total_length, total, completed, text = ''):
	percent = float(completed)/total
	bar_length = int(total_length - (len(text) + 4 + len(str(int(percent*100)))))
	n_bars = int(percent * bar_length)
	return "%s[%s%s] %d%%" % (text, 'X' * n_bars, '-' * (bar_length - n_bars), int(percent*100))

	# TODO: fazer as primeiras 2 horas em outra cor(come up)
	
def clear_screen():
	if ON_WINDOWS:
		os.system("cls")
	elif ON_LINUX:
		os.system("clear")
		
def get_terminal_width():
	if ON_LINUX:
		return int(os.popen('stty size', 'r').read().split()[1])
	else:
		return 80 # FIX ME

if __name__ == '__main__':
	print "Horario atual: %02d:%02d:%02d" % (dt.now().hour, dt.now().minute, dt.now().second)
	choice = raw_input("Duracao inicial(hh, mm, ss), 0 se comeca agora: ")
	if choice == '0':
		h, m, s = 0, 0, 0
	else:
		h, m, s = eval(choice)
	passed = timedelta(hours = h, minutes = m, seconds = s)
	start_time = dt.now() - passed

	choice_pb = raw_input("Ate que horas(hh, mm, ss), 0 pra nao ter progress bar: ")
	if choice_pb != '0':
		h2, m2, s2 = eval(choice_pb)
		later = dt.now().replace(hour = h2, minute = m2, second = s2)
		total_duration = (later - start_time).seconds

	while True:
		clear_screen()
		seconds_passed = (dt.now() - start_time).seconds
		aftercomeup_passed = max(0, (seconds_passed - COMEUP_TIME))
		
		# TODO: refatorar esse negocio feio
		h_passed, m_passed, s_passed = seconds_passed / 3600, (seconds_passed % 3600) / 60, (seconds_passed % 3600) % 60
		hcu_passed, mcu_passed, scu_passed = (aftercomeup_passed / 3600, (aftercomeup_passed % 3600) / 60, (aftercomeup_passed % 3600) % 60)
		
		print "Duracao:  %02d:%02d:%02d (%02d:%02d:%02d)" % (h_passed, m_passed, s_passed, hcu_passed, mcu_passed, scu_passed)
		
		if choice_pb != '0':
			seconds_remaining = (later - dt.now()).seconds
			print "Restante: %02d:%02d:%02d (%02d:%02d:%02d)" % (seconds_remaining / 3600, (seconds_remaining % 3600) / 60,
																 (seconds_remaining % 3600) % 60, h2, m2, s2)
			print "Porcentagem comeup: %d%%" % ((COMEUP_TIME/total_duration)*100)
			print progress_bar(get_terminal_width(), total_duration, seconds_passed, 'Duracao: ')
		sleep(1)

		# TODO: opcao de debug: salvar ultima hora que inseriu e perguntar se é ela, ajuda quando to rodando varias vezes pra testar se ta rodando bonitinho
		# TODO: jeito de calcular comeup com mais acuracia, e talvez nao-fixo(tolerancia vai aumentando etc)
		# TODO: quando o tempo acabar, avisar o user e mostrar quanto tempo ele ta de "overtime"
		# TODO: opcao de settar tempo que fez o setup pra estudar(chegou na biblioteca por ex)
		# TODO: opcao de considerar comeup ou nao(pra quando nao tomou nada), se sim, mostrar barra pós-comeup com porcentagem ajustada
		# TODO: opção de settar um alarme pra daqui x tempo, pra lembrar a pessoa de voltar a produção(usar push notifications e maybe som)
		# TODO: função pomodoro(usar push notifications e maybe som)
		# TODO: alguma metrica pra testar eficacia, ai fazer regressao linear pra mostrar o % de eficacia atual
		# TODO: overlay no desktop(linux e windows) mostrando format string combinando valores atuais(duracao, duracao_comeup, duracao_percent, restante, end_time, etc), also uma forma de mostrar intensidade atual
