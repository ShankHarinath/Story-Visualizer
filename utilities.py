__author__ = 'Shank'

import codecs


class Utility:

    patterns = [
        (r'.*ing$', 'VBG'),  # gerunds
        (r'.*ed$', 'VBD'),  # simple past
        (r'.*es$', 'VBZ'),  # 3rd singular present
        (r'.*ould$', 'MD'),  # modals
        (r'.*\'s$', 'NN$'),  # possessive nouns
        (r'.*s$', 'NNS')  # plural nouns
    ]

    @staticmethod
    def read_file(filename):
        with codecs.open(filename, "r", encoding='ISO-8859-1', errors="REPLACE") as file:
            lines = file.readlines()
            file.close()
            return lines

    @staticmethod
    def write_file(filename, text):
        with open(filename, 'wb') as file:
            file.write(text)