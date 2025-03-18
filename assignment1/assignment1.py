# Write your code here.
#Task 1
def hello():
    return 'Hello!'
hello()

#Task 2
def greet(name):
    return f"Hello, {name}!"

print(greet("Marina"))

#Task 3
def calc (a, b, default="multiply"):
    result = None
    try:
        match default:
            case "multiply":
                result = a * b
            case "add":
                result = a + b
            case "subtract":
                result = a - b
            case "modulo":
                result = a % b
            case "power":
                result = a ** b
            case "int_divide":
                result = a // b
            case  "divide":
                result = a / b
            case _:
                return "Invalid operation!"
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"
    
    return result

#Task 4 Data type conversion
def data_type_conversion (value, name):
    try:
        match name:
            case "int":
                return int(value)
            case "float":
                return float(value)
            case "str":
                return str(value)
            case _:
                return "Invalid data type!"
    except ValueError:
        return fr"You can't convert {value} into a {name}."
    
    #Task 5 using *args
def grade(*args):
    try:
        if not all(isinstance (arg, (int, float)) for arg in args):
            return "Invalid data was provided."
        avg = sum(args) / len(args)
        if avg >= 90:
            return "A"
        elif avg >= 80 and avg <= 89:
            return "B"
        elif avg >=70 and avg <= 79:
            return "C"
        elif avg >= 60 and avg <=69:
            return "D"
        elif avg < 60:
            return "F"
    except ZeroDivisionError:
        return "No grades provided!"

#Task 6 For loop with a range

def repeat (str, count):
    result = ""
    for i in range (count):
        result += str
    return result

#Task 7  *kwargs
def student_scores(par, **kwargs):
    if par == "best":
        if kwargs:
            best_student = max(kwargs, key=kwargs.get)
            return best_student
        else:
            return "No scores provided!" 
    elif par == "mean":
        if kwargs:
            mean_score = sum(kwargs.values()) / len(kwargs)
            return mean_score
    else:
        return "Invalid option provided!"  

#Task 8 string and list operations
def titleize (text):
    little_words = ["a", "on", "an", "the", "of", "and", "in"]
    word = text.split()
    for i, w in enumerate(word):
          if i == 0 or i == len(word) -1:
             word[i]= word[i].capitalize()
          elif word[i].lower() not in little_words:
              word[i]= word[i].capitalize()
    return " ".join(word)

#Task 9 Hangman with > string operations

def hangman(secret, guess):
    result = ""
    for i in secret:
        if i in guess:
            result += i
        else:
            result += "_"
    return result

#task 10 Pig Latin, string manipulation

def pig_latin(text):
    vowels = ["a", "e", "i", "o", "u"]
    split_text = text.split()
    result = []
    for word in split_text:
        if word[0] in vowels:
            result.append(word + "ay")
        elif "qu" in word:
            index = word.index("qu")
            result.append(word[index + 2:] + word[:index +2] + "ay")
        else:
            consonants = ""
            for letter in word:
                if letter in vowels:
                    break
                consonants += letter
            result.append(word[len(consonants):] + consonants +"ay")
    return " ".join(result)





