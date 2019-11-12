# -*- coding: utf-8 -*-

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import json

bootstrap_servers = "localhost:9092"
topic = "wordcount"  # топик


# Функция для обновления значений количества слов
def update_total_count(current_count, count_state):
    if count_state is None:
        count_state = 0
    return sum(current_count, count_state)


# Создаем Spark Context
sc = SparkContext(appName="KafkaWordCount")

sc.setLogLevel("OFF")

# Создаем Streaming Context
ssc = StreamingContext(sc, 10)

# Объявляем checkpoint и указываем директорию в HDFS, где будут храниться значения
ssc.checkpoint("tmp_spark_streaming1")

# Создаем подписчика на поток от Kafka c топиком topic = "wordCount"
kafka_stream = KafkaUtils.createDirectStream(ssc, 
                                             topics=[topic], 
                                             kafkaParams={"bootstrap.servers": bootstrap_servers})

# Трансформируем мини-batch
lines = kafka_stream.map(lambda x: json.loads(x[1])["content"])

# Подсчитываем количество слов для мини-batch
counts = lines.flatMap(lambda line: line.split())\
    .map(lambda word: (word, 1))\
    .reduceByKey(lambda x1, x2: x1 + x2)

# Обновляем значения количества слов с учетом нового мини-batch
total_counts = counts.updateStateByKey(update_total_count)

# Выводим текущий результат
total_counts.pprint()

# Запускаем Spark Streaming
ssc.start()

# Ожидаем остановку
ssc.awaitTermination()

