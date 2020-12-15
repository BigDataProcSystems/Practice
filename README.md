# Main topics

## Current

### Spark Basics

#### Lectures:
- [Spark basics](https://github.com/BigDataProcSystems/Lectures/blob/master/BigData_Spark.pdf)
- [User-Defined Functions (UDF) in PySpark](https://github.com/BigDataProcSystems/Lectures/blob/master/BigData_PySpark_UDF.pdf)

#### Practice:
- [Configuring Spark on YARN](docs/spark_basics.md)
- [DEPRECATED] [Introduction to Spark App](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_RDD/blob/master/spark_rdd_intro.ipynb)
- [Introduction to PySpark RDD API](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_RDD/blob/master/spark_rdd_basics.ipynb)
- [Introduction to PySpark Dataframe API](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_Dataframe/blob/master/spark_df_basics.ipynb)
- Spark and Processing Customer Reviews:
    - Part 1. Interactive shell with Jupyter ([Python](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_RDD/blob/master/spark_rdd_reviews.ipynb))
    - Part 2. Self-Contained Application ([Java](docs/spark_reviews.md) | [Python](docs/spark_reviews_py.md))
- [UDF in PySpark](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_Dataframe/blob/master/spark_udf.ipynb)
- [Spark and Jupyter with Livy as Spark REST Server](docs/spark_livy_jupyter.md)

### Spark Streaming

#### Lectures:

- [Spark Streaming](https://github.com/BigDataProcSystems/Lectures/blob/master/BigData_Spark_Streaming.pdf)

#### Practice:


DStreams (RDD API):
- [Introduction to Spark Streaming](docs/spark_streaming.md)
- [Web Service with Spark Streaming and Kafka](docs/spark_streaming_service.md)


Structured Streaming (DataFrame API):
- [Complete and Update Output Modes](https://github.com/BigDataProcSystems/Spark_Streaming/blob/master/docs/spark_streaming_structured_output_modes.md)
- [Window with Append Output Mode](https://github.com/BigDataProcSystems/Spark_Streaming/blob/master/docs/spark_streaming_structured_window_append.md)

### Spark MLlib

#### RDD

- [Регрессия, классификация и кластеризация и Spark](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_ML_RDD/blob/master/spark_rdd_ml_basics.ipynb)
- [Классификация текстовых документов в Spark](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_ML_RDD/blob/master/spark_rdd_spam_classification.ipynb)

#### DataFrame

- [Boston House Price and Spark MLlib](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_ML_Dataframe/blob/master/notebooks/spark_df_price_regression_cv.ipynb)
- [Multiclass Text Document Classification using Spark](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_ML_Dataframe/blob/master/notebooks/spark_df_docclass.ipynb)
- Recommendation Systems:
    - [Факторизация матрицы рейтингов и Spark MLlib](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_ML_Dataframe/blob/master/notebooks/spark_df_movie_recommendation.ipynb)
    - [Item-based collaborative filtering](https://github.com/BigDataProcSystems/Spark_ML_Dataframe/blob/master/lib/python/recommend/itemrecom.py) (python module)
- [Комбинация решающих деревьев и Spark MLlib](https://nbviewer.jupyter.org/github/BigDataProcSystems/Spark_ML_Dataframe/blob/master/notebooks/spark_df_purchase_tree.ipynb)