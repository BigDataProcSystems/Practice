# Introduction to HDFS
### Sergei Yu. Papulin (papulin_bmstu@mail.ru)

#### [Version 2018](https://github.com/BigDataProcSystems/Hadoop/blob/2018/hdfs_basics.ipynb)

## Contents

- HDFS Shell Commands
- HDFS Java API
    - Reading Files
    - Copying Files From Local To HDFS
    - Other manipulations
- Running on Cloudera
- HDFS on EMR Cluster
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

#### Basic files to configure:

- `hadoop/etc/hadoop/hadoop-env.sh`
- `hadoop/etc/hadoop/core-site.xml` ([default values](https://hadoop.apache.org/docs/r3.1.2/hadoop-project-dist/hadoop-common/core-default.xml))
- `hadoop/etc/hadoop/hdfs-site.xml` ([default values](https://hadoop.apache.org/docs/r3.1.2/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml))

#### Configure logs systems

- `hadoop/logs/`

#### HDFS dashboard

`http://localhost:9870`

## HDFS Shell Commands

- [HDFS Commands Guide](https://hadoop.apache.org/docs/r3.1.2/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html)

- [File System Shell Guide](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/FileSystemShell.html)

Create a directory

`hdfs dfs -mkdir /data`

Copy a local file to HDFS

`hdfs dfs -copyFromLocal LOCAL_FILE /data`

Change file permissions

`hdfs dfs -chmod 600 /data/file`

Display basic filesystem information and statistics

`hdfs dfsadmin -report`

Show HDFS topology

`hdfs dfsadmin -printTopology`

Print out locations for every block

`hdfs fsck /myfile.txt -files -blocks -locations`

Remove a directory recursively

`hdfs dfs -rm -r /data`


## HDFS Java API

### Create Java project in IntelliJ (v2019.2)

1) Open IntelliJ
2) `Create New Project` on start or `File` -> `Project...`

#### Main option 
Maven project

3) Select Maven and project SDK 1.8 -> `Next`
4) GroupId: `edu.classes.hdfs`; ArtifactId: `basic-hdfs-app` -> `Next`
4) Project name: BasicHDFSApp -> `Finish`

Project structure:
```
src --> main/
    |
    +-> test/
    |
    --> pom.xml
```

#### Alternative way
Common Java project

3) Select Java and project SDK 1.8 -> `Next` -> `Next`
4) Project name: `BasicHDFSApp` -> `Finish`
5) Click the right mouse button on `BasicHDFSApp` in the project structure panel and choose `Add framework support...`
6) Select `Maven` -> `OK` 
7) In emerged message box click `Import changes`

### Add dependencies to `pom.xml`
```
    <dependencies>
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-client</artifactId>
            <version>3.1.0</version>
        </dependency>
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-common</artifactId>
            <version>3.1.0</version>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>RELEASE</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
```

### Attach HDFS source code

1) Download the Hadoop source code ([here Hadoop 3.1.0](https://archive.apache.org/dist/hadoop/core/hadoop-3.1.0/))
2) Extract the archive
3) `File` -> `Project structure` -> Select `Libraries`
4) Find `org.apache.hadoop:hadoop-common:3.1.0` -> Remove `Source` -> Add `Source`: `HADOOP_SOURCE_DIR/hadoop-common-project/hadoop-common` -> `OK` -> Select `src/main/java` -> `OK` -> `Apply` and `OK`

### Run and Debug

1) `Run` -> `Edit Configurations...`
2) `Add new configuration...` for Application
3) Main class: `edu.classes.hdfs.BasicWriteFile` - (class with the main method)
4) Program arguments: `INPUT_LOCAL_FILE OUTPUT_HDFS_FILE`
5) `Apply` -> `OK`
6) `Run` -> `Run...` -> Choose your configuration


### Create `jar`

1) `File` -> `Project Structure` -> Select `Artifacts` -> `Add` -> Select `Jar`
2) `Apply` -> `OK`
3) `Build` -> `Build Artifacts...`


### Run `jar`

`
hadoop jar ReadFileApp.jar edu.classes.hdfs.BasicReadFile hdfs://localhost:9000/FULL_FILE_PATH_TO_READ
`

## Running on Docker cluster

See

- Coming soon

## Running on AWS using Cloudera

See 

1. [HOWTO_Cloudera: configure Hadoop](https://github.com/BigDataProcSystems/HOWTO_Cloudera/blob/master/config_hadoop.ipynb)

2. [HOWTO_AWS: deploy Cloudera cluster](https://github.com/BigDataProcSystems/HOWTO_AWS/blob/master/deploy_cloudera_cluster.ipynb)

## HDFS on EMR Cluster

See

- [Hadoop Configuration on Amazon EMR cluster](https://github.com/BigDataProcSystems/HOWTO_AWS/blob/master/config_aws_emr_hadoop.ipynb)

## References
