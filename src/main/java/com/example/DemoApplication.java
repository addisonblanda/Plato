package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.*;

import java.io.BufferedReader;
import java.io.InputStreamReader;

@Controller
@SpringBootApplication
public class DemoApplication {
  
  public String runpy() {
    Runtime rt = Runtime.getRuntime();
    String[] commands = {"ls"};
    Process proc = rt.exec(commands);

    BufferedReader stdInput = new BufferedReader(new 
        InputStreamReader(proc.getInputStream()));

    BufferedReader stdError = new BufferedReader(new 
        InputStreamReader(proc.getErrorStream()));

    // read the output from the command
    String s = null;
    while ((s = stdInput.readLine()) != null) {
       System.out.println(s);
    }

    // read any errors from the attempted command
    String str = "";
    while ((s = stdError.readLine()) != null) {
        str += s;
    } 
    return str;
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
  public @ResponseBody String get(@PathVariable("id") String id) {
    String str = "Hello there " + id + "!";
    return str + runpy();
  }

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }
}
