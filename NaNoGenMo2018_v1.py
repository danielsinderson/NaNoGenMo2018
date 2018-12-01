import spacy
import random


def process_hivemind_chapter(n, model):
    #load statistical model
    nlp = spacy.load(model)
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
    chpt = process_hivemind_chapter(chapter_number, spacy_model)
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
            for token in sentences[x]: #iterate through tokens in chosen sentence
                for k, v in pos_dictionary.items(): #per token, iterate through key:value pairs in dictionary to match POS tag type
                    pos_choices = []
                    if k == token.tag_: #once the lexical address for the POS tag type is found...
                        pos_choices = pos_lexicon[v] #...randomly choose a word from the lexicon...
                        choice = random.randint(0, len(pos_choices)-1)
                        #print(pos_choices[choice])
                        s.append(pos_choices[choice]) #...to add to the sentence being generated
            chapter.append(' '.join(s)) #add the generated sentence to the chapter
    output = ' '.join(chapter).replace(' ?', '?').replace(' .', '.').replace(' ,', ',')
    return output #return chapter as a single string joined by spaces
    






'''
code section
'''
model = 'en'
novel = "                                       REACHING\nA Novel for NaNoGenMo2018\nVersion1\n\n\n\n\n"
count = 1
chapters = [1, 2, 4, 5, 7]
for chapter in chapters:
    heading = "CHAPTER " + str(count) + '\n\n'
    novel += heading
    chpt = generate_hivemind_chapter(575, chapter, model) + '\n\n\n\n'
    novel += chpt
    count += 1
    print(str(count - 1) + ' down and ' + str(11 - count) + ' to go!')
chapters.reverse()
for chapter in chapters:
    heading = "CHAPTER " + str(count) + '\n\n'
    novel += heading
    chpt = generate_hivemind_chapter(575, chapter, model) + '\n\n\n\n'
    novel += chpt
    count += 1
    print(str(count - 1) + ' down and ' + str(11 - count) + ' to go!')
file = open("Reaching_v1.txt", 'w')
file.write(novel)
file.close()

    
