import nltk
nltk.download('punkt')
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det N | N PP | AP NP | Det AP N | NP P NP
AP -> Adj | Adj AP
PP -> P NP
VP -> V | V NP | V PP | Adv VP | VP Adv | VP Conj VP
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
    print(s)

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
    s = sentence.lower()

    tokens = nltk.tokenize.word_tokenize(s)
    
    words = []

    for token in tokens:
        alphabetical = 0
        for char in token:
            if char.isalpha():
                alphabetical += 1

        if alphabetical > 0:
            words.append(token)

    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []

    print(tree)
    print("----------")
    for subtree in tree:
        # import pdb; pdb.set_trace()
        print(subtree)
        print(type(subtree)==nltk.tree.Tree)
        print(subtree.label())
        for np in find_nps(subtree):
            np_chunks.append(np)
        print(np_chunks)
    return np_chunks

def find_nps(subtree):

    if type(subtree) != nltk.tree.Tree:
        # too deep
        return

    nps = []
    # if NP, return or check further
    if subtree.label() == "NP":
        nps.append(subtree)

    for branch in subtree:
        try:
            for np in find_nps(branch):
                nps.append(np) 
        except TypeError:
            # No nps found in branch
            continue

    return nps

if __name__ == "__main__":
    main()
