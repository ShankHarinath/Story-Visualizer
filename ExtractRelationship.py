from nltk.tree import *
from copy import deepcopy
from operator import itemgetter
import re
import os
from nltk.tag.stanford import NERTagger
import pickle
import sys
from nltk.tag import *
from nltk import *
from collections import *
from InformationExtraction import InfoExtractor
import json

info = []
characters = set()


def extract_relations(input_file):
    global info

    # os.system("cd Java/ && /usr/local/java/jdk1.8.0_20/bin/javac -cp \"*\" TextSimplification.java ")
    # os.system("cd Java/ && /usr/local/java/jdk1.8.0_20/bin/java -cp \"*:.\" TextSimplification "+os.path.abspath(input_file))
    os.system("cd Java/ && javac -cp \"*\" TextSimplification.java ")
    os.system("cd Java/ && java -cp \"*:.\" TextSimplification " + os.path.abspath(input_file))

    trees = read_parse_trees("Java/trees.txt")
    relations = []

    for tree in trees:
        positions = tree.treepositions()
        # positions = level_wise_sort(positions,[0])
        while len(positions) != 0:
            position = list(positions[0])

            if str(tree[position]).startswith("(VP"):
                left = get_left_part(tree, list(position))
                #	relation = get_base_relation(tree,list(position))
                get_right_part(tree, "", position, left)
                positions = update_positions(positions)
            else:
                positions.pop(0)
        relations = deepcopy(print_output(relations))
        info = []
        # tree.draw()
    pickle.dump(relations, open('relations.txt', 'wb'))
    return relations


def update_positions(positions):
    start = positions[0]
    start = "".join([str(x) for x in start])
    updated_positions = []

    for position in positions[1:]:
        if not ("".join([str(x) for x in position])).startswith(start):
            updated_positions.append(position)
    return updated_positions


def read_parse_trees(file_name):
    f = open(file_name)
    trees = f.readlines()

    for index in range(len(trees)):
        trees[index] = Tree.fromstring(trees[index])

    return trees


def format_tree(tree):
    tree = str(tree).split(")")
    sentence = []
    for token in tree:
        token = token[::-1]
        sentence.append(token[:token.find(" ")][::-1])

    sentence = " ".join(sentence).strip()
    sentence = ' '.join(sentence.split())
    return sentence


def print_output(relations):
    global info
    for index in range(len(info)):
        if info[index][0] is None:
            continue
        info[index][0] = format_tree(info[index][0])
        info[index][1] = format_tree(info[index][1])
        info[index][2] = format_tree(info[index][2])
        if re.search('[a-zA-Z]', info[index][0]) and re.search('[a-zA-Z]',
                                                               info[index][1]) and re.search('[a-zA-Z]',
                                                                                             info[index][2]):
            print([[info[index][0]], [info[index][1]], [info[index][2]]])
            relations.append([[info[index][0]], [info[index][1]], [info[index][2]]])
    return relations


def get_right_part(tree, relation, root, left):
    global info
    root1 = deepcopy(root)
    flag = False
    if str(tree[tuple(root + [0])]).startswith("(VB"):
        relation += str(tree[tuple(root + [0])])
        flag = True

    root = "".join(str(x) for x in root)
    positions = tree.treepositions()
    positions = level_wise_sort(positions, root)
    if flag:
        positions.remove(root1 + [0])
    for position in positions:
        if str(tree[position]).startswith("(RB") or str(tree[position]).startswith("(ADVP"):
            relation += str(tree[position])
        elif str(tree[position]).startswith("(VP") and not str(tree[position]).startswith("(VB"):
            get_right_part(tree, relation, position, left)
        else:
            info.append([left, relation, tree[position]])


def get_left_part(tree, position):
    position = list(position)
    if position[-1] > 0:
        position[-1] -= 1
        return tree[tuple(position)]


def get_base_relation(tree, position):
    return tree[tuple(position + [0])]


def level_wise_sort(positions, root):
    heirarchy = []
    root = "".join(str(x) for x in root)
    for index in range(len(positions)):
        positions[index] = list(positions[index])
        positions[index] = "".join(str(x) for x in positions[index])
        if (len(positions[index]) == (len(root) + 1)) and positions[index].startswith(root) is not False and positions[
            index] is not root:
            heirarchy.append(positions[index])
    positions = deepcopy(heirarchy)

    for index in range(len(positions)):
        positions[index] = [positions[index], len(positions[index])]

    positions = sorted(positions, key=itemgetter(1))
    for index in range(len(positions)):
        positions[index] = positions[index][0]
        positions[index] = [int(x) for x in positions[index]]
    return positions


