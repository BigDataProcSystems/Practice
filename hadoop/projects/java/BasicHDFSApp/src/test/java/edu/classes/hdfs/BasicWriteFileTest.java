package edu.classes.hdfs;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.net.URI;

class BasicWriteFileTest {

    private static Configuration conf;

    @BeforeAll
    static void setUp() {
        // Get configuration instance
        conf = BasicWriteFile.setupHDFSConfiguration();
    }

    @Test
    void copyLocalFileToHDFS_Success() throws Exception {

        final String local = "/media/sf_Hadoop/data/samples_100.json";
        final String hdfs = "/examples/tests/hadoop/basicwritefile/sample_100_copy.json";

        Path hdfsPath = new Path(hdfs);

        // Get file system instance
        FileSystem fs = FileSystem.get(URI.create(hdfs), conf);

        // Check existence
        assertFalse(fs.exists(hdfsPath));

        BasicWriteFile.main(new String[]{local, hdfs});

        // Check existence
        assertTrue(fs.exists(hdfsPath));

        // Remove directory
        fs.delete(hdfsPath, true);

        // Check existence
        assertFalse(fs.exists(hdfsPath));

    }




}
