package edu.classes.spark.controllers;

import edu.classes.spark.models.Message;
import edu.classes.spark.models.WordCountPair;
import edu.classes.spark.services.WordCountService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.List;

@Controller
public class WordCountServiceController {

    @Autowired
    WordCountService service;

    @ResponseBody
    @RequestMapping(value = "/messages", produces = "application/json", method = RequestMethod.POST)
    ResponseEntity<String> submitMessage(@RequestBody Message message, HttpServletRequest request) {
        service.submitMessage(message);
        return new ResponseEntity<>("Submitted successfully", HttpStatus.OK);
    }

    @ResponseBody
    @GetMapping(value = "/top-words")
    public ResponseEntity<List<WordCountPair>> getTopWords() {
        return new ResponseEntity<>(service.getTopWords(), HttpStatus.OK);
    }

    @GetMapping("/")
    public String index() {
        return "forward:index.html";
    }
}
