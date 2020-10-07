# Word Count of Review Text using Java Spark Application
Sergei Yu. Papulin (papulin_bmstu@mail.ru)

#### [Version 2018](https://nbviewer.jupyter.org/github/BigDataProcSystems/Hadoop/blob/2018/mapreduce_basics.ipynb)

## Contents

- Prerequisites
- Configuration
- Creating Java project in IntelliJ
- Source code in Java
- Running Spark with local files
- Building `jar` file with `maven`
- Running Spark `jar` file on:
    - Local cluster
    - YARN cluster
- References


## Creating Java project in IntelliJ (v2019.2+)

1) Open IntelliJ
2) `Create New Project` on start or `File` -> `Project...`
3) Select Maven and project SDK 1.8 -> `Next`
4) GroupId: `edu.classes.spark`; ArtifactId: `wordcount-review-app` -> `Next`
4) Project name: WordCountReviewSparkApp -> `Finish`


## Datasets

- [Small subset of reviews](https://github.com/BigDataProcSystems/Hadoop/blob/master/data/samples_100.json)
- [Amazon product datasets](http://jmcauley.ucsd.edu/data/amazon/links.html)


## Source code in Java

1. [pom.xml](https://github.com/BigDataProcSystems/Spark_RDD/blob/master/code/java/WordCountReviewApp/pom.xml)
2. [Review model class](https://github.com/BigDataProcSystems/Spark_RDD/blob/master/code/java/WordCountReviewApp/src/main/java/edu/classes/spark/Review.java)
3. [Driver class](https://github.com/BigDataProcSystems/Spark_RDD/blob/master/code/java/WordCountReviewApp/src/main/java/edu/classes/spark/WordCountReviewDriver.java)
4. Test class: `TODO`


### Creating Spark Context


To apply operations over RDD, we have to get or create a Spark Context.

#### Option 1

```java
// Configuration for a Spark application
SparkConf conf = new SparkConf()
        .setMaster(sparkMaster)
        .setAppName(APP_NAME);

// Create a JavaSparkContext that loads settings from system properties
JavaSparkContext sc = new JavaSparkContext(conf);
```

#### Option 2

```java
// Spark Session is provided by a spark-sql package
SparkSession spark = SparkSession
                .builder()
                .master(sparkMaster)
                .appName(APP_NAME)
                .getOrCreate();

JavaSparkContext sc = new JavaSparkContext(spark.sparkContext());
```

### Parsing JSON of Reviews


#### Option 1. Anonymous function

```java
JavaRDD<Review> reviewsRDD = textFileRDD.mapPartitions(records -> {

    Gson gson = new Gson();
    List<Review> reviews = new ArrayList<>();

    // Iterate over records of a RDD partition
    while (records.hasNext()) {
        String item = records.next();
        Review review = gson.fromJson(item, Review.class);
        reviews.add(review);
    }

    return reviews.iterator();
});
```

#### Option 2. Implementing FlatMapFunction interface

```java
/**
 * Implementation of the FlatMapFunction interface for the mapPartitions() methods
 * to deserialize json records.
 *
 */
public static final class ReviewConverterPartitionFunction implements FlatMapFunction<Iterator<String>, Review> {

    /**
     * Convert records of a partition to the Review class
     *
     * @param records   records of a partition
     * @return          records of the Review class
     * @throws Exception
     */
    @Override
    public Iterator<Review> call(Iterator<String> records) throws Exception {

        Gson gson = new Gson();
        List<Review> reviews = new ArrayList<>();

        // Iterate over records of a RDD partition
        while (records.hasNext()) {
            String record = records.next();
            Review review = gson.fromJson(record, Review.class);
            reviews.add(review);
        }

        return reviews.iterator();
    }
}
```

And then apply **ReviewConverterPartitionFunction**:

```java
JavaRDD<Review> reviewsRDD = textFileRDD.mapPartitions(new ReviewConverterPartitionFunction());
```


#### Option 3. Custom serializable class

```java
/**
 * Custom serializable class for json deserialization
 *
 * Inspired by https://stackoverflow.com/a/56626264
 */
public static final class ReviewConverterRDD implements Serializable {

    private transient Gson gson;

    /**
     * Get/create a Gson instance
     *
     * Note: If the variable is not initialized on an executor, the instance will be created.
     * Otherwise the method returns the existing Gson instance.
     *
     * @return  a Gson instance
     */
    private Gson getGsonInstance() {
        if (gson == null) gson = new Gson();
        return gson;
    }

    /**
     * Transform RDD from RDD<String> to RDD<Review>
     *
     * @param rdd   an input rdd with records of the String type
     * @return      a rdd of the Review type
     */
    public JavaRDD<Review> fromJson(JavaRDD<String> rdd) {
        return rdd.map(record -> getGsonInstance().fromJson(record, Review.class));
    }
}
```

Code below shows how to use this class:

```java
ReviewConverterRDD converter = new ReviewConverterRDD();
JavaRDD<Review> reviewsRDD = converter.fromJson(textFileRDD);
```

### Word Count

```java
sc.textFile(args[0])
    .mapPartitions(new ReviewConverterPartitionFunction())
    .flatMap(review -> Arrays.asList(review.getReview().split(SEPARATOR)).iterator())
    .mapToPair(word -> new Tuple2<>(word, 1))
    .reduceByKey((x, y) -> x + y)
    .saveAsTextFile(args[1])
```

## Running application with local files

1) `Run` -> `Edit Configurations...`
2) `Add new configuration...` for Application -> Name: `wordcount`
3) Main class: `edu.classes.spark.WordCountReviewDriver` - (class with the main method)
4) Program arguments: `INPUT_LOCAL_FILE OUTPUT_LOCAL_DIR`, e.g. `data/samples_100.json output` for a local file system
5) Working directory: `/YOUR_LOCAL_PATH/WordCountReviewApp`
6) Environment variable: `SPARK_MASTER=local[2]`
7) `Apply` -> `OK`
8) Comment out the **provided** scope in the pom file for `spark-core_2.11` if you haven't already done so.
9) `Run` -> `Run...` -> Choose your configuration


