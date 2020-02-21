import os.path
from os import path
import sys


# This is a function that creates a new list with the words of the original
# text without the use of symbols.
def remove_symbols(words):
    words_new = []
    notalpha = []
    new_word = ''

    # First we search each word letter by letter and check if the letter is
    # alpha. If its not, we store the letter in the notalpha list.
    for key in words:
        i = 0
        for letter in key:
            if not letter.isalpha():
                if letter not in notalpha:
                    notalpha.append(letter)
            i = i+1

        # If the word has letters that are not alpha, we "delete" them by
        # replacing them with an empty character. Then, we store the word in
        # the new_word list, which contains all the words of the text without
        # the symbols.
        if notalpha:
            j = 0

            for key_ in notalpha:
                if j == 0:
                    new_word = key.replace(key_, '')
                    j = 1
                else:
                    new_word = new_word.replace(key_, '')

            words_new.append(new_word)
            notalpha.clear()
            j = 0
        # If the word doesnt have any symbols, it is stored directly to the
        # list.
        else:
            words_new.append(key)

    return(words_new)


# This is the main function of the program. It creates the reversed words
# list, based on the choices the user made.
def reverse_words(words, words_new, option_one, option_two):
    m = 0
    k = 0
    difference = {}
    rev_words=[]

    # If the user chose not to count symbols, then we use the words_new list
    # and we find the 5 biggest words in it.
    if option_one.lower() == 'n':
        loop = 0
        for key in words_new:
            # The first 5 words are instantly added.
            if loop < 5:
                rev_words.append(key[::-1])
            else:

                max_difference = 0
                pos = 0
                second_loop = 0

                # For the rest of the words, we count the length difference
                # between the word and the previously added reversed words.
                # Then, if it exists, we swap the previous reversed word with
                # the biggest difference with the new word.
                for rev_keys in rev_words:
                    if len(key) > len(rev_keys):
                        if len(key) - len(rev_keys) > max_difference:
                            max_difference = len(key) - len(rev_keys)
                            pos = second_loop

                    second_loop += 1

                    rev_words[pos] = key[::-1]
            loop +=1

    # If the user chose to count the symbols, we have two different cases:
    # either the symbols are printed out,or not. In the first case, we use
    # only the words list, while in the later we use both.
    elif option_one.lower() == 'y' :
        loop = 0
        temp = []
        for key in words:
            # Same explanation as line 61.
            if loop < 5:
                if option_two.lower() == 'n':
                    # We capitalize on the fact that the words in both lists
                    # are on the same index.
                    rev_word = words_new[loop]
                else:
                    rev_word = words[loop]
                rev_words.append(rev_word[::-1])
                # We use a temporary list that holds account of the reversed
                # words including the symbols. We do that because the user
                # chose to count the symbols so if he choses not to print them
                # out, we have to have a way to still be able to count them
                # while they include the symbols.
                temp.append(key)
            else:

                max_difference = 0
                pos = 0
                second_loop = 0

                # Same explanation as line 70.
                for key_ in temp:
                    if len(key) > len(key_):
                        if len(key) - len(key_) > max_difference:
                            max_difference = len(key) - len(key_)
                            pos = second_loop
                        second_loop += 1

                    if option_two.lower() == 'n':
                        rev_words[pos] = words_new[loop][::-1]
                    else:
                        rev_words[pos] = key[::-1]

                    temp[pos] = key

            loop += 1

    return(rev_words)

# Intro header.
print('*******************************************************************\
******\nTHIS IS A PYTHON PROGRAM THAT TAKES A FILE, FINDS THE\
FIVE\n BIGGEST WORDS IN IT, AND PRINTS THEM OUT REVERSED AND WITHOUT\
THE VOWELS.\n********************************************************\
*****************\n')

# Here we ask for the file that the user wants to use.
file = input('Enter the name of the file you want to use: ')

# Check to see if the file exists in the current directory.
while not path.exists(file):
    answer = input('File doesnt exist in current directory. Do you want to\
    try again?(y/n): ')

    while answer.lower() not in ['y', 'n']:
        answer = input('Invalid answer. Please try again.: ')

    if answer.lower() == 'y':
        file = input('Enter the name of the file you want to use: ')
    else:
        sys.exit()

# Splitting the text document into an array of words.
with open(file, 'r') as in_:
    for line in in_:
        words = line.split()

option_symbols = input('Do you want symbols to be counted? (y/n): ')

while option_symbols not in ['y', 'n']:
    option_symbols = input('Invalid option.Please try again.: ')

if option_symbols.lower() == 'n':
    words_new = remove_symbols(words)
    rev_words = reverse_words(words, words_new, option_symbols, 'n')

elif option_symbols.lower() == 'y':
    option_wordsToPrint = input('Do you want the words to be printed out\
 with the symbols?(y/n): ')

    while option_wordsToPrint.lower() not in ['y', 'n']:
        option_wordsToPrint = input('Invalid option.Please try again.: ')

    if option_wordsToPrint == 'n':
        words_new = remove_symbols(words)
        rev_words = reverse_words(words, words_new, option_symbols,
        option_wordsToPrint)

    else:
        rev_words = reverse_words(words, [], option_symbols,
        option_wordsToPrint)

#Here we remove the vowels from the reversed words.
loop = 0
for key in rev_words:
    second_loop = 0
    lettersToDelete = []

    # We keep the existing vowels in each word in a word specific list.
    for letter in key:
        if letter in ['a', 'e', 'y', 'i', 'o', 'u', 'a']:
            lettersToDelete.append(letter)

    # Here we use the list to replace each existing vowel with an empty
    # character.
    for key_ in lettersToDelete:
        rev_words[loop] = rev_words[loop].replace(key_, '')

    loop += 1

output = 'The biggest words in the text document are: {0},{1},{2},{3} and\
 {4}.'
print(output.format(*rev_words))
sys.exit()
