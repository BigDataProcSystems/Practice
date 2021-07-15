# Sorted ratings with Partitioner, SortComparator and GroupingComparator
Sergei Yu. Papulin (papulin.study@mail.ru)

## Contents

- Prerequisites
- Configuration
- Creating Java project in IntelliJ
- Source code in Java
- Partitioning and sorting by custom key
- Grouping by custom key

## Prerequisites

To get started, you need to have done the following:

- Install Ubuntu 14+
- Install Java 8
- Download Hadoop 3+
- Install IntelliJ 2019+ (for Java code)

## Configuration

See [Introduction to MapReduce](mapreduce_basics.md)

## Creating Java project in IntelliJ (v2019.2)

1) Open IntelliJ
2) `Create New Project` on start or `File` -> `Project...`
3) Select Maven and project SDK 1.8 -> `Next`
4) GroupId: `edu.classes.mr`; ArtifactId: `sorted-rating-app` -> `Next`
4) Project name: SortedRatingApp -> `Finish`

## Source code in Java

1. [pom.xml](/code_java/SortedRatingApp/pom.xml)
2. [Review model class](/code_java/SortedRatingApp/src/main/java/edu/classes/mr/Review.java)
3. [Custom writable class](/code_java/SortedRatingApp/src/main/java/edu/classes/mr/RatingKeyWritable.java)
4. [Enum for json parsing result](/code_java/SortedRatingApp/src/main/java/edu/classes/mr/ReviewState.java)
5. [Driver class](/code_java/SortedRatingApp/src/main/java/edu/classes/mr/SortedRatingDriver.java)
6. [Mapper class](/code_java/SortedRatingApp/src/main/java/edu/classes/mr/SortedRatingMapper.java)
7. [Reducer class](/code_java/SortedRatingApp/src/main/java/edu/classes/mr/SortedRatingReducer.java)
8. Test class: `TODO`

## Partitioning and sorting by custom key

#### SortComparator

```java
/**
* Define the comparator that controls how the keys are sorted before they
* are passed to the Reducer.
*
* Sorting by product ids and then by ratings
*
*/
public static class SortComparator extends WritableComparator {

    protected SortComparator() {
        super(RatingKeyWritable.class, true);
    }

}
```

#### WritableComparable

```java
public class RatingKeyWritable implements WritableComparable<RatingKeyWritable> {

    // Code before

    @Override
    public int compareTo(RatingKeyWritable ratingKeyWritable) {
        int cmp = productId.compareTo(ratingKeyWritable.productId);
        if (cmp != 0) return cmp;
        return rating.compareTo(ratingKeyWritable.rating);
    }

    // Code after
}

```

#### KeyPartitioner

```java
/**
* The total number of partitions is the same as the number of reduce tasks for the job. Hence this controls
* which of the reduce tasks the intermediate key (and hence the record) is sent for reduction.
*
* In this case the Partitioner class is used to shuffle map outputs to reducers by product ids.
* That means all products with the same id will be passed to an identical reducer
*
* Note: A Partitioner is created only when there are multiple reducers.
*
*/
public static class KeyPartitioner extends Partitioner<RatingKeyWritable, IntWritable> {

    @Override
    public int getPartition(RatingKeyWritable ratingKeyWritable, IntWritable intWritable, int numPartitions) {
        return Math.abs(ratingKeyWritable.getProductId().hashCode() % numPartitions);
    }
}

```

#### Applying SortComparator and KeyPartitioner in Driver

```java
public class SortedRatingDriver extends Configured implements Tool {

    public int run(String[] args) throws Exception {

        Job job = Job.getInstance(getConf(), "SortedRatingApp");
        
        // Code before

        job.setPartitionerClass(RatingKeyWritable.KeyPartitioner.class);
        job.setSortComparatorClass(RatingKeyWritable.SortComparator.class);

        // Code after
    }
}
```

#### Output

Structure of output:

1. `product id` 
2. `sorted rating` 
3. `count` (a total number of reviews for a given product id and rating)

```
0528881469	1.0	2
0528881469	2.0	1
0528881469	3.0	1
0528881469	5.0	1
0594451647	2.0	1
0594451647	4.0	1
0594451647	5.0	3
0594481813	3.0	3
0594481813	4.0	2
0594481813	5.0	3
0972683275	1.0	2
0972683275	2.0	1
0972683275	3.0	6
0972683275	4.0	27
0972683275	5.0	46
```


## Grouping by custom key

#### GroupComparator

```java
/**
 * Grouping class defines the comparator that controls which keys are grouped together
 *
 */
public static class GroupComparator extends WritableComparator {

    protected GroupComparator() {
        super(RatingKeyWritable.class, true);
    }

    @Override
    public int compare(WritableComparable a, WritableComparable b) {
        RatingKeyWritable r1 = (RatingKeyWritable) a;
        RatingKeyWritable r2 = (RatingKeyWritable) b;
        return r1.getProductId().compareTo(r2.getProductId());
    }

}
```

#### Applying GroupComparator in Driver

```java
public class SortedRatingDriver extends Configured implements Tool {

    public int run(String[] args) throws Exception {

        Job job = Job.getInstance(getConf(), "SortedRatingApp");
        
        // Code before

        job.setPartitionerClass(RatingKeyWritable.KeyPartitioner.class);
        job.setSortComparatorClass(RatingKeyWritable.SortComparator.class);
        job.setGroupingComparatorClass(RatingKeyWritable.GroupComparator.class);

        // Code after
    }
}
```

#### Output

Structure of output:

1. `product id` 
2. `max rating` (grouped)
3. `count` (a total number of reviews for a given product id)


```
0528881469	5.0	5
0594451647	5.0	5
0594481813	5.0	8
0972683275	5.0	82
```