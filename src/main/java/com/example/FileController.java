package com.example;

import java.io.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class FileController {

    public String csvToFile(String csv) {
        List<String> arrayList = Arrays.asList(csv.split(","));

        rawToFile(arrayList.get(0));
	    
        BufferedWriter bw = null;
        FileWriter fw = null;
        String name, data;
        int index;

        try{
            for(int i = 1; i < arrayList.size(); i++) {
                index = arrayList.get(i).indexOf('~');
                if(index != arrayList.get(i).length()-1) {
                    name = arrayList.get(i).substring(0, index);
                    data = arrayList.get(i).substring(index+1, arrayList.get(i).length());
                    File f = new File(name);
                    //f.getParentFile().mkdirs();
                    fw = new FileWriter(f);
                    bw = new BufferedWriter(fw);
                    bw.write(data);
                    bw.close();
                    fw.close();
                }
            }
            return arrayList.get(0);
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
        return "";
    }

    public String fileToCsv(String raw) {
        File[] directories = new File("/app/data/").listFiles(new FileFilter() {
            @Override
            public boolean accept(File file) {
                return file.isDirectory();
            }
        });
	    
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
        StringBuilder sb = new StringBuilder();
        sb.append(raw + ",");

        for(int i = 0; i < names.size(); i++) {
            sb.append(names.get(i) + "~" + data.get(i) + ",");
        }
        return sb.toString().substring(0, sb.toString().length()-1);
    }

  public String readFile(String path, Charset encoding)
            throws IOException
    {
        byte[] encoded = Files.readAllBytes(Paths.get(path));
        return new String(encoded, encoding);
  }

  public void rawToFile(String raw) {
        try {
            PrintWriter writer = new PrintWriter("input.txt", "UTF-8");
            writer.println(raw);
            writer.close();
        } catch (IOException e) {
            // do nothing
        }
  }
	
  public void deleteDirectory(File directory) {
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
        //return(directory.delete());
  }
}
