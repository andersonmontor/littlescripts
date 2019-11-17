# -*- coding: utf-8 -*-
# plotar meu uso de combustivel a partir do meu log
# tentar encontrar dias que viajei pra plotar junto
# inserir dados da kilometragem do carro também, pra plotar km/l

from datetime import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import dates

path = r'./data/combustivel.csv'

f = open(path)
lines = f.read().strip().split('\n')[1:]
f.close()

dataset = []

sum_litros = 0
for row in lines:
	row = row.split(';')	
	
	data = dt.strptime(row[0], "%d/%m/%Y")
	valor = float(row[1])
	custo_unit = float(row[2])
	tipo = row[3]
	if row[4] == '#':
		continue	
	
	litros = valor/custo_unit
	sum_litros += litros
	if row[4].isdigit():		
		km = float(row[4])		
		km_por_litro = km/sum_litros		
		dataset.append((data, tipo, sum_litros, km, km_por_litro))
		sum_litros = 0
		
# for line in dataset:
	# print line
	
Xd = []
Y = []
for line in dataset:
	Xd.append(line[0])
	Y.append(line[4])
	print line
	
X = dates.date2num(Xd)
average = sum(Y)/len(X)

plt.plot_date(X, Y, '.-')
plt.axhline(y=average, color='r', linestyle='-')
plt.show()

	
	