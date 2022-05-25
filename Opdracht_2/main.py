# ------------------ IMPORTS ------------------ #
from collections import Counter  # Counting frequencies
from itertools import chain  # Flattening 2D arrays
import numpy as np  # Creation of matrices and calculation


# ---------------- FUNCTIONS ----------------- #
def mapper(sentence):
    """
    Maps over a string and creates pairs of all the characters.
    It then returns a list with all of these pairs.
    @param sentence: str
    @return: list
    """
    return list(map(lambda pair: ''.join(pair).lower(), zip(sentence, sentence[1:])))


def reducer(lst):
    """
    Counts and sums up all the occurences of the pairs of characters in the list.
    In short, it counts the frequencies. (It could also count numbers or other values)
    @param lst: list
    @return: list
    """
    return list(Counter(lst).items())


def chopper(lst, n):
    """
    Chops a string or list into n parts.
    @param lst: list
    @param n: int
    @return: list
    """
    chops = int(len(lst) / n)
    for i in range(0, len(lst), chops):
        yield lst[i:i + chops]


def create_matrix(lan_dict, text):
    """
    Creates a matrix, then fills it with the frequencies of the pairs of characters.
    Can be used for strings and lists (a sentence or an entire book)
    @param lan_dict: dictionary
    @param text: list / str
    @return: list
    """
    matrix = np.zeros((max(lan_dict.values()) + 1, (max(lan_dict.values()) + 1)), dtype=int)

    if type(text) == list:
        chops = chopper(text, 4)
        for chop in chops:
            map_result = list(chain.from_iterable(map(mapper, chop)))  # Apply mapper()
            for freq in reducer(map_result):  # For each frequency in result from reducer()
                try:
                    matrix[lan_dict[freq[0][0]]][lan_dict[freq[0][1]]] += freq[1]  # Add frequency to matrix
                except:
                    pass
    else:
        senmap = list(map(lambda pair: ''.join(pair).lower(), zip(text, text[1:])))  # Apply mapper()
        for freq in reducer(senmap):  # For each frequency in result from reducer()
            try:
                matrix[lan_dict[freq[0][0]]][lan_dict[freq[0][1]]] += freq[1]  # Add frequency to matrix
            except:
                pass

    # NOTE: The following line may give a Invalid Value Runtime Warning, because it can divide by zero.
    result = np.divide(matrix, sum(sum(matrix)))  # Normalization for the matrix
    return result


def define_language_of_sentences(lan_dict, book, eng_book_matrix, nl_book_matrix):
    """
    Determines if a sentence is in Dutch or English. It multiplies the matrix of
    the sentence with the matrix of another book (eng/nl) and checks which sum
    is larger. The biggest value (either of the English matrix or the Dutch matrix)
    determines if the sentence is in English or Dutch.
    @param lan_dict: dictionary
    @param book: list
    @param eng_book_matrix: list
    @param nl_book_matrix: list
    @return: list
    """
    nl_sen_num, eng_sen_num = 0, 0
    for sentence in book:
        senmat = create_matrix(lan_dict, sentence)
        eng = sum(sum(np.multiply(senmat, eng_book_matrix)))
        nl = sum(sum(np.multiply(senmat, nl_book_matrix)))

        if eng > nl:
            # print(f"ENG: {sentence}")
            eng_sen_num += 1
        elif nl > eng:
            # print(f"NL: {sentence}")
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

    language_dict = {
        "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
        "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18,
        "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25, " ": 26, "0": 27,
        "1": 27, "2": 27, "3": 27, "4": 27, "5": 27, "6": 27, "7": 27, "8": 27, "9": 27,
        ".": 28, ",": 28, "-": 28, "_": 28, "/": 28, ":": 28, ";": 28, "*": 28, "&": 28,
        "?": 28, "!": 28, "(": 28, ")": 28
    }

    # Create book matrices for use in other functions.
    eng_book_matrix = create_matrix(language_dict, eng_book)
    nl_book_matrix = create_matrix(language_dict, nl_book)

    result = define_language_of_sentences(language_dict, validation_book, eng_book_matrix, nl_book_matrix)
    print(f"\nLines: {result[0]} NL | {result[1]} ENG")

    return result

# ---------------- EXECUTION ----------------- #
main()
