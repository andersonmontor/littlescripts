# -*- coding: utf-8 -*-
# Take a list of (source, destination) files/dirs and sync them
# TODO: sync, encrypt and sync, outras funções interessantes
from hashlib import md5
import os


def checksum(path):
	f = open(path, 'rb')
	sum = md5(f.read()).hexdigest()
	f.close()
	
	return sum

# TODO
def gather_sums(path, checksums = []):
	
	for arq in os.listdir(path):
		arq_path = src + '\\' + arq
		if os.path.isdir(arq_path):
			gather_sums(arq_path, checksums)
		else:
			sum = checksum(path)
			if sum not in dest_checksums:
				pair = (arq_path, checksum)
				dest_checksums.append(sum)
				
			
	
	