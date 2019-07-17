import spacy
import random


def process_hivemind_chapter(n, nlp):
    #filename for chapter n
    filename = 'chpt' +str(n) + '.txt'
    #open chapter file and store contents
    file = open(filename, 'r')
    chpt = file.read().lower()
    file.close
    #print(chpt)
    #process chapter through loaded statistical model
    chpt_modelled = nlp(chpt)
    #return processed chapter
    return chpt_modelled


def split_into_sentences(chpt):
    sentences = []
    for sent in chpt.sents:
        sentences.append(sent)
    return sentences


def most_similar(word):
    queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
    by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
    return by_similarity[5:20]


def create_similar_word_dictionary(chpt):
    dictionary = {}
    words = []
    yes_pos = ['NN', 'NNS', 'JJ']
    for token in chpt:
        if token.tag_ in yes_pos:
            if token.text not in words:
                similar_words = [w.lower_ for w in most_similar(nlp.vocab[token.text])]
                words.append(token.text)
                dictionary.update({token.text:list(set(similar_words))})
    return dictionary
        


def create_lexicon(chpt):
    tag_types = []
    lexicon = []
    dictionary = {}
    count = 0
    tag_types = []
    #Iterate through chapter to create a list of pos tag types
    for word in chpt:
        if word.tag_ not in tag_types: tag_types.append(word.tag_)
    #iterate through tag types and create a dictionary mapping tag type to index in lexicon
    for t in tag_types:
        dictionary.update({t:count})
        count += 1
        words = []
        #then iterate through words to create a lexicon organized into pos tag types
        for word in chpt:
            if word.tag_ == t and word.text not in words: words.append(word.text)
        lexicon.append(words)
    return lexicon, dictionary





def generate_hivemind_chapter(chapter_length, chapter_number, spacy_model):
    nlp = spacy_model
    chpt = process_hivemind_chapter(chapter_number, nlp)
    sentences = split_into_sentences(chpt)
    words = create_lexicon(chpt)
    pos_lexicon = words[0]
    pos_dictionary = words[1]
    chapter = []
    for i in range(chapter_length): #generate n sentences
        x = random.randint(0, len(sentences)-1) #choose sentence to use
        y = random.randint(0, 11) #differentially choose whether to use the chosen sentence...
        #print(sentences[x])
        if y < 3: #...directly
            chapter.append(sentences[x].text)
        elif y >= 3: #...or as a template
            s = []
            vector_tags = ['NN', 'NNS', 'JJ']
            for token in sentences[x]: #iterate through tokens in chosen sentence
                if token.tag_ in vector_tags: #Use word vectors to replace nouns, verbs, adjectives, and adverbs with a similar one
                    similar_words = [w.lower_ for w in most_similar(nlp.vocab[token.text])] #find similar words
                    choice = random.randint(0, len(similar_words)-1)
                    #print(pos_choices[choice])
                    s.append(similar_words[choice]) #...to add to the sentence being generated
                        
                else: #for everything else pull a random item from the lexicon
                    s.append(token.text) #...to add to the sentence being generated
            chapter.append(' '.join(s)) #add the generated sentence to the chapter
    output = ' '.join(chapter).replace(' ?', '?').replace(' .', '.').replace(' ,', ',')
    return output #return chapter as a single string joined by spaces
    






'''
code section
'''
model = spacy.load('en_core_web_md')
novel = ""
count = 1
chapters = [1, 2, 4, 5, 7]
for chapter in chapters:
    heading = "CHAPTER " + str(count) + '\n'
    novel += heading
    chpt = generate_hivemind_chapter(50, chapter, model) + '\n\n'
    novel += chpt
    count += 1
    print('One Down')
chapters.reverse()
for chapter in chapters:
    heading = "CHAPTER " + str(count) + '\n'
    novel += heading
    chpt = generate_hivemind_chapter(50, chapter, model) + '\n\n'
    novel += chpt
    count += 1
    print('One Down')
file = open("Reaching_v4.txt", 'w')
file.write(novel)
file.close()


    
