# -*- coding: utf-8 -*-
import chatclasses as cc

def main():
	path = raw_input("Digite o path do arquivo de chat(normalizado): ")
	
	chat = cc.ChatLog(path)

if __name__ == '__main__':
	main()