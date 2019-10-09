# Introduction to YARN
Sergei Yu. Papulin (papulin_bmstu@mail.ru)


## Configuration files

#### Basic files to configure

Previously configured for HDFS:
- `hadoop/etc/hadoop/hadoop-env.sh`
- `hadoop/etc/hadoop/core-site.xml` ([default values](https://hadoop.apache.org/docs/r3.1.2/hadoop-project-dist/hadoop-common/core-default.xml))
- `hadoop/etc/hadoop/hdfs-site.xml` ([default values](https://hadoop.apache.org/docs/r3.1.2/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml))


YARN specific configuration files:

- `hadoop/etc/hadoop/yarn-env.sh` - environment variables used for YARN daemons and running YARN commands
- `hadoop/etc/hadoop/yarn-site.xml` ([default values](https://hadoop.apache.org/docs/r3.1.2/hadoop-yarn/hadoop-yarn-common/yarn-default.xml)) -  configuration parameters
- `hadoop/etc/hadoop/capacity-scheduler.xml` - the configuration file for the `CapacityScheduler` option

Precedence rules:

`yarn-env.sh` > `hadoop-env.sh` > hard-coded defaults

`YARN_xyz` > `HADOOP_xyz` > hard-coded defaults


### Memory allocation and vcores

NodeManager memory

Container memory


## Scheduler

### Capacity scheduler

To configure the capacity scheduler, edit the `capacity-scheduler.xml` file in the configuration directory of Hadoop 

### Queue hierarchy

Queue/sub-queue | Capacity | Maximum capacity
--- | --- | ---
mrapp | 90% | 100%
mrapp.dev | 80% | -
mrapp.prod | 20% | -
sparkapp | 5% | 10%
default | 5% | 10%

### 

To specify a queue to use you can directly write rules in `capacity-scheduler.xml`.

Syntax: [u or g]:[name]:[queue_name][,next_mapping]*. 

Example,

```xml
<property>
    <name>yarn.scheduler.capacity.queue-mappings</name>
    <value>g:bigdata:dev</value>
</property>
<property>
    <name>yarn.scheduler.queue-placement-rules.app-name</name>
    <value>wordCountMRApp:prod</value>
</property>
```

### Refreshing queue configuration

To edit by file, you need to edit `capacity-scheduler.xml` and run `yarn rmadmin -refreshQueues`.

`$HADOOP_HOME/bin/yarn rmadmin -refreshQueues`


Deleting queue via file
<div style="margin-left: 2rem;">
Step 1: Stop the queue

Step 2: Delete the queue

Step 3: Run `yarn rmadmin -refreshQueues`
</div>

### Others



[Hadoop: Capacity Scheduler](https://hadoop.apache.org/docs/r3.1.2/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html)


## Run applications

For a single node cluster, tasks can fail due to resource scarcity. In this case you have to disable memory check. Change `yarn-site.xml` by adding the following strings:

```xml
<property>
    <name>yarn.nodemanager.pmem-check-enabled</name>
    <value>false</value>
</property>
<property>
    <name>yarn.nodemanager.vmem-check-enabled</name>
    <value>false</value>
</property>
```

### Download and unpack dataset

`mkdir -p ~/datasets/reviews`

`wget -P ~/datasets/reviews/ http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Electronics_5.json.gz`

`gzip -dk ~/datasets/reviews/reviews_Electronics_5.json.gz`

### Run HDFS and YARN

`$HADOOP_HOME/sbin/start-dfs.sh`

`$HADOOP_HOME/sbin/start-yarn.sh`

`$HADOOP_HOME/bin/mapred --daemon start historyserver`

`jps`

### Run application

`hdfs dfs -rm -r -f /data/yarn/output`

`yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar wordcount -D mapreduce.job.reduces=2 /data/yarn/reviews_Electronics_5.json /data/yarn/output`
