# ------------------ IMPORTS ------------------ #
from collections import Counter  # Counting frequencies
from itertools import chain  # Flattening 2D arrays
import numpy as np


# ---------------- FUNCTIONS ----------------- #
def create_map_reduced_matrix(lan_dict, book):
    matrix = np.zeros((max(dict.values()) + 1, (max(dict.values()) + 1)), dtype=int)

    def mapper(sentence):  # Split all into pairs
        return list(map(lambda pair: ''.join(pair).lower(), zip(sentence, sentence[1:])))

    def reducer(lst):  # Count all pairs
        return list(Counter(lst).items())

    flatmap = list(chain.from_iterable(list(map(mapper, book))))  # Apply mapper and flatten 2D list
    for freq in reducer(flatmap):  # For each frequency in result from reducer
        try:
            matrix[lan_dict[freq[0][0]]][lan_dict[freq[0][1]]] += freq[1]  # Add frequency to matrix
        except:
            pass

    return matrix

def main():
    with open("english_book.txt", "r") as file:
        book = file.readlines()

    lan_dict = {
        "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
        "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18,
        "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25, " ": 26, "0": 27,
        "1": 27, "2": 27, "3": 27, "4": 27, "5": 27, "6": 27, "7": 27, "8": 27, "9": 27,
        ".": 28, ",": 28, "-": 28, "_": 28, "/": 28, ":": 28, ";": 28, "*": 28, "&": 28,
        "?": 28, "!": 28, "(": 28, ")": 28
    }

    print(create_map_reduced_matrix(lan_dict, book))


# ---------------- EXECUTION ----------------- #
main()