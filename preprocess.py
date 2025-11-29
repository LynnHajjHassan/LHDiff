# preprocessing/normalize.py
# Python program which takes a whole file and outputs a list of normalized lines
# strip, collapse spaces, maybe lowercase, maybe remove comments
# Additionally, there is an option to put everything in lowercase


def normalize_line(line: str, lowercase: bool) -> str:
    """ Method to normalize a line of text.
        Works by first tokenizing all of the characters in a loop, lowercasing non string stuff if asked, and putting
        them into the list Tokens(new line is not included, not sure if that is desireable or not)
        It sends back an empty string if there are no tokens
        otherwise it loops through the tokens list and makes space between each

        A pretty apparent weakness is the lack of communication between lines, especially if there is a comment spanning
        multiple lines.
    """
    if line == "":
        return ""
    tokens = [] # makes a list of tokens that will separated with space
    token = "" # an element of tokens
    new_line = "" #the output of this method
    prev_quotation= '' # makes sure that the same initial quotation is being used
    prev_char = "" # Used to see what the previous character in the string was
    string_mode = False # This mode is for reading strings
    operators = {"+", "-", "*", "/", "%", "!", ">", "<", ":", ";", "(", ")", "[", ']', '{', '}'} # list of characters we want as individual tokens
    for char in line: #go through each character of line
        if char == '\n': #like I said, new line character is excluded
            if token != '':
                tokens.append(token)
            break
        if string_mode: #string mode, the loop will stay here until the same quotation marks appear
            token += char
            if char == prev_quotation:
                string_mode = False
                tokens.append(token)
                token = ''
        else: #the normal loop
            if char == "\"" or char == "'":  # Checks if a quotation mark forms to turn into string mode
                if token != "":
                    tokens.append(token)
                    token = ""
                string_mode = True
                prev_quotation = char
                token += char
            elif char == " ": # checks for a space character, ignores it, only really using it to isolate tokens
                if token != "":
                    tokens.append(token)
                    token = ''
            elif char == "#" or (char == "/" and prev_char == "/"): #checks if it is a comment, if so, exits the loop
                break
            elif  char in operators: #checks if it is an operator, if so tokenize it individually
                if token != '':
                    tokens.append(token)
                token = ''
                tokens.append(char)
            else: # basic case, will lowercase it if the lowercase option is turned on
                if lowercase and char.isupper():  # converts uppercase into lowercase
                    char = char.lower()
                token += char
        prev_char = char
    if tokens == []: #checks for empty list and returns an empty string if so
        return ""
    for index, token in enumerate(tokens): # Combine each string and seperate them with space character
        if index == 0:
            new_line += token
            continue
        if token == "":
            continue
        new_line += ' ' + token
    return new_line

def normalize_file(path: str, lowercase: bool) -> list[str]: #reads from a file and makes a list of lines in the file
    normalize_list = [] #output of method
    with open(path) as f: #opens file
        lines = f.readlines() #makes the lines list
    for l in lines: #basic loop that gives each line to normalize_line() and combines them into a list of non empty strings
        temp = normalize_line(l, lowercase)
        if temp != "":
            normalize_list.append(temp)
    return normalize_list