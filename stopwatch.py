# -*- coding: utf-8 -*-
from time import sleep
import os
from datetime import datetime as dt
from datetime import timedelta
from sys import platform

COMEUP_TIME = 2 * 3600. # 2 horas

def progress_bar(total_length, total, completed, text = ''):
	percent = float(completed)/total
	bar_length = int(total_length - (len(text) + 4 + len(str(int(percent*100)))))
	n_bars = int(percent * bar_length)
	return "%s[%s%s] %d%%" % (text, 'X' * n_bars, '-' * (bar_length - n_bars), int(percent*100))

	# fazer as primeiras 2 horas em outra cor(come up)
	
def clear_screen():
	if platform.startswith("win"):
		os.system("cls")
	elif platform.startswith("linux"):
		os.system("clear")
		
def get_terminal_width():
	if platform.startswith("linux"):
		return int(os.popen('stty size', 'r').read().split()[1])
	else:
		return 80 # FIX ME

if __name__ == '__main__':
    print "Horario atual: %d:%d:%d" % (dt.now().hour, dt.now().minute, dt.now().second)
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
        seconds_passed =  (dt.now() - start_time).seconds
        
        print "Duracao:  %02d:%02d:%02d" % (seconds_passed / 3600, (seconds_passed % 3600) / 60, (seconds_passed % 3600) % 60)
        if choice_pb != '0':
            seconds_remaining = (later - dt.now()).seconds
            print "Restante: %02d:%02d:%02d (%02d:%02d:%02d)" % (seconds_remaining / 3600, (seconds_remaining % 3600) / 60,
            													 (seconds_remaining % 3600) % 60, h2, m2, s2)
            print "Porcentagem comeup: %d%%" % ((COMEUP_TIME/total_duration)*100)
            print progress_bar(get_terminal_width(), total_duration, seconds_passed, 'Duracao: ')
        sleep(1)

        # TODO: quando o tempo acabar, avisar o user e mostrar quanto tempo ele ta de "overtime"
        # TODO: opcao de settar tempo que fez o setup pra estudar(chegou na biblioteca por ex)
        # TODO: opcao de considerar comeup ou nao(pra quando nao tomou nada), se sim, mostrar barra pós-comeup com porcentagem ajustada
        
