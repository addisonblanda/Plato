package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.*;

import java.io.*;

@RestController
@SpringBootApplication
public class DemoApplication {
  
    private static String runpy() {
        try {
            //
            Process p = Runtime.getRuntime().exec("python information.py");

            BufferedReader stdInput = new BufferedReader(new
                    InputStreamReader(p.getInputStream()));
		
	    BufferedReader stdError = new BufferedReader(new 
     		    InputStreamReader(p.getErrorStream()));

            // read the output from the command
            String s;
            StringBuilder sb = new StringBuilder();
            while ((s = stdInput.readLine()) != null) {
                sb.append(s);
            }
	    while ((s = stdError.readLine()) != null) {
		sb.append(s);
	    }
            return sb.toString();
        }
        catch (IOException e) {
            return "Python exception...";
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
  public String get(@PathVariable("id") String id) {
	  id = id.replaceAll("%20", " ");
	  id = id.replaceAll("%3F", "/");
	  id = id.replace("!", "\n");
	  id = id.replace("?", "/");
	  FileController fc = new FileController();
	  String raw = fc.csvToFile(id);
	  runpy();
	  String response = fc.fileToCsv(raw);
	  fc.deleteDirectory(new File("data"));
	  return response;
  }

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }
}
