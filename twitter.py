from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import emoji 
import nltk
import re 
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
from collections import Counter
from nltk.tag import pos_tag
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')

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

def clean_words(new_tokens):

    """
    Function to clean twitter data
    """
    new_tokens = [t.lower() for t in new_tokens]
    new_tokens =[t for t in new_tokens if t not in stopwords.words('english')]
    new_tokens = [t for t in new_tokens if t.isalpha()]
    words_avoided = ["https","rt","also"]
    new_tokens = [t for t in new_tokens if t not in words_avoided]
    lemmatizer = WordNetLemmatizer()
    new_tokens =[lemmatizer.lemmatize(t) for t in new_tokens]

    return new_tokens

def readdatastream():

    """
    Function to read data as stream
    """
    checkpoint = "/var/jenkins_home/workspace/checkpoint/"
    spark = SparkSession.builder.appName("Read JSON Data").getOrCreate()
    df_schema = spark.read.format("json").load("/var/jenkins_home/workspace/ikea_assignment/").schema

    read_df = (spark
               .readStream
               .format('json')
               .option('ignoreChanges', 'true')
               .option('ignoreMissingFiles', 'true')
               .option('ignoreDeletes', 'true')
               .option('ignoreCorruptFiles', 'true')
               .option('ignoreChanges', 'true')
               .option('maxFilesPerTrigger', 100)
               .option('Path', "/var/jenkins_home/workspace/ikea_assignment/")
               .option("failOnDataLoss", "false")
               .schema(df_schema)
               .load()
               )
    
    print(read_df.show(5))
    
    query = read_df \
        .writeStream \
        .option("checkpointLocation", checkpoint) \
        .trigger(once=True) \
        .foreachBatch(batch_function) \
        .start().awaitTermination()

    print("Finished Analysis of data")
    return query.lastProgress


def batch_function():

    """
    Function to perform twitter data sentiment analysis 
    """

    #Reading Data & selecting relevant columns 
    # spark = SparkSession.builder.appName("Read JSON Data").getOrCreate()
    # df_twitter = spark.read.format("json").load("/var/jenkins_home/workspace/ikea_assignment/")
    df_twitter_pandas = df_twitter.toPandas()
    df_twitter = df_twitter.select("text")
    df_twitter_pandas['text'] = df_twitter_pandas['text'].astype('str')

    #Invoking function to perform analysis on emoji 
    emojis_bow = get_emojis(df_twitter_pandas['text'])
    emoji_count= (Counter(emojis_bow).items())
    emoji_frame = pd.DataFrame(emoji_count,columns=['emoji','count'])
    print("Twitter Data Emoji analysis")
    plt.figure(figsize=(20,10))
    print(emoji_frame.head(10).sort_values(by='count',ascending=False))
    print("***********************************************************")

    #Invoking function to perform analysis on data 
    comments =" ".join(df_twitter_pandas['text'])
    words = word_tokenize(comments)
    lowered = clean_words(words)
    bow = Counter(lowered)
    data = pd.DataFrame(bow.items(),columns=['word','frequency']).sort_values(by='frequency',ascending=False)
    data =data.head(20)
    print("Twitter Data analysis")
    print(data)
    print("***********************************************************")

    #Invoking function to perform trend analysis on the data 
    wordcloud = twitter_data_trend_analysis(df_twitter_pandas)
    print("Twitter data trend analysis report: Analysis report has been saved as PNG : /var/jenkins_home/workspace/ikea_assignment/trend_analysis_twitter_data.png")
    wordcloud.to_file("/var/jenkins_home/workspace/ikea_assignment/trend_analysis_twitter_data.png")
    plt.axis('off')
    plt.imshow(wordcloud)

#Invoking main function to perform reading & all analysis on twitter data 
readdatastream()
