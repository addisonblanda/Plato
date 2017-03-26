import nltk
import os
import string
import threading
from queue import Queue
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.parse.stanford import StanfordDependencyParser
from rt import RelationTree
from creation import tree_parser
from creation import read_file

# ------------------------------------------------------
# -----              conversion.py                 -----
# ------------------------------------------------------
# handle all pre-processing duties:
# clean and prepare the raw text for writing to file.
# ------------------------------------------------------

nltk.data.path.append(os.getcwd()+"/nltk_data")

V_TYPES = {'VBZ', 'VBD', 'VBN', 'VBP', 'VBG', 'VB'}
POS_TYPES = {'NN', 'JJS', 'NNP', 'JJ', 'VB'}
OBJ_TYPES = {'nsubj', 'dobj'}
DIR_TYPES = {'amod', 'advmod', 'nmod', 'nmod:poss'}

NUM_SIZE = 6
NODE_SIZE = 53
SEEK_NAME = 0
SEEK_ID = 32
SEEK_PID = 38
SEEK_NUM = 44

lock = threading.Lock()
q = queue()

#
# ~~SETUP CORENLP LIBRARY~~
#

java_path = "C:/Program Files/Java/jre1.8.0_101/bin"
os.environ['JAVA_HOME'] = java_path
path_to_jar = 'corenlp/stanford-corenlp-3.7.0.jar'
path_to_models_jar = 'corenlp/stanford-corenlp-3.7.0-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

# ---------------------------
# --- Convert list to str ---
# ---------------------------
def list_to_str(content):
    s = ""
    for word in content:
        if word in string.punctuation:
            s = s.rstrip(' ')
        s += word + ' '
    return s.rstrip(' ')

# ---------------------
# --- Lemmatization ---
# ---------------------
def lemmatize(content):
    my_list = []
    lemmatizer = WordNetLemmatizer()
    words = nltk.word_tokenize(content)
    for word in words:
        my_list.append(lemmatizer.lemmatize(word, 'v'))
    return list_to_str(my_list)

# ---------------------
# --- Validate text ---
# ---------------------
def vs(words):
    for word in words:
        for c in word:
            if not c.isalpha():
                return False
    return True

# -----------------------
# --- Handles threads ---
# -----------------------
def tree_worker():
    while True:
        item = q.get()
        if item:
            tree_parser(lock, item[0], item[1])
        q.task_done()


# -------------------------
# --- Form dependencies ---
# -------------------------
def dep_to_file(s):

    result = dependency_parser.raw_parse(s)
    deps = next(result)

    relations = []
    objectiveRelations = []
    reverseRelations = []
    directModifiers = []
    reverseModifiers = []
    detModifiers = []
    vbModifiers = []

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Step 1: Sort dependencies by category
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    for item in list(deps.triples()):
        w1 = item[0][0]
        w1t = item[0][1]
        w2 = item[2][0]
        w2t = item[2][1]

        if w1t in V_TYPES:
            v1t = "-"+w1t
            w1t = "VB"
        if w2t in V_TYPES:
            v2t = "-"+w2t
            w2t = "VB"
        if item[1] in OBJ_TYPES and w1t in POS_TYPES and w2t in POS_TYPES and vs([w1, w2]):
            relations.append(item[1])
            objectiveRelations.append(item)
        elif item[1] in DIR_TYPES and w1t in POS_TYPES and w2t in POS_TYPES and vs([w1, w2]):
            directModifiers.append(item)
            if w1t == "VB":
                obj = [[w1, w1t], item[1], [(w1 + v1t), w2t]]
                vbModifiers.append(obj)
            elif w2t == "VB":
                obj = [[(w2 + v2t), w1t], item[1], [w2, w2t]]
                vbModifiers.append(obj)
        elif item[1] == "det" and w1t in POS_TYPES and w2t == "DT" and vs([w1, w2]):
            detModifiers.append(item)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Step 2: Create reversed relation pairs
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if 'nsubj' in relations and 'dobj' in relations:
        action = None
        for item in reversed(objectiveRelations):
            if item[1] == 'dobj':
                action = item[2][0]
                temp = [[action, item[2][1]], 'nsubj', [item[0][0], item[0][1]]]
                reverseRelations.append(temp)
            elif item[1] == 'nsubj' and action is not None:
                temp = [[action, item[2][1]], 'dobj', [item[2][0], item[2][1]]]
                reverseRelations.append(temp)

    for item in directModifiers:
        temp = [[item[2][0], item[2][1]], item[1], [item[0][0], item[0][1]]]
        reverseModifiers.append(temp)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Step 3: Create Dependency Trees
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    create_obj_tree(objectiveRelations)
    create_obj_tree(reverseRelations)
    create_mod_tree(directModifiers, "")
    create_mod_tree(reverseModifiers, "")
