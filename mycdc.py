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
mod=10000000000000
basewindow=1
for a in range(0,window-1):	#用來計算rabin的第一個base值
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
		if check==0:#第一段的fingerprint
			check=1			
			r=0
			j=0			
			while j<(window):
					r=(r*base+asc[i+j])%mod
					j=j+1
					#print r,j									
					pass
			#print i,r
			#break						
		else:
			#print r
			r=((r-asc[i-1]*basewindow)*base%mod+asc[i+window-1])%mod#其他段
			#print i,(i+window-1),r
			#break
		#if i==0 or i==1 or i==49 or i==50 or i==51:
		#	print i,r,asc[i+window-1]
		if tempsize<minsize:			
			continue						
		if r % avsize == 1013:#符合
			#print i,r			
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
	anythesame=0
	maker=1
	fo_out = open("hash.txt", 'a+')		
	for j in range(0,len(b)):
		found=""		
		line = a.read(b[j])
		find=str([hashlib.sha512(line).hexdigest()])
		#print "find:",find
		fo_out.seek(0)
		for check in fo_out:
			checkhash=check.split(",")[1]				
			#print checkhash
			if checkhash==find:
				anythesame=1
				find=str([0])
				found=check.split(",")[0]
				#print "got!find=",find
				#print found
				break				
		fo_out.seek(0,2)		
		if j==0:		
			fo_out.write(a.name+"-"+str(j)+","+find+",0,"+str(c[j]))
			if found!="":
				anythesame=1
				fo_out.write(","+found)
				#print "found!"			
		else:
			fo_out.write(a.name+"-"+str(j)+","+find+","+str(c[j-1])+","+str(c[j]))
			if found!="":
				fo_out.write(","+found)
				#print "found!"
		if anythesame==0:
			fo_out.write(","+a.name+"-r"+str(0))
		if anythesame==1 and found=="": 
			fo_out.write(","+a.name+"-r"+str(maker))
			maker=maker+1
		fo_out.write("\n")				
	fo_out.close()	
		
'''
for i in range(0,0):
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

for i in range(0,1):
	with open('big10.txt') as infile:
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
'''
for i in range(0,1):
	with open('500A.txt') as infile:
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

for i in range(0,1):
	with open('500B.txt') as infile:
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
for i in range(0,1):
	with open('500C.txt') as infile:
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

for i in range(0,1):
	with open('500D.txt') as infile:
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
		
