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
			if not PersonList:
				PersonList.append(word)
			
			tempList = list(PersonList)
			for per in PersonList:
				if per in word:
					PersonList.remove(per)
					PersonList.append(word)
				if word not in per:
					PersonList.append(word)
			elementMap["Person"] = PersonList
		tempList=[]	
		if NERtag == "B-ORG" :
			word = element[i][0]
			if i < len(element) -2:
				if element[i+1][1] == "I-ORG":
					i+=1
					while element[i][1] == "I-ORG": 
						word = word +" "+element[i][0]
						i+=1
			if not OrganisationList:
				OrganisationList.append(word)
			
			tempList = list(OrganisationList)
			for org in OrganisationList:
				if org in word:
					OrganisationList.remove(org)
					OrganisationList.append(word)
				if word not in org:
					OrganisationList.append(word)
			elementMap["Organisation"] = OrganisationList
			
		tempList=[]	
		if NERtag == "B-LOC" :
			word = element[i][0]
			if i < len(element) -2:
				if element[i+1][1] == "I-LOC":
					i+=1
					while element[i][1] == "I-LOC": 
						word = word +" "+element[i][0]
						i+=1
			if not LocationList:
				LocationList.append(word)
			
			tempList = list(LocationList)
			for loc in LocationList:
				if loc in word:
					LocationList.remove(loc)
					LocationList.append(word)
				if word not in loc:
					LocationList.append(word)
			elementMap["Location"] = LocationList
		tempList = []
		'''
		if NERtag == "O":
			word = element[i][0]
			i+=1
			while i < len(element) -2 and element[i][1] == "O":
				word = word +" "+element[i][0]
				i+=1
			elementMap[word] = "Other"
		'''
			
	
	print(elementName)
	print(elementMap)
	elementMap.clear()
	PersonList = []
	OrganisationList = []
	LocationList = []
	
	
				

def GenerateSubjectRelationObject(lineWithTags,subject,action,object):
	#subjectList = subject.split()
	#actionList = action.split()
	#objectList = object.split()
	
	intermediateSubjectList = []
	intermediateActionList = []
	intermediateObjectList = []
	
	
	for token in lineWithTags[2:len(lineWithTags)-2]:
		if token[0] in subject:
			intermediateSubjectList.append([token[0],token[1]])
		if token[0] in action:
			intermediateActionList.append([token[0],token[1]])
		if token[0] in object:
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
	print(taggedLine)
	GenerateSubjectRelationObject(taggedLine,subject,action,object)	

	
	