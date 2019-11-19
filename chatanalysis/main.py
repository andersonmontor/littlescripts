# -*- coding: utf-8 -*-
import chat as cc
import plotter

def main():
	path = raw_input("Digite o path do arquivo de chat(normalizado): ")
	
	chat = cc.ChatLog(path)
	plotter = plotter.ChatPlotter(chat)
	plotter.plot_daily_count()

if __name__ == '__main__':
	main()