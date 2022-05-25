import numpy as np

with open("english_book.txt", "r") as file:
    book = file.readlines()

dict = {
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
    "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18,
    "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25, " ": 26, "0": 27,
    "1": 27, "2": 27, "3": 27, "4": 27, "5": 27, "6": 27, "7": 27, "8": 27, "9": 27,
    ".": 28, ",": 28, "-": 28, "_": 28, "/": 28, ":": 28, ";": 28, "*": 28, "&": 28,
    "?": 28, "!": 28, "(": 28, ")": 28
}

def get_frequencies_from_text(text, dict):
    matrix = np.zeros((max(dict.values())+1, (max(dict.values())+1)), dtype=int)
    for line in text:
        for ind in range(0, len(line)):
            try:
                char_1, char_2 = line[ind].lower(), line[ind+1].lower()
                if char_1 in dict and char_2 in dict:
                    matrix[dict[char_1]][dict[char_2]] += 1
            except:
                pass

    return matrix

freqs = get_frequencies_from_text(book, dict)

for row in freqs:
    print(row)

