#!/usr/bin/env python3

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
                # We replace this pai by a Japanese character
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
        # We replace the japanse characters in vocabulary by he corresponding groups of characters
        unfodled_vocab_list = []
        for vocab in self.vocabulary:
            unfodled_vocab_list.append(self.unfold_vocab(vocab))
        
        print(unfodled_vocab_list)
    
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



def main(args=None):

    init_vocab_text = "Suckin’ at something is the first step to being sorta good at something."
    max_vocab_size = 30
    bpe = BPE_Tokeniser(init_vocab_text, max_vocab_size)
    bpe.loop()
    bpe.unfold()

if __name__ == '__main__':
    main()