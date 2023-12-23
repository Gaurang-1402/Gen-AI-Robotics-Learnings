#!/usr/bin/env python3

import copy
import math 

class BPE_Tokeniser(object):

    def __init__(self, init_vocab_text, max_vocab_size, max_iterations=100 , min_pair_repeat=2):
        self.iterations = 0
        self._max_iterations = max_iterations
        self._min_pair_repeat = min_pair_repeat
        self.text = init_vocab_text
        self._max_vocab_size = max_vocab_size

        # We generate our list of replacement characters
        self.hiragana_characters = [
                            'あ', 'い', 'う', 'え', 'お',
                            'か', 'き', 'く', 'け', 'こ',
                            'さ', 'し', 'す', 'せ', 'そ',
                            'た', 'ち', 'つ', 'て', 'と',
                            'な', 'に', 'ぬ', 'ね', 'の',
                            'は', 'ひ', 'ふ', 'へ', 'ほ',
                            'ま', 'み', 'む', 'め', 'も',
                            'や', 'ゆ', 'よ',
                            'ら', 'り', 'る', 'れ', 'ろ',
                            'わ', 'を', 'ん',
                            'が', 'ぎ', 'ぐ', 'げ', 'ご',
                            'ざ', 'じ', 'ず', 'ぜ', 'ぞ',
                            'だ', 'ぢ', 'づ', 'で', 'ど',
                            'ば', 'び', 'ぶ', 'べ', 'ぼ',
                            'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ',
                            'ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ',
                            'っ',
                            'ゃ', 'ゅ', 'ょ',
                            'ー'
                        ]



        self.generate_base_vocab()

    def generate_base_vocab(self):
        print("######### GENERATE VICAB ################")
        # Print how many characters are in this text file
        print("length of dataset in characters: ", len(self.text))
        # Print the first 1000 characters stored in the variable `text`
        print(self.text)
        self.original_text = copy.deepcopy(self.text)

        # We extract from the text , all the different characters that are used
        # And we sort them
        self.vocabulary = sorted(list(set(self.text)))
        self.vocab_size = len(self.vocabulary)
        print(self.vocabulary)
        print(self.vocab_size)

        self.correspondance = {}
        print("######### ######## ####### ################")


    def extract_substrings(self, text, length=2):
        substrings = [text[i:i+length] for i in range(len(text) - length + 1)]
        return substrings

    def count_occurrences(self, substrings):
        occurrence_count = {}
        for substring in substrings:
            if substring in occurrence_count:
                occurrence_count[substring] += 1
            else:
                occurrence_count[substring] = 1
        return occurrence_count

    def loop(self):

        while self.vocab_size < self._max_vocab_size and self.iterations < self._max_iterations and len(self.hiragana_characters) > 0:
            substrings = self.extract_substrings(self.text)
            occurrence_count = self.count_occurrences(substrings)

            
            sorted_items = sorted(occurrence_count.items(), key=lambda item: item[1], reverse=True)
            
            most_common_pair = sorted_items[0]
            most_common_pair_value = most_common_pair[0]
            most_common_pair_num = most_common_pair[1]
            if most_common_pair_num < self._min_pair_repeat:
                print("Ending because Pairs are not repeating ="+str(self._min_pair_repeat))
                break
            else:
                # We replace this pair by a Japanese character
                japanese_char = self.hiragana_characters.pop(0)
                self.correspondance.update({most_common_pair_value: japanese_char}) 
                # We add the new pair to the vocabulary
                self.vocabulary.append(japanese_char)
                # We replace the pair by the japanese character in the text
                new_string = self.text.replace(most_common_pair_value, japanese_char)
                self.text = new_string

            

            self.iterations += 1

        print(self.text)
        print(len(self.text))
        print(self.vocabulary)
        print(len(self.vocabulary))
        print(self.correspondance)

    def unfold(self):
        # We replace the japanse characters in vocabulary by the corresponding groups of characters
        self.unfodled_vocab_list = []
        for vocab in self.vocabulary:
            self.unfodled_vocab_list.append(self.unfold_vocab(vocab))
        
        print(self.unfodled_vocab_list)
    
    def unfold_vocab(self,vocab):
        character_string = ""
        for e in vocab:
            if e in self.correspondance.values():
                key = self.get_key_by_value(self.correspondance, e)
                character_string += self.unfold_vocab(key)
            else:
                character_string += e
            
        return character_string

    def get_key_by_value(self,dictionary, search_value):
        for key, value in dictionary.items():
            if value == search_value:
                return key
        return None  # Value not found in the dictionary
    
    def round_up_to_one_decimal(self,float_number):
        rounded_number = math.ceil(float_number * 10) / 10
        return rounded_number

    def optimise(self):
        print(self.original_text)
        # Example vocabulary list
        vocabulary = self.unfodled_vocab_list
        corpus = self.original_text
        
        opt_vocabulary = self.optimize_vocabulary(vocabulary, corpus)

        print("Optimal Vocab="+str(opt_vocabulary))
        improvement = 100* (len(vocabulary) - len(opt_vocabulary)) / len(vocabulary)
        round = self.round_up_to_one_decimal(improvement)
        print("Reduced vocab list in ="+str(round)+"%")

    def optimize_vocabulary(self,vocabulary, corpus):
        # Example string
        text = corpus
        optimal_vocab = []
        mergeable_vocabs = []
        # We check each substring of the vocab in order
        for vocab1 in vocabulary:
            vocab1_unmergeable = False
            for vocab2 in vocabulary:
                if vocab1 != vocab2:
                    occurrences_not_contained = self.find_occurrences_not_contained(text, vocab1, vocab2)
                    #print("Occurrences of '{}' not contained inside '{}' occurrences:".format(vocab1, vocab2))
                    if len(occurrences_not_contained) == 0:
                        #print("The substring ="+str(vocab1+", has to be removed"))
                        if vocab1 not in mergeable_vocabs:
                            mergeable_vocabs.append(vocab1)                   
                    else:
                        for occurrence_range in occurrences_not_contained:
                            #print("At positions:", occurrence_range)
                            pass
                        
                else:
                    # We don't evaluate the same vocab otherwise it would cancel itsel all the time
                    pass
            
        # We remove form the vocab the elements in the mergeable_vocabs list
        print(mergeable_vocabs)
        optimal_vocab = list(set(vocabulary) - set(mergeable_vocabs))
        
    
        return optimal_vocab
    
    def append_if_not_exists(self,lst, item):
        if item not in lst:
            lst.append(item)


    def find_substring_ranges(self, string, substring):
        substring_ranges = []
        start = 0
        
        while start < len(string):
            index = string.find(substring, start)
            
            if index == -1:
                break
            
            end = index + len(substring) - 1
            substring_ranges.append((index, end))
            
            start = index + 1
        
        return substring_ranges

    def is_substring_contained(self, vocab1_range, vocab2_range):
        return vocab1_range[0] >= vocab2_range[0] and vocab1_range[1] <= vocab2_range[1]

    def find_occurrences_not_contained(self,string, vocab1, vocab2):
        vocab1_ranges = self.find_substring_ranges(string, vocab1)
        vocab2_ranges = self.find_substring_ranges(string, vocab2)
        
        occurrences_not_contained = []

        for vocab1_range in vocab1_ranges:
            is_contained = False
            
            for vocab2_range in vocab2_ranges:
                if self.is_substring_contained(vocab1_range, vocab2_range):
                    is_contained = True
                    break
            
            if not is_contained:
                occurrences_not_contained.append(vocab1_range)
        
        return occurrences_not_contained




def main(args=None):

    init_vocab_text = "Suckin’ at something is the first step to being sorta good at something."
    max_vocab_size = 30
    bpe = BPE_Tokeniser(init_vocab_text, max_vocab_size)
    bpe.loop()
    bpe.unfold()
    bpe.optimise()

if __name__ == '__main__':
    main()