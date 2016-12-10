#-*-coding:utf-8 -*-
import tempfile
import os
import sys
import hashlib
import random

window=10
base=101
avsize=1024
minsize=512
maxsize=2048
mod=11987

basewindow=1
for a in range(0,window):	#用來計算rabin的第一個值
	basewindow=(basewindow*base)%mod

def puretxt(a,b):#純文字檔(去空格空白)，可以不用做
	#print (a.read())
	for line in a:
		temp=line.strip()
		temp1=temp.split(' \t')
		temp="".join(temp1)
		#print temp;
		b.write(temp)

def rb(a):
	asc=[]
	for line in a:		
		for c in line:
			temp=ord(c)
			asc.append(temp)
	#print(len(asc)-window)
	hashv=[]
	cutpoint=[]
	sizeofchunk=[]
	tempsize=9;	
	for i in range(0,(len(asc)-window)+1):#0到總長-window,+1是因為不包括
		tempsize=tempsize+1
		if i==0:			
			r=0
			j=0
			#for j in range(i,i+window):
			while j<(window):
					r=(r*base+asc[i+j])%mod
					j=j+1
					#print r
					pass
		else:
			r=((r-asc[i-1]*basewindow)*base+asc[i+window-1])%mod
			#print (i+window-1),r,asc[i-1]*basewindow,asc[i+window-1]
			#break			
		if r % avsize ==0:			
			hashv.append(r)
			cutpoint.append(i+10)
			sizeofchunk.append(tempsize)
			#print tempsize
			tempsize=0
	#print tempsize
	sizeofchunk.append(tempsize)	
	print "cuthash:",hashv
	print "cutpoint:",cutpoint
	print "chunksize:",sizeofchunk
	return cutpoint

def makefile(a,b):
	#print len(b)
	chunk=0
	max=len(b)
	index=0
	f = open('rbmake%d.txt' %index, 'w')	
	for line in a:		
		for c in line:
			f.write(c)
			chunk=chunk+1
			if index < max:
				if chunk == b[index]:
					#print "cut",index
					index=index+1
					f = open('rbmake%d.txt' %index, 'w')
	print "cuts:",index+1



with open('a.txt') as infile:
	f_pureout = open('pure.txt' ,'w')	
	puretxt(infile,f_pureout)
	infile.seek(0)
	cp=[]
	cp=rb(infile)
	infile.seek(0)	
	makefile(infile,cp)
	
f_pureout.close()
"""
with open('pure.txt') as seefile:	
	cp=[]
	cp=rb(seefile)
	seefile.seek(0)	
	makefile(seefile,cp)
"""