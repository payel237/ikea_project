import unittest
import twitter
import pandas as pd
from unittest.mock import MagicMock
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

    def test_twitter_data_trend_analysis(self):
        """
        #Test twitter_data_trend_analysis function
        """
        
        text_values = ["solar energy", "furniture", "gift card"]
        df_twitter_pandas = pd.DataFrame({'text': text_values})
        
        wordcloud = twitter.twitter_data_trend_analysis(df_twitter_pandas)
        self.assertIsInstance(wordcloud, WordCloud)

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
