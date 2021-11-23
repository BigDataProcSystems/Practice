# Spark Structured Streaming: Complete and Update Output Modes

Sergei Yu. Papulin (papulin.study@yandex.ru)

## Contents

- [Prerequisites](#Prerequisites)
- [Source Code](#Source-Code)
- [Running Application](#Running-Application)
    - [Complete Mode and Console Sink](#Complete-Mode-and-Console-Sink)
    - [Update Mode and Console Sink](#Update-Mode-and-Console-Sink)
    - [Complete Mode and ForeachBatch Sink](#Complete-Mode-and-ForeachBatch-Sink)
    - [Update Mode and ForeachBatch Sink](#Update-Mode-and-ForeachBatch-Sink)
- [References](#References)

## Prerequisites

To get started, you need to have done the following:

- Install Ubuntu 14+
- Install Java 8
- Install Anaconda (Python 3.7)
- Install Spark 2.4+
- Install IntelliJ 2019+ with Python Plugin or PyCharm 2019+


## Source Code

- Spark Structured Streaming Application ([complete_update_streaming.py](../projects/structuredstreaming/complete_update_streaming.py))


## Running Application



### Application Structure


Main function:

```python
def main(mode, sink):

    spark_session = start_spark()
    lines = load_input_stream(spark_session)
    output = transformations(lines)

    if sink == "foreach":
        query = start_query_with_custom_sink(output, mode)
    elif sink == "console":
        # Note: sorting is available only in the complete mode.
        output = output.sort(F.desc("count")) if mode == "complete" else output
        query = start_query(output, mode)
    else:
        raise Exception("Unsupported sink.")

    query.awaitTermination()
```

Starting Spark session:

```python
def start_spark():

    # Note: spark.executor.* options are not the case in the local mode
    #  as all computation happens in the driver.
    conf = pyspark.SparkConf() \
        .set("spark.executor.memory", "1g") \
        .set("spark.executor.core", "2") \
        .set("spark.driver.memory", "2g")

    spark = SparkSession \
        .builder \
        .config(conf=conf) \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    return spark
```

Loading a stream:

```python
def load_input_stream(spark):
    """Load stream."""
    return spark \
        .readStream \
        .format("socket") \
        .option("host", STREAM_HOST) \
        .option("port", STREAM_PORT) \
        .load()
```

Transforming the stream:

```python
def transformations(stream):
    """Count words."""
    return stream \
        .select(F.explode(F.split("value", " ")).alias("word")) \
        .groupBy("word") \
        .count()
```

### Complete Mode and Console Sink

Note: You cannot run multiple queries to a single stream source. Only the first one will get data and be executed. 

```python
def start_query(output, mode):

    return output \
        .writeStream \
        .outputMode(mode) \
        .format("console") \
        .trigger(processingTime="10 seconds") \
        .queryName("wordcount_query") \
        .option("truncate", False) \
        .start()
```

Open a terminal and start listening to 9999 port for new client connection:

`nc -lk 9999`

Open another terminal to run the spark streaming application. Execute the following command:

```
spark-submit --master local[2] complete_update_mode.py -m complete -s console
```

Note: The application has two options: a mode (`-m`) and sink (`-s`).

In the terminal with running netcat util, type the following text:

```
a a b c
b d e
```

After a while (10 seconds later), type more text: 

```
a b c
a c
```

Eventually you should get a result that is similar to this one:

```
-------------------------------------------
Batch: 0
-------------------------------------------
+----+-----+
|word|count|
+----+-----+
+----+-----+

-------------------------------------------
Batch: 1
-------------------------------------------
+----+-----+
|word|count|
+----+-----+
|b   |2    |
|a   |2    |
|e   |1    |
|d   |1    |
|c   |1    |
+----+-----+

-------------------------------------------
Batch: 2
-------------------------------------------
+----+-----+
|word|count|
+----+-----+
|a   |4    |
|c   |3    |
|b   |3    |
|e   |1    |
|d   |1    |
+----+-----+
```

Stop your application.


### Update Mode and Console Sink

Repeat the same steps as before, but use the command below to start the spark streaming application:

```
spark-submit --master local[2] complete_update_mode.py -m update -s console
```

Output in terminal:

```
-------------------------------------------
Batch: 0
-------------------------------------------
+----+-----+
|word|count|
+----+-----+
+----+-----+

-------------------------------------------
Batch: 1
-------------------------------------------
+----+-----+
|word|count|
+----+-----+
|e   |1    |
|d   |1    |
|c   |1    |
|b   |2    |
|a   |2    |
+----+-----+

-------------------------------------------
Batch: 2
-------------------------------------------
+----+-----+
|word|count|
+----+-----+
|c   |3    |
|b   |3    |
|a   |4    |
+----+-----+
```

### Complete Mode and ForeachBatch Sink

Note: Each batch is sorted and limited to top 4 records


```python
def sort_batch(df, epoch_id):
    """Sort mini-batch and write to console."""
    df.sort(F.desc("count")) \
        .limit(4) \
        .write \
        .format("console") \
        .save()


def start_query_with_custom_sink(output, mode):
    """Start a query with the foreachBatch sink type."""
    return output \
        .writeStream \
        .foreachBatch(sort_batch) \
        .outputMode(mode) \
        .trigger(processingTime=STREAM_QUERY_TRIGGER) \
        .queryName("wordcount_query") \
        .option("truncate", STREAM_QUERY_TRUNCATE) \
        .start()
```

```
spark-submit --master local[2] complete_update_mode.py -m complete -s foreach
```

```
+----+-----+
|word|count|
+----+-----+
+----+-----+

+----+-----+
|word|count|
+----+-----+
|   b|    2|
|   a|    2|
|   e|    1|
|   d|    1|
+----+-----+

+----+-----+
|word|count|
+----+-----+
|   a|    4|
|   c|    3|
|   b|    3|
|   e|    1|
+----+-----+

```



### Update Mode and ForeachBatch Sink

```
spark-submit --master local[2] complete_update_mode.py -m update -s foreach
```

```
+----+-----+
|word|count|
+----+-----+
+----+-----+

+----+-----+
|word|count|
+----+-----+
|   b|    2|
|   a|    2|
|   e|    1|
|   d|    1|
+----+-----+

+----+-----+
|word|count|
+----+-----+
|   a|    4|
|   c|    3|
|   b|    3|
+----+-----+

```

## References

[Structured Streaming Programming Guide](https://spark.apache.org/docs/2.4.7/structured-streaming-programming-guide.html) (Spark 2.4.7)