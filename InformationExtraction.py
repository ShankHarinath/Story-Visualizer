'''
Created on Apr 1, 2015

@author: Ankita
'''
import pickle
import sys
import nltk
from nltk import *
from nltk.tag.stanford import NERTagger

def BifurcateInformation(elements,elementName):
	elementMap = {}
	Person = set()
	Organisation = set()
	Location= set()

	list1=[]
	word = ""
	
	
	for i,element in enumerate(elements):
		NERtag = element[1]
		if NERtag == "PERSON":
			word = element[0]
			i+=1
			while i < len(elements)-2 and elements[i][1] == "PERSON": 
				word = word +" "+elements[i][0]
				#print("adding "+ word)
				i+=1
			
			Name = word.split()
			for words in Person:
				a = words.split()
				for b in a:
					list1.append(b)
			intersection = [val for val in Name if val in list1]
			if len(intersection) == 0: 
				Person.add(word)
			word = ""
			list1 = []

		if NERtag == "ORGANIZATION":
			word = element[0]
			i+=1
			while i < len(elements)-2 and elements[i][1] == "ORGANIZATION": 
				word = word +" "+elements[i][0]
				#print("adding "+ word)
				i+=1
			
			Name = word.split()
			for words in Organisation:
				a = words.split()
				for b in a:
					list1.append(b)
			intersection = [val for val in Name if val in list1]
			if len(intersection) == 0: 
				Organisation.add(word)
			word = ""
			list1 = []
			
		if NERtag == "LOCATION":
			word = element[0]
			i+=1
			while i < len(elements)-2 and elements[i][1] == "LOCATION": 
				word = word +" "+elements[i][0]
				#print("adding "+ word)
				i+=1
			
			Name = word.split()
			for words in Location:
				a = words.split()
				for b in a:
					list1.append(b)
			intersection = [val for val in Name if val in list1]
			if len(intersection) == 0: 
				Location.add(word)
			word = ""
			list1 = []
	
	elementMap["Person"] = Person
	elementMap["Organisation"] = Organisation
	elementMap["Location"] = Location
	print(elementName)
	print(elementMap)
	elementMap.clear()
	PersonList = []
	OrganisationList = []
	LocationList = []

	
				

def GenerateSubjectRelationObject(lineWithTags,subject,action,object):
	subjectList = subject.split()
	actionList = action.split()
	objectList = object.split()

	intermediateSubjectList = []
	intermediateActionList = []
	intermediateObjectList = []
	
	

	for token in lineWithTags:
		if token[0] in subjectList and [token[0],token[1]] not in intermediateSubjectList:
			intermediateSubjectList.append([token[0],token[1]])
		if token[0] in actionList and [token[0],token[1]] not in intermediateActionList:
			intermediateActionList.append([token[0],token[1]])
		if token[0] in objectList and [token[0],token[1]] not in intermediateObjectList:
			intermediateObjectList.append([token[0],token[1]])
	
	
	BifurcateInformation(intermediateSubjectList,"Subject")
	BifurcateInformation(intermediateActionList,"Action")
	BifurcateInformation(intermediateObjectList,"Object")
	print "*******************************"
	

	intermediateSubjectList = []
	intermediateActionList = []
	intermediateObjectList = []
	
	
relations = pickle.load(open(sys.argv[1],"rb"))
ner_tagger = NERTagger('Java/english.muc.7class.nodistsim.crf.ser.gz', 'Java/stanford-ner-3.5.2.jar')

sentence =""
subject=""
action = ""
object = ""
for relation in relations:
	sentence = ""
	subject = relation[0][0]
	action = relation[1][0]
	object = relation[2][0]
	
	for token in relation:
		for word in token:
			sentence = sentence +" "+ word
	
	taggedLine = ner_tagger.tag(word_tokenize(sentence))
	print(taggedLine)
	GenerateSubjectRelationObject(taggedLine[0],subject,action,object)	
	
	
	