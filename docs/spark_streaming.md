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

[Introduction to Spark Streaming](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_Streaming/blob/master/spark_streaming_intro.ipynb):
Stateless/stateful and window transformations 

[Spark Streaming with Kafka](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_Streaming/blob/master/spark_streaming_kafka.ipynb): Using Kafka as input source for Spark Streaming application

[Spark Streaming with Kafka and Twitter API](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_Streaming/blob/master/spark_streaming_kafka_tweets.ipynb): Using Kafka producer with messages received from Twitter API and Spark Steaming application with Kafka Consumer as input source to process tweets

[Spark Streaming with Kafka and Sklearn](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_Streaming/blob/master/spark_streaming_spam_classification.ipynb): Using spam classification model built with sklearn library in Spark Streaming application

