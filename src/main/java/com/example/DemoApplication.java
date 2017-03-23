package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.*;

import java.io.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

@RestController
@SpringBootApplication
public class DemoApplication {
  
  private static String runpy() {
        try {
	     // run the Unix "ls" command
            // using the Runtime exec method:
            Process p = Runtime.getRuntime().exec("python information.py");
            
            BufferedReader stdInput = new BufferedReader(new 
                 InputStreamReader(p.getInputStream()));

            // read the output from the command
            String s;
	    StringBuilder sb = new StringBuilder();
            while ((s = stdInput.readLine()) != null) {
                sb.append(s);
            }     
            return sb.toString();
        }
        catch (IOException e) {
            e.printStackTrace();
	    return "";
        }
  }

  @RequestMapping("/")
  @ResponseBody
  String home() {
    return "Hello! This is a demo application linked to this tutorial: http://jkutner.github.io/2016/08/18/android-backend-api-heroku-retrofit.html";
  }

  @RequestMapping("/hello")
  @ResponseBody
  String hello() {
    return "Hello from Heroku!";
  }

  @RequestMapping(value = "/{id}", method = RequestMethod.GET)
  @ResponseBody
  public String get(@PathVariable("id") String[] id) {
	  return id + " ok!";
  }

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }
}
