# Web Service with Spark Streaming and Kafka
Sergei Yu. Papulin (papulin.study@yandex.ru)

## Contents

- Prerequisites
- Spark configuration
- Kafka configuration
- Installing and running Redis
- Web service
- Spark Streaming Application
- Deploying Web Service and Spark Streaming application

## Spark configuration

In this tutorial the default configuration involves deploying Spark on `YARN` cluster. So you should configure, and run `HDFS` and `YARN`.

The configuration files you can find [here](spark_basics.md).

## Kafka configuration

Some examples below require the `Kafka` server as a message broker, so follow [this link](kafka_basics.md) to see guidelines that instruct how to install, configure and run `Kafka`

## Installing and running Redis 

#### With sudo

`apt install redis-server`

#### Without sudo

Download the `Redis` release:

`wget -P ~/redis/source http://download.redis.io/releases/redis-5.0.6.tar.gz`

Extract the archive:

`tar -xvzf ~/redis/redis-5.0.6.tar.gz --directory ~/redis --strip-components 1`

Compile `Redis`:

`cd ~/redis && make`

#### Starting Redis Server

Run the `Redis` server:

`$REDIS_HOME/src/redis-server`

To check the server run the `Redis` CLI and enter the `PING` command:

`$REDIS_HOME/src/redis-cli`

```
127.0.0.1:6379> PING
PONG
```

#### Python Redis client


Install `redis-py`:

`pip install redis --user` (optional)



## Web service


```
./src
├── main
│   ├── java
│   │   └── edu
│   │       └── classes
│   │           └── spark
│   │               ├── Application.java
│   │               ├── configurations
│   │               │   ├── KafkaConfiguration.java
│   │               │   └── RedisConfiguration.java
│   │               ├── controllers
│   │               │   ├── WordCountAPIServiceController.java
│   │               │   └── WordCountWebServiceController.java
│   │               ├── models
│   │               │   ├── Message.java
│   │               │   └── WordCountPair.java
│   │               └── services
│   │                   ├── IWordCountService.java
│   │                   └── WordCountService.java
│   └── resources
│       ├── application.yml
│       ├── static
│       └── templates
│           ├── index.html
│           ├── top_words.html
│           └── word_counts.html
└── test
    └── java

```



## Twitter API



## Spark Streaming Application

#### Kafka consumer

Apply the Kafka consumer as an input source. Below code snippet exemplifies how to use Kafka inside a `Spark Streaming` application. The full source code is available [here]()

```python
import json

from pyspark.streaming.kafka import KafkaUtils


KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "wordcount"

# Create subscriber (consumer) to the Kafka topic
kafka_stream = KafkaUtils.createDirectStream(ssc, 
                                             topics=[KAFKA_TOPIC],
                                             kafkaParams={"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

# Extract a content of messages from Kafka topic stream (per mini-batch)
lines = kafka_stream.map(lambda x: json.loads(x[1])["content"])

```

#### Redis client

```python
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_CHARSET = "utf-8"
REDIS_DECODE_RESPONSES = True

REDIS_KEY_WORD_COUNT = "count_word"
REDIS_KEY_TOP_10_WORD = "top_10_words"

def save_partition_in_redis(partition):
    """Insert/update word count pairs in Redis for each partition"""
    import redis
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset=REDIS_CHARSET, decode_responses=REDIS_DECODE_RESPONSES)
    for row in partition:
        r.zadd(REDIS_KEY_WORD_COUNT, {row[0]: row[1]})


def save_rdd_in_redis(time, rdd):
    """Insert/update word count pairs in Redis"""
    rdd.foreachPartition(save_partition_in_redis)


def save_top_10_in_redis(time, rdd):
    """Insert/update top 10 words """
    import redis
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset=REDIS_CHARSET, decode_responses=REDIS_DECODE_RESPONSES)
    r.delete(REDIS_KEY_TOP_10_WORD)
    top_10_words = rdd.takeOrdered(10, key=lambda x: -x[1])
    for word, count in top_10_words:
        r.zadd(REDIS_KEY_TOP_10_WORD, {word: count})


# Save word counts in redis (job 1)
total_counts.foreachRDD(save_rdd_in_redis)

# Save top 10 words in redis (job 2)
total_counts.foreachRDD(save_top_10_in_redis)
```


## Deploying Web Service and Spark Streaming application

#### Starting HDFS and Spark on YARN

Run `HDFS` and `YARN`

`$HADOOP_HOME/sbin/start-dfs.sh && $HADOOP_HOME/sbin/start-yarn.sh`

Run `History Server`

`$SPARK_HOME/sbin/start-history-server.sh`

Check whether all daemons are running

`jps`

Web UI:
- YARN Resource Manager port: `8088`
- Spark History Server port: `18080`
- Spark Cluster port: `8080` (for standalone cluster mode)

#### Launching Kafka Server

Start the `Zookeeper` Server:

`sudo $ZOOKEEPER_HOME/bin/zkServer.sh start`

Run the `Kafka` server:

`sudo $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties`


#### Submitting Spark Streaming Application

Before we configured Spark to being run on `YARN`. So the following command runs a spark streaming application on `YARN` by default:

`spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 wordcount_streaming.py`

To run locally use the command below:

`spark-submit --master local[2] --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 wordcount_streaming.py`

#### Launching Web Service



# References

[How To Install and Secure Redis on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04)

[An introduction to Redis data types and abstractions](https://redis.io/topics/data-types-intro)

[Spark Streaming Programming Guide](https://spark.apache.org/docs/2.3.0/streaming-programming-guide.html)

[PySpark Streaming Module API](https://spark.apache.org/docs/2.3.0/api/python/pyspark.streaming.html)

[Jedis](https://github.com/xetorthio/jedis)

[Spring Data Redis](https://docs.spring.io/spring-data/data-redis/docs/current/reference/html/#reference)
