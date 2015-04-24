'''
Created on Apr 1, 2015

@author: Ankita
'''
import pickle
import sys
import nltk
from nltk import *

def BifurcateInformation(element,elementName):
	elementMap = {}
	PersonList = []
	OrganisationList = []
	LocationList = []
	
	
	for i,w in enumerate(element):
		NERtag = element[i][1]
		if NERtag == "B-PER" :
			word = element[i][0]
			if i < len(element) -2:
				if element[i+1][1] == "I-PER":
					i+=1
					while element[i][1] == "I-PER": 
						word = word +" "+element[i][0]
						i+=1
			elementMap["Person"] = word
		
		if NERtag == "B-ORG" :
			word = element[i][0]
			if i < len(element) -2:
				if element[i+1][1] == "I-ORG":
					i+=1
					while element[i][1] == "I-ORG": 
						word = word +" "+element[i][0]
						i+=1
	
			elementMap["Organisation"] = word
		
			
		
		if NERtag == "B-LOC" :
			word = element[i][0]
			if i < len(element) -2:
				if element[i+1][1] == "I-LOC":
					i+=1
					while element[i][1] == "I-LOC": 
						word = word +" "+element[i][0]
						i+=1
			elementMap["Location"] = word
		
			
	
	print(elementName)
	print(elementMap)
	elementMap.clear()
	PersonList = []
	OrganisationList = []
	LocationList = []
	
	
				

def GenerateSubjectRelationObject(lineWithTags,subject,action,object):
	subjectList = subject[0].split()
	actionList = action[0].split()
	objectList = object[0].split()
	
	intermediateSubjectList = []
	intermediateActionList = []
	intermediateObjectList = []
	
	for token in lineWithTags[2:len(lineWithTags)-2]:
		
		if token[0] in subjectList:
			intermediateSubjectList.append([token[0],token[1]])
		if token[0] in actionList:
			intermediateActionList.append([token[0],token[1]])
		if token[0] in objectList:
			intermediateObjectList.append([token[0],token[1]])
	
	
	BifurcateInformation(intermediateSubjectList,"Subject")
	BifurcateInformation(intermediateActionList,"Action")
	BifurcateInformation(intermediateObjectList,"Object")
	print "*******************************"
	

	intermediateSubjectList = []
	intermediateActionList = []
	intermediateObjectList = []
	
	
relations = pickle.load(open(sys.argv[1],"rb"))
ner_tagger = SennaNERTagger('C:\Users\Ankita\eclipse_workspace\StoryTeller\storyteller\senna')

sentence =""
subject=""
action = ""
object = ""
for relation in relations:
	sentence = ""
	subject = relation[0]
	action = relation[1]
	object = relation[2]
	for token in relation:
		for word in token:
			sentence = sentence +" "+ word

	sentences1 = tokenize.sent_tokenize(sentence)
	taggedLine = ner_tagger.tag(word_tokenize(str(sentences1)))
	GenerateSubjectRelationObject(taggedLine,subject,action,object)	

	
	