
import math
import os
from preprocess import get_char_count, get_words, get_sentences, count_syllables, count_complex_words, count_syllables2, count_polysyllables, count_long_words
import pkg_resources
from symspellpy.symspellpy import SymSpell



class Readability:
    """
    This is a text analysis class that measures the quality of a block of text.
    """

    def __init__(self, text: str = '', debug: bool = False):
        self._debug = debug
        self.text_stats = {}
        self.text_analysis = {}
        self.results = {}
        self.sym_spell = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
        self.dictionary_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_dictionary_en_82_765.txt"
            )
        self.sym_spell.load_dictionary(self.dictionary_path, term_index=0, count_index=1)
        self.text = text

        # Calculate initial stats
        self.analyze_text()

    def get_text(self):
        '''Return the given text'''
        return(self.text)

    def spellcheck(self,text):
        pass

    def analyze_text(self):
        """
        Main Function to call the Readability
        Metrics function
        """
        if not self.text:
            print('No text to analyze.')
            self.text_analysis = {
            'ari': 0,
            'flesch_reading_ease': 0,
            'flesch_kincaid_grade_level': 0,
            'gunning_fog_index': 0,
            'smog_index': 0,
            'coleman_liau_index': 0,
            'lix': 0,
            'rix': 0,
            }
            self.text_stats = {
            'char_count': 0,
            'word_count': 0,
            'sentence_count': 0,
            'syllable_count': 0,
            'syllable_count2': 0,
            'syllable_per_word':0,
            'polysyllable_count':0,
            'complex_word_count': 0,
            'avg_words_per_sentence': 0
            }
            self.results['statistics'] = self.text_stats.copy()
            self.results['analysis'] = self.text_analysis.copy()
            return

        if not self.text_stats:
            self.calculate_text_stats()

        self.text_analysis = {
            'ari': self.ari(),
            'flesch_reading_ease': self.flesch_reading_ease(),
            'flesch_kincaid_grade_level': self.flesch_kincaid_grade_level(),
            'gunning_fog_index': self.gunning_fog_index(),
            'smog_index': self.smog_index(),
            'coleman_liau_index': self.coleman_liau_index(),
            'lix': self.lix(),
            'rix': self.rix(),
        }

        self.results['statistics'] = self.text_stats.copy()
        self.results['analysis'] = self.text_analysis.copy()
        if not self._debug:
            del self.results['statistics']['words']

    def calculate_text_stats(self):
        '''
        Main function to call the statistics function
        Of the preprocess file and get the statistics
        For the given text
        '''
        if not self.text:
            self.text_stats = {}
            return
        words = get_words(self.text)
        if len(words)>0:
            char_count = get_char_count(words)
            word_count = len(words)
            sentence_count = len(get_sentences(self.text))
            syllable_count = count_syllables(words)
            syllable_count2 = count_syllables2(words)
            polysyllable_count = count_polysyllables(words)
            long_words = count_long_words(words)
            complexwords_count = count_complex_words(self.text)
            avg_words_per_sentence = word_count / sentence_count
        else:
            char_count = 0.1
            word_count = 0.1
            sentence_count = 0.1
            syllable_count = 0.1
            syllable_count2 = 0.1
            polysyllable_count = 0.1
            long_words = 0.1
            complexwords_count = 0.1
            avg_words_per_sentence = 0.1

        self.text_stats = {
            'words': words,
            'char_count': float(char_count),
            'word_count': float(word_count),
            'long_word': float(long_words),
            'sentence_count': float(sentence_count),
            'syllable_count': float(syllable_count),
            'syllable_count2': float(syllable_count2),
            'syllable_per_word': float(syllable_count/word_count),
            'polysyllable_count':float(polysyllable_count),
            'complex_word_count': float(complexwords_count),
            'avg_words_per_sentence': float(avg_words_per_sentence)
        }

    def ari(self):
        """
        Using the collected statistics on the text,
        calculate the ARI score
        """
        score = 4.71*(self.text_stats['char_count']/self.text_stats['word_count']) + 0.5*(self.text_stats['word_count']/self.text_stats['sentence_count']) -21.43
        return score

    def flesch_reading_ease(self):
        """
        Using the collected statistics on the text,
        calculate the Flesch Reading Ease score
        """
        score = 206.835 - 84.6 * (self.text_stats['syllable_count']/self.text_stats['word_count']) - 1.015 * (self.text_stats['word_count']/self.text_stats['sentence_count'])
        return round(score, 4)

    def flesch_kincaid_grade_level(self):
        """
        Using the collected statistics on the text,
        calculate the Flesch Kincaid Grade score
        """
        score = 0.39 * (self.text_stats['word_count']/self.text_stats['sentence_count']) + 11.8* (self.text_stats['syllable_count']/self.text_stats['word_count']) -15.59
        return round(score, 4)

    def gunning_fog_index(self):
        """
        Using the collected statistics on the text,
        calculate the Gunning Fox Index
        """
        score = 0.4 * ((self.text_stats['word_count']/self.text_stats['sentence_count'])+100*(self.text_stats['complex_word_count']/self.text_stats['word_count']))
        return round(score, 4)

    def smog_index(self):
        """
        Using the collected statistics on the text,
        calculate the Smog Index
        """
        score = 1.0430 * math.sqrt(self.text_stats['polysyllable_count']*30/self.text_stats['sentence_count']) +3.1291
        return score

    def coleman_liau_index(self):
        """
        Using the collected statistics on the text,
        calculate the Coleman Liau Index
        """
        score = 0.0588* (self.text_stats['char_count']/self.text_stats['word_count']*100) - 0.296* (self.text_stats['sentence_count']/self.text_stats['word_count']*100) -15.8
        return round(score, 4)

    def lix(self):
        """
        Using the collected statistics on the text,
        calculate the LIX readability score
        """
        score = self.text_stats['long_word'] / self.text_stats['word_count'] * 100 + self.text_stats['word_count'] / self.text_stats['sentence_count']
        return score

    def rix(self):
        longwords = 0.0
        score = 0.0
        return score
