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
            ner = element[1]
            if ner_tag in ner:
                word = element[0]
                i += 1
                while i < len(elements) - 2 and ner_tag in elements[i][1]:
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
    def extract_ner(elements, element_name):
        element_map = dict()
        person = InfoExtractor.extract_list_by_tag(elements, element_name, "PER")
        person.update(InfoExtractor.extract_list_by_tag(elements, element_name, "MISC"))
        organization = InfoExtractor.extract_list_by_tag(elements, element_name, "ORG")
        location = InfoExtractor.extract_list_by_tag(elements, element_name, "LOC")

        element_map["person"] = person
        element_map["organization"] = organization
        element_map["location"] = location
        return element_map


    @staticmethod
    def extract_relation_breakdown(line_with_tags, subject, action, object, filter1, filter2):
        intermediate_subject_list = line_with_tags[0:len(subject.split())]
        intermediate_action_list = line_with_tags[len(subject.split()):len(subject.split())+len(action.split())]
        intermediate_object_list = line_with_tags[len(subject.split())+len(action.split()):]

        if filter1 is None and filter2 is None:
            subject_map = InfoExtractor.extract_ner(intermediate_subject_list, "Subject")
            relation_map = InfoExtractor.extract_ner(intermediate_action_list, "Action")
            object_map = InfoExtractor.extract_ner(intermediate_object_list, "Object")
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
            tagged_line = ner_tagger.tag(word_tokenize(sentence))

            if InfoExtractor.extract_relation_breakdown(tagged_line, sub, actn, obj, filter1, filter2):
                filtered_list.append(relation)
        return filtered_list


    @staticmethod
    def get_relation_entities(relation, ner_tagger):
        sub = relation[0][0]
        actn = relation[1][0]
        obj = relation[2][0]
        sentence = relation[0][0] + " " + relation[1][0] + " " + relation[2][0]
        tagged_line = ner_tagger.tag(word_tokenize(sentence))

        return InfoExtractor.extract_relation_breakdown(tagged_line, sub, actn, obj, None, None)

if __name__ == "__main__":
    ner_tagger = NERTagger('Java/english.muc.7class.nodistsim.crf.ser.gz', 'Java/stanford-ner-3.5.2.jar')
    relations = pickle.load(open("relations.txt", "rb"))

    # print(get_relation_entities([["Junie and Pam from Sheila 's class"], ['introduced'], ['themselves']], ner_tagger))
    print(InfoExtractor.filter_relations(relations, "PERSON", "PERSON", ner_tagger))