import nltk
nltk.download('words')
from nltk.corpus import words

word_list = words.words()

short_words = [word.strip() for word in word_list if len(word) == 5 and word.isalpha() and not word[0].istitle()]

word_list = list(set(short_words))

try:
    with open("adicao.txt", "r") as f:
        for word in f:
            if word.strip():
                word_list.append(word.strip())
except FileNotFoundError:
    print("Arquivo adicao.txt não encontrado, ignorando.")

# Salvar a lista em JSON para usar no frontend
import json
with open("words.json", "w") as f:
    json.dump(word_list, f)
