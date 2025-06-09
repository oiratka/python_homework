#TASK 4

def make_hangman(secret_word):
    guesses = []
    def hangman_closure(letter):
        guesses.append(letter)
        guessed = ''
        for char in secret_word:
            if char in guesses:
                guessed += char
            else:
                guessed +='_'
        print(guessed)

        if all(char in guesses for char in secret_word):
           return True
        else:
           return False
    return hangman_closure

secret_word = input("Enter the secret word: ".lower())
game = make_hangman(secret_word)

while True:
    letter = input("Guess a letter: ".lower())
    if game(letter):
        print("You guessed the word!")
        break
