# create an application
# to generate a random word ['apple','banana', 'python', 'hangman']
# present the word with * (where the number of * is the number of the letters in the word)
# ask the user to input a letter at a time, and show if it exist in the random word
# give 5 chances to the user to guess the letters
# the game ends if the user gives all correct letters, or if the user exhaust the 5 chances

import random


words = ['apple', 'banana', 'python', 'hangman']

# generate a word from the list ['apple','banana', 'python', 'hangman']
word = random.choice(words)

letter_list = list(word)


# print the masked word
for letter in letter_list:
    print('*', end='')
print()

max_wrong_guess = 5
threshold = 0

guesses = []
done = False

while threshold != max_wrong_guess and not done:
    # ask for input letter
    guess = input(f"Please enter your guess [{threshold}/{max_wrong_guess}]: ")
    guesses.append(guess)

    if guess not in letter_list:
        threshold += 1

    for letter in set(letter_list):
        if letter not in guesses:
            done = False
            break

        done = True
