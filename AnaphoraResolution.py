import nltk
from nltk import *
import os
from subprocess import Popen, PIPE
from nltk.tag import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *


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


with open("newone","r") as f:
	lines = f.readlines()

for line in lines:
	singleSentence+=line

sentences = tokenize.sent_tokenize(singleSentence)

ner_tagger = SennaNERTagger('/home/ankita1005/Pictures/senna')
for sentence in sentences:
	taggedLine = ner_tagger.tag(word_tokenize(sentence))
	length = len(taggedLine)
	for i,w in enumerate(taggedLine):
		
		NERtag = taggedLine[i][1]
		if NERtag == "B-PER" :
			word = taggedLine[i][0]
			if i < length -1:
				if taggedLine[i+1][1] == "I-PER":
					i+=1
					while taggedLine[i][1] == "I-PER": 
						word = word +" "+taggedLine[i][0]
						i+=1
			Person.add(word)
		if NERtag == "B-ORG":
			word = taggedLine[i][0]
			if i < length -1:
				if taggedLine[i+1][1] == "I-ORG":
					i+=1
					while taggedLine[i][1] == "I-ORG": 
						word = word +" "+taggedLine[i][0]
						i+=1
			Organisation.add(word)
		if NERtag == "B-LOC":
			word = taggedLine[i][0]
			if i < length -1:
				if taggedLine[i+1][1] == "I-LOC":
					i+=1
					while taggedLine[i][1] == "I-LOC": 
						word = word +" "+taggedLine[i][0]
						i+=1
			Location.add(word)
		



process = Popen(["java", "-jar", "/home/ankita1005/NLP/Project/JavaRAP_1.13/AnaphoraResolution.jar", "/home/ankita1005/NLP/Project/JavaRAP_1.13/newone"], stdout=PIPE)
(output, err) = process.communicate()
anaphores = str(output).split("\\n***********Head of Results**************\\n")[1].split("\\n***********End of Results***************\\n\\n")[0].split(", \\n")
	
previousNoun = ""

for anaphor in anaphores:
	#print(anaphor)

	data = anaphor.split("<--")
	value = data[0].split(")")
	if len(value) > 1:
		noun = value[1].strip()
	else:
		noun = previousNoun
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
	
	
	#print(noun)
	
	if pronounToBeReplaced in PRP and noun in Person:
		a = lineToBeReplaced.replace(pronounToBeReplaced,noun)
		sentences[int(lineNumber)] = a
	elif pronounToBeReplaced in PRP_Other and noun in Person:
		a = lineToBeReplaced.replace(pronounToBeReplaced,noun)
		sentences[int(lineNumber)] = a
	elif pronounToBeReplaced in it:
		if noun in Person and previousNoun not in Person:
			a = lineToBeReplaced.replace(pronounToBeReplaced,previousNoun)
			sentences[int(lineNumber)] = a
		else:
			a = lineToBeReplaced.replace(pronounToBeReplaced,noun)
			sentences[int(lineNumber)] = a
			
	elif pronounToBeReplaced in theyThem:
		a = lineToBeReplaced.replace(pronounToBeReplaced,noun)
		sentences[int(lineNumber)] = a
	else:
		a = lineToBeReplaced.replace(pronounToBeReplaced,noun)
		sentences[int(lineNumber)] = a
		
	previousNoun = noun	
	print(a)
	print("******")
	
