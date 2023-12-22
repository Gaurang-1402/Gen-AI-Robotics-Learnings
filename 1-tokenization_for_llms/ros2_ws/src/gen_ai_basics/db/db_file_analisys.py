#!/usr/bin/env python3

# We open the Db file, and read it, saving it into var `text`
with open('db_tinyshakespeare.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Print how many characters are in this text file
print("length of dataset in characters: ", len(text))
# Print the first 1000 characters stored in the variable `text`
print(text[:1000])

# We extract from the text , all the different characters that are used
# And we sort them
chars = sorted(list(set(text)))
vocab_size = len(chars)
print(''.join(chars))
print(vocab_size)


#################### NEW ########################
# create a mapping from characters to integers
string_to_integer = { ch:i for i,ch in enumerate(chars) }
integer_to_string = { i:ch for i,ch in enumerate(chars) }
encode = lambda s: [string_to_integer[c] for c in s] # encoder: take a string, output a list of integers
decode = lambda l: ''.join([integer_to_string[i] for i in l]) # decoder: take a list of integers, output a string

print("stoi=>"+str(string_to_integer))
print("itos=>"+str(integer_to_string))

print(encode("hii there"))
print(decode(encode("hii there")))
#################### NEW ########################