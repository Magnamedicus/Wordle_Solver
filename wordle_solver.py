
# Import necessary libraries
# `nltk` is used for accessing a large corpus of English words.
# `wordfreq` is used to rank words based on their frequency in the English language.

import nltk
from nltk.corpus import words
from wordfreq import word_frequency
nltk.download('words')

# Download the NLTK 'words' dataset, which provides a list of English words.
# Ensure you have `nltk` and `wordfreq` installed. You can install them using:
# pip install nltk wordfreq

# A 'word_list' is created, filtering the nltk corpus for only those words containing 5 characters
word_list = [word.lower() for word in words.words() if len(word) == 5]

def filter_words(greens, yellows, positions):
    """
       Filters the word list based on green and yellow letter inputs.
       Parameters:
       - greens: List of green letters (correct letters in the correct position).
       - yellows: List of yellow letters (correct letters in the wrong position).
       - positions: List of positions corresponding to the green letters.

       Returns:
       A list of words matching the green and yellow letter criteria.
       """
    words_containing_yellow = []
    green_position = {}

    # Create a dictionary to map green letters to their positions.
    for i in range(len(greens)):
        green_position[greens[i]] = positions[i]

    # Function to check if all characters in char_list are present in the word.
    def all_characters_in_word(char_list, word):
        return all(char in word for char in char_list)

    # Filter words containing yellow letters but ensuring they are not in green positions.
    for word in word_list:
        if all_characters_in_word(yellows, word):

            if all(word[green_position[char]] != char for char in yellows if char in green_position):
                words_containing_yellow.append(word)

    green_filtered_words = []
    for word in words_containing_yellow:
        if all(word[pos] == char for char, pos in green_position.items()):
            green_filtered_words.append(word)

    return green_filtered_words

def rank_words(words):
    """
        Ranks words based on their frequency in the English language using the `wordfreq` library.
        Parameters:
        - words: List of filtered words to rank.

        Returns:
        A list of words sorted by frequency (most frequent first).
        """

    return sorted(words, key=lambda word: word_frequency(word, 'en'), reverse=True)




def main():
    print("Welcome to Wordle Solver!")
    print("Enter all yellow, green and gray letters from your most recent guesses")
    print("We will then suggest the most likely solutions to your Wordle\n")


    on_yellows = True
    on_greens = False
    on_grays = False

    yellow_letters = []
    gray_letters = {}
    green_letters = []
    green_positions = []
    rankings = {}


    while on_yellows and not on_greens and not on_grays:
        yellow_input = input("Enter a yellow letter or enter '0' to move on: ")
        if yellow_input == '0':
            on_yellows = False
            on_grays = False
            on_greens = True
            break
        elif yellow_input.isdigit() or len(yellow_input) > 1:
            print("\nYou must enter a single letter as input\n")
            continue
        else:
            yellow_letters.append(yellow_input)

    while on_greens and not on_yellows and not on_grays:
        green_input = input("Enter a green letter or enter '0' to move on: ")
        if green_input == '0':
            on_greens = False
            on_yellows = False
            on_grays = True

            break

        elif green_input.isdigit() or len(green_input) > 1:
            print("\nYou must enter a single letter as input\n")
            continue

        else:

            green_letters.append(green_input)
            while True:
                position_input = input("What is the position of the green letter you just entered? ")
                if position_input.isalpha() or int(position_input) > 5:
                    print("You must enter an integer between 1 and 5")
                    continue
                else:
                    position_input = int(position_input)
                    if position_input > 0:
                        position_input = position_input - 1
                green_positions.append(position_input)
                break


    while on_grays:
        gray_input = input("Enter a gray letter or enter '0' to generate a word list: ")
        if gray_input == '0':
            on_grays = False
            break
        elif gray_input.isdigit() or len(gray_input) > 1:
            print("\nYou must enter a single letter as input\n")
            continue
        else:
            gray_letters[gray_input] = True

    all_words = filter_words(green_letters, yellow_letters, green_positions)
    filtered_words = [word for word in all_words if not any(char in word for char in gray_letters)]
    ranked_words = rank_words(filtered_words)
    ranked_words = list(dict.fromkeys(ranked_words))

    for index,value in enumerate(ranked_words):
        if index == 0:
            rankings[value] = "Most Likely"
        elif index == len(ranked_words) - 1:
            rankings[value] = "Least Likely"
        else:
            rankings[value] = index + 1
    if rankings:
        print("\n\nPossible word choices (Most to least likely)\n")

        for key,value in rankings.items():
            print(f"Possible Word: {key}, Likelihood: {value}")
    else:
        print("\nThere are no words that match your inputs :(")




main()




