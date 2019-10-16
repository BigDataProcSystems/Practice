# Introduction to MapReduce
Sergei Yu. Papulin (papulin_bmstu@mail.ru)

#### [Version 2018](https://github.com/BigDataProcSystems/Hadoop/blob/2018/mapreduce_basics.ipynb)

## Contents

- Prerequisites
- Configuration
- MapReduce configuration
- Starting Hadoop cluster
- Creating Java project in IntelliJ
- Java source code for WordCount example
- Running MapReduce with local files
- Building `jar` file with `maven`
- Running MapReduce `jar` file on YARN cluster
- Applying configuration settings
- References

## Prerequisites

To get started, you need to have done the following:

- Install Ubuntu 14+
- Install Java 8
- Download Hadoop 3+
- Install IntelliJ 2019+ (for Java code)

## Configuration

#### Hadoop directories:

- `hadoop/bin` - hadoop commands
- `hadoop/sbin/` - scripts
- `hadoop/etc/hadoop` - configuration
- `hadoop/logs` - hadoop logs

Previously configured for HDFS and YARN:
- `hadoop/etc/hadoop/hadoop-env.sh`
- `hadoop/etc/hadoop/core-site.xml` ([default values](https://hadoop.apache.org/docs/r3.1.2/hadoop-project-dist/hadoop-common/core-default.xml))
- `hadoop/etc/hadoop/hdfs-site.xml` ([default values](https://hadoop.apache.org/docs/r3.1.2/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml))
- `hadoop/etc/hadoop/yarn-env.sh`
- `hadoop/etc/hadoop/yarn-site.xml` ([default values](https://hadoop.apache.org/docs/r3.1.2/hadoop-yarn/hadoop-yarn-common/yarn-default.xml)) -  configuration parameters
- `hadoop/etc/hadoop/capacity-scheduler.xml`

The configuration files you can find [here](/config/) 

## MapReduce configuration

MapReduce specific configuration files:

- `hadoop/etc/hadoop/mapred-env.sh` - override for `hadoop-env.sh` for all work done by the `mapred` and related commands
- `hadoop/etc/hadoop/mapred-site.xml` ([default values](https://hadoop.apache.org/docs/r3.1.2/hadoop-mapreduce-client/hadoop-mapreduce-client-core/mapred-default.xml)) -  configuration parameters

Precedence rules:

- `mapred-env.sh` > `hadoop-env.sh` > hard-coded defaults
- `MAPRED_xyz` > `HADOOP_xyz` > hard-coded defaults

Set `YARN` as a framework for MapReduce applications

```xml
<property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
    <description>The runtime framework for executing MapReduce jobs.
    Can be one of local, classic or yarn.
    </description>
</property>
```

## Starting Hadoop cluster

Run `HDFS`:

`$HADOOP_HOME/sbin/start-dfs.sh`

Run `YARN`:

`$HADOOP_HOME/sbin/start-yarn.sh`

Run the Job History Server:

`mapred --daemon start historyserver`

Check out whether all daemons are running:

`jps`

## Creating Java project in IntelliJ (v2019.2)

1) Open IntelliJ
2) `Create New Project` on start or `File` -> `Project...`
3) Select Maven and project SDK 1.8 -> `Next`
4) GroupId: `edu.classes.mr`; ArtifactId: `word-count-app` -> `Next`
4) Project name: WordCountApp -> `Finish`

## Java source code for WordCount example

1. [Main class](/code_java/WordCountApp/src/main/java/edu/classes/mr/WordCount.java)

2. [Test class](/code_java/WordCountApp/src/test/java/edu/classes/mr/WordCountTest.java)

3. [pom.xml](/code_java/WordCountApp/pom.xml)

## Running MapReduce with local files

1) `Run` -> `Edit Configurations...`
2) `Add new configuration...` for Application
3) Main class: `edu.classes.mr.WordCount` - (class with the main method)
4) Program arguments: `INPUT_LOCAL_FILE OUTPUT_LOCAL_DIR`
5) `Apply` -> `OK`
6) `Run` -> `Run...` -> Choose your configuration

## Building `jar` file with `maven`

1. Modify `pom.xml` by adding the following maven plugin to `pom.xml`:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-jar-plugin</artifactId>
    <version>3.1.2</version>
    <configuration>
        <archive>
            <addMavenDescriptor>false</addMavenDescriptor>
            <manifest>
                <mainClass>edu.classes.mr.WordCount</mainClass>
            </manifest>
        </archive>
    </configuration>
</plugin>
```

The `mainClass` parameter is necessary to define the entry point for a map-reduce application when you run it with the `yarn jar` command, otherwise you need add a full class path (with a package) directly in command line. 

2. Build `jar` file. Go to the maven panel, find `Plugins` folder -> `jar` -> `jar:jar`. After completion, the actual `jar` file will be located in the target directory.

The `jar` file contains `MANIFEST.MF`, where the main class is defined.

```
Manifest-Version: 1.0
Build-Jdk-Spec: 1.8
Created-By: Maven Archiver 3.4.0
Main-Class: edu.classes.mr.WordCount

```

## Running MapReduce `jar` file on YARN cluster


Command to run `jar` file:

`yarn jar <jar> [mainClass] args... `

For the word count application, the command will be as below:

`yarn jar ./target/word-count-app-1.0.jar -D mapreduce.job.reduces=2 /data/yarn/reviews_Electronics_5_2.json /data/yarn/output`

Remove the output directory if needed:

`hdfs dfs -rm -r -f /data/yarn/output`


## Applying configuration settings

### Priority

1. `yarn jar` command line settings: 

```cmd
-D mapreduce.job.reduces=2
```

2. In Java code settings: 

```java
job.setNumReduceTasks(2);
```

3. `yarn-site.xml` and `mapred-site.xml`: 

```xml
<property>
  <name>mapreduce.job.reduces</name>
  <value>1</value>
  <description>The default number of reduce tasks per job. Typically set to 99%
  of the cluster's reduce capacity, so that if a node fails the reduces can
  still be executed in a single wave.
  Ignored when mapreduce.framework.name is "local".
  </description>
</property>
```

## References

