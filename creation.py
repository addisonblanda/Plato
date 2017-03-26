import os
from rt import RelationTree

# ------------------------------------------------------
# -----               creation.py                   ----
# ------------------------------------------------------
# handle all post-processing duties:
# creates or appends file from dep tree
# ------------------------------------------------------


NUM_MAX = 999999
NUM_SIZE = 6
NODE_SIZE = 53
SEEK_NAME = 0
SEEK_ID = 32
SEEK_PID = 38
SEEK_NUM = 44
SEEK_TAG = 50
TAG_SIZE = 3

# ----------------------
# --- Read from file ---
# ----------------------
def read_file(fn, pos, size):
    with open(fn, 'ab+') as f:
        f.seek(pos, 0)
        s = str(bytes.decode(f.read(size)))
    return s.rstrip(' ')

# --------------------------
# --- Create/append file ---
# --------------------------
def create_file(fn, tree):
    with open(fn, 'ab+') as f:
        f.seek(SEEK_NAME, 1)
        f.write(str.encode(tree.name))
        f.seek(SEEK_ID, 1)
        f.write(str.encode(str(tree.id)))
        f.seek(SEEK_PID, 1)
        f.write(str.encode(str(tree.parent)))
        f.seek(SEEK_NUM, 1)
        f.write(str.encode(str(tree.num)))
        f.seek(SEEK_TAG, 1)
        f.write(str.encode(tree.tag))
        f.write(str.encode('\n'))



# -----------------------------
# --- Overwrite file at pos ---
# -----------------------------
def write_file(fn, data, pos):
    with open(fn, 'r+b') as f:
        f.seek(pos, 0)
        f.write(str.encode(data))

# -------------------------
# ---  Update root node ---
# -------------------------
def incrementRoot(fn):
    pos = SEEK_NUM
    n = str(int(read_file(fn, pos, NUM_SIZE)) + 1)
    if n != NUM_MAX:
        write_file(fn, n, pos)

# --------------------------
# --- Parse tree to file ---
# --------------------------
def tree_parser(lock, tree, fn):
    with lock:
        cwd = os.getcwd()

        path = tree.path
        name = tree.name
        tag = tree.tag
        num = str(tree.num)
        id = str(tree.id)
        parent = str(tree.parent)

        while len(name) < SEEK_ID:  name += ' '
        while len(tag) < TAG_SIZE: tag += ' '
        while len(str(id)) < NUM_SIZE: id += ' '
        while len(str(parent)) < NUM_SIZE: parent += ' '
        while len(str(num)) < NUM_SIZE: num += ' '

        tree.set_name(name)
        tree.set_id(id)
        tree.set_parent(parent)
        tree.set_num(num)
        tree.set_tag(tag)

        if not os.path.exists(path):
            os.makedirs(path)
            os.chdir(path)

        os.chdir(path)

        if os.path.isfile(fn):
            size = os.stat(fn).st_size
            infile = False
            for i in range(0, size, NODE_SIZE + 1):
                res = read_file(fn, i, SEEK_ID)
                name = name.rstrip(' ')
                p = read_file(fn, i + SEEK_PID, NUM_SIZE)
                parent = parent.rstrip(' ')
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Case 1: Node has same name and parent as
                # an existing node in file. Increment node.
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if res == name and p == parent:
                    incrementNode(fn, i)
                    infile = True
                    break
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Case 2: Node has same name but different
                # parent than existing node.
                # Check the remainder of the file for a match.
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif res == name and p != parent:
                    for j in range(i, size, NODE_SIZE + 1):
                        res1 = read_file(fn, j, SEEK_ID)
                        p1 = read_file(fn, j + SEEK_PID, NUM_SIZE)
                        if res1 == name and p1 == parent:
                            break
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Case 3: Node does not exist in file.
            # Append node.
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if not infile:
                appendNode(fn, tree)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Case 4: File does not exist.
        # Create file.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        else:
            createNode(fn, tree, path)

        os.chdir(cwd)


# -----------------------------------
# --- Append the node to the tree ---
# -----------------------------------
def appendNode(fn, tree):
    incrementRoot(fn)
    pos = SEEK_PID
    n = str(int(read_file(fn, pos, NUM_SIZE)) + 1)
    write_file(fn, n, pos)
    if noProblem(fn, tree):
        create_file(fn, tree)

# --------------------------------------
# --- Create root node and first dep ---
# --------------------------------------
def createNode(fn, tree, path):
    rootName = fn[0:len(fn) - 4]
    while len(rootName) < SEEK_ID: rootName += ' '
    root = RelationTree(rootName, '0     ', '1     ', '1     ', path, '   ')
    create_file(fn, root)
    create_file(fn, tree)

# -------------------------------
# --- Increment 'num' in node ---
# -------------------------------
def incrementNode(fn, i):
    incrementRoot(fn)
    pos = SEEK_NUM + i
    n = str(int(read_file(fn, pos, NUM_SIZE)) + 1)
    write_file(fn, n, pos)

#  ~~~~~~~~~~~  #
#  hmm
#  ~~~~~~~~~~~ #
def noProblem(fn, tree):
    children = str(int(read_file(fn, SEEK_PID, NUM_SIZE)))
    if tree.id != children:
        while len(children) < NUM_SIZE: children += ' '
        tree.set_id(children)
    if tree.id == tree.parent:
        parent = "0"
        while len(parent) < NUM_SIZE: parent += ' '
        tree.set_parent(parent)
    if tree.name == fn[:-3] or \
                    int(tree.id) == NUM_MAX or \
                    int(tree.num) == NUM_MAX:
        return False
    return True
