import nltk
import sys
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
import re
import pdb

# great resource to manage Python versions: https://ericsysmin.com/2024/02/05/how-to-install-pyenv-on-macos/

TERMINALS = """
A -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
A -> "down" | "here" | "never"
Conj -> "and" | "until"
D -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
    S -> NP VP | N V D N

    AP -> A | A AP
    NP -> N | D NP | AP NP | N PP | N VP D NP
    PP -> P NP
    VP -> V | V NP | V NP PP
"""
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    list_of_substrings  = word_tokenize(sentence)
    processed_list = [word.lower() for word in list_of_substrings if re.search('[a-zA-Z]', word)]

    return processed_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # pdb.set_trace()
    list_of_noun_phrases = []
    for s in tree.subtrees():
        tree_label = s.label()
        if tree_label == 'NP':
            list_of_noun_phrases.append(s)

    return list_of_noun_phrases

if __name__ == "__main__":
    main()
