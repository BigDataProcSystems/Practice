# Spark Structured Streaming: How To Include Timestamp

Sergei Yu. Papulin (papulin.study@yandex.ru)

## Contents

- [Prerequisites](#Prerequisites)
- [Source Code](#Source-Code)
- [Structured Streaming Application](#Structured-Streaming-Application )
    - [Main part](#Main-part)
    - [Including item timestamp](#Including-item-timestamp)
    - [Including batch timestamp](#Including-batch-timestamp)
    - [Embedded timestamp](#Embedded-timestamp)
- [References](#References)

## Prerequisites

To get started, you need to have done the following:

- Install Ubuntu 14+
- Install Java 8
- Install Anaconda (Python 3.7)
- Install Spark 2.4+
- Install IntelliJ 2019+ with Python Plugin or PyCharm 2019+

## Source Code

- Stream Server ([stream_server.py](../projects/structuredstreaming/stream_server.py))
- Spark Structured Streaming Application ([append_timestamp_streaming.py](../projects/structuredstreaming/append_timestamp_streaming.py))


## Structured Streaming Application 

### Main part

The application has only one option `timestamp_mode` that controls how we add the timestamp column to dataframes.


There are three values of the option:

- include (adding a timestamp when data is received)
- include_batch (adding the same timestamp values for all items for each batch)
- embedded (using timestamps of data itself, e.g. when they were generated)



```python
def main(timestamp_mode):

    cleanup()
    spark_session = start_spark()

    if timestamp_mode == "include":
        query = main_include_timestamp(spark_session)
    elif timestamp_mode == "include_batch":
        query = main_include_batch_timestamp(spark_session)
    elif timestamp_mode == "embedded":
        query = main_embedded_timestamp(spark_session)
    else:
        raise Exception("Unsupported timestamp mode.")

    query.awaitTermination()
```

For `include`:

```python
def main_include_timestamp(spark_session):
    lines = load_input_stream(spark_session, True)
    output = transformation_include_item(lines)
    return start_query(output)
```

For `include_batch`:

```python
def main_include_batch_timestamp(spark_session):
    lines = load_input_stream(spark_session, False)
    output = transformation_include_batch(lines)
    return start_query(output)
```

For `embedded`:

```python
def main_embedded_timestamp(spark_session):
    lines = load_input_stream(spark_session, False)
    output = transformations_embedded_steps(lines)
    return start_query(output)
```

To load input stream, we'll use socket connection:

```python
def load_input_stream(spark, include_timestamp=True):
    """Load stream."""
    return spark \
        .readStream \
        .format("socket") \
        .option("host", STREAM_HOST) \
        .option("port", STREAM_PORT) \
        .option("includeTimestamp", include_timestamp) \
        .load()
```


### Including item timestamp

To demonstrate how timestamps work, we will use the stream server that generate a random integer stream:

```python
def random_output(delay):
    import random
    for i in range(1000):
        yield random.randint(0, 10)
        sleep(delay)
```

Use the `includeTimestamp` option to include a timestamp to each received value:

```python
def load_input_stream(spark, include_timestamp=True):
    """Load stream."""
    return spark \
        .readStream \
        .format("socket") \
        .option("host", STREAM_HOST) \
        .option("port", STREAM_PORT) \
        .option("includeTimestamp", include_timestamp) \
        .load()
```

In this case the stream dataframe will have two columns: a value that represents a data flow from the stream server and timestamp included on the Spark application side.

```python
def transformation_include_item(stream):
    """Raw input data with timestamp when an item arrived."""
    return stream \
        .withColumnRenamed("value", "number")
```

To run the application, first, start the stream server to generate random integers:

`python stream_server.py --output random`

After that run the Spark streaming application using `include` as a value of the `timestamp_mode` option:

`spark-submit --master local[4] append_timestamp_streaming.py --timestamp_mode include`

Output:

```
-------------------------------------------
Batch: 1
-------------------------------------------
+------+-----------------------+
|number|timestamp              |
+------+-----------------------+
|9     |2020-12-17 20:54:04.573|
|5     |2020-12-17 20:54:06.574|
|0     |2020-12-17 20:54:08.576|
+------+-----------------------+

-------------------------------------------
Batch: 2
-------------------------------------------
+------+-----------------------+
|number|timestamp              |
+------+-----------------------+
|4     |2020-12-17 20:54:10.579|
|9     |2020-12-17 20:54:18.588|
|8     |2020-12-17 20:54:12.582|
|0     |2020-12-17 20:54:14.583|
|1     |2020-12-17 20:54:16.585|
+------+-----------------------+
```

### Including batch timestamp


First of all, let's disable the `includeTimestamp` option by the following line of code:

```python
...
lines = load_input_stream(spark_session, False)
...
```

To include a batch timestamp, we'll add a new column called `timestamp` during a transformation step with a current time that is returned by the `F.current_timestamp()` function. So, all items that belong to the same batch will have the same values of their timestamps.


```python
def transformation_include_batch(stream):
    """Raw input data with timestamp when processing is started."""
    return stream \
        .withColumn("timestamp", F.current_timestamp()) \
        .withColumnRenamed("value", "number")
```

Start the stream server with the `random` option value:

`python stream_server.py --output random`

Next run the spark application:

`spark-submit --master local[4] append_timestamp_streaming.py --timestamp_mode include_batch`


Output:

```
-------------------------------------------
Batch: 1
-------------------------------------------
+------+-----------------------+
|number|timestamp              |
+------+-----------------------+
|8     |2020-12-17 20:57:00.001|
|2     |2020-12-17 20:57:00.001|
|10    |2020-12-17 20:57:00.001|
|0     |2020-12-17 20:57:00.001|
|10    |2020-12-17 20:57:00.001|
+------+-----------------------+

-------------------------------------------
Batch: 2
-------------------------------------------
+------+-----------------------+
|number|timestamp              |
+------+-----------------------+
|3     |2020-12-17 20:57:10.001|
|3     |2020-12-17 20:57:10.001|
|4     |2020-12-17 20:57:10.001|
|7     |2020-12-17 20:57:10.001|
|5     |2020-12-17 20:57:10.001|
+------+-----------------------+
```

### Embedded timestamp

Sometimes, it's important to use embedded timestamps of data during transformations, e.g. timestamps when data were generated as opposed to when they were received. On a spark streaming application side, we should extract them and use appropriately.

To simulate data that contain a timestamp, we'll use the following code:

```python
def random_json_with_timestamp(delay, random_timestamp=False, timestamp_delay=60):
    import random
    import datetime
    import json
    for i in range(1000):
        timestamp = datetime.datetime.today() if not random_timestamp \
            else datetime.datetime.today() - datetime.timedelta(seconds=random.randint(0, timestamp_delay))
        yield json.dumps({
            "number": random.randint(0, 10),
            "timestamp": timestamp.isoformat()
        })
        sleep(delay)
```

Sample output:

```json
{
    "number": 3, 
    "timestamp": "2020-12-17T20:54:44"
}
```

To extract values from json, the code below will be used:


```python
def transformations_embedded(stream):
    """Transformation steps."""

    schema = StructType()
    schema.add("number", StringType())
    schema.add("timestamp", StringType())

    return stream \
        .select(F.from_json("value", schema).alias("data")) \
        .select("data.number", F.to_timestamp("data.timestamp").alias("timestamp"))
```

Let's check how it works. Start the streaming application with the `json_random_timestamp` option value:

`python stream_server.py --output json_random_timestamp`

And then run the spark application with the `embedded` value of the `timestamp_mode` option:

`spark-submit --master local[4] append_timestamp_streaming.py --timestamp_mode embedded`


Output:

```
-------------------------------------------
Batch: 1
-------------------------------------------
+------+--------------------------+
|number|timestamp                 |
+------+--------------------------+
|1     |2020-12-17 21:00:35.21267 |
|5     |2020-12-17 21:00:35.215084|
+------+--------------------------+

-------------------------------------------
Batch: 2
-------------------------------------------
+------+--------------------------+
|number|timestamp                 |
+------+--------------------------+
|9     |2020-12-17 21:00:40.218604|
|6     |2020-12-17 21:00:29.234105|
|6     |2020-12-17 21:00:09.220058|
|9     |2020-12-17 21:00:29.223873|
|4     |2020-12-17 20:59:58.23132 |
+------+--------------------------+
```

To make clear what happens when we apply the transformations above, use the function below instead of `transformations_embedded()`:

```python
def transformations_embedded_steps(stream):
    """Transformation steps."""

    schema = StructType()
    schema.add("number", StringType())
    schema.add("timestamp", StringType())

    return stream \
        .select("*", F.from_json("value", schema).alias("data")) \
        .select("*", "data.*") \
        .select("*", F.to_timestamp("timestamp").alias("datetime"))

```

Samples from the stream server:

```json
{"number": 1, "timestamp": "2020-12-17T21:03:58.363641"}
{"number": 3, "timestamp": "2020-12-17T21:03:42.366133"}
{"number": 10, "timestamp": "2020-12-17T21:04:35.369384"}
```

Generated output:

```
-------------------------------------------
Batch: 1
-------------------------------------------
+---------------------------------------------------------+--------------------------------+------+--------------------------+--------------------------+
|value                                                    |data                            |number|timestamp                 |datetime                  |
+---------------------------------------------------------+--------------------------------+------+--------------------------+--------------------------+
|{"number": 1, "timestamp": "2020-12-17T21:03:58.363641"} |[1, 2020-12-17T21:03:58.363641] |1     |2020-12-17T21:03:58.363641|2020-12-18 21:03:58.363641|
|{"number": 3, "timestamp": "2020-12-17T21:03:42.366133"} |[3, 2020-12-17T21:03:42.366133] |3     |2020-12-17T21:03:42.366133|2020-12-18 21:03:42.366133|
|{"number": 10, "timestamp": "2020-12-17T21:04:35.369384"}|[10, 2020-12-17T21:04:35.369384]|10    |2020-12-17T21:04:35.369384|2020-12-17 21:04:35.369384|
+---------------------------------------------------------+--------------------------------+------+--------------------------+--------------------------+

```

## References

[Structured Streaming Programming Guide](https://spark.apache.org/docs/2.4.7/structured-streaming-programming-guide.html) (Spark 2.4.7)