#-*-coding:utf-8 -*-
import hashlib
import base64

clustersize=1024*4
window=48
base=101
"""
avsize=1024*4
minsize=1024
maxsize=1024*8
"""
avsize=1024*32
minsize=1024*4
maxsize=1024*256
#mod=119870
mod=1000000000
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
	tempsize=window
	check=0
	for i in range(0,(len(asc)-window)):#0到總長-window
		tempsize=tempsize+1
		if tempsize<minsize:			
			continue
		if check==0:#第一段的fingerprint
			check=1			
			r=0
			j=0			
			while j<(window):
					r=(r*base+asc[i+j])%mod
					j=j+1					
					pass
		else:
			r=((r-asc[i-1]*basewindow)*base+asc[i+window-1])%mod#其他段
			#print (i+window-1),r,asc[i-1]*basewindow,asc[i+window-1]
			#break			
		if r % avsize ==0:#符合			
			hashv.append(r)
			cutpoint.append(i+window)
			sizeofchunk.append(tempsize)
			#print tempsize
			tempsize=0
		if tempsize>=maxsize:#達maxsize,直接切
			cutpoint.append(i+window)
			sizeofchunk.append(tempsize)
			#print tempsize
			tempsize=0
	#print tempsize,i
	sizeofchunk.append(tempsize)
	cutpoint.append(i+window)	
	#print "cuthash:",hashv
	#print "cutpoint:",cutpoint,len(cutpoint)
	#print "chunksize:",sizeofchunk,len(sizeofchunk)
	#return cutpoint,sizeofchunk[len(sizeofchunk)-1]
	#return sizeofchunk[len(sizeofchunk)-1]#最後一個	
	return sizeofchunk,cutpoint

def disktail(a):#算每個chunk的渣渣
	tail=[]
	num=0
	for i in a:
		num=num+i/clustersize	
		m=i%clustersize
		if m != 0:
			tail.append(m)
			num=num+1
	return tail,num


def makefile(a,b):#切出檔案 a為要切的檔案,b為cutpoint
	#print len(b)
	chunk=0
	max=len(b)	
	index=1	
	f = open('%s-%d.txt' %(a.name.split(".")[0],index-1), 'w')	
	for line in a:		
		for c in line:
			f.write(c)
			chunk=chunk+1
			if index < max:
				if chunk == b[index-1]:
					#print "cut",index
					index=index+1
					chunk=0
					f = open('%s-%d.txt' %(a.name.split(".")[0],index-1), 'w')
	print "cuts:",index

def checktail(dtail):
	tempsize=0
	realsize=0		
	files=[]
	combine=[]
	for i in range(0,len(dtail)):
		tempsize=tempsize+dtail[i]
		files.append("chunk%d"%i)
		if tempsize <= clustersize:
			realsize=tempsize
		else:
			files.pop()
			oup=str(realsize),files
			files=[]
			files.append("chunk%d"%i)
			combine.append(oup)
			tempsize=dtail[i]
			realsize=dtail[i]
		if i==(len(dtail)-1):
			if realsize != 0:
				oup=str(realsize),files
				combine.append(oup)
	#print combine
	save=(len(dtail)-len(combine))*1.0/clusternum
	print len(dtail),"\t",len(combine),"\t","%.4f"%save,"\t",clusternum,"\t",clusternum-len(dtail)+len(combine)

def hashoutput(a,b,c):	
	fo_out = open("hash.txt", 'a')	
	for j in range(0,len(b)):		
		line = a.read(b[j])
		if j==0:
			fo_out.write(a.name+"-"+str(j)+","+str([hashlib.sha512(line).hexdigest()])+",0,"+str(c[j])+"\n")
		else:							           
			fo_out.write(a.name+"-"+str(j)+","+str([hashlib.sha512(line).hexdigest()])+","+str(c[j-1])+","+str(c[j])+"\n")				
	fo_out.close()
		

for i in range(0,1):
	with open('big%d.txt'%i) as infile:
		cp=[]
		(soc,cp)=rb(infile)#soc:sizeofchunk cp:cutpoint
		dtail=[]
		(dtail,clusternum)=disktail(soc)#dtail:掉下的tail clusternum:佔用叢集數
		checktail(dtail)
		#print dtail
			
		#infile.seek(0)#回到檔案一開始,準備切
		#makefile(infile,soc)
		#print infile.name.split(".")[0]
		
		infile.seek(0)
		hashoutput(infile,soc,cp)

		
