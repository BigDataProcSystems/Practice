# Apache Spark

## Spark Basics

#### Lectures:
- [Spark RDD](https://drive.google.com/file/d/1jMTfYdtKAGT5jHaX9QxgwGm-KoYtBRVc/view?usp=sharing)
- [Spark DataFrame](https://drive.google.com/file/d/1zlj4erLDJTbvsBLYPP-ZArr7lnkIIzLE/view?usp=sharing)
- [User-Defined Functions (UDF) in PySpark](https://drive.google.com/file/d/1iUC-IlvbvG7AeD-72-5HWJy3MSZqEdKJ/view?usp=sharing)

#### Practice:
- [Configuring Spark on YARN](docs/spark_basics.md)
- [DEPRECATED] [Introduction to Spark App](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_rdd_intro.ipynb)
- [Introduction to PySpark RDD API](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_rdd_basics.ipynb)
- [Introduction to PySpark DataFrame API](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_df_basics.ipynb)
- Spark and Processing Customer Reviews:
    - Part 1. Interactive shell with Jupyter ([Python](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_rdd_reviews.ipynb))
    - Part 2. Self-Contained Application ([Java](docs/spark_reviews.md) | [Python](docs/spark_reviews_py.md))
- [UDF in PySpark](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_udf.ipynb)
- [Bikeshare and Spark DataFrames](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_gf_biketrips.ipynb)
- [Spark and Jupyter with Livy as Spark REST Server](docs/spark_livy_jupyter.md)

## Spark Streaming

#### Lectures:

- [Spark Streaming](https://drive.google.com/file/d/10LpgzZCyGoO_pTvNSS_nf4ybQG1ezcdh/view?usp=sharing)
- [Spark Structured Streaming](https://drive.google.com/file/d/1lXL00oqy4iVF3ZOkK8j17ECPRdzkYwKv/view?usp=sharing)

#### Practice:

Kafka:
- [Introduction to Kafka distributed message broker](docs/kafka_basics.md): How to Set Up Kafka

DStreams (RDD API):

- [Introduction to Spark Streaming](docs/spark_streaming_intro.md)<br>Stateless/stateful and window transformations 
- [Spark Streaming with Kafka](docs/spark_streaming_kafka.md)<br>Using Kafka as input source for Spark Streaming application
- [Spark Streaming with Kafka and Twitter API](docs/spark_streaming_kafka_tweets.md)<br>Using Kafka producer with messages received from Twitter API and Spark Steaming application with Kafka Consumer as input source to process tweets
- [Spam Classification using Sklearn and Spark Streaming](docs/spark_streaming_classifier.md)<br>Using spam classification model built with `sklearn` library in Spark Streaming application
- [Updatable Broadcast in Spark Streaming Application](docs/spark_streaming_update.md)<br>How to use ML models that change periodically in Spark Streaming applications 
- [Web Service with Spark Streaming and Kafka](docs/spark_streaming_service.md)
<!--[Introduction to Spark Streaming](docs/spark_streaming.md)-->

Structured Streaming (DataFrame API):
- [Complete and Update Output Modes](docs/spark_streaming_structured_output_modes.md)
- [How To Include Timestamp](docs/spark_streaming_structured_append_timestamp.md)
- [Window with Append Output Mode](docs/spark_streaming_structured_window_append.md)

## Spark MLlib

#### Lectures:

- [Stochastic Gradient Descent](https://drive.google.com/file/d/1tCb3A93A0Fo4tkGCo1ckU3-5zt6Jt8VC/view?usp=sharing)
- [Naive Bayes Classifier](https://drive.google.com/file/d/13W5If_KIinFKCJpSe0l9_8jQRuI5mD0S/view?usp=sharing)
- [Recommendation Systems using ALS](https://drive.google.com/file/d/18uJnyk2kP_1Zmn4p5ITnilFjTR0E1xkL/view?usp=sharing)

#### Practice:

RDD API:

- [Регрессия, классификация и кластеризация и Spark](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_rdd_ml_basics.ipynb)
- [Классификация текстовых документов в Spark](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_rdd_ml_spam_classification.ipynb)

DataFrame API:

- [Boston House Price and Spark MLlib](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_df_price_regression_cv.ipynb)
- [Multiclass Text Document Classification using Spark](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_df_docclass.ipynb)
- Recommendation Systems:
    - [Факторизация матрицы рейтингов и Spark MLlib](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_df_movie_recommendation.ipynb)
    - [Item-based collaborative filtering](lib/python/recommend/itemrecom.py) (python module)
- [Комбинация решающих деревьев и Spark MLlib](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_df_purchase_tree.ipynb)

Extra topics:

- [Spark and sklearn models](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_df_sklearn.ipynb)
- [Image Recognition using SynapseML](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_synapseml.ipynb)


## Spark GraphFrame

#### Lectures:

- [Spark GraphX](https://drive.google.com/file/d/1RaU3pxpnrJRQa1fiFWuUU9Mr5yRLfOxh/view?usp=sharing) (related)

#### Practice:

- [Introduction to Graph Analysis with Spark GraphFrames](https://nbviewer.jupyter.org/github/BigDataProcSystems/Practice/blob/master/spark/notebooks/spark_gf_airplanes.ipynb)


## Spark on Docker

#### Lectures:

- [Introduction to Docker](https://drive.google.com/file/d/1vb_fAwhB3oZxnukpuMKYRNFJa0bGn74C/view?usp=sharing) 

#### Practice:

- [HOWTO: Install Docker and Docker-Compose](https://github.com/BigDataProcSystems/Docker/blob/master/docs/howto_install_docker.md)
- [Deploying Spark on YARN cluster using Docker](https://github.com/BigDataProcSystems/Docker/blob/master/docs/spark_docker.md)


## Spark on Kubernetes

#### Lectures:

- [Spark on Kubernetes](https://drive.google.com/file/d/1hKwSqKd-eC3ALg5TxrHQAMDgtUfUTar0/view?usp=sharing) 

#### Practice:

- [Spark Standalone Cluster on Kubernetes using Deployments](https://github.com/BigDataProcSystems/Docker/blob/master/docs/spark_k8s_deployment.md)
- [Spark on Kubernetes: spark-submit](https://github.com/BigDataProcSystems/Docker/blob/master/docs/spark_k8s_spark-submit.md)
