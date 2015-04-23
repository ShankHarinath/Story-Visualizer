__author__ = 'Shank'

import codecs
from textblob import TextBlob
from operator import and_, add
from functools import reduce

from nltk.data import show_cfg
from nltk.tag import RegexpTagger
from nltk.parse import load_parser
from nltk.parse.malt import MaltParser
from nltk.sem.drt import resolve_anaphora, AnaphoraResolutionException
from nltk.sem.glue import DrtGlue

from nltk.inference.mace import MaceCommand
from nltk.inference.prover9 import Prover9Command


class Utility:

    @staticmethod
    def read_file(filename):
        with codecs.open(filename, "r", encoding='ISO-8859-1', errors="REPLACE") as file:
            lines = file.readlines()
            file.close()
            return lines

    @staticmethod
    def write_file(filename, text):
        with codecs.open(filename, "w", encoding='ISO-8859-1', errors="REPLACE") as file:
            file.write(text)
            file.close()

    @staticmethod
    def get_sentiment_polarity(knowledge_base):
        polarity = 0
        for sent in knowledge_base:
            blob = TextBlob(sent)
            for sentence in blob.sentences:
                polarity += sentence.sentiment.polarity
        return polarity

    @staticmethod
    def get_character_influence(knowledge_base, character):
        raise NotImplementedError("Yet to be implemented")