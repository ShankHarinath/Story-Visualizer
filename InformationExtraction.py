"""
Created on Apr 1, 2015

@author: Ankita
"""
from nltk.tag.stanford import NERTagger
from nltk import *
import pickle


class InfoExtractor:

    @staticmethod
    def extract_list_by_tag(elements, element_name, ner_tag):
        list1 = []
        ner_List = set()
        for i, element in enumerate(elements):
            ner_tag = element[1]
            if ner_tag == ner_tag:
                word = element[0]
                i += 1
                while i < len(elements) - 2 and elements[i][1] == ner_tag:
                    word = word + " " + elements[i][0]
                    i += 1

                name = word.split()
                for words in ner_List:
                    a = words.split()
                    for b in a:
                        list1.append(b)
                intersection = [val for val in name if val in list1]
                if len(intersection) == 0:
                    ner_List.add(word)
        return ner_List


    @staticmethod
    def extract_ner(elements, element_name, relation):
        if relation == "ANY" or relation is None:
            element_map = dict()
            person = InfoExtractor.extract_list_by_tag(elements, element_name, "PERSON")
            organization = InfoExtractor.extract_list_by_tag(elements, element_name, "ORGANIZATION")
            location = InfoExtractor.extract_list_by_tag(elements, element_name, "LOCATION")

            element_map["person"] = person
            element_map["organization"] = organization
            element_map["location"] = location
            return element_map
        else:
            element_map = dict()
            get_relation = InfoExtractor.extract_list_by_tag(elements, element_name, relation)
            if len(get_relation) != 0:
                element_map[relation] = get_relation
            return element_map


    @staticmethod
    def extract_relation_breakdown(line_with_tags, subject, action, object, filter1, filter2):
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

        if filter1 is None and filter2 is None:
            subject_map = InfoExtractor.extract_ner(intermediate_subject_list, "Subject", filter1)
            relation_map = InfoExtractor.extract_ner(intermediate_action_list, "Action", "")
            object_map = InfoExtractor.extract_ner(intermediate_object_list, "Object", filter2)
            return [subject_map, relation_map, object_map]
        else:
            tags = ([tag[1] for tag in intermediate_subject_list])
            if filter1 not in tags:
                return False
            tags = ([tag[1] for tag in intermediate_object_list])
            if filter2 not in tags:
                return False
            return True


    @staticmethod
    def filter_relations(relations, filter1, filter2, ner_tagger):
        filtered_list = list()
        for relation in relations:
            sub = relation[0][0]
            actn = relation[1][0]
            obj = relation[2][0]
            sentence = relation[0][0] + " " + relation[1][0] + " " + relation[2][0]
            tagged_line = ner_tagger.tag(word_tokenize(sentence))[0]
            print(tagged_line)
            if InfoExtractor.extract_relation_breakdown(tagged_line, sub, actn, obj, filter1, filter2):
                filtered_list.append(relation)
        return filtered_list


    @staticmethod
    def get_relation_entities(relation, ner_tagger):
        sub = relation[0][0]
        actn = relation[1][0]
        obj = relation[2][0]
        sentence = relation[0][0] + " " + relation[1][0] + " " + relation[2][0]
        tagged_line = ner_tagger.tag(word_tokenize(sentence))[0]
        return InfoExtractor.extract_relation_breakdown(tagged_line, sub, actn, obj, None, None)

if __name__ == "__main__":
    ner_tagger = NERTagger('Java/english.muc.7class.nodistsim.crf.ser.gz', 'Java/stanford-ner-3.5.2.jar')
    relations = pickle.load(open("relations.txt", "rb"))

    # print(get_relation_entities([["Junie and Pam from Sheila 's class"], ['introduced'], ['themselves']], ner_tagger))
    print(InfoExtractor.filter_relations(relations, "PERSON", "PERSON", ner_tagger))