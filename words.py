import random
import sys

from collections import Counter

MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 6

MIN_SOLUTION_SET_SIZE = 10
GET_SIX_LETTER_WORD_TIMEOUT = 5

def get_six_letter_word(filename="wordlists/6letterwords.txt"):
    """
    Choose a random six letter word from the specified dictionary file.
    """
    validate_file_name(filename)

    try:
        with open(filename, "r") as words:
            word_list = []
            for i, word in enumerate(words):
                word = word.strip()
                if not word.isalpha() or word.split()[0] != word:
                    raise ValueError(
                        f"Formatting error on line {i+1} of '{filename}'.")
                word_list.append(word)
    except ValueError as error:
        print(error, "Exiting.")
        sys.exit()
    
    base_word = word_list[random.randint(0, len(word_list)-1)]
    words_from_base_word = get_words_from_base_word(base_word)

    while (len(words_from_base_word) < MIN_SOLUTION_SET_SIZE):
        base_word = word_list[random.randint(0, len(word_list)-1)]
        words_from_base_word = get_words_from_base_word(base_word)

    return base_word

def get_words_from_base_word(base_word, filename="wordlists/allwords.txt"):
    """
    Get a list of all words that can be made from the letters in the
    first argument 'base_word'. Select words from an optional dictionary
    file, or the defaul, "allwords.txt."
    """
    validate_file_name(filename)

    try:
        with open(filename, "r") as allwords:
            results = []
            for i, word in enumerate(allwords):
                word = word.strip()
                if not word.isalpha() or word.split()[0] != word:
                    raise ValueError(
                        f"Formatting error on line {i+1} of '{filename}'.")
                if base_word_contains_test_word(base_word, word):
                    results.append(word)
    except ValueError as error:
        print(error, "Exiting.")
        sys.exit()

    return results


def base_word_contains_test_word(base_word, test_word):
    """
    Check if 'base_word' contains all of the letters to make 'test_word.'
    """
    base_word = Counter(base_word)
    test_word = Counter(test_word)

    # if 'test_word' has letters that are not in 'base_word',
    # the following subtraction will result in negative values in
    # the 'base_word' counter
    base_word.subtract(test_word)
    if min(base_word.values()) >= 0:
        return True
    else:
        return False

def validate_file_name(filename):
    if not is_valid_file_name(filename):
        import os
        print(f"'{os.path.abspath(filename)}' is not a valid file. Exiting.")
        sys.exit()

def is_valid_file_name(filename):
    """
    Check for valid file before opening.
    """
    if type(filename) != str:
        return False

    try:
        with open(filename, "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        print(f"Word file '{filename}' not found.")
        return False
    except UnicodeError:
        print(f"Word file '{filename}' is not a valid UTF-8 file.")
        return False
    else:
        return True


# for testing purposes
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(get_six_letter_word())
    elif len(sys.argv) == 2:
        print(get_words_from_base_word(sys.argv[1]))
