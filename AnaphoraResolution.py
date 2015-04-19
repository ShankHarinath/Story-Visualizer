import nltk
from nltk import *
import os
from subprocess import Popen, PIPE


currPerson = ""
currOrg = ""
currLoc = ""

Person = set()
Organisation = set()
Location = set()

PRP = ["he","she","She","He"]
it = ["it","It"]
theyThem = ["they","them","Them","They"]
PRP_Other = ["his","her","His","Her"]

memory = {}

singleSentence = ""
taggedList=[]

with open("NewTestFile","r") as f:
	lines = f.readlines()

for line in lines:
	singleSentence+=line

sentences = tokenize.sent_tokenize(singleSentence)



process = Popen(["java", "-jar", "/home/ankita1005/NLP/Project/JavaRAP_1.13/AnaphoraResolution.jar", "/home/ankita1005/NLP/Project/JavaRAP_1.13/NewTestFile"], stdout=PIPE)
(output, err) = process.communicate()
anaphores = str(output).split("\\n***********Head of Results**************\\n")[1].split("\\n***********End of Results***************\\n\\n")[0].split(", \\n")

with open("NERTaggedOutput","r") as f1:
	NERTaggedlines = f1.readlines()

for line in NERTaggedlines:
	newLine = line.split("\n")
	for aLine in newLine:
		taggedList.append(aLine.split("\t"))
newTaggedList = [x for x in taggedList if x != ['']]
length = len(newTaggedList)
for i,w in enumerate(newTaggedList):
	
	NERtag = newTaggedList[i][1].lstrip()
	if NERtag == "S-PER":
		word = newTaggedList[i][0].lstrip()
		Person.add(word)
	if NERtag == "S-ORG":
		word = newTaggedList[i][0].lstrip()
		Organisation.add(word)
	if NERtag == "S-LOC":
		word = newTaggedList[i][0].lstrip()
		Location.add(word)
	if i < length -2:
		if NERtag == "B-PER":
			
			if NERtag == "B-PER" and newTaggedList[i+1][1].lstrip() == "E-PER":
				word = newTaggedList[i][0].lstrip()+" "+ newTaggedList[i+1][0].lstrip()
				Person.add(word)
			if newTaggedList[i+1][1].lstrip() == "I-PER":
				
				word = newTaggedList[i][0].lstrip()
				i+=1
				while newTaggedList[i][1].lstrip() == "I-PER": 
					word = word +" "+newTaggedList[i][0].lstrip()
					i+=1
				if newTaggedList[i][1].lstrip() == "E-PER":
					word = word+" "+ newTaggedList[i][0].lstrip()
				Person.add(word)
		if NERtag == "B-ORG":
			if NERtag == "B-ORG" and newTaggedList[i+1][1].lstrip() == "E-ORG":
				word = newTaggedList[i][0].lstrip()+" "+ newTaggedList[i+1][0].lstrip()
				Organisation.add(word)
			if newTaggedList[i+1][1].lstrip() == "I-ORG":
				
				word = newTaggedList[i][0].lstrip()
				i+=1
				while newTaggedList[i][1].lstrip() == "I-ORG": 
					word = word +" "+newTaggedList[i][0].lstrip()
					i+=1
				if newTaggedList[i][1].lstrip() == "E-ORG":
					word = word+" "+ newTaggedList[i][0].lstrip()
				Organisation.add(word)
		if NERtag == "B-LOC":
			if NERtag == "B-LOC" and newTaggedList[i+1][1].lstrip() == "E-LOC":
				word = newTaggedList[i][0].lstrip()+" "+ newTaggedList[i+1][0].lstrip()
				Location.add(word)
			if newTaggedList[i+1][1].lstrip() == "I-LOC":
				
				word = newTaggedList[i][0].lstrip()
				i+=1
				while newTaggedList[i][1].lstrip() == "I-LOC": 
					word = word +" "+newTaggedList[i][0].lstrip()
					i+=1
				if newTaggedList[i][1].lstrip() == "E-LOC":
					word = word+" "+ newTaggedList[i][0].lstrip()
				Location.add(word)
			
			

print(anaphores)
print("****")
for anaphor in anaphores:
	#print(anaphor)
	data = anaphor.split("<--")
	value = data[0].split(")")
	noun = value[1].strip()
	key = data[1].strip()
	lineNumber = key.split(" ")[0].split(",")[0].lstrip("(")
	pronounToBeReplaced = key.split(" ")[1]
	if data[0] in memory.keys():
		getValue = memory[value]
		memeory[key] = getValue
	else:
		memory[key] = noun
	#output_parsed.write(lines[i].replace(noun[1], pronoun[2]))
	lineToBeReplaced = sentences[int(lineNumber)]
	print(lineToBeReplaced)
	
	if (pronounToBeReplaced in PRP and noun in Person)  or (pronounToBeReplaced in it and (noun in Location or noun in Organisation)):
		
		a = lineToBeReplaced.replace(pronounToBeReplaced,noun)
		sentences[int(lineNumber)] = a
	elif pronounToBeReplaced in theyThem:
		
		a = lineToBeReplaced.replace(pronounToBeReplaced,noun)
		sentences[int(lineNumber)] = a
		
	print(a)
	print("******")
