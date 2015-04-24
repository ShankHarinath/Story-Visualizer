import nltk
from nltk.tree import *
from copy import deepcopy
from operator import itemgetter
import re
import os
import cPickle
import sys

info = []


def main(input_file):
    global info
    left = ""

    #os.system("cd Java/ && /usr/local/java/jdk1.8.0_20/bin/javac -cp \"*\" TextSimplification.java ")
    #os.system("cd Java/ && /usr/local/java/jdk1.8.0_20/bin/java -cp \"*:.\" TextSimplification "+os.path.abspath(input_file))
    os.system("cd Java/ && javac -cp \"*\" TextSimplification.java ")
    os.system("cd Java/ && java -cp \"*:.\" TextSimplification "+os.path.abspath(input_file))
    
    trees = read_parse_trees("Java/trees.txt")
    relations = []

    for tree in trees:
        positions = tree.treepositions()
        #positions = level_wise_sort(positions,[0])
        while len(positions)!=0:
            position = list(positions[0])

            if str(tree[position]).startswith("(VP"):
                left = get_left_part(tree,list(position))
                #	relation = get_base_relation(tree,list(position))
                get_right_part(tree,"",position,left)
                positions = update_positions(positions)
            else:
                positions.pop(0)
        relations = deepcopy(print_output(relations))
        info = []
        tree.draw()
    cPickle.dump(relations, open('relations.txt', 'wb'))


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
        if re.search('[a-zA-Z]', info[index][0]) and re.search('[a-zA-Z]', info[index][1]) and re.search('[a-zA-Z]', info[index][2]):
            print([[info[index][0]], [info[index][1]], [info[index][2]]])
            relations.append([[info[index][0]], [info[index][1]], [info[index][2]]])
    return relations


def get_right_part(tree,relation,root,left):
    global info
    root1 = deepcopy(root)
    flag = False
    if str(tree[tuple(root+[0])]).startswith("(VB") :
        relation += str(tree[tuple(root+[0])])
        flag = True

    root = "".join(str(x) for x in root)
    heirarchy = []
    positions = tree.treepositions()
    positions = level_wise_sort(positions, root)
    if flag:
        positions.remove(root1+[0])
    for position in positions:
        if str(tree[position]).startswith("(RB") or str(tree[position]).startswith("(ADVP"):
            relation += str(tree[position])
        elif str(tree[position]).startswith("(VP") and not str(tree[position]).startswith("(VB"):
            get_right_part(tree,relation,position,left)
        else:
            # print(relation)
            # print(tree[position])
            # print("\n\n")
            info.append([left,relation,tree[position]])


def get_left_part(tree,position):
    #LEFT
    position = list(position)
    if position[-1] > 0:
        position[-1] -= 1
        return tree[tuple(position)]


def get_base_relation(tree,position):
    #RELATION
    return tree[tuple(position+[0])]


def level_wise_sort(positions, root):
    heirarchy = []
    root = "".join(str(x) for x in root)
    for index in range(len(positions)):
        positions[index] = list(positions[index])
        positions[index] = "".join(str(x) for x in positions[index])
        if (len(positions[index]) == (len(root)+1)) and positions[index].startswith(root)!=False and positions[index] != root:
            heirarchy.append(positions[index])
    positions = deepcopy(heirarchy)

    for index in range(len(positions)):
        positions[index] = [positions[index],len(positions[index])]

    positions = sorted(positions, key=itemgetter(1))
    for index in range(len(positions)):
        positions[index] = positions[index][0]
        positions[index] = [int(x) for x in positions[index]]
    return positions

if __name__ == "__main__":
    main(sys.argv[1])