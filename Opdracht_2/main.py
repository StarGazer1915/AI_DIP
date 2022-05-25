# ------------------ IMPORTS ------------------ #
from collections import Counter  # Counting frequencies
from itertools import chain  # Flattening 2D arrays
import numpy as np


# ---------------- FUNCTIONS ----------------- #
def mapper(sentence):  # Split all into pairs
    return list(map(lambda pair: ''.join(pair).lower(), zip(sentence, sentence[1:])))


def reducer(lst):  # Count all pairs
    return list(Counter(lst).items())


def chopper(lst, n):
    chops = int(len(lst) / n)
    for i in range(0, len(lst), chops):
        yield lst[i:i + chops]


def create_matrix(lan_dict, text):
    matrix = np.zeros((max(lan_dict.values()) + 1, (max(lan_dict.values()) + 1)), dtype=int)

    if type(text) == list:
        chops = chopper(text, 4)
        for chop in chops:
            map_result = list(chain.from_iterable(map(mapper, chop)))
            for freq in reducer(map_result):  # For each frequency in result from reducer
                try:
                    matrix[lan_dict[freq[0][0]]][lan_dict[freq[0][1]]] += freq[1]  # Add frequency to matrix
                except:
                    pass
    else:
        senmap = list(map(lambda pair: ''.join(pair).lower(), zip(text, text[1:])))  # Apply mapper
        for freq in reducer(senmap):  # For each frequency in result from reducer
            try:
                matrix[lan_dict[freq[0][0]]][lan_dict[freq[0][1]]] += freq[1]  # Add frequency to matrix
            except:
                pass

    return np.divide(matrix, sum(sum(matrix)))  # Normalization


def define_language_of_sentences(lan_dict, book, eng_book_matrix, nl_book_matrix):
    nl_sen_num, eng_sen_num = 0, 0
    for sentence in book:
        senmat = create_matrix(lan_dict, sentence)
        eng = sum(sum(np.multiply(senmat, eng_book_matrix)))
        nl = sum(sum(np.multiply(senmat, nl_book_matrix)))

        if eng > nl:
            eng_sen_num += 1
        elif nl > eng:
            nl_sen_num += 1
        else:
            pass

    return [nl_sen_num, eng_sen_num]


def main():
    with open("english_book.txt", "r") as file:
        eng_book = file.readlines()

    with open("dutch_book.txt", "r") as file:
        nl_book = file.readlines()

    with open("english_book_test.txt", "r") as file:
        test_eng_book = file.readlines()

    with open("dutch_book_test.txt", "r") as file:
        test_nl_book = file.readlines()

    with open("sentences.nl-en.txt", "r") as file:
        validation_book = file.readlines()

    lan_dict = {
        "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
        "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18,
        "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25, " ": 26, "0": 27,
        "1": 27, "2": 27, "3": 27, "4": 27, "5": 27, "6": 27, "7": 27, "8": 27, "9": 27,
        ".": 28, ",": 28, "-": 28, "_": 28, "/": 28, ":": 28, ";": 28, "*": 28, "&": 28,
        "?": 28, "!": 28, "(": 28, ")": 28
    }

    eng_book_matrix = create_matrix(lan_dict, eng_book)
    nl_book_matrix = create_matrix(lan_dict, nl_book)

    result = define_language_of_sentences(lan_dict, validation_book, eng_book_matrix, nl_book_matrix)
    print(result)

    return result


# ---------------- EXECUTION ----------------- #
main()
