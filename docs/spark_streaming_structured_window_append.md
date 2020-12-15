# Spark Structured Streaming: Window with Append Output Mode

Sergei Yu. Papulin (papulin.study@yandex.ru)

## Contents

- Prerequisites
- Source Code
- Stream Server
- Spark Structured Streaming Application
- Running application
- References

## Prerequisites

To get started, you need to have done the following:

- Install Ubuntu 14+
- Install Java 8
- Install Anaconda (Python 3.7)
- Install Spark 2.4+
- Install IntelliJ 2019+ with Python Plugin or PyCharm 2019+


## Source Code

- Stream Server ([stream_server.py](../projects/structuredstreaming/stream_server.py))
- Spark Structured Streaming Application ([window_append_streaming.py](../projects/structuredstreaming/window_append_streaming.py))



## Stream Server

```python
def send_messages(message_gen, send_func):
    for message in message_gen:
        send_func("{}\n".format(message).encode("utf-8"))
        print("Sent value: {}".format(message))


def random_output(delay):
    import random
    for i in range(1000):
        yield random.randint(0, 10)
        sleep(delay)


for i in range(repeat):
    send_messages(init_iterator(output, delay, file), client_socket.send)
```

## Spark Structured Streaming Application


```python
def main(sink):

    # Cleaning up all previous data (for the local mode only)
    cleanup()

    # Creating a Spark session
    spark_session = start_spark()

    # Loading input stream
    lines = load_input_stream(spark_session)

    # Transformations
    output = transformations(lines)

    # Writing to output sink
    if sink == "console":
        query = start_query_console(output)
    elif sink == "file":
        query = start_query_csv(output)
    else:
        raise Exception("Provided output sink type is not supported.")

    # Waiting for termination
    query.awaitTermination()
```


```python

def load_input_stream(spark):
    return spark \
        .readStream \
        .format("socket") \
        .option("host", STREAM_HOST) \
        .option("port", STREAM_PORT) \
        .option("includeTimestamp", "true") \
        .load()


def transformations(stream):
    """Group by value and window."""
    return stream.withWatermark("timestamp", "15 seconds") \
        .groupBy("value", F.window("timestamp", "30 seconds", "15 seconds")) \
        .count() \
        .select(stringify_window("window").alias("window"), "value", "count") \
        .coalesce(1)


def start_query_console(output):
    """Start a query with the console sink type."""
    return output.writeStream \
        .option("checkpointLocation", APP_CHECKPOINT_DIR) \
        .outputMode("append") \
        .format("console") \
        .queryName("wordcount_query") \
        .option("truncate", False) \
        .trigger(processingTime="15 seconds") \
        .start()


def start_query_csv(output):
    """Start a query with the console sink type."""
    return output.writeStream \
        .format("csv") \
        .partitionBy("window") \
        .option("checkpointLocation", APP_CHECKPOINT_DIR) \
        .option("path", APP_DATA_OUTPUT_DIR) \
        .trigger(processingTime="10 seconds") \
        .outputMode("append") \
        .start()
```

## Running application

Run the stream server that will generate random integers from 0 to 10 (included) each 2 seconds to simulate a stream:

`python stream_server.py --output random`

After that, start the streaming application with the console output sink by the following command:

`spark-submit --master local[4] window_append_streaming.py --sink console`

In your terminal you should see something similar to the one below:

```
-------------------------------------------
Batch: 0
-------------------------------------------
+------+-----+-----+
|window|value|count|
+------+-----+-----+
+------+-----+-----+

...

-------------------------------------------
Batch: 3
-------------------------------------------
+-------------+-----+-----+
|window       |value|count|
+-------------+-----+-----+
|173300-173330|2    |2    |
|173300-173330|10   |1    |
|173300-173330|9    |2    |
|173300-173330|0    |1    |
|173300-173330|1    |1    |
+-------------+-----+-----+

-------------------------------------------
Batch: 4
-------------------------------------------
+-------------+-----+-----+
|window       |value|count|
+-------------+-----+-----+
|173315-173345|7    |2    |
|173315-173345|1    |1    |
|173315-173345|9    |4    |
|173315-173345|0    |2    |
|173315-173345|10   |1    |
|173315-173345|3    |1    |
|173315-173345|2    |3    |
+-------------+-----+-----+
```

Now let's run the same application but using the file sink mode:

`spark-submit --master local[4] window_append_streaming.py --sink file`


The output directory will contain files for each window:

```
output
├── window=173930-174000
│   └── part-00000-28ff049b-1ebd-405a-8718-f7b18e330e74.c000.csv
├── window=173945-174015
│   └── part-00000-19768e0f-bfa0-4fbc-a8ed-7957af6bd093.c000.csv
├── window=174000-174030
│   └── part-00000-2cb0fc9f-113a-42b0-a996-0f4c81a6e082.c000.csv
└── window=174015-174045
    └── part-00000-ada6ad74-ffad-4e9f-a217-a2cdd75be268.c000.csv
```


Content of the `part-00000-ada6ad74-ffad-4e9f-a217-a2cdd75be268.c000.csv` file:
```
5,2
6,3
1,2
3,3
9,1
8,4
```


## References

[Structured Streaming Programming Guide](https://spark.apache.org/docs/2.4.7/structured-streaming-programming-guide.html) (Spark 2.4.7)