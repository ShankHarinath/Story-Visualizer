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


#utility function 

def person_person_relation():
    if len(subject_map["person"]) != 0:
        print subject_map["person"]
    else:
        print "Sorry no person relations in subject"
    if len(object_map["person"]) != 0:
        print object_map["person"]
    else:    
        print "Sorry no person relation in object"
        
    print "****************************"
    
    

def person_any_relation():
    if len(subject_map["person"]) != 0:
        print subject_map["person"]
    else:
        print "Sorry no person relations in subject"

    print object_map["person"]
        
    print "****************************"
    

def any_person_relation():
    
    print subject_map["person"]
    
    if len(object_map["person"]) != 0:
        print object_map["person"]
    else:    
        print "Sorry no person relation in object"
        
    print "****************************"
    


def organization_organization_relation():
    if len(subject_map["organization"]) != 0:
        print subject_map["organization"]
    else:
        print "Sorry no organization relations in subject"
    if len(object_map["person"]) != 0:
        print object_map["organization"]
    else:    
        print "Sorry no organization relation in object"
        
    print "****************************"
    

def location_location_relation():
    if len(subject_map["location"]) != 0:
        print subject_map["location"]
    else:
        print "Sorry no location relations in subject"
    if len(object_map["location"]) != 0:
        print object_map["location"]
    else:    
        print "Sorry no location relation in object"
        
    print "****************************"
    

#end of ulility functions


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
            
    
def extract_ner(elements, element_name):
    
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
    #print(element_name)
    #print(element_map)
    return element_map


def extract_relation_info(line_with_tags, subject, action, object):

    global subject_map
    global relation_map
    global object_map
    
    subject_list = subject.split()
    action_list = action.split()
    object_list = object.split()

    intermediate_subject_list = list()
    intermediate_action_list = list()
    intermediate_object_list = list()

    for token in line_with_tags:
        if token[0] in subject_list and [token[0], token[1]] not in intermediate_subject_list:
            intermediate_subject_list.append([token[0], token[1]])
        if token[0] in action_list and [token[0], token[1]] not in intermediate_action_list:
            intermediate_action_list.append([token[0], token[1]])
        if token[0] in object_list and [token[0], token[1]] not in intermediate_object_list:
            intermediate_object_list.append([token[0], token[1]])

    subject_map = extract_ner(intermediate_subject_list, "Subject")
    relation_map = extract_ner(intermediate_action_list, "Action")
    object_map = extract_ner(intermediate_object_list, "Object")
    '''
    print("Subject")
    print(subject_map)
    print("Relation")
    print(relation_map)
    print("Object")
    print(object_map)
    print("*******************************")
    '''


relations = pickle.load(open("relations.txt", "rb"))
ner_tagger = NERTagger('Java/english.muc.7class.nodistsim.crf.ser.gz', 'Java/stanford-ner-3.5.2.jar')

for relation in relations:
    sub = relation[0][0]
    actn = relation[1][0]
    obj = relation[2][0]

    sentence = relation[0][0] + " " + relation[1][0] + " " + relation[2][0]

    taggedLine = ner_tagger.tag(word_tokenize(sentence))[0]
    #print(taggedLine)

    extract_relation_info(taggedLine, sub, actn, obj)
    #utility_function = sys.argv[2]
    person_person_relation()
    
   