#!/usr/bin/env python3

text = "Suckか’ atきomethかg is the firstきtep to beかgきorta good atきomethかg."

# Print how many characters are in this text file
print("length of dataset in characters: ", len(text))
# Print the first 1000 characters stored in the variable `text`
print(text)

# We extract from the text, all the different characters that are used
# And we sort them
chars = sorted(list(set(text)))
chars.append('in')
chars.append('s')
vocab_size = len(chars)
print(chars)
print(''.join(chars))
print(vocab_size)


def extract_substrings(text, length=2):
    substrings = [text[i:i+length] for i in range(len(text)-length + 1)]
    return substrings


def count_occurrences(substrings):
    occurrences = {}
    for substring in substrings:
        if substring in occurrences:
            occurrences[substring] += 1
        else:
            occurrences[substring] = 1
    return occurrences

substrings = extract_substrings(text, length=2)
print(substrings)
occurence_count = count_occurrences(substrings)

print("Occurrences of substrings of two characters:")
sorted_items = sorted(occurence_count.items(), key=lambda x: x[1], reverse=True)
print(sorted_items)

