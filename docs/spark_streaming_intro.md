# Introduction to Spark Streaming

Sergei Yu. Papulin (papulin.study@yandex.ru)

## Contents

- Spark configuration
- Stateless Transformation
- Stateful Transformation
- Window Transformation
- References

## Spark configuration

In this tutorial the default configuration involves deploying Spark on `YARN` cluster. So you should configure, and run `HDFS` and `YARN`.

The configuration files you can find [here](https://github.com/BigDataProcSystems/Spark/blob/master/docs/spark_basics.md).


## Stateless Transformation

Spark Streaming application code:

```python
# -*- coding: utf-8 -*-

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


# Create Spark Context
sc = SparkContext(appName="WordCount")

# Set log level
#sc.setLogLevel("INFO")

# Batch interval (10 seconds)
batch_interval = 10

# Create Streaming Context
ssc = StreamingContext(sc, batch_interval)

# Create a stream (DStream)
lines = ssc.socketTextStream("localhost", 9999)


# TRANSFORMATION FOR EACH BATCH


"""
    MapFlat Transformation

    Example: ["a a b", "b c"] => ["a", "a", "b", "b", "c"] 

"""
words = lines.flatMap(lambda line: line.split())


"""
    Map Transformation

    Example: ["a", "a", "b", "b", "c"] => [("a",1), ("a",1), ("b",1), ("b",1), ("c",1)] ] 

"""
word_tuples = words.map(lambda word: (word, 1))



"""
    ReduceByKey Transformation

    Example: [("a",1), ("a",1), ("b",1), ("b",1), ("c",1)] => [("a",3),("b",2), ("c",1)]

"""
counts = word_tuples.reduceByKey(lambda x1, x2: x1 + x2)


# Print the result (10 records)
counts.pprint()

# Save to permanent storage
#counts.transform(lambda rdd: rdd.coalesce(1)).saveAsTextFiles("/YOUR_PATH/output/wordCount")

# Start Spark Streaming
ssc.start()

# Await terminiation
ssc.awaitTermination()
```

Copy and paste the content above into a separate py file.

Create a test text source using the netcat tool. The netcat will set a listener to port 9999, and text typed in terminal will be read by Spark Streaming:

`nc -lk 9999`

Run the spark streaming application (above code):

`spark-submit /YOUR_PATH/spark_streaming_wordcount.py`


By default we use YARN client mode to deploy Spark application. To run locally use the following command with the explicit master argument:

`spark-submit --master local[2] /YOUR_PATH/spark_streaming_wordcount.py`

Now you should have two terminal (one for messages and the other for spark streaming app). Enter random text messages in the terminal with netcat and look at the terminal with spark streaming. How can you describe behaviour of the spark streaming app? What features do you notice? Why is it stateless?

## Stateful Transformation

Spark Streaming application code:

```python
# -*- coding: utf-8 -*-

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


# Create Spark Context
sc = SparkContext(appName="WordCountStatefull")

# Set log level
#sc.setLogLevel("INFO")

# Batch interval (10 seconds)
batch_interval = 10

# Create Streaming Context
ssc = StreamingContext(sc, batch_interval)

# Add checkpoint to preserve the states
ssc.checkpoint("tmp_spark_streaming") # == /user/cloudera/tmp_spark_streaming

# Create a stream
lines = ssc.socketTextStream("localhost", 9999)

# TRANSFORMATION FOR EACH BATCH
words = lines.flatMap(lambda line: line.split())
word_tuples = words.map(lambda word: (word, 1))
counts = word_tuples.reduceByKey(lambda x1, x2: x1 + x2)

# function for updating values
def update_total_count(currentCount, countState):
    if countState is None:
        countState = 0
    return sum(currentCount, countState)

# Update current values
total_counts = counts.updateStateByKey(update_total_count)

# Print the result (10 records)
counts.pprint()
#counts.transform(lambda rdd: rdd.coalesce(1)).saveAsTextFiles("/YOUR_PATH/output/wordCount")

# Start Spark Streaming
ssc.start()

# Await terminiation
ssc.awaitTermination()
```

Copy and paste the content above into a separate py file.

Run this spark streaming app in terminal as in the previous case. What is the difference between the results of the two applications?

## Window Transformation

Spark Streaming application code:

```python
# -*- coding: utf-8 -*-

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


# Create Spark Context
sc = SparkContext(appName="WordCountStatefullWindow")

# Set log level
#sc.setLogLevel("INFO")

# Batch interval (10 seconds)
batch_interval = 10

# Create Streaming Context
ssc = StreamingContext(sc, batch_interval)

# Add checkpoint to preserve the states
ssc.checkpoint("tmp_spark_streaming") # == /user/cloudera/tmp_spark_streaming

# Create a stream
lines = ssc.socketTextStream("localhost", 9999)


# TRANSFORMATION FOR EACH BATCH
words = lines.flatMap(lambda line: line.split())
word_tuples = words.map(lambda word: (word, 1))
counts = word_tuples.reduceByKey(lambda x1, x2: x1 + x2)

# Apply window
windowed_word_counts = counts.reduceByKeyAndWindow(lambda x, y: x + y, lambda x, y: x - y, 20, 10)
#windowed_word_counts = counts.reduceByKeyAndWindow(lambda x, y: x + y, None, 20, 10)


# Print the result (10 records)
windowed_word_counts.pprint()
#windowed_word_counts.transform(lambda rdd: rdd.coalesce(1)).saveAsTextFiles("/YOUR_PATH/output/wordCount")

# Start Spark Streaming
ssc.start()

# Await terminiation
ssc.awaitTermination()
```

Copy and paste the content above into a separate py file.

## References

[Spark Streaming Programming Guide](https://spark.apache.org/docs/2.3.0/streaming-programming-guide.html)