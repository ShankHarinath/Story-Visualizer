"""
Created on Apr 1, 2015

@author: Ankita
"""

import pickle
import sys
from nltk import *
from nltk.tag.stanford import NERTagger


def extract_ner(elements, element_name):
    element_map = dict()
    person = set()
    organization = set()
    location = set()

    list1 = []

    for i, element in enumerate(elements):
        ner_tag = element[1]
        if ner_tag == "PERSON":
            word = element[0]
            i += 1
            while i < len(elements) - 2 and elements[i][1] == "PERSON":
                word = word + " " + elements[i][0]
                # print("adding "+ word)
                i += 1

            name = word.split()
            for words in person:
                a = words.split()
                for b in a:
                    list1.append(b)
            intersection = [val for val in name if val in list1]
            if len(intersection) == 0:
                person.add(word)
            list1 = []

        if ner_tag == "ORGANIZATION":
            word = element[0]
            i += 1
            while i < len(elements) - 2 and elements[i][1] == "ORGANIZATION":
                word = word + " " + elements[i][0]
                # print("adding "+ word)
                i += 1

            name = word.split()
            for words in organization:
                a = words.split()
                for b in a:
                    list1.append(b)
            intersection = [val for val in name if val in list1]
            if len(intersection) == 0:
                organization.add(word)
            list1 = []

        if ner_tag == "LOCATION":
            word = element[0]
            i += 1
            while i < len(elements) - 2 and elements[i][1] == "LOCATION":
                word = word + " " + elements[i][0]
                # print("adding "+ word)
                i += 1

            name = word.split()
            for words in location:
                a = words.split()
                for b in a:
                    list1.append(b)
            intersection = [val for val in name if val in list1]
            if len(intersection) == 0:
                location.add(word)
            list1 = []

    element_map["person"] = person
    element_map["organization"] = organization
    element_map["location"] = location
    print(element_name)
    print(element_map)
    element_map.clear()


def extract_relation_info(line_with_tags, subject, action, object):
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

    extract_ner(intermediate_subject_list, "Subject")
    extract_ner(intermediate_action_list, "Action")
    extract_ner(intermediate_object_list, "Object")
    print("*******************************")


relations = pickle.load(open(sys.argv[1], "rb"))
ner_tagger = NERTagger('Java/english.muc.7class.nodistsim.crf.ser.gz', 'Java/stanford-ner-3.5.2.jar')

for relation in relations:
    sub = relation[0][0]
    actn = relation[1][0]
    obj = relation[2][0]

    sentence = relation[0][0] + " " + relation[1][0] + " " + relation[2][0]

    taggedLine = ner_tagger.tag(word_tokenize(sentence))[0]
    print(relation)

    extract_relation_info(taggedLine, sub, actn, obj)