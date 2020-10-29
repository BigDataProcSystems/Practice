# Introduction to Spark Streaming
Sergei Yu. Papulin (papulin_bmstu@mail.ru)


## Contents

- Prerequisites
- Spark configuration
- Kafka configuration
- Practice
- Spark and Jupyter

## Prerequisites

To get started, you need to have done the following:

- Install Ubuntu 14+
- Install Java 8
- Download Hadoop 3+
- Download Spark 2+
- [Optional] Anaconda Python 3.7
- IntelliJ with Python Plugin or PyCharm
- Install Jupyter (Python)

## Spark configuration

In this tutorial the default configuration involves deploying Spark on `YARN` cluster. So you should configure, and run `HDFS` and `YARN`.

The configuration files you can find [here](spark_basics.md).

## Kafka configuration

Some examples below require the `Kafka` server as a message broker, so follow [this link](kafka_basics.md) to see guidelines that instruct how to install, configure and run `Kafka`

## Practice

[Introduction to Spark Streaming](https://github.com/BigDataProcSystems/Spark_Streaming/blob/master/docs/spark_streaming_intro.md): Stateless/stateful and window transformations 

[Introduction to Kafka distributed message broker](../docs/kafka_basics.md): How to Set Up Kafka

[Spark Streaming with Kafka](https://github.com/BigDataProcSystems/Spark_Streaming/blob/master/docs/spark_streaming_kafka.md): Using Kafka as input source for Spark Streaming application

[Spark Streaming with Kafka and Twitter API](https://github.com/BigDataProcSystems/Spark_Streaming/blob/master/docs/spark_streaming_kafka_tweets.md): Using Kafka producer with messages received from Twitter API and Spark Steaming application with Kafka Consumer as input source to process tweets

[Spam Classification using Sklearn and Spark Streaming](https://github.com/BigDataProcSystems/Spark_Streaming/blob/master/docs/spark_streaming_classifier.md): Using spam classification model built with `sklearn` library in Spark Streaming application

[Updatable Broadcast in Spark Streaming Application](https://github.com/BigDataProcSystems/Spark_Streaming/blob/master/docs/spark_streaming_update.md): How to use ML models that change periodically in Spark Streaming applications 

