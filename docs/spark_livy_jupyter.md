# Spark and Jupyter with Livy as Spark REST Server
Sergei Yu. Papulin (papulin_bmstu@mail.ru)

## Contents

- Prerequisites
- Livy Server
- Job submission using Livy Server
- Jyputer with Sparkmagic
	- PySpark kernel	
	- Scala kernel
- References

## Livy Server

According to the [official site](https://livy.apache.org/):

> Apache Livy is a service that enables easy interaction with a Spark cluster over a REST interface. It enables easy submission of Spark jobs or snippets of Spark code, synchronous or asynchronous result retrieval, as well as Spark Context management, all via a simple REST interface or an RPC client library. Apache Livy also simplifies the interaction between Spark and application servers, thus enabling the use of Spark for interactive web/mobile applications. 

![alt Livy Architecture](https://livy.apache.org/assets/images/livy-architecture.png "Livy Architecture")

#### Installing and starting Livy

Download the `Livy` server:

`wget -P ~/livy/ http://apache-mirror.rbc.ru/pub/apache/incubator/livy/0.6.0-incubating/apache-livy-0.6.0-incubating-bin.zip`

Unpack the archive:

`sudo unzip ~/livy/apache-livy-0.6.0-incubating-bin.zip -d /opt`

Modify the `livy.conf` configuration file. The file is located in the `/opt/apache-livy-0.6.0-incubating-bin/conf` directory. Add the following lines that activate the YARN option for the server:

```
# What spark master Livy sessions should use.
livy.spark.master = yarn

# What spark deploy mode Livy sessions should use.
livy.spark.deploy-mode = cluster
```
Run the `Livy` server:

`/opt/apache-livy-0.6.0-incubating-bin/bin/livy-server`


## Job submission using Livy Server


`Livy` Server dashboard default `port`: `8998`

Submit the Spark application

*Request*

`POST http://localhost:8998/batches`

*Body*
```json
{ 
	"className": "edu.classes.spark.WordCount",
	"args": ["/data/yarn/samples_100.json", "/data/yarn/output"], 
	"file": "/data/jars/word-count-java-app-2.0.jar"
}
```

*Response*

```json
{
    "id": 6,
    "name": null,
    "state": "starting",
    "appId": null,
    "appInfo": {
        "driverLogUrl": null,
        "sparkUiUrl": null
    },
    "log": [
        "stdout: ",
        "\nstderr: ",
        "\nYARN Diagnostics: "
    ]
}
```

Getting status

*Request*

`GET http://localhost:8998/batches/6/state`

*Response*

```json
{
    "id": 6,
    "state": "running"
}
```

Getting logs

*Request*

`GET http://localhost:8998/batches/6/log`

*Response*

```json
{
    "id": 6,
    "from": 0,
    "total": 40,
    "log": [
        "stdout: ",
		...
	]
}

```
Check the result using `WebHDFS` REST API (see [docs](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/WebHDFS.html#Create_and_Write_to_a_File))

*Request*

`GET http://localhost:9870/webhdfs/v1/data/yarn/output/?user.name=bigdata&op=LISTSTATUS`

*Response*

```json
{
    "FileStatuses": {
        "FileStatus": [
            {
                "accessTime": 1573077801331,
                "blockSize": 134217728,
                "childrenNum": 0,
                "fileId": 18713,
                "group": "supergroup",
                "length": 0,
                "modificationTime": 1573077801396,
                "owner": "bigdata",
                "pathSuffix": "_SUCCESS",
                "permission": "644",
                "replication": 1,
                "storagePolicy": 0,
                "type": "FILE"
            },
            {
                "accessTime": 1573077800180,
                "blockSize": 134217728,
                "childrenNum": 0,
                "fileId": 18712,
                "group": "supergroup",
                "length": 12923,
                "modificationTime": 1573077800762,
                "owner": "bigdata",
                "pathSuffix": "part-00000",
                "permission": "644",
                "replication": 1,
                "storagePolicy": 0,
                "type": "FILE"
            },
            {
                "accessTime": 1573077800113,
                "blockSize": 134217728,
                "childrenNum": 0,
                "fileId": 18710,
                "group": "supergroup",
                "length": 12453,
                "modificationTime": 1573077800850,
                "owner": "bigdata",
                "pathSuffix": "part-00001",
                "permission": "644",
                "replication": 1,
                "storagePolicy": 0,
                "type": "FILE"
            }
        ]
    }
}
```
Other REST API commands you can find [here](http://livy.incubator.apache.org/docs/latest/rest-api.html).

###

## Jyputer with Sparkmagic

As stated on github webpage of the [`sparkmagic` project](https://github.com/jupyter-incubator/sparkmagic):

> Sparkmagic is a set of tools for interactively working with remote Spark clusters through Livy, a Spark REST server, in Jupyter notebooks. The Sparkmagic project includes a set of magics for interactively running Spark code in multiple languages, as well as some kernels that you can use to turn Jupyter into an integrated Spark environment.

#### Installing Sparkmagic

`pip install sparkmagic` [optional `--user`]

```
Successfully installed autovizwidget-0.13.1 hdijupyterutils-0.13.1 plotly-4.2.1 pykerberos-1.2.1 requests-kerberos-0.12.0 retrying-1.3.3 sparkmagic-0.13.1
```

`/home/bigdata/.sparkmagic/config.json`

```json
{
	"session_configs": {
	    "driverMemory": "1G",
	    "executorCores": 1,
	    "executorMemory": "512M",
	    "proxyUser": "bigdata",
	    "conf": {
            "spark.master": "yarn-cluster",
            "spark.eventLog.enabled": "true",
            "spark.eventLog.dir": "file:///tmp/spark-events"
	    }
	}
}
```

### PySpark Kernel

`pip show sparkmagic`

```
Name: sparkmagic
Version: 0.13.1
Summary: SparkMagic: Spark execution via Livy
Home-page: https://github.com/jupyter-incubator/sparkmagic
Author: Jupyter Development Team
Author-email: jupyter@googlegroups.org
License: BSD 3-clause
Location: /home/bigdata/.local/lib/python3.7/site-packages
Requires: ipython, notebook, mock, requests-kerberos, hdijupyterutils, ipywidgets, numpy, requests, pandas, ipykernel, tornado, nose, autovizwidget
Required-by:
```

`jupyter-kernelspec install sparkmagic/kernels/pysparkkernel` [optional `--user`]

```
[InstallKernelSpec] Installed kernelspec pysparkkernel in /home/bigdata/.local/share/jupyter/kernels/pysparkkernel
```

#### For Python 3

Modify the file below to assign python 3 instead of 2

`/home/bigdata/.local/share/jupyter/kernels/pysparkkernel/pysparkkernel.py`

```python
language_info = {
    'name': 'pyspark',
    'mimetype': 'text/x-python',
    'codemirror_mode': {'name': 'python', 'version': 3},
    'pygments_lexer': 'python3'
}
```

#### Example

```
TODO
```

## Spark Kernel

`jupyter-kernelspec install /home/bigdata/.local/lib/python3.7/site-packages/sparkmagic/kernels/sparkkernel`


#### Example

```
TODO
```

## References

[Configure Livy with Spark Modes](https://mapr.com/docs/61/Hue/Configure_Livy_Spark_Modes.html)

[Apache Livy: Getting Started](https://livy.apache.org/get-started/)

[Submitting Spark Applications Through Livy](https://docs.cloudera.com/HDPDocuments/HDP3/HDP-3.1.4/running-spark-applications/content/submitting_spark_applications_through_livy.html)