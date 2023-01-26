
# Import libraries
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from nltk import tokenize
import re
# nltk.download('punkt')
import syllable as syllables_en

TOKENIZER = RegexpTokenizer('(?u)\W+|\$[\d\.]+|\S+')
SPECIAL_CHARS = ['.', ',', '!', '?','\'',' ',r'\n',' \'', ' (',';',' ','',')']
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"


def count_long_words(words):
    '''
    Return the number of word longer than 6 characters
    For the list of given words
    '''
    counter = 0
    for w in words:
        if len(w)>=6:
            counter+=1
    return counter

def get_char_count(words):
    '''
    Return the number of characters for
    The list of given words
    '''
    characters = 0
    for word in words:
        characters += len(word)
    return characters

def check(words):
    '''
    For a given list of words,
    Check if the word are alphabetic
    Returns the new list of words
    '''
    new_words = []
    for w in words:
        if re.match('\s[a-z]+[A-Z]',w):
            res_list = re.findall('[a-z][^A-Z]*', w)
            new_words += res_list
        else:
            new_words.append(w)
    return (new_words)


def get_words(text=''):
    '''
    For a given text,
    Clean and filter the get_words,
    Return a filtered list of words
    '''
    words = []
    words = nltk.word_tokenize(text)
    filtered_words = []
    words = check(words)
    for word in words:
        if word in SPECIAL_CHARS or word == " ":
            pass
        elif '-' in word:
            tmp = word.split('-')
            for t in tmp:
                if t != '':
                    filtered_words.append(clean_word(t))
        elif '\'' in word:
            tmp = word.split('\'')
            for t in tmp:
                clean = clean_word(t)
                if clean != '' or clean not in SPECIAL_CHARS:
                    filtered_words.append(clean)
        else:
            filtered_words.append(clean_word(word))
    return filtered_words

def clean_word(word):
    '''
    For a given word,
    Delete special characters in the words
    Return the word without special characters
    '''
    new_word = word.replace(",", "").replace(".", "").replace('\'','').replace(')','').replace(';','').replace('-','').replace('_','')#.replace('\n\n','')
    new_word = new_word.replace("!", "").replace("?", "")

    return new_word


def get_sentences(text=''):
    '''
    For a given text, return the list of sentences
    '''
    #https://stackoverflow.com/questions/4576077/how-can-i-split-a-text-into-sentences
    sentences = sent_tokenize(text)
    return sentences


def count_syllables(words):
    '''
    For a given list of words,
    Returns the number of syllables
    '''
    syllable_count = 0
    for word in words:
        syllable_count += syllables_en.count(word)
    return syllable_count

def count_syllables2(words):
    '''
    For a given list of words,
    Returns the number of syllables
    (Intended to have two ways of calculating nb sillables)
    '''
    syllable_count = 0
    for word in words:
        syllable_count += syllables_en.syllable_count(word)
    return syllable_count

def count_polysyllables(words):
    '''
    For a given list of words,
    Returns the number of polysyllables
    '''
    syllable_count = 0
    for word in words:
        syllable_count += syllables_en.count_polysyllable(word)
    return syllable_count

def count_complex_words(text=''):
    '''
    For a given text
    Returns the number of complex words
    '''
    words = get_words(text)
    sentences = get_sentences(text)
    complex_words = 0
    found = False
    cur_word = []

    for word in words:
        cur_word.append(word)
        if count_syllables(cur_word) >= 3:
            if not (word[0].isupper()):
                complex_words += 1
            else:
                for sentence in sentences:
                    if str(sentence).startswith(word):
                        found = True
                        break
                if found:
                    complex_words += 1
                    found = False

        cur_word.remove(word)
    return complex_words
