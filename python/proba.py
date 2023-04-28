import pymorphy2
import nltk
import re
from nltk.tokenize import WordPunctTokenizer, sent_tokenize, word_tokenize
from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    Doc
)
# from IPython.display import display

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

lst = []
text_lst = ""
move_words = []
male_names = []
female_names = []
all_names = []

with open('../files/2.txt', encoding='utf-8') as movement:
    for line in movement:
        move_words = line.split()

with open('../books/lermontov1.txt', encoding='utf-8') as text_book:
    for line in text_book:
        try:
            line_text = line.strip()
            if line_text != "":
                lst.append(line_text)
                text_lst += line_text + ' '
        except UnicodeEncodeError:
            pass

doc = Doc(text_lst)
doc.segment(segmenter)
doc.tag_morph(morph_tagger)
doc.parse_syntax(syntax_parser)
doc.tag_ner(ner_tagger)

for span in doc.spans:
    span.normalize(morph_vocab)

for token in doc.tokens:
    token.lemmatize(morph_vocab)

