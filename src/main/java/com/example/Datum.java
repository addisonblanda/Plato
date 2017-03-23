package com.example;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
public class Datum {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    public String raw;
    public String[] names;
    public String[] data;

    public Datum(String raw, String[] names, String[] data) {
        this.raw = raw;
        this.names = names;
        this.data = data;
    }
}
