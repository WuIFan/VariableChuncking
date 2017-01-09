#-*-coding:utf-8 -*-
import os

dirname="remake"
if not os.path.exists(dirname): #確認資料夾是否存在 
	os.makedirs(dirname)

with open('hash.txt') as infile:
	opened=[]#開過的檔名
	openflag=0
	openlist=[]#開好的f

	##########################################這裡放想remake的檔案##################################################
	WantToRemake="500B.txt"
	################################################################################################################

	R = open(dirname+"/"+WantToRemake, 'w')
	num=0

	for line in infile:		
		if line.split(",")[0] == WantToRemake:
			#print "i want to open",line.split(",")[3]
			num=0
	##########################################避免重複開檔##########################################################
			for o in opened:				
				if o == line.split(",")[3]:#檔案開過								
					openflag=1					
					break
				else:
					openflag=0
				num=num+1
			if openflag==0:
				f = open("dedup/"+line.split(",")[3], 'r')
				openlist.append(f)#增加 開好的檔名->用來讀檔
				opened.append(line.split(",")[3])#增加 開過的檔名->用來判斷

	################################################################################################################			

			start=int(line.split(",")[4].strip())
			end=int(line.split(",")[2])	
			openlist[num].seek(start)#從start開始			
			
	##########################################REMAKE################################################################
					
			while openlist[num].tell() < end:
				c=openlist[num].read(1)	
				R.write(c)				
			#print "start:",start,"\t","end:",end,"\t",num,"\t","R:",R.tell()
	print WantToRemake ,"REMAKE Successfully!"
	################################################################################################################			
