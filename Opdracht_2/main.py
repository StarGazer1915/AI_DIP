# ------------------ IMPORTS ------------------ #
from collections import Counter  # Counting frequencies
from itertools import chain  # Flattening 2D arrays
import numpy as np


# ---------------- FUNCTIONS ----------------- #
def mapper(sentence):  # Split all into pairs
    return list(map(lambda pair: ''.join(pair).lower(), zip(sentence, sentence[1:])))


def reducer(lst):  # Count all pairs
    return list(Counter(lst).items())


def create_sentence_matrix(lan_dict, sentence):
    matrix = np.zeros((max(lan_dict.values()) + 1, (max(lan_dict.values()) + 1)), dtype=int)
    senmap = list(map(lambda pair: ''.join(pair).lower(), zip(sentence, sentence[1:])))  # Apply mapper
    for freq in reducer(senmap):  # For each frequency in result from reducer
        try:
            matrix[lan_dict[freq[0][0]]][lan_dict[freq[0][1]]] += freq[1]  # Add frequency to matrix
        except:
            pass

    return matrix


def create_book_matrix(lan_dict, book):
    matrix = np.zeros((max(lan_dict.values()) + 1, (max(lan_dict.values()) + 1)), dtype=int)
    flatmap = list(chain.from_iterable(list(map(mapper, book))))  # Apply mapper and flatten 2D list
    for freq in reducer(flatmap):  # For each frequency in result from reducer
        try:
            matrix[lan_dict[freq[0][0]]][lan_dict[freq[0][1]]] += freq[1]  # Add frequency to matrix
        except:
            pass

    return matrix


def define_language_of_sentences(book, eng_book_matrix, nl_book_matrix):
    nl_sen_num, eng_sen_num = 0, 0
    for sentence in book:
        create_sentence_matrix


    return #[nl_sen_num, eng_sen_num]


def main():
    with open("english_book.txt", "r") as file:
        eng_book = file.readlines()

    with open("dutch_book.txt", "r") as file:
        nl_book = file.readlines()

    with open("test_book_eng.txt", "r") as file:
        test_eng_book = file.readlines()
    
    with open("test_book_nl.txt", "r") as file:
        test_nl_book = file.readlines()

    lan_dict = {
        "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
        "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18,
        "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25, " ": 26, "0": 27,
        "1": 27, "2": 27, "3": 27, "4": 27, "5": 27, "6": 27, "7": 27, "8": 27, "9": 27,
        ".": 28, ",": 28, "-": 28, "_": 28, "/": 28, ":": 28, ";": 28, "*": 28, "&": 28,
        "?": 28, "!": 28, "(": 28, ")": 28
    }

    eng_book_matrix = create_book_matrix(lan_dict, eng_book)
    nl_book_matrix = create_book_matrix(lan_dict, nl_book)

    print(define_language_of_sentences(bookie, eng_book_matrix, nl_book_matrix))

    return eng_book_matrix


# ---------------- EXECUTION ----------------- #
main()
