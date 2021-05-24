import os

import nltk
from nltk.tokenize import word_tokenize

class FileReader:
    def __init__(self, file_name):
        self.file_name = file_name
        file = None
        self.file_lines = []
        self.file_content = ''
        self.line_count = None
        self.word_count = None
        try:
            file = open(file_name, 'r', encoding='utf8')
            self.file_lines = file.readlines()
            self.file_content = ''.join(self.file_lines)
            self.line_count = len(self.file_lines)
            self.word_count = len(
                word_tokenize(self.file_content, language='russian')
            )
        except FileNotFoundError:
            print('ERROR: file does not exist')
        file.close()

    def read(self):
        return self.file_contentЫ

    def write_line(self, content):
        try:
            file = open(self.file_name)
            file.write(content)
        except FileNotFoundError:
            print('ERROR: file does not exist')

    def count_lines(self):
        return [self.line_count, self.word_count]

    def __add__(self, other):
        new_name = self.file_name[:-4] + '_add_' + other.file_name[:-4] + '.txt'
        new_content = self.file_lines + other.file_lines

        try:
            new_file = open(new_name, 'w', encoding='utf8')
            new_file.writelines(new_content)
            new_file.close()
        except FileExistsError:
            print('ERROR: file already exist')

        new_file_reader = FileReader(new_name)
        return new_file_reader

    def __str__(self):
        return os.getcwd() + self.file_name
