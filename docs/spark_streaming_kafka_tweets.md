# Spark Streaming and Twitter API

Sergei Yu. Papulin (papulin.study@yandex.ru)

## Contents

- Prerequisites
- Spark configuration
- Kafka configuration
- Kafka Producer and Twitter API for Python
- Kafka Consumer and Spark Streaming Word Count
- Run and Test
- References

## Spark configuration

In this tutorial the default configuration involves deploying Spark on `YARN` cluster. So you should configure, and run `HDFS` and `YARN`.

The configuration files you can find [here](https://github.com/BigDataProcSystems/Spark/blob/master/docs/spark_basics.md).

## Kafka configuration

Some examples below require the `Kafka` server as a message broker, so follow [this link](https://github.com/BigDataProcSystems/Spark/blob/master/docs/kafka_basics.md) to see guidelines that instruct how to install, configure and run `Kafka`

## Kafka Producer and Twitter API for Python

Install python packages for Kafka and Twitter API:

`sudo pip install kafka-python tweepy`

Create a Kafka Producer that will receive messages from Twitter API and put them in Kafka Broker for the "tweets-kafka" topic.


```python
# -*- coding: utf-8 -*-

import tweepy
from tweepy.streaming import json
from kafka import KafkaProducer


"""

    KAFKA PRODUCER INIT


"""

producer = KafkaProducer(bootstrap_servers="localhost:9092")
topic_name = "tweets-kafka"


"""

    TWITTER API AUTHENTICATION


"""

consumer_token = "YOUR_CONSUMER_TOKEN"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_secret = "YOUR_ACCESS_SECRET"

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


"""

    LISTENER TO MESSAGES FROM TWITTER


"""


class MoscowStreamListener(tweepy.StreamListener):
    
    def on_data(self, raw_data):

        data = json.loads(raw_data)

        if "extended_tweet" in data:
            text = data["extended_tweet"]["full_text"]
            
            # print(text)
            
            # put message into Kafka
            producer.send(topic_name, text.encode("utf-8"))
        else:
            if "text" in data:
                text = data["text"].lower()
                
                # print(data["text"])
                
                # put message into Kafka
                producer.send(topic_name, data["text"].encode("utf-8"))


"""

    RUN PROCESSING


"""


# Create instance of custom listener
moscowStreamListener = MoscowStreamListener()

# Set stream for twitter api with custom listener
moscowStream = tweepy.Stream(auth=api.auth, listener=moscowStreamListener)

# Region that approximately corresponds to Moscow
region = [34.80, 49.87, 149.41, 74.13]

# Start filtering messages
moscowStream.filter(locations=region)

```


## Kafka Consumer and Spark Streaming Word Count

```python
# -*- coding: utf-8 -*-

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


SPARK_APP_NAME = "KafkaTwitterWordCount"
SPARK_CHECKPOINT_TMP_DIR = "tmp_spark_streaming"
SPARK_BATCH_INTERVAL = 10
SPARK_LOG_LEVEL = "OFF"

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "tweets-kafka"


# Update word count
def update_total_count(current_count, count_state):
    if count_state is None:
        count_state = 0
    return sum(current_count, count_state)


# Create Spark Context
sc = SparkContext(appName=SPARK_APP_NAME)

# Set log level
sc.setLogLevel(SPARK_LOG_LEVEL)

# Create Streaming Context
ssc = StreamingContext(sc, SPARK_BATCH_INTERVAL)

# Sets the context to periodically checkpoint the DStream operations for master
# fault-tolerance. The graph will be checkpointed every batch interval.
# It is used to update results of stateful transformations as well
ssc.checkpoint(SPARK_CHECKPOINT_TMP_DIR)

# Create subscriber (consumer) to the Kafka topic
kafka_stream = KafkaUtils.createDirectStream(ssc,
                                             topics=[KAFKA_TOPIC],
                                             kafkaParams={"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

# Extract only messages (works on RDD that is mini-batch)
lines = kafka_stream.map(lambda x: x[1])

# Count words for each RDD (mini-batch)
counts = lines.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda x1, x2: x1 + x2)

# Update word counts
total_counts = counts.updateStateByKey(update_total_count)

# Sort by counts
total_counts_sorted = total_counts.transform(lambda x_rdd: x_rdd.sortBy(lambda x: -x[1]))

# Print result
total_counts_sorted.pprint()

# Start Spark Streaming
ssc.start()

# Waiting for termination
ssc.awaitTermination()
```

## Run and Test

Create two py files for Kafka Producer with Twitter API connection (kafka_producer_tweets.py) and for Spark Streaming word count (spark_streaming_wordcount_kafka.py)

In terminal create the `tweets-kafka` topic that will refer to tweet stream from Twitter API:

`$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --topic tweets-kafka --partitions 1 --replication-factor 1`

Open four terminals:

1. Run the `Kafka` server:
    `$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties`

2. Run the `Kafka` console consumer:

    `$KAFKA_HOME/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic tweets-kafka --from-beginning`

3. Run the producer with Twitter API:

    `python ./kafka_producer.py`

4. Run the Spark Streaming application:

    on YARN

    `spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 ./spark_streaming_app.py`

    or locally

    `spark-submit --master local[2] --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 ./spark_streaming_app.py`


## References

[Spark Streaming Programming Guide](https://spark.apache.org/docs/2.3.0/streaming-programming-guide.html)

[Kafka Python client](https://github.com/dpkp/kafka-python)

[Kafka configuration](https://kafka.apache.org/documentation/#configuration)

[Tweepy: Twitter for Python!](https://github.com/tweepy/tweepy)

[Spark Streaming + Kafka Integration Guide](https://spark.apache.org/docs/2.3.0/streaming-kafka-0-8-integration.html)