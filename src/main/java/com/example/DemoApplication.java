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
	
  private static void datumToFile(Datum datum) {
        String[] names = datum.names;
        String[] data = datum.data;
        
        if(names.length != data.length) {
            System.err.print("Name must match length!");
        }

        int len = names.length;
        BufferedWriter bw = null;
        FileWriter fw = null;

        try{
            for(int i = 0; i < len; i++) {
                if(!data[i].equals("")) {
                    File f = new File(names[i]);
                    f.getParentFile().mkdirs();
                    fw = new FileWriter(f);
                    bw = new BufferedWriter(fw);
                    bw.write(data[i]);
                    bw.close();
                    fw.close();
                }
            }
        } catch (IOException e) {

            e.printStackTrace();

        } finally {

            try {

                if (bw != null)
                    bw.close();

                if (fw != null)
                    fw.close();

            } catch (IOException ex) {

                ex.printStackTrace();

            }

        }
    }

  private static Datum fileToDatum(String raw) {
        File[] directories = new File("data/").listFiles(new FileFilter() {
            @Override
            public boolean accept(File file) {
                return file.isDirectory();
            }
        });

        assert directories != null;

        List<String> names = new ArrayList<String>();
        List<String> data = new ArrayList<String>();

        for (File directory : directories) {
            File[] files = new File(directory.toString()).listFiles();
            assert files != null;
            for (File f : files) {
                try {
                    String s = readFile(f.toString(), StandardCharsets.UTF_8);
                    names.add(f.toString());
                    data.add(s);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return new Datum(raw, names.toArray(new String[0]), data.toArray(new String[0]));
  }

  private static String readFile(String path, Charset encoding)
            throws IOException
    {
        byte[] encoded = Files.readAllBytes(Paths.get(path));
        return new String(encoded, encoding);
  }

  private static void rawToFile(String raw) {
        try {
            PrintWriter writer = new PrintWriter("input.txt", "UTF-8");
            writer.println(raw);
            writer.close();
        } catch (IOException e) {
            // do nothing
        }
  }
	
  private static boolean deleteDirectory(File directory) {
        if(directory.exists()){
            File[] files = directory.listFiles();
            if(null!=files){
                for(int i=0; i<files.length; i++) {
                    if(files[i].isDirectory()) {
                        deleteDirectory(files[i]);
                    }
                    else {
                        files[i].delete();
                    }
                }
            }
        }
        return(directory.delete());
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
	/*
  @RequestMapping(value = "/datum", method = RequestMethod.POST)
  @ResponseBody
    public String get(@RequestBody String id) {
        //datumToFile(datum);
        //rawToFile(datum.raw);
        //runpy();
        //Datum response = fileToDatum(datum.raw);
	//deleteDirectory(new File("data"));
	return id + " friend";
  }
  */
	
  @RequestMapping(value = "/{id}", method = RequestMethod.GET)
  @ResponseBody
  public String get(@PathVariable("id") String[] id) {
	  return id + " ok!";
  }

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }
}
