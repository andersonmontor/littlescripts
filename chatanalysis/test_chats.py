import pytest
import chat as cc
from datetime import datetime as dt

# Line

def test_lineconst():
	# Padrao
	l_obj = cc.Line(1, 1, 2019, 22, 0, "NomeTeste", "MensagemTeste")
	assert (l_obj.nome == "NomeTeste")
	assert (l_obj.mensagem == "MensagemTeste")
	assert (l_obj.dt == dt(2019, 1, 1, 22, 0))
	
	# ano < 100
	l_obj = cc.Line(1, 1, 17, 22, 0, "NomeTeste", "MensagemTeste")
	assert (l_obj.dt == dt(2017, 1, 1, 22, 0))
	
	# segundos
	l_obj = cc.Line(1, 1, 2019, 22, 0, "NomeTeste", "MensagemTeste", segundos = 13)
	assert (l_obj.dt == dt(2019, 1, 1, 22, 0, 13))
	
	# am_pm
	l_obj = cc.Line(1, 1, 2019, 3, 0, "NomeTeste", "MensagemTeste", am_pm = "PM")
	assert (l_obj.dt == dt(2019, 1, 1, 15, 0))
	l_obj = cc.Line(1, 1, 2019, 12, 0, "NomeTeste", "MensagemTeste", am_pm = "AM")
	assert (l_obj.dt == dt(2019, 1, 1, 0, 0))
	
def test_linestr():
	l_obj = cc.Line(1, 1, 2019, 22, 0, "NomeTeste", "MensagemTeste")
	assert (str(l_obj) == "2019.01.01 - 22:00:00; NomeTeste: MensagemTeste\n")
	
	l_obj = cc.Line(1, 1, 2019, 22, 0, "NomeTeste", "")
	assert (str(l_obj) == "2019.01.01 - 22:00:00; NomeTeste: <Media omitted>\n")
	
	
# ChatLog
# def test_chatlogconst():
	# pass
	
# def test_loadfromfile():
	# pass
	
# def test_getdatetimes():
	# pass
	
# def test_getuniquedays():
	# pass
	
# def test_groupbydays():
	# pass
	
# def test_getfullstring():
	# pass
	
# def test_countbydays():
	# pass
	
# ChatAnalysis

# ChatPlotter

