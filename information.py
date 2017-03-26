import datetime
import os
import sys
import time
import nltk
import conversion

nltk.data.path.append(os.getcwd()+"/nltk_data")

NUM_MAX = 999999
NUM_SIZE = 6
NODE_SIZE = 53
SEEK_NAME = 0
SEEK_ID = 32
SEEK_PID = 38
SEEK_NUM = 44
SEEK_TAG = 50
TAG_SIZE = 3

# -------------------------------------------------------
# -----              information.py                 -----
# -------------------------------------------------------
# retrieve the proper file and open it for processing
# ------------------------------------------------------

LEN = 500


# -----------------------------------------------------
# --- Open file and return a string of the contents ---
# -----------------------------------------------------
def file_opener(file_name):
    s = ""
    try:
        with open(file_name) as f:
            content = f.read()
            for word in content:
                if word is not '\n':
                    s += word
                else:
                    s += ' '
        f.close
        return s
    except:
        print("No such file exists!")
        sys.exit()


# ----------------------------------
# --- Log the progress of the fs ---
# ----------------------------------
def log(file, start, end, additions):
    fn = "log.txt"
    with open(fn, "a") as f:
        f.write(file + ": " + "\nstart: " + start + " end: " + end + "\nadditions: " + str(additions) + "\n")

print("processing...")
file = "input.txt"

s = file_opener(file)

sd = nltk.data.load('tokenizers/punkt/english.pickle')
sentences = sd.tokenize(s)

count = 0
size = len(sentences)

for sentence in sentences:
    if len(sentence) < LEN:
        conversion.dep_to_file(sentence)


