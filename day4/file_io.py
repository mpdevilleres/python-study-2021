import random


def random_word():
    words = ['Good', 'Bad', 'Morning', 'Afternoon', 'Yesterday', 'Tomorrow']
    return random.choice(words)


with open('tmp.txt', 'a') as f:

    word = random_word()
    f.write(f'{word}\n')

    word = random_word()
    f.write(f'{word}\n')

    word = random_word()
    f.write(f'{word}\n')


with open('tmp.txt', 'r') as f:
    words = f.readlines()
    print(words)
