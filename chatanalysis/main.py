import chatclasses as cc


def main():
	path = "../data/normalized_chat.txt"
	
	chat = cc.ChatLog(path)
	print chat.len()
	
	plotter = cc.ChatPlotter(chat)

if __name__ == '__main__':
	main()