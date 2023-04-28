import nltk
import pymorphy2
import string
from nltk.tokenize import WordPunctTokenizer, sent_tokenize
from nltk.corpus import stopwords

lst = []
text_lst = ""
move_words = []

with open('D:/University/final_qualifying_work/files/2.txt', encoding='utf-8') as movement:
    for line in movement:
        move_words = line.split()

# Верн Жюль. Вокруг света в восемьдесят дней - royallib.com.txt
# lermontov1.txt

with open('D:/University/final_qualifying_work/books/lermontov1.txt', encoding='utf-8') as text_book:
    i = 0
    for line in text_book:
        line_text = line.strip()
        if line_text != "":
            lst.append(line_text)
            text_lst += line_text + ' \n'

morth = pymorphy2.MorphAnalyzer()
sentences = sent_tokenize(text_lst)

Tokenizer=WordPunctTokenizer()
token_text = Tokenizer.tokenize(text_lst)
token_text = [token.lower() for token in token_text]

# print(token_text)

stopWords = stopwords.words("russian")
# print(stopWords)
result = string.punctuation

token_text_without = [token for token in token_text if token not in stopWords]
token_clear_text = []
for token in token_text_without:
    bln = False
    for pnkt in result:
        if pnkt in token:
            bln = True
    if not bln:
        token_clear_text.append(token)


# ------------ получение списка стран, имеющиейся в художественном тексте ----------------------------------
str_file = ""
try:
    with open("../files/cities.txt", "r+", encoding="utf-8") as file:      # file = open("myfile.txt")
        s = file.read()
        str_file = s

except FileNotFoundError:
    print("Невозможно открыть файл")

cities = str_file.split('\n')
list_cities = set([city.lower() for city in cities if city != ''])

morth_token_geox = []
morth_token_name = []
morth_token_surn = []
morth_token_patr = []
rezult_token = []
text_normalize = []

for token in token_clear_text:
    p = morth.parse(token)
    for p_elem in p:
        rezult_token.append(p_elem)
        if 'Geox' in p_elem.tag:
            morth_token_geox.append(p_elem.normal_form)
        if 'Name' in p_elem.tag:
            morth_token_name.append(p_elem.normal_form)
        if 'Surn' in p_elem.tag:
            morth_token_surn.append(p_elem.normal_form)
        if 'Patr' in p_elem.tag:
            morth_token_patr.append(p_elem.normal_form)


# print(morth_token)
rezult_token = set(rezult_token)
morth_token = set(morth_token_geox)
# print(morth_token)

result_cities = morth_token & list_cities        # итоговый список стран
result_names = set(morth_token_name)
result_surn = set(morth_token_surn)
result_patr = set(morth_token_patr)
# # print(rezult_token)
print("-------------------------------------------------")
print(result_cities)
print(result_names)
print("-------------------------------------------------")
print(result_surn)
print(result_patr)
# print(len(rezult_token & list_cities))
# print(rezult_token & list_cities)
# print(len(morth_token & list_cities))
# print(morth_token & list_cities)



# ---------------------- получение имен персонажей книги --------------------