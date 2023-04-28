import json
import pymorphy2
import nltk
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

with open('../files/cities.json', 'r', encoding='utf-8') as read_json:
    data_countries = json.load(read_json)

name_countries = []         # названия стран
city_counties = []          # список массивов городов по странам
for obj in data_countries:
    name_countries.append(obj['country']['name'])
    cities = []
    for obj_cit in obj['country']['cities']:
        for city in obj_cit:
            cities.append(city.lower())
    city_counties.append(cities)

for country in city_counties:
    country = list(map(lambda x: x.replace('ё','е'), country))

doc = Doc(text_lst)
doc.segment(segmenter)
doc.tag_morph(morph_tagger)
doc.parse_syntax(syntax_parser)
doc.tag_ner(ner_tagger)

for span in doc.spans:
    span.normalize(morph_vocab)

for token in doc.tokens:
    token.lemmatize(morph_vocab)

# index = 0
# sents = doc.sents
# for i in range(len(sents)):
#     if index > 170:
#         for token in sents[i].tokens:
#             for move in move_words:
#                 if token.lemma == move:
#                     if i != 0 and i != 1 and i != (len(sents) - 2) and i != (len(sents) - 1):
#                         print(sents[i - 1].text)
#                         sents[i].syntax.print()
#                         print(sents[i].syntax)
#                         print(sents[i + 1].text)
#                         print("--------------")
#         print(i)
#     index += 1


list_head_id = [token.head_id for token in doc.tokens]

person_list = []
result_cities = []
per_route = []

loc_spans = []
per_spans = []
ne_per_spans = []
for span in doc.spans:
    if span.type == 'LOC':
        normal_word = span.normal.lower()
        # извлечение из морфологического разбора слова существительное в именительном падеже
        loc_spans.append(morph_vocab.lemmatize(normal_word, 'NOUN', {'Animacy': 'Inan', 'Case': 'Nom'}))
    if span.type == 'PER':
        # print(span)
        # print(span.tokens)
        tokens = span.tokens
        flg = True
        for token in tokens:    # 
            if token.pos != 'PROPN':
                flg = False
            if ('Animacy' in token.feats) and ('Number' in token.feats):
                if token.feats['Animacy'] != 'Anim' and token.feats['Number'] != 'Sing':
                    flg = False
        if flg:               
            per_spans.append(span.normal)
        else:
            ne_per_spans.append(span.normal)

loc_spans = list(set(loc_spans))
per_spans = list(set(per_spans))

# print(loc_spans)
print(per_spans)
# print("--------------------------------")

# ---------------------------------------------------
# если страна в тексте упоминается, но не названо ни одного города в ней, то в список мест войдет название страны
for i in range(len(name_countries)):
    list_cities = set(city_counties[i]) & set(loc_spans)
    list_names = set(name_countries[i]) & set(loc_spans)
    if list_cities:
        result_cities.extend(list(list_cities)) 
    elif list_names:
        result_cities.extend(list(list_names))

# print(result_cities)        # итоговый список городов
# ---------------------------------------------------


# for per in per_spans:
#     print(morph_vocab(per))

Tokenizer=WordPunctTokenizer()
morph = pymorphy2.MorphAnalyzer()

token_text = Tokenizer.tokenize(text_lst)
token_text = [token.lower() for token in token_text]

result_charact = []

for pers in per_spans:
    final_name = {}
    tokens = Tokenizer.tokenize(pers)
    for tkn in tokens:
        p = morph.parse(tkn)
        # print(p)
        cont_flag = False
        for pars in p:
            if 'Surn' in pars.tag:
                final_name['Surn'] = pars.normal_form
                final_name['gend_surn'] = pars.tag.gender
                cont_flag = True
            elif 'Name' in pars.tag:
                final_name['Name'] = pars.normal_form
                final_name['gend'] = pars.tag.gender
                cont_flag = True
            elif 'Patr' in pars.tag:
                final_name['Patr'] = pars.normal_form
                final_name['gend_patr'] = pars.tag.gender
                cont_flag = True

            if cont_flag:
                break
    if final_name:
        result_charact.append(final_name)

print("--------------------")
print(result_charact)
print("--------------------")
normal_list = []

for charact in result_charact:
    full_name = ""
    if 'Name' in charact and 'Surn' in charact and 'Patr' in charact:
        for key in charact:
            if (key == 'Name' or key == 'Surn' or key == 'Patr'):
                parse_name = morph.parse(charact[key])[0].inflect({'sing', 'nomn', charact['gend']})
                if parse_name != None:
                    full_name += parse_name.word + " "
                else:
                    full_name += charact[key] + " "
        
    elif 'Name' in charact and 'Surn' in charact:
        for key in charact:
            if (key == 'Name' or key == 'Surn'):
                parse_name = morph.parse(charact[key])[0].inflect({'sing', 'nomn', charact['gend']})
                if parse_name != None:
                    full_name += parse_name.word + " "
                else:
                    full_name += charact[key] + " "
    elif 'Name' in charact and 'Patr' in charact:
        for key in charact:
            if (key == 'Name' or key == 'Patr'):
                parse_name = morph.parse(charact[key])[0].inflect({'sing', 'nomn', charact['gend']})
                if parse_name != None:
                    full_name += parse_name.word + " "
                else:
                    full_name += charact[key] + " "

    elif 'Name' in charact:
        parse_name = morph.parse(charact['Name'])[0].inflect({'sing', 'nomn', charact['gend']})
        if parse_name != None:
            full_name += parse_name.word + " "
        else:
            full_name += charact['Name'] + " "

    elif 'Surn' in charact and charact['gend_surn'] != None:
        parse_name = morph.parse(charact['Surn'])[0].inflect({'sing', 'nomn', charact['gend_surn']})
        if parse_name != None:
            full_name += parse_name.word + " "
        else:
            full_name += charact['Surn'] + " "
    elif 'Patr' in charact and charact['gend_patr'] != None:
        parse_name = morph.parse(charact['Patr'])[0].inflect({'sing', 'nomn', charact['gend_patr']})
        if parse_name != None:
            full_name += parse_name.word + " "
        else:
            full_name += charact['Patr'] + " "
        
    two_word = full_name.strip().split(' ')
    if len(two_word) > 1:
        if two_word[0] == two_word[1]:
            full_name = two_word[0]
    normal_list.append(full_name.strip())

print(set(normal_list))
