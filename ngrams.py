import os
import json
import requests
import sys
from bs4 import BeautifulSoup as bs

NGRAMS_FILENAME = "ngrams.json"

REPLACEMENTS_FILE = "replacements.json"
if os.path.exists(REPLACEMENTS_FILE):
    with open(REPLACEMENTS_FILE, "r") as fh:
        REPLACEMENTS = json.load(fh)
else:
    REPLACEMENTS = {}

BRACKET_CHAR = "Ⱙ"  # Glagolitic Capital Letter Iotated Big Yus, because it had to be something


def unicode_lookup(symbol):
    url = 'http://graphemica.com/' + symbol
    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    document = req.text
    soup = bs(document, 'html5lib')
    return soup.title.text


def ascii_replace(s):
    out = ""
    for ch in s:
        if ord(ch) > 127:
            if ch not in REPLACEMENTS:
                print(f"Warning: not ASCII: {ch}")
                print(unicode_lookup(ch))
                replacement = input("Replacement (enter // to not replace): ")
                if replacement == "//":
                    replacement = ch
                REPLACEMENTS[ch] = replacement

            out += REPLACEMENTS[ch]
        else:
            out += ch

    with open(REPLACEMENTS_FILE, "w") as fh:
        json.dump(REPLACEMENTS, fh, indent=2, sort_keys=True)

    return out


def get_ngrams(dirname, max_n=8):
    ngrams = {}
    for filename in os.listdir(dirname):
        with open(os.path.join(dirname, filename), "r") as fh:
            content = fh.read()

        bracketed = BRACKET_CHAR + ascii_replace(content) + BRACKET_CHAR

        for n in range(1, max_n+1):
            if n not in ngrams:
                ngrams[n] = {}

            for i in range(len(bracketed) - n + 1):
                ngram = bracketed[i:i+n]
                ngrams[n][ngram] = ngrams[n].get(ngram, 0) + 1

    return ngrams


def record_ngrams(dirname, max_n=10):
    ngrams = get_ngrams(dirname, max_n)
    with open(NGRAMS_FILENAME, "w") as fh:
        json.dump(ngrams, fh, indent=2, sort_keys=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Please specify a directory of training data")
    record_ngrams(sys.argv[1])