The output directory looks as follows:

```shell
output
├── part-00000
├── .part-00000.crc
├── part-00001
├── .part-00001.crc
├── _SUCCESS
└── ._SUCCESS.crc
```

First few rows from `part-00000`:
```
(better.,1)
(bone,1)
(charm!,1)
(chair).,1)
(GPS,7)
(price!,1)
(pickup.,2)
(heat,1)
(problem--u,1)
```

## Building `jar` file with `maven`

Add the **provided** scope in the pom file for `spark-core_2.11` (or uncomment it) to exclude spark dependencies from your jar file. 

Go to the maven panel, reload the maven project (if needed), find `Lifecycle` folder -> `package`. After completion, the generated `jar` file will be located in the target directory.

```
target
└── wordcount-review-app-1.0-SNAPSHOT.jar
```

You can build a `jar` file as an artifact as described [here](mapreduce_scala.md).

## Running Spark `jar` file

### Local cluster


Change a working directory:
```
cd target
```

Run the spark application:
```
SPARK_MASTER=local[2] spark-submit \
    wordcount-review-app-1.0-SNAPSHOT.jar \
    file:///YOUR_LOCAL_PATH/samples_100.json \
    file:///YOUR_LOCAL_PATH/output
```

The output directory has the following structure:

```
/YOUR_LOCAL_PATH/output
├── part-00000
├── .part-00000.crc
├── part-00001
├── .part-00001.crc
├── _SUCCESS
└── ._SUCCESS.crc
```


### YARN cluster

#### Starting Hadoop cluster

Run `HDFS`:

`$HADOOP_HOME/sbin/start-dfs.sh`

Run `YARN`:

`$HADOOP_HOME/sbin/start-yarn.sh`

Run the Job History Server:

`mapred --daemon start historyserver`

Or all in one line command:

`$HADOOP_HOME/sbin/start-dfs.sh && $HADOOP_HOME/sbin/start-yarn.sh && mapred --daemon start historyserver`

Check out whether all daemons are running:

`jps`

#### Launching application

Remove the output directory if needed:

`hdfs dfs -rm -r -f /data/yarn/output`

Run the job:

```
SPARK_MASTER=yarn spark-submit \
    wordcount-review-app-1.0-SNAPSHOT.jar \
    /data/yarn/samples_100.json \
    /data/yarn/output
```

Note: It runs the application on YARN using the client mode by default.

Job output:

`hdfs dfs -head /data/yarn/output/part-00000`

```
(better.,1)
(charm!,1)
(chair).,1)
(bone,1)
(price!,1)
(GPS,7)
(pickup.,2)
...
```


