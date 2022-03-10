import ast
from distutils import text_file
from email import message
import random 
import requests
from seleniumbase import __version__
from seleniumbase import BaseCase

class WordleTests(BaseCase):

    word_list = []

    def initialize_word_list(self):
        text_file = "https://seleniumbase.io/cdn/txt/wordle_words.txt";
        word_string = requests.get(text_file).text
        self.word_list = ast.literal_eval(word_string)
    
    def modify_word_list(self, word, letter_state):
        new_word_list = []
        correct_letters = []
        present_letters = []
        for i in range(len(word)):
            if letter_state[i] == "correct":
                correct_letters.append(word[i])
                for w in self.word_list:
                    if w[i] == word[i]:
                        new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []
        for i in range(len(word)):
            if letter_state[i] == "present":
                present_letters.append(word[i])
                for w in self.word_list:
                    if word[i] in w and word[i] != w[i]:
                        new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []
        for i in range(len(word)):
            if (
                letter_state[i] == "absent"
                and word[i] not in correct_letters
                and word[i] not in present_letters
            ):
                for w in self.word_list:
                    if word[i] not in w:
                        new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []
    
    def skip_incorrect_env(self):
        if self.headless:
            message = "This test does not run in headless mode!"
            print(message)
            self.skip(message)
        version = [int(i) for i in __version__.split(".") if i.isdigit()]
        if version < [2, 4, 4]:
            message = "Requires SeleniumBase 2.4.4 or newer!"
            print(message)
            self.skip(message)
            


