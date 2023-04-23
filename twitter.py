from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import emoji 
import nltk
import re 
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.tag import pos_tag
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import warnings
warnings.filterwarnings("ignore")

def get_emojis(sentence):

    """ 
    Function to extract emojis from dataframe and calculate the occurance 
    """
    sentence =" ".join(sentence)
    words = word_tokenize(sentence)
    emojis = [e for e in words if e in emoji.UNICODE_EMOJI['en']]
    return emojis

    
def twitter_data_trend_analysis(df_twitter_pandas):

    """
    Function to perform twitter data trend analysis 
    """

    stopwords = set(STOPWORDS)
    stopwords.update(["https","@"])

    bigstring = df_twitter_pandas.apply(lambda x: ' '.join(x)).str.cat(sep=' ')
    bigstring = re.sub('[^A-Za-z0-9]+',' ',bigstring)

    plt.figure(figsize=(20,15))
    wordcloud = WordCloud(stopwords=stopwords,background_color='white',width=1500, height=1000,min_word_length=4,collocations=True,collocation_threshold=10) \
                .generate(bigstring)

    return wordcloud

def twitter_data_analyis():

    """
    Function to perform twitter data sentiment analysis 
    """

    #Reading Data & selecting relevant columns 
    spark = SparkSession.builder.appName("Read JSON Data") .getOrCreate()
    df_twitter = spark.read.format("json").load("/var/jenkins_home/workspace/ikea_assignment/")
    df_twitter = df_twitter.select("text")
    df_twitter_pandas = df_twitter.toPandas()
    df_twitter_pandas['text'] = df_twitter_pandas['text'].astype('str')

    #Invoking function to perform analysis on emoji 
    emojis_bow = get_emojis(df_twitter_pandas['text'])
    emoji_count= (Counter(emojis_bow).items())
    emoji_frame = pd.DataFrame(emoji_count,columns=['emoji','count'])
    print("Twitter Data Emoji analysis")
    plt.figure(figsize=(20,10))
    print(emoji_frame.head(10).sort_values(by='count',ascending=False))
    print("***********************************************************")

    #Invoking function to perform trend analysis on the data 
    wordcloud = twitter_data_trend_analysis(df_twitter_pandas)
    print("Twitter data trend analysis report: Analysis report has been saved as PNG : /var/jenkins_home/workspace/ikea_assignment/trend_analysis_twitter_data.png")
    wordcloud.to_file("/var/jenkins_home/workspace/ikea_assignment/trend_analysis_twitter_data.png")
    plt.axis('off')
    plt.imshow(wordcloud)
    

twitter_data_analyis()
