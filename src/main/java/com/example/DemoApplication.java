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
        try {
	     // run the Unix "ls" command
            // using the Runtime exec method:
            Process p = Runtime.getRuntime().exec("ls");
            
            BufferedReader stdInput = new BufferedReader(new 
                 InputStreamReader(p.getInputStream()));

            BufferedReader stdError = new BufferedReader(new 
                 InputStreamReader(p.getErrorStream()));

            // read the output from the command
            String s = "";
	    String str = "";
            while ((s = stdInput.readLine()) != null) {
                str += s;
            }     
            return str;
        }
        catch (IOException e) {
            // do nothing
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
  public @ResponseBody String get(@PathVariable("id") String id) {
    String str = "Hello there " + id + "!";
    return str + runpy();
  }

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }
}
