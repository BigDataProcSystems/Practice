# Introduction to Spark Streaming

Sergei Yu. Papulin (papulin.study@yandex.ru)

## Contents

- Spark configuration
- Datasets
- Source Code
- Stateless Transformation
- Stateful Transformation
- Window Transformation
- TCP Server as Stream Source
- References

## Spark configuration

In this tutorial the default configuration involves deploying Spark on `YARN` cluster. So you should configure, and run `HDFS` and `YARN`.

The configuration files you can find [here](https://github.com/BigDataProcSystems/Spark/blob/master/docs/spark_basics.md).

## Datasets

- Small subset of reviews: [samples_100.json](https://github.com/BigDataProcSystems/Hadoop/blob/master/data/samples_100.json)

## Source Code

- Stateless Transformation: [spark_streaming_stateless.py](../projects/wcountstreaming/spark_streaming_stateless.py)
- Stateful Transformation: [spark_streaming_stateful.py](../projects/wcountstreaming/spark_streaming_stateful.py)
- Window Transformation: [spark_streaming_window.py](../projects/wcountstreaming/spark_streaming_window.py)
- TCP Server: [tcp_server.py](../projects/tcpserver/tcp_server.py)

## Stateless Transformation


Spark Streaming application code ([spark_streaming_stateless.py](../projects/wcountstreaming/spark_streaming_stateless.py)):

```python
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

Spark Streaming application code ([spark_streaming_stateful.py](../projects/wcountstreaming/spark_streaming_stateful.py)):

```python
...

# Add checkpoint to preserve the states
ssc.checkpoint(CHECKPOINT_DIR)

...

counts = word_tuples.reduceByKey(lambda x1, x2: x1 + x2)


# function for updating values
def update_total_count(currentCount, countState):
    """
    Update the previous value by a new ones.

    Each key is updated by applying the given function 
    on the previous state of the key (count_state) and the new values 
    for the key (current_count).
    """
    if countState is None:
        countState = 0
    return sum(currentCount, countState)


# Update current values
total_counts = counts.updateStateByKey(update_total_count)

# Print the result (10 records)
total_counts.pprint()

...
```

Run this spark streaming app in terminal as in the previous case. What is the difference between the results of the two applications?

## Window Transformation

Spark Streaming application code ([spark_streaming_window.py](../projects/wcountstreaming/spark_streaming_window.py)):

```python
...

# Add checkpoint to preserve the states
ssc.checkpoint(CHECKPOINT_DIR)

...

counts = word_tuples.reduceByKey(lambda x1, x2: x1 + x2)

# Apply window
windowed_word_counts = counts.reduceByKeyAndWindow(
    lambda x, y: x + y, 
    lambda x, y: x - y, 
    20, 10)

# windowed_word_counts = counts.reduceByKeyAndWindow(
# lambda x, y: x + y, None, 20, 10)


# Print the result (10 records)
windowed_word_counts.pprint()
# windowed_word_counts.transform(lambda rdd: rdd.coalesce(1)).saveAsTextFiles("/YOUR_PATH/output/wordCount")
```


## TCP Server

We'll use a TCP server as a stream source. The server starts on `localhost` and listens to `port 9999`. When connection with a client is established, the server sends messages to the client. In this case the messages are reviews that are stored in a json file. We emit each review from the file to the client with a short delay (4s by default).


TCP server code ([tcp_server.py](../projects/tcpserver/tcp_server.py)):
```python
# -*- coding: utf-8 -*-

import json
import socket
from time import sleep
import click


SERVER_HOST = "localhost"
SERVER_PORT = 9999
SERVER_WAIT_FOR_CONNECTION = 10
MESSAGE_DELAY = 4


def get_file_line(file_path):
    """Read a file line by line"""
    with open(file_path, "r") as f:
        for line in f:
            try:
                yield json.loads(line)["reviewText"]
            except json.JSONDecodeError:
                pass


@click.command()
@click.option("-h", "--host", default=SERVER_HOST, help="Server host.")
@click.option("-p", "--port", default=SERVER_PORT, help="Server port.")
@click.option("-f", "--file", help="File to send.")
@click.option("-d", "--delay", default=MESSAGE_DELAY, help="Delay between messages.")
def main(host, port, file, delay):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        print("Starting the server...")

        server_socket.bind((host, port))
        server_socket.listen()

        print("The server is running on {}:{} and listening to a new connection. "
              "To exit press CTRL+C.".format(host, port))

        while True:
            client_socket = None
            try:
                server_socket.settimeout(SERVER_WAIT_FOR_CONNECTION)
                print("Waiting for client connection...")
                client_socket, client_address = server_socket.accept()
                server_socket.settimeout(None)
                print("Connection established. Client: {}:{}".format(client_address[0], client_address[1]))
                print("Sending data...")
                for indx, review in enumerate(get_file_line(file)):
                    client_socket.send("{}\n".format(review).encode("utf-8"))
                    print("Sent line: {}".format(indx+1))
                    sleep(delay)
                print("Closing connection...")
                client_socket.close()

            except socket.timeout:
                print("No clients to connect.")
                break

            except KeyboardInterrupt:
                print("Interrupt")
                if client_socket:
                    client_socket.close()
                break

        print("Stopping the server...")


if __name__ == "__main__":
    main()

```

Start a spark streaming application as a client, and then run the script of the server by the following command:

`python tcp_server.py --file /YOUR_PATH/samples_100.json`


## References

[Spark Streaming Programming Guide](https://spark.apache.org/docs/2.3.0/streaming-programming-guide.html)