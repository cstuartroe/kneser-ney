import random
import json
from ngrams import BRACKET_CHAR, NGRAMS_FILENAME


class NgramManager:
    def __init__(self, filename):
        with open(filename, "r") as fh:
            ngrams_string_keys = json.load(fh)

        self.ngrams = {}
        for n_str, grams in ngrams_string_keys.items():
            self.ngrams[int(n_str)] = grams

        self.unique_grams = {}
        for n, grams in self.ngrams.items():
            self.unique_grams[n] = len(grams)

        self.unique_continuations = {}
        for n, grams in self.ngrams.items():
            if n != 1:
                for gram in grams.keys():
                    context = gram[:-1]
                    self.unique_continuations[context] = self.unique_continuations.get(context, 0) + 1

        self.corpus_length = sum(count for ch, count in self.ngrams[1].items())

        self.included_chs = list(self.ngrams[1].keys())
        self.included_chs.sort()

        self.charsetd = {}
        for i, ch in enumerate(self.included_chs):
            self.charsetd[ch] = i


class KNLanguageModel:
    def __init__(self, gram_size, filename=NGRAMS_FILENAME, discount=.75):
        self.gram_size = gram_size
        self.ngram_manager = NgramManager(filename)
        self.unique_continuations = {}
        self.discount = discount
        self.context = ""

    def put_char(self, ch):
        self.context += ch
        if len(self.context) > self.gram_size - 1:
            self.context = self.context[-self.gram_size + 1:]

    def generate(self):
        out = ''
        self.put_char(BRACKET_CHAR)

        while True:
            ch = self.generate_character()
            if ch == BRACKET_CHAR:
                break
            self.put_char(ch)
            out += ch

        return out

    def generate_character(self):
        probs = self.get_probs()
        roll = random.random()
        cum_prob = 0
        j = -1
        while cum_prob < roll:
            j += 1
            cum_prob += probs[j]
        return self.ngram_manager.included_chs[j]

    def get_prob(self, ch):
        probs = self.get_probs()
        return probs[self.ngram_manager.charsetd[ch]]

    def get_probs(self):
        probs = self.model()
        s = sum(probs)
        probs = [prob / s for prob in probs]
        return probs

    def model(self):
        grams = [self.context + ch for ch in self.ngram_manager.included_chs]
        probs = [self.prob(gram) for gram in grams]
        return probs

    # Kneser-Ney smoothed ngram probability
    def prob(self, gram):
        n = len(gram)
        if n == 1:
            return self.ngram_manager.ngrams[1].get(gram, 0) / self.ngram_manager.corpus_length

        else:
            context = gram[:-1]
            if context in self.ngram_manager.ngrams[n-1]:
                pkn = (max(self.ngram_manager.ngrams[n].get(gram, 0) - self.discount, 0) /
                       self.ngram_manager.ngrams[n-1][context])
                lambdaw = (self.discount * self.ngram_manager.unique_continuations[context] /
                           self.ngram_manager.ngrams[n-1][context])
            else:
                pkn = 0
                lambdaw = 1

            return pkn + (lambdaw * self.prob(gram[1:]))


if __name__ == "__main__":
    print(KNLanguageModel(10).generate())
