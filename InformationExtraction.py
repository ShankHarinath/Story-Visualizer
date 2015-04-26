"""
Created on Apr 1, 2015

@author: Ankita
"""

import pickle
import sys
from nltk import *
from nltk.tag.stanford import NERTagger

subject_map = dict()
relation_map = dict()
object_map = dict()

summary_lines = []
def extract_list_by_tag(elements,element_name,NERtag):
    list1 = []
    NERList = set()
    for i, element in enumerate(elements):
        ner_tag = element[1]
        if ner_tag == NERtag:
            word = element[0]
            i += 1
            while i < len(elements) - 2 and elements[i][1] == NERtag:
                word = word + " " + elements[i][0]
                # print("adding "+ word)
                i += 1

            name = word.split()
            for words in NERList:
                a = words.split()
                for b in a:
                    list1.append(b)
            intersection = [val for val in name if val in list1]
            if len(intersection) == 0:
                NERList.add(word)
    return NERList
            
    
def extract_ner(elements, element_name,relation):
    
    if relation == "ANY" or relation == "":
        element_map = dict()
        person = set()
        organization = set()
        location = set()

        person = extract_list_by_tag(elements,element_name,"PERSON")
        organization = extract_list_by_tag(elements,element_name,"ORGANIZATION")
        location = extract_list_by_tag(elements,element_name,"LOCATION")
        
        element_map["person"] = person
        element_map["organization"] = organization
        element_map["location"] = location
        return element_map
    else:
        element_map = dict()
        getRelation1 = set()
        getRelation2 = set()
        
        getRelation1 = extract_list_by_tag(elements,element_name,relation)
        #getRelation2 = extract_list_by_tag(elements,element_name,relation2)
        if len(getRelation1) != 0:
            element_map[relation] = getRelation1
        #element_map[relation2] = getRelation
        return element_map


def extract_relation_info(line_with_tags, subject, action, object,relation1,relation2):

    global subject_map
    global relation_map
    global object_map
    global summary_lines
    
    subject_list = subject.split()
    action_list = action.split()
    object_list = object.split()

    intermediate_subject_list = list()
    intermediate_action_list = list()
    intermediate_object_list = list()
    
    subject_map = dict()
    relation_map = dict()
    object_map = dict()
    
    
    for token in line_with_tags:
        if token[0] in subject_list and [token[0], token[1]] not in intermediate_subject_list:
            intermediate_subject_list.append([token[0], token[1]])
        if token[0] in action_list and [token[0], token[1]] not in intermediate_action_list:
            intermediate_action_list.append([token[0], token[1]])
        if token[0] in object_list and [token[0], token[1]] not in intermediate_object_list:
            intermediate_object_list.append([token[0], token[1]])
    
    subject_map = extract_ner(intermediate_subject_list, "Subject","ANY")
    relation_map = extract_ner(intermediate_action_list, "Action","ANY")
    object_map = extract_ner(intermediate_object_list, "Object","ANY")
    if relation1 == "" and relation2=="":
        summary_lines.append(line_with_tags)
    else:
        if len(subject_map) != 0 and len(object_map) != 0:
            summary_lines.append(line_with_tags)
           
def multiple_relation(relation,relation1,relation2):
    ner_tagger = NERTagger('Java/english.muc.7class.nodistsim.crf.ser.gz', 'Java/stanford-ner-3.5.2.jar')
    sub = relation[0][0]
    actn = relation[1][0]
    obj = relation[2][0]
    sentence = relation[0][0] + " " + relation[1][0] + " " + relation[2][0]
    taggedLine = ner_tagger.tag(word_tokenize(sentence))[0]
    extract_relation_info(taggedLine, sub, actn, obj,relation1,relation2)
       
def single_relation(relation):

    ner_tagger = NERTagger('Java/english.muc.7class.nodistsim.crf.ser.gz', 'Java/stanford-ner-3.5.2.jar')
    sub = relation[0][0]
    actn = relation[1][0]
    obj = relation[2][0]
    sentence = relation[0][0] + " " + relation[1][0] + " " + relation[2][0]
    taggedLine = ner_tagger.tag(word_tokenize(sentence))[0]
    extract_relation_info(taggedLine, sub, actn, obj,"","")
        
'''
relations = pickle.load(open("relations.txt", "rb"))
print("Single relation SRO -------- >")
single_relation([["Junie and Pam from Sheila 's class"], ['introduced'], ['themselves']])
print(summary_lines)
summary_lines=[]
print("**************************")
print(str(sys.argv[1]) +" to "+str(sys.argv[2])+" relation ------------>")
for relation in relations:
    multiple_relation(relation,str(sys.argv[1]),str(sys.argv[2]))
print(summary_lines)
'''