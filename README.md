# The Kneser-Ney language generator

This is a tiny bit of code that uses a Kneser-Ney smoothed character ngram language model to generate text. 
It must be trained on a corpus first, the format of which should be a directory that contains only the plaintext files you wish to train on.
If you're not sure what to use, you can try what I did! Clone my [repo of classic rock lyrics](https://github.com/cstuartroe/classic-rock) in an adjacent repo.

It's currently hardcoded to use 10-grams. You can modify that number in the code if you want.

## How to use this repo

First, install all requirements:

```
pip install -r requirements.txt
```

Then, record ngram counts:

```
python ngrams.py ../classic-rock/lyrics
```

It will generate a json file with ngram counts. Depending on the size of your corpus, this file may be quite massive. The classic rock corpus contains lyrics for
about 1500 songs, and for me the generated json file is 62MB.

It may also prompt you for substitutions for non-ASCII characters it encounters, if it doesn't already know a substitution for them (stored in `replacements.json`).
You're free to say that a character shouldn't be substituted by entering `//`, or enter any other substitution of your choosing, including the empty string.
The only reason to replace non-ASCII characters is that the algorithm will work a little better with a smaller character set to pick from.
I've included my choices for some substitutions in this repo, but if you're
not sure you trust my judgement or you just want to see the dialogue yourself you can simply delete `replacements.json` and it will generate afresh.

Lastly, generate a new document!

```
python language_model.py
```

It will simply print to stdout, provided nothing goes horribly wrong.

Here's an example of a song it generated for me:

```
[Intro]

You know I've got to go to heaven above you
And it was the one

[Chorus]
Have yourselves)
Home (We salute you
For those who are you? (Who are you? Who, who, who?)
Oh, can't you feel like you did it right

[Instrumental intro]
Fading like a child anymore
Well, say that I'm not the ones that you've been
You gotta stop

[Chorus]
You're out of the way, the way back home

[Verse 4]
On the way
There for the starting to work the same
All the business, don't ask for more

[Chorus]

Hey, look over yonder, where the big time
Waterloo sunset's fine
```

Not great, not terrible. Unlike recurrent neural networks, which have a memory of previous tokens that fades gradually, and which can potentially keep
track of long-term dependencies in text, an ngram-based algorithm like this one has a hard cutoff (by default for this repo, 10 characters) after which
it has no memory of what came before. This means that it has trouble keeping track of things like sentence structure and parenthesis matching, so it's
hard to confuse its output for genuine natural language.
