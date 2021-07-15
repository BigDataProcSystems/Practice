# -*- coding: utf-8 -*-

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


# Application name
APP_NAME = "WordCount"

# Batch interval (10 seconds)
BATCH_INTERVAL = 10

# Source of stream
STREAM_HOST = "localhost"
STREAM_PORT = 9999


# Create Spark Context
sc = SparkContext(appName=APP_NAME)

# Set log level
sc.setLogLevel("ERROR")

# Batch interval (10 seconds)
batch_interval = 10

# Create Streaming Context
ssc = StreamingContext(sc, batch_interval)

# Create a stream (DStream)
lines = ssc.socketTextStream(STREAM_HOST, STREAM_PORT)


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
# counts.transform(lambda rdd: rdd.coalesce(1))
# .saveAsTextFiles("/YOUR_PATH/output/wordCount")

# Start Spark Streaming
ssc.start()

# Await termination
ssc.awaitTermination()
