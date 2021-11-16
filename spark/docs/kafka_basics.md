# Introduction to Kafka distributed message broker
Sergei Yu. Papulin (papulin_bmstu@mail.ru)

## Contents

- Prerequisites
- Zookeeper installation
- Kafka installation
- Configuring Kafka
- Running Kafka
- Creating topic
- Testing with Console Producer and Consumer
- Quick commands to start

## Prerequisites

To get started, you need to have done the following:

- Install Ubuntu 14+
- Install Java 8

## Zookeeper installation

Install the server:

`apt install zookeeperd`

Display a version of the server:

`echo stat | nc localhost 2181`

```
Zookeeper version: 3.4.5--1, built on 06/10/2013 17:26 GMT
Clients:
 /127.0.0.1:57312[0](queued=0,recved=1,sent=0)
```

After the installation the `Zookeeper` server will be started automatically. You can manually start/stop the server by the following commands:

`$ZOOKEEPER_HOME/bin/zkServer.sh start | stop`

## Kafka installation

Create a directory where the `Kafka` will be placed:

`mkdir /opt/kafka`

Download a `Kafka` archive:

`wget -P ~/Downloads/ http://apache-mirror.rbc.ru/pub/apache/kafka/2.3.0/kafka_2.11-2.3.0.tgz`

Here we use `Kafka` with `Scala` `2.11` that corresponds to the `Scala` version of our `Spark` installation.

Unpack the archive: 

`tar -xvzf ~/Downloads/kafka_2.11-2.3.0.tgz --directory /opt/kafka --strip-components 1`

## Configuring `Kafka`

#### Kafka directories:

- `kafka/bin/` - kafka commands
- `kafka/config/` - configuration
- `kafka/logs/` - kafka logs

#### Configuration

`server.properties`

```bash
# The id of the broker. This must be set to a unique integer for each broker.
broker.id=0

# Zookeeper connection string (see zookeeper docs for details).
# This is a comma separated host:port pairs, each corresponding to a zk
# server. e.g. "127.0.0.1:3000,127.0.0.1:3001,127.0.0.1:3002".
# You can also append an optional chroot string to the urls to specify the
# root directory for all kafka znodes.
zookeeper.connect=localhost:2181

# The default number of log partitions per topic. More partitions allow greater
# parallelism for consumption, but this will also result in more files across
# the brokers.
num.partitions=1

# A comma separated list of directories under which to store log files
log.dirs=/opt/kafka/logs/data
```

## Running `Kafka`

Start the `kafka` server:

`$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties`

## Creating topic

`$KAFKA_HOME/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --topic word-count`

```
Created topic word-count.
```

`sudo $ZOOKEEPER_HOME/bin/zkCli.sh`

```
Welcome to ZooKeeper!
JLine support is enabled
[zk: localhost:2181(CONNECTING) 0] 
```

`get /brokers/ids/0`

```
{"listener_security_protocol_map":{"PLAINTEXT":"PLAINTEXT"},"endpoints":["PLAINTEXT://bigdata-VirtualBox:9092"],"jmx_port":-1,"host":"bigdata-VirtualBox","timestamp":"1572980758106","port":9092,"version":4}
cZxid = 0xdd
ctime = Tue Nov 05 22:05:58 MSK 2019
mZxid = 0xdd
mtime = Tue Nov 05 22:05:58 MSK 2019
pZxid = 0xdd
cversion = 0
dataVersion = 1
aclVersion = 0
ephemeralOwner = 0x16e3c184ad30001
dataLength = 206
numChildren = 0
```

`quit`


## Testing with Console Producer and Consumer

Open a new terminal window and run the following command to start the `Kafka` Console Consumer:

`$KAFKA_HOME/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic word-count --from-beginning`

In another terminal window run the `Kafka` Console Producer:

`$KAFKA_HOME/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic word-count`

Enter some text in the producer console, and apply it. In the Consumer console you should see the text that you applied in the producer:

## Quick commands to start

Start the `Zookeeper` Server:

`sudo $ZOOKEEPER_HOME/bin/zkServer.sh start`

Start the `Kafka` server:

`sudo $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties`

In one line:
`$ZOOKEEPER_HOME/bin/zkServer.sh start & $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties`