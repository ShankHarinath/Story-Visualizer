__author__ = 'Shank'

import codecs
from textblob import TextBlob


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
    def get_sentiment_polarity(sentences):
        polarity = 0
        for sent in sentences:
            blob = TextBlob(sent)
            for sentence in blob.sentences:
                polarity += sentence.sentiment.polarity
        return polarity
