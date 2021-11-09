# Spark Streaming and Kafka

Sergei Yu. Papulin (papulin.study@yandex.ru)

## Contents

- Prerequisites
- Spark configuration
- Kafka configuration
- Source Code
- Spark Streaming Application
- References

## Spark configuration

In this tutorial the default configuration involves deploying Spark on `YARN` cluster. So you should configure, and run `HDFS` and `YARN`.

The configuration files you can find [here](https://github.com/BigDataProcSystems/Spark/blob/master/docs/spark_basics.md).

## Kafka configuration

Some examples below require the `Kafka` server as a message broker, so follow [this link](https://github.com/BigDataProcSystems/Spark/blob/master/docs/kafka_basics.md) to see guidelines that instruct how to install, configure and run `Kafka`

Create a Kafka topic:

`$KAFKA_HOME/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --topic kafka-word-count`

Run a Kafka producer:

`$KAFKA_HOME/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic kafka-word-count`

Run a Kafka consumer:

`$KAFKA_HOME/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kafka-word-count --from-beginning`

## Source Code

- Spark Streaming with Kafka: [spark_streaming_kafka_wcount.py](../projects/kakfastreaming/spark_streaming_kafka_wcount.py)

## Spark Streaming Application

Spark Streaming application code ([spark_streaming_kafka_wcount.py](../projects/kakfastreaming/spark_streaming_kafka_wcount.py))

```python
# -*- coding: utf-8 -*-

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

SPARK_APP_NAME = "KafkaWordCount"
SPARK_CHECKPOINT_TMP_DIR = "tmp_spark_streaming"
SPARK_BATCH_INTERVAL = 10
SPARK_LOG_LEVEL = "OFF"

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "kafka-word-count"


def update_total_count(current_count, count_state):
    """
    Update the previous value by a new ones.

    Each key is updated by applying the given function 
    on the previous state of the key (count_state) and the new values 
    for the key (current_count).
    """
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

# Print result
total_counts.pprint()

# Start Spark Streaming
ssc.start()

# Waiting for termination
ssc.awaitTermination()

```

Run the spark streaming application (above code):

`spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 /YOUR_PATH/spark_streaming_kafka_wcount.py`

By default we use YARN client mode to deploy Spark application. To run locally use the following command with the explicit master argument:

`spark-submit --master local[2] --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 /YOUR_PATH/spark_streaming_kafka_wcount.py`

Type any text in the producer terminal and look at the output of your application.

## References

1. [Spark Streaming Programming Guide](https://spark.apache.org/docs/2.4.0/streaming-programming-guide.html)
2. [Apache Kafka Quickstart](https://kafka.apache.org/quickstart)
