import unittest
import 
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

    def setUp(self):
        """
        Initialize SparkSession for testing
        """
        
        self.spark = SparkSession.builder.appName("TestTwitterDataAnalysis").getOrCreate()

    def test_get_emojis(self):
        """
        Testing get_emoji function 
        """
        
        sentence = ["I love ❤️ coding in Python 🐍!"]
        emojis = get_emojis(sentence)
        expected_output = ['❤️', '🐍']
        self.assertEqual(emojis, expected_output)

    def test_twitter_data_trend_analysis(self):
        """
        Test twitter_data_trend_analysis function
        """
        
        df_twitter_pandas = DataFrame(
            [("I love Python programming",), ("Python is awesome",)], ["text"]
        )
        wordcloud = twitter_data_trend_analysis(df_twitter_pandas)
        self.assertIsInstance(wordcloud, WordCloud)

    def test_clean_words(self):
        """
        Test clean_words function
        """
        new_tokens = ["I", "love", "Python", "programming"]
        cleaned_tokens = clean_words(new_tokens)
        expected_output = ['love', 'python', 'programming']
        self.assertEqual(cleaned_tokens, expected_output)

    def test_readdatastream(self):
        # Test readdatastream function
        read_df = readdatastream()
        self.assertIsInstance(read_df, DataFrame)

    def test_batch_function(self):
        # Test batch_function function
        df = DataFrame(
            [("I love Python programming",)], ["text"]
        )
        batch_function(df, 0)
        # You can use assert methods to check the expected output from the function

    def test_writestream(self):
        # Test writestream function
        df = DataFrame(
            [("I love Python programming",)], ["text"]
        )
        checkpoint = "/var/jenkins_home/workspace/checkpoint/"
        query = writestream(df)
        self.assertIsInstance(query, MagicMock)

if __name__ == '__main__':
    unittest.main()
