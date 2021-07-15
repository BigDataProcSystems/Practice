# MapReduce and Scala
Sergei Yu. Papulin (papulin_bmstu@mail.ru)

## Contents

- Prerequisites
- Configuration
- Installing `Scala` plugin for `IntelliJ`
- Creating `Scala` project
- Sample source code
- Running MapReduce with local files
- Building `jar` file
- Running MapReduce `jar` file on YARN cluster
- References

## Prerequisites

To get started, you need to have done the following:

- Install Ubuntu 14+ (with Python 3.x)
- Install Java 8
- Download Hadoop 3+
- Install IntelliJ 2019+ (for Scala code)
- (Optional) Install PyCharm 2019+ (for Python code)


## Installing `Scala` plugin for `IntelliJ`

`File` -> `Settings` -> `Plugins` -> Find the `Scala` plugin from `JetBrains` -> Click on `Install` -> Restart IDE

## Creating `Scala` project

`File` -> `New` -> `Project...` -> `Scala` with `sbt` -> Next ->  Name: `WordCountApp` - > Finish

Project structure:
```
App --> src --> main --> scala/
    |       |
    |       --> test --> scala/
    |    
    --> build.sbt

```


## Sample `source code`

[WordCount.scala](/code_scala/WordCountApp/src/main/scala/edu/classes/mr/WordCount.scala)

[build.sbt](/code_scala/WordCountApp/build.sbt)

## Running MapReduce with local files

1) `Run` -> `Edit Configurations...`
2) `Add new configuration...` for Application
3) Set the following configuration:
- Main class: `edu.classes.mr.WordCount` - (class with the main method)
- Program arguments: `INPUT_LOCAL_FILE OUTPUT_LOCAL_DIR`
- Use classpath of module: `WordCountApp`
- others by default

5) `Apply` -> `OK`
6) `Run` -> `Run...` -> Choose your configuration

## Building `jar` file

1. `File` -> `Project Structure...` -> `Artifacts`
2. `Add` -> `JAR` -> `Empty`
3. Rename the artifact to `word-count-scala-app`
4. Change the output directory to `/FULL_PATH/WordCountApp/target`
5. Click on the `root jar` (`word-count-scala-app.jar`) and below click on `Create Manifest...`
6. Select the `/FULL_PATH/WordCountApp/src/main/scala` directory -> OK
7. Main class: `edu.classes.mr.WordCount`
8. Add `WordCountApp` to `jar` from `Available Elements`
9. Extract `sbt:org.scala-lang:scala-library:2.13.1:jar` into `jar` (you have to extract, not to put this `jar` inside the `root jar`)
10. `Apply` -> `OK`
11. `Build` -> `Build artifacts...` -> `word-count-scala-app` -> build

If everything has been done correctly, you will see the `jar` file in the `target` directory of your project.

## Running MapReduce `jar` file on YARN cluster

#### Starting Hadoop cluster

Run `HDFS`:

`$HADOOP_HOME/sbin/start-dfs.sh`

Run `YARN`:

`$HADOOP_HOME/sbin/start-yarn.sh`

Run the Job History Server:

`mapred --daemon start historyserver`

Check out whether all daemons are running:

`jps`

#### Running `jar`

Run the application by the command below:

`yarn jar ./target/word-count-scala-app.jar /data/yarn/reviews_Electronics_5_2.json /data/yarn/output`

Remove the output directory if needed:

`hdfs dfs -rm -r -f /data/yarn/output`

## References