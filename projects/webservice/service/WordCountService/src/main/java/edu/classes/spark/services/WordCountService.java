package edu.classes.spark.services;

import edu.classes.spark.models.Message;
import edu.classes.spark.models.WordCountPair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class WordCountService implements IWordCountService {

    @Autowired
    private KafkaTemplate<String, Message> kafkaTemplate;

    @Value("${app.topic.wordcount}")
    private String topic;

    private static Integer timestamp;
    private static List<WordCountPair> topWordsCache = new ArrayList<>();

    @Override
    public void submitMessage(Message message) {

        //String[] arr = message.getContent().split(" ");
        //topWordsCache = Arrays.asList(arr).stream().map(x -> new WordCountPair(x, 1)).collect(Collectors.toList());

        kafkaTemplate.send(topic, message);

    }

    @Override
    public List<WordCountPair> getTopWords() {
        return topWordsCache;
    }
}