#    create_mod_tree(detModifiers, "-DET")
#    create_mod_tree(vbModifiers, "-FRM")

    return len(objectiveRelations) + len(reverseRelations) + len(directModifiers) + len(reverseModifiers)

# ----------------------
# ---  Create Child  ---
# ----------------------
def create_mod_tree(directModifiers, mod):
    id = {}
    modTree = []
    mtParent = 0
    accessed = False

    for item in directModifiers:
        subj = lemmatize(item[0][0]).lower()
        dmod = lemmatize(item[2][0]).lower()
        fn = subj + mod + '.txt'
        dir = item[0][1]
        child_tag = item[2][1]
        if dir in V_TYPES: dir = 'VB'
        mtPath = os.getcwd() + '/data/' + dir + '/'
        if subj not in id:
            id[subj] = 1
        if os.path.isfile(mtPath + fn) and not accessed:
            cwd = os.getcwd()
            os.chdir(mtPath)
            id[subj] = int(read_file(fn, SEEK_PID, NUM_SIZE)) + 1
            os.chdir(cwd)
            accessed = True
        mt = RelationTree(dmod, id[subj], mtParent, 1, mtPath, child_tag)
        modTree.append([mt, fn])
        id[subj] += 1

    t = threading.Thread(target=tree_worker)
    t.daemon = True
    t.start()

    if modTree:
        for tree in modTree:
            q.put([tree[0], tree[1]])
    q.join()

# ----------------------
# ---  Create tree  ---
# ---------------------
def create_obj_tree(objectiveRelations):
    cwd = os.getcwd()
    objTree = None
    subjParent = 0
    subjID = 1

    for item in objectiveRelations:

        dobj = lemmatize(item[0][0]).lower()
        subj = lemmatize(item[2][0]).lower()
        dir = item[2][1]
        child_tag = item[0][1]

        if item[1] == 'nsubj' and objTree is None:
            if dir in V_TYPES: dir = 'VB'
            f_name = subj + '.txt'
            otPath = cwd + '/data/' + dir + '/'

            if os.path.isfile(otPath + f_name):
                os.chdir(otPath)
                size = os.stat(f_name).st_size
                exists = False

                for i in range(0, size, NODE_SIZE + 1):
                    res = read_file(f_name, i, SEEK_ID)
                    pid = read_file(f_name, i + SEEK_PID, NUM_SIZE)
                    if res == dobj and pid == 0:
                        subjID = int(read_file(f_name, i + SEEK_ID, NUM_SIZE)) + 1
                        exists = True
                if not exists:
                    subjID = int(read_file(f_name, SEEK_PID, NUM_SIZE)) + 1
                os.chdir(cwd)
            objTree = RelationTree(dobj, subjID, 0, 1, otPath, child_tag)
            subjID += 1
            subjParent += 1

        elif (item[1] == 'dobj' or item[1] == 'case' or item[1] == 'nmod') and objTree is not None:
            if os.path.isfile(otPath + f_name):
                os.chdir(otPath)
                size = os.stat(f_name).st_size
                unique = True

                for i in range(0, size, NODE_SIZE + 1):
                    res = read_file(f_name, i, SEEK_ID)
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    # Case 0: action exists in file already.
                    # if the node is not already one of its children,
                    # it will be appended to the file.
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    if res == dobj:
                        subjParent = int(read_file(f_name, i + SEEK_ID, NUM_SIZE))
                        for j in range(i, size, NODE_SIZE + 1):
                            name = str(read_file(f_name, j, SEEK_ID))
                            child = int(read_file(f_name, j + SEEK_PID, NUM_SIZE))
                            if child == subjParent and name == subj:
                                unique = False
                                break
                        if unique:
                            subjID = int(read_file(f_name, SEEK_PID, NUM_SIZE)) + 1
                            unique = False
                    if unique:
                        subjParent = int(read_file(f_name, SEEK_PID, NUM_SIZE)) + 1
                        subjID = subjParent + 1

                os.chdir(cwd)
            objTree.__add_leaf__(subj, subjID, subjParent, 1, dir)
            subjID += 1
            subjParent += 1

    t = threading.Thread(target=tree_worker)
    t.daemon = True
    t.start()

    if objTree is not None:
        q.put([objTree, f_name])
        for leaf in objTree.leaf:
            q.put([leaf, f_name])
        q.join()
