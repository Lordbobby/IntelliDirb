from dirb.wordlist.wordlist_file import WordlistFile

class ExtendedWordlist(WordlistFile):

    def __init__(self, file_path):
        super().__init__(file_path)

        self.supplemental = []
        self.supplemental_index = 0

    def add_words(self, words, tag):
        for word in words:
            if word not in self.supplemental:
                self.supplemental.append((word, tag))

    def reset_index(self):
        super().reset_index()
        self.supplemental_index = 0

    def get_words(self, num):
        # no supplemental words, pull from file
        if self.supplemental_index == len(self.supplemental):
            return super().get_words(num)

        # not enough supplemental words to satisfy the request, pull some from file
        if len(self.supplemental) - self.supplemental_index < num:
            words = self.supplemental[self.supplemental_index:]
            words = words + self.get_words(num - len(words))

            return words

        words = self.supplemental[self.supplemental_index:self.supplemental_index + num]
        self.supplemental_index += num

        return words