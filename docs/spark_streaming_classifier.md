# Spam Classification using Sklearn and Spark Streaming

Sergei Yu. Papulin (papulin.study@yandex.ru)

## Contents

- Prerequisites
- Spark configuration
- Datasets
- Source Code
- Fitting Spam Classifier
- Classification in Stream
- Message Stream Source
- Running application
- References

## Prerequisites

To get started, you need to have done the following:

- Install Ubuntu 14+
- Install Java 8
- Install Anaconda (Python 3.7)
- (Optional) Install Hadoop 3+
- Install Spark 2+
- Install IntelliJ 2019+ with Python Plugin or PyCharm 2019+


## [Optional] Spark configuration

In this tutorial the default configuration involves deploying Spark on `YARN` cluster. So you should configure, and run `HDFS` and `YARN`.

The configuration files you can find [here](https://github.com/BigDataProcSystems/Spark/blob/master/docs/spark_basics.md).


## Datasets

[Initial dataset](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection) containing sms messages has been divided into two subsets `smstrain` and `smstest`:

- [SMS messages for training models](../data/smstrain)
- [SMS messages for streaming](../data/smstest)


The code for splitting the initial data:

```python
import pandas as pd
import os
from sklearn.model_selection import train_test_split

BASE_DATA_DIR = os.path.dirname(DATASET_PATH)
data = pd.read_csv(DATASET_PATH, sep="\t", header=None, names=["class", "message"])
data_train, data_test = train_test_split(data, test_size=0.2, random_state=RANDOM_STATE)
data_train.to_csv(os.path.join(BASE_DATA_DIR, "smstrain"), sep="\t", header=False, index=False)
data_test[["message"]].to_csv(os.path.join(BASE_DATA_DIR, "smstest"), sep="\t", header=False, index=False)
```


## Source Code

- Fitting Spam Classifier: [spam_classification.py](../projects/spamstreaming/spam_classification.py)
- Classification in Stream: [spark_streaming_spam.py](../projects/spamstreaming/spark_streaming_spam.py)
- Message Stream Source: [tcp_server.py](../projects/spamstreaming/tcp_server.py)


## Fitting Spam Classifier

Source code: [spam_classification.py](../projects/spamstreaming/spam_classification.py)

```python
...

@click.command()
@click.option("-i", "--input", default=INPUT_DATASET_PATH, help="Input dataset path.")
@click.option("-o", "--output", default=OUTPUT_MODEL_PATH, help="Output model directory.")
def main(input, output):

    models = [
        LogisticRegression(penalty="l2",
                           fit_intercept=True,
                           max_iter=LOGREG_MAX_ITER,
                           C=LOGREG_REGUL,
                           solver=LOGREG_SOLVER,
                           random_state=RANDOM_STATE),
        BernoulliNB(alpha=BERNOULLI_ALPHA)]

    print("Loading dataset...")
    data = load_data(input)

    print("Splitting data onto train and test subsets...")
    train, test = train_test_split(data, test_size=0.2, random_state=RANDOM_STATE)

    print("Finding the best model...")
    best_model, best_model_accuracy = find_best_model(models, train, test)

    print("Best model: {}::{}".format(best_model.__class__.__name__, best_model_accuracy))

    print("Fitting the best model on the entire dataset...")
    final_vectorizer_model, final_model = fit(best_model, data)

    print("Serializing models...")
    save_models(output, final_vectorizer_model, final_model)

    print("Done.")

...
```

## Classification in Stream

Source code: [spark_streaming_spam.py](../projects/spamstreaming/spark_streaming_spam.py)


```python
...

@click.command()
@click.option("-s", "--classifier", default=MODEL_SPAM_PATH, help="Model for classification.")
@click.option("-v", "--vectorizer", default=MODEL_BINARIZER_PATH, help="Model for text vectorization.")
def main(vectorizer, classifier):

    # Create Spark Context
    sc = SparkContext(appName=SPARK_APP_NAME)

    # Set log level
    sc.setLogLevel(SPARK_LOG_LEVEL)

    # Load models
    tf_model = load_binarizer_model(model_path=vectorizer)
    spam_model = load_spam_model(model_path=classifier)

    # Transfer model to all executors
    tf_model_broadcast = sc.broadcast(tf_model)
    spam_model_broadcast = sc.broadcast(spam_model)

    # Create Streaming Context
    ssc = StreamingContext(sc, SPARK_BATCH_INTERVAL)

    # Create a stream
    lines = ssc.socketTextStream(STREAM_HOST, STREAM_PORT)

    # Predict class of messages

    # Option 1
    spam_predictions = lines.mapPartitions(predict_wrapper(tf_model_broadcast, spam_model_broadcast))

    # Option 2
    # spam_predictions = lines.mapPartitions(lambda part: predict_with_broadcast(part,
    #                                                                            tf_model_broadcast,
    #                                                                            spam_model_broadcast))

    output = spam_predictions.map(format_output)

    # Print the result (10 records) in terminal
    output.pprint()

    # If you want to save the result in file systems
    # output.transform(lambda rdd: rdd.coalesce(1)).saveAsTextFiles("FILE_PATH")

    # Start Spark Streaming
    ssc.start()

    # Await termination
    ssc.awaitTermination()

...
```

Loading models:

```python
...

MODEL_SPAM_PATH = "models/spammodel.pickle"
MODEL_BINARIZER_PATH = "models/vecmodel.pickle"


def load_spam_model(model_path=MODEL_SPAM_PATH):
    with open(model_path, "rb") as f:
        return pickle.load(f)


def load_binarizer_model(model_path=MODEL_BINARIZER_PATH):
    with open(model_path, "rb") as f:
        return pickle.load(f)

...
```

Prediction:

```python
...

# Option 1

def predict_wrapper(br_bin_model, br_spam_model):

    def predict(messages):
        """
        Classify messages in each partition

        Note: Commonly messages are processed on multiple nodes,
        so sklearn must be installed on each of them
        """

        # Load models
        bin_model = br_bin_model.value
        spam_model = br_spam_model.value

        # Predict class of each message
        for message in messages:
            message_vector = bin_model.transform([message])
            yield spam_model.predict(message_vector), message

    return predict


def main(vectorizer, classifier):
    ...

    # Option 1
    spam_predictions = lines.mapPartitions(predict_wrapper(tf_model_broadcast, spam_model_broadcast))

    ...

...
```

```python
...

# Option 2

def predict_with_broadcast(messages, br_bin_model, br_spam_model):

    # Load models
    bin_model = br_bin_model.value
    spam_model = br_spam_model.value

    # Predict class of each message
    for message in messages:
        message_vector = bin_model.transform([message])
        yield spam_model.predict(message_vector), message


def main(vectorizer, classifier):
    ...

    # Option 2
    spam_predictions = lines.mapPartitions(lambda part: predict_with_broadcast(part,
                                                                               tf_model_broadcast,
                                                                               spam_model_broadcast))

    ...

...
```

Output operations:

```python
# Print the result (10 records) in terminal
output.pprint()
```

```python
# If you want to save the result in file systems
output.transform(lambda rdd: rdd.coalesce(1)).saveAsTextFiles("FILE_PATH")
```


## Message Stream Source

Source code: [tcp_server.py](../projects/spamstreaming/tcp_server.py)

```python
# -*- coding: utf-8 -*-

import socket
from time import sleep
import click


SERVER_HOST = "localhost"
SERVER_PORT = 9999
SERVER_WAIT_FOR_CONNECTION = 10
MESSAGE_DELAY = 4


def get_file_line(file_path):
    """Read a file line by line"""
    with open(file_path, "r") as f:
        for line in f:
            yield line.strip()


@click.command()
@click.option("-h", "--host", default=SERVER_HOST, help="Server host.")
@click.option("-p", "--port", default=SERVER_PORT, help="Server port.")
@click.option("-f", "--file", help="File to send.")
@click.option("-d", "--delay", default=MESSAGE_DELAY, help="Delay between messages.")
def main(host, port, file, delay):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        print("Starting the server...")

        server_socket.bind((host, port))
        server_socket.listen()

        print("The server is running on {}:{} and listening to a new connection. "
              "To exit press CTRL+C.".format(host, port))

        while True:
            client_socket = None
            try:
                server_socket.settimeout(SERVER_WAIT_FOR_CONNECTION)
                print("Waiting for client connection...")
                client_socket, client_address = server_socket.accept()
                server_socket.settimeout(None)
                print("Connection established. Client: {}:{}".format(client_address[0], client_address[1]))
                print("Sending data...")
                for indx, review in enumerate(get_file_line(file)):
                    client_socket.send("{}\n".format(review).encode("utf-8"))
                    print("Sent line: {}".format(indx+1))
                    sleep(delay)
                print("Closing connection...")
                client_socket.close()

            except socket.timeout:
                print("No clients to connect.")
                break

            except KeyboardInterrupt:
                print("Interrupt")
                if client_socket:
                    client_socket.close()
                break

        print("Stopping the server...")


if __name__ == "__main__":
    main()
```


## Running application

To create models for text vectorization and spam classification run the following command:

```shell
python spam_classification.py \
    --input /YOUR_PATH/smstrain \
    --output models    
```

The `output` option specifies the directory where the models will be placed.

Now start the Spark streaming application:

```shell
spark-submit --master local[2] spark_streaming_spam.py \
    --vectorizer models/vecmodel.pickle \
    --classifier models/classmodel.pickle
```

To create a stream of messages, run the tcp server by the command below:

```shell
python tcp_server.py \
    --file /YOUR_PATH/smstest
```

