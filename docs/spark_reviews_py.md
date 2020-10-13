# Spark and Processing Customer Reviews
## Part 2. Self-Contained Application
Sergei Yu. Papulin (papulin_bmstu@mail.ru)

#### [Version 2018](https://github.com/BigDataProcSystems/Hadoop/blob/2018/mapreduce_basics.ipynb)

## Contents

- Prerequisites
- Configuration
- Installing `Python` plugin for `IntelliJ`
- Creating `Python` project
- Source code
- Running with local files
- Running `python` app on YARN cluster
- References

## Prerequisites

To get started, you need to have done the following:

- Install Ubuntu 14+ (with Python 3.x)
- Install Java 8
- Install Hadoop 3+
- Install Spark 2+
- Install IntelliJ 2019+
- (Optional) Install PyCharm 2019+ (for Python code)


## Installing `Python` plugin for `IntelliJ`

`File` -> `Settings` -> `Plugins` -> Find the `Python Community Edition` plugin from `JetBrains` -> Click on `Install` -> Restart IDE

## Creating `Python` project

`File` -> `New` -> `Project...` -> `Python` -> Next ->  Name: `reviewsparkapp` - > Finish

## Datasets

- [Small subset of reviews](https://github.com/BigDataProcSystems/Hadoop/blob/master/data/samples_100.json)
- [Amazon product datasets](http://jmcauley.ucsd.edu/data/amazon/links.html)

## Source Code

1. [Word Count for Review Text]()

Code Snippet

```python
...

def extract_words(items):
    """
    Extract words from a review text

    :param items:   records of a partition
    :return:
    """
    import json
    for item in items:
        try:
            for word in json.loads(str(item))["reviewText"].split(" "):
                yield (word, 1)
        except:
            pass


def main(input_file, output_path):
    """
    Entrypoint to the application

    :param input_file: the 1st input argument
    :param output_path: the 2nd input argument
    :return:
    """

    if not input_file or not output_path:
        raise Exception("Wrong input arguments.")

    sc = create_spark_context()

    # Count words
    wcount_rdd = sc.textFile(input_file) \
        .mapPartitions(extract_words) \
        .reduceByKey(lambda v1, v2: v1 + v2) \
        .sortBy(lambda x: -x[1]) \
        .map(lambda x: "{}\t{}".format(x[0], x[1])) \
        .coalesce(1)

    # Save the result
    wcount_rdd.saveAsTextFile(output_path)
    sc.stop()

...
```

2. [Average Product Rating]()

Code Snippet

```python
...

def extract_prod_rating_per_partition(items):
    """
    Extract words from a review text

    :param items:   records of a partition
    :return:
    """
    import json
    for item in items:
        try:
            review = json.loads(item)
            yield review["asin"], float(review["overall"])
        except:
            pass


def main(input_file, output_path):
    """
    Entrypoint to the application

    :param input_file: the 1st input argument
    :param output_path: the 2nd input argument
    :return:
    """

    if not input_file or not output_path:
        raise Exception("Wrong input arguments.")

    sc = create_spark_context()

    # Calculate average ratings
    avg_prod_rating_rdd = sc.textFile(input_file) \
        .mapPartitions(extract_prod_rating_per_partition) \
        .aggregateByKey((0,0),
                        lambda x, value: (x[0] + value, x[1] + 1),
                        lambda x, y: (x[0] + y[0], x[1] + y[1])) \
        .map(lambda x: "{}\t{}".format(x[0], x[1][0]/x[1][1])) \
        .coalesce(1)

    # Save the result
    avg_prod_rating_rdd.saveAsTextFile(output_path)
    sc.stop()
...
```

3. Test class: `TODO`

## Running Spark Application with Local Files

Add the Spark modules:

`File` -> `Project Structure...` -> `Project Settings` -> `Modules` -> `Add Content Root` -> `$SPARK_HOME/python` and `$SPARK_HOME/python/lib/py4j-0.10.7-src.zip` -> `Apply` + `OK`

Create a configuration to run:

1) `Run` -> `Edit Configurations...`
2) `Add new configuration...` for Application -> Name: `wordcount`
3) Script path: `/YOUR_LOCAL_PATH/reviewsparkapp/wcount_reviews.py`
4) Program arguments: `INPUT_LOCAL_FILE OUTPUT_LOCAL_DIR`, e.g. `data/samples_100.json output` for a local file system
5) Environment variable: `PYTHONUNBUFFERED=1;PYSPARK_PYTHON=/opt/anaconda3/bin/python;PYSPARK_DRIVER_PYTHON=/opt/anaconda3/bin/python;SPARK_MASTER=local[2]`
6) Working directory: `/YOUR_LOCAL_PATH/reviewsparkapp`
7) `Apply` -> `OK`
8) `Run` -> `Run...` -> Choose your configuration


The output directory looks as follows:

```shell
output
├── part-00000
├── .part-00000.crc
├── _SUCCESS
└── ._SUCCESS.crc
```

First few rows from `part-00000`:
```
the	460
to	304
a	265
I	253
and	210
	192
it	187
is	130
of	127
for	113
```

To do the same steps for the average rating app and yuo will get the following result:

```shell
output
├── part-00000
├── .part-00000.crc
├── _SUCCESS
└── ._SUCCESS.crc
```

First few rows from `part-00000`:
```
0972683275	4.390243902439025
0528881469	2.4
0594451647	4.2
0594481813	4.0
```

## Running Spark Application on Cluster

### Local cluster (with local files)

Note: You can use HDFS as well


Run the spark application:

```
spark-submit --master local[2] \
    wcount_reviews.py \
    file:///YOUR_LOCAL_PATH/samples_100.json \
    file:///YOUR_LOCAL_PATH/output
```

First few rows from `part-00000`:

```
the	460
to	304
a	265
I	253
and	210
	192
it	187
is	130
of	127
for	113
```



### YARN cluster

#### Starting Hadoop cluster

Run `HDFS`:

`$HADOOP_HOME/sbin/start-dfs.sh`

Run `YARN`:

`$HADOOP_HOME/sbin/start-yarn.sh`

Run the Job History Server:

`mapred --daemon start historyserver`

Or all in one line command:

`$HADOOP_HOME/sbin/start-dfs.sh && $HADOOP_HOME/sbin/start-yarn.sh && mapred --daemon start historyserver`

Check out whether all daemons are running:

`jps`


#### Launching application

Remove the output directory if needed:

`hdfs dfs -rm -r -f /data/yarn/output`

Run the job:

```
spark-submit --master yarn --deploy-mode cluster --name ReviewPySparkClusterApp \
    wcount_reviews.py \
    /data/yarn/samples_100.json \
    /data/yarn/output
```


Job output:

`hdfs dfs -head /data/yarn/output/part-00000`

```
the     460
to      304
a       265
I       253
and     210
        192
it      187
is      130
of      127
for     113
...
```

Run the second job:

```
spark-submit --master yarn --deploy-mode cluster --name ReviewPySparkClusterApp \
    avgratings_reviews.py \
    /data/yarn/samples_100.json \
    /data/yarn/output
```

Job output:

`hdfs dfs -head /data/yarn/output/part-00000`

```
0972683275      4.390243902439025
0528881469      2.4
0594451647      4.2
0594481813      4.0
```
