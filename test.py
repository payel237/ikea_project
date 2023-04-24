import unittest
import twitter
import pandas as pd
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from wordcloud import WordCloud
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import emoji
import re
from nltk.tokenize import word_tokenize

class TestTwitterDataAnalysis(unittest.TestCase):

    def test_get_emojis(self):
        """
        #Testing get_emoji function 
        """
        
        sentence = ["I love ❤️ coding in Python 🐍!"]
        emojis = twitter.get_emojis(sentence)
        expected_output = ['❤️', '🐍']
        self.assertEqual(emojis, expected_output)


    def test_clean_words(self):
        """
        #Test clean_words function
        """
        new_tokens = ["I", "love", "Python", "programming"]
        cleaned_tokens = twitter.clean_words(new_tokens)
        expected_output = ['love', 'python', 'programming']
        self.assertEqual(cleaned_tokens, expected_output)

if __name__ == '__main__':
    unittest.main()
