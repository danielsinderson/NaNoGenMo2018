import random


def process_poetry_corpus(filename):
    file = open(filename, 'r')
    data = file.read()
    file.close()
    data = data.split('\n')
    lines = []
    for elem in data:
        x = elem.split(' ')
        lines.append(x)
    return lines


def process_wittgenstein(filename):
    file = open(filename, 'r')
    data = file.read()
    file.close()
    data = data.split('\n\n')
    theorems = []
    for elem in data:
        x = elem.replace("\n", " ").replace('.', ',', 1)
        y = x.split('.')
        for sentence in y:
            z = sentence.split(' ')[2:]
            theorems.append(z)
    return theorems


def process_opticks(filename):
    file = open(filename, 'r')
    data = file.read()
    file.close()
    data = data.split('.')
    return data

'''
def most_similar(word):
    queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
    by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
    words = by_similarity[5:10]
    words.append(word)
    return words
'''

def find_selection(words, corpus):
    selections = []
    x = random.randint(1, 10)
    for elem in corpus:
        similarity = False
        for word in words:
            if word in elem: similarity = True
        if similarity == True: selections.append(elem)
    if len(selections) != 0:
        choice = random.randint(0, len(selections)-1)
        return ' '.join(selections[choice])
    else:
        return '*buzzing*'





bones = [['world'],
         ['game'],
         ['nonexistence'],
         ['bone'],
         ['gaze'],
         ['endless'],
         ['door'],
         ['I am'],
         ['lava'],
         ['scream'],
         ['touch'],
         ['mouth'],
         ['other'],
         ['confusion'],
         ['awe']]
for bone in bones:
    c = random.randint(1, 10)
    if c < 8: print(find_selection(bone, process_poetry_corpus('Corpus/poetry.txt')), '\n')
    elif c > 7: print(find_selection(bone, process_wittgenstein('Corpus/tractatus.txt')), '\n')
    else: print(find_selection(bone, process_opticks('Corpus/opticks.txt')), '\n')
    
 






