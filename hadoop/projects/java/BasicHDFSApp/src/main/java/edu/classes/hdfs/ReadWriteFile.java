package edu.classes.hdfs;

import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

import java.util.logging.Logger;

public class ReadWriteFile {

    private final static Logger LOGGER = Logger.getGlobal();

    private FileSystem fs;

    public ReadWriteFile(FileSystem fs) {
        this.fs = fs;
    }

    public void displayFileContent(Path filePath) {

        // TODO: check file existence

        // TODO: write file content output to the console

    }

    public void copyFromLocalToHDFS(Path srcFilePath, Path dstFilePath) {

        // TODO: write local file to HDFS

    }

}