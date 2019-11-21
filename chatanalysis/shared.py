# TODO: separar constantes desse projeto num arquivo(globals.py ou algo assim), e funcoes/constantes gerais que costumo usar(myshared.py ou algo assim) num arquivo que todos projetos tem acesso, e usar uma forma rapida de importar(macro por exemplo), ai separar caso for mandar pra um repo de um projeto especifico
#DEPRECRATED

### User set ###

#Verbose level required
VERBOSE_LEVEL = 1

### Constants ###

# Verbose levels
QUIET = 0
NORMAL = 1
VERBOSE = 2
DEBUG = 3

### Functions ###

def print_verbose(text, min_vb):
	if VERBOSE_LEVEL >= min_vb:
		print(text)
		
def sort_by_kelement(tosort, k):
	return sorted(tosort, key = lambda x: x[k-1])
	
def convert12hto24h(h, m, s, am_pm):
	if am_pm == "AM" and h == 12:
		h = 0
	elif am_pm == "AM":
		pass
	elif am_pm == "PM" and h == 12:
		pass
	else:
		h += 12
		
	return (h, m, s)