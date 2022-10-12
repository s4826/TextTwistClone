import random
import sys

from collections import Counter

MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 6

def get_six_letter_word(filename="wordlists/6letterwords.txt"):
    """
    Choose a random six letter word from the specified dictionary file.
    """
    with open(filename, "r") as words:
        word_list = []
        for word in words:
            word_list.append(word.strip())
    
    base_word = word_list[random.randint(0, len(word_list)-1)]
    words_from_base_word = get_words_from_base_word(base_word)
    while (len(words_from_base_word) < 12):
        base_word = word_list[random.randint(0, len(word_list)-1)]
        words_from_base_word = get_words_from_base_word(base_word)

    return base_word

def get_words_from_base_word(base_word, filename="wordlists/allwords.txt"):
    """
    Get a list of all words that can be made from the letters in the
    first argument 'base_word'. Select words from an optional dictionary
    file, or the defaul, "allwords.txt."
    """
    with open(filename, "r") as allwords:
        results = []
        for word in allwords:
            word = word.strip()
            if base_word_contains_test_word(base_word, word):
                results.append(word)
    return results


def base_word_contains_test_word(base_word, test_word):
    """
    Check if 'base_word' contains all of the letters to make 'test_word.'
    """
    base_word = Counter(base_word)
    test_word = Counter(test_word)
    base_word.subtract(test_word)
    if min(base_word.values()) >= 0:
        return True
    else:
        return False


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(get_six_letter_word())
    elif len(sys.argv) == 2:
        print(get_words_from_base_word(sys.argv[1]))