def get_family_rel(sentence, relation):
    tagged_sent = ""
    for tag in sentence:
        tagged_sent += tuple2str(tag) + " "

    ner = tagged_sent.split(relation)

    if len(ner) < 2:
        return

    ner1 = ner2 = ""

    for idx, word in enumerate(reversed(word_tokenize(ner[0]))):
        wtag = str(word).split("/")
        if len(wtag) > 1 and wtag[1] == "NNP":
            ner1 = wtag[0]
            characters.add(ner1)
            if idx + 1 < len(word_tokenize(ner[0])[::-1]) and "/" in word_tokenize(ner[0])[::-1][idx + 1] and \
                            str(word_tokenize(ner[0])[::-1][idx + 1]).split("/")[1] == "NNP":
                ner1 = str(word_tokenize(ner[0])[::-1][idx + 1]).split("/")[0] + " " + ner1
                characters.add(ner1)
            break

    for idx, word in enumerate(word_tokenize(ner[1])[1:]):
        wtag = str(word).split("/")
        if len(wtag) > 1 and wtag[1] == "NNP":
            ner2 = wtag[0]
            characters.add(ner2)
            if idx + 1 < len(word_tokenize(ner[1])[1:]) and "/" in word_tokenize(ner[1])[1:][idx + 1] and \
                            word_tokenize(ner[1])[1:][idx + 1].split("/")[1] == "NNP":
                ner2 += " " + str(word_tokenize(ner[1])[1:][idx + 1]).split("/")[0]
                characters.add(ner2)
            break

    if str(word_tokenize(ner[0])[-1]).split("/")[0] == "'s":
        rel = ner1 + " -> " + relation + " -> " + ner2
    else:
        rel = ner2 + " -> " + relation + " -> " + ner1

    if not ner1 or not ner2:
        return
    return rel


if __name__ == "__main__":

    family_list = ["father", "mother", "brother", "sister", "uncle", "aunt", "grandmother", "grandfather",
                   "great grandmother", "great grandfather", "dad", "mom", "pappa", "mamma", "grandma", "grandpa",
                   "grand son", "grand daughter", "daughter", "son", "nephew", "cousin", "niece", "friend", "mate",
                   "wife", "husband", "newborn", "sibling", "offspring", "stepmother", "stepmom", "stepfather",
                   "stepdad", "friends", "sisters", "brothers", "daughters", "sons", "cousins", "mates", "siblings",
                   "offsprings", "raises", "fellow", "parents", "parent", "peers", "ex-wife", "ex-husband", "love",
                   "roommate", "child", "children", "brother-in-law", "sister-in-law", "son-in-law", "daughter-in-law",
                   "relationship", "relation", "colleague", "girlfriend", "boyfriend"]

    location_list = ["went", "came", "gone", "from", "go", "been", "visited"]

    ner_tagger = SennaNERTagger('/usr/share/senna-v3.0')
    tagger = SennaTagger('/usr/share/senna-v3.0')
    relations = extract_relations(sys.argv[1])
    # relations = pickle.load(open("relations.txt", "rb"))

    family_relations = set()
    output = dict()

    for relation in relations:
        words = str(relation[0][0]).split() + str(relation[1][0]).split() + str(relation[2][0]).split()
        sent = str(relation[0][0]) + " " + str(relation[1][0]) + " " + str(relation[2][0])

        for word in words:
            if str(word).lower() in family_list:
                val = get_family_rel(tagger.tag(word_tokenize(sent)), word)
                if val is not None:
                    family_relations.add(val)

    print()
    print("Family Relations:")
    print()
    for r in family_relations:
        print(r)

    output["family_rel"] = list(family_relations)
    output["name"] = sys.argv[1]

    influence = Counter()
    char_rel = defaultdict(list)
    total = 0
    for relation in relations:
        words = str(relation[0][0]).split() + str(relation[1][0]).split() + str(relation[2][0]).split()

        for word in words:
            if str(word) in characters:
                char_rel[word].append(relation)
                influence[word] += 1
                total += 1

    print()
    print("Character Influence")
    print()
    for character in OrderedDict(sorted(influence.items(), key=itemgetter(1), reverse=True)):
        influence[character] /= total * 0.01
        print(character + " -> " + str(influence[character]) + " %")

    output["char_infl"] = dict(influence)
    output["chars"] = list(influence.keys())
    output["char_rel"] = dict(char_rel)

    js_res = {val: output[val] for val in output}

    print()
    print("Character Relations")
    print()
    for character in char_rel:
        print()
        print(character + " -> ")
        print()
        for rel in char_rel[character]:
            print(rel)

    with open('result.json', 'w') as fp:
        json.dump(js_res, fp)