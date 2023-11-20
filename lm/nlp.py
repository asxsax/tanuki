import nltk
from nltk.corpus import treebank

sentence = "heres a random sentence for example"
tokens = nltk.word_tokenize(sentence)

print(tokens)

tagged = nltk.pos_tag(tokens)
print(tagged)

entities = nltk.chunk.ne_chunk(tagged)
print(entities)