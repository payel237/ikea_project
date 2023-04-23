from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
# import numpy as np # linear algebra
# import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# import matplotlib.pyplot as plt
# import seaborn as sns
# from wordcloud import WordCloud, STOPWORDS
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("Read JSON Data") \
    .getOrCreate()

def wordcloudbot():
    """
    """
    df_twitter = spark.read.format("json").load("/var/jenkins_home/workspace/ikea_assignment/")
    df_twitter.show()

wordcloudbot()
