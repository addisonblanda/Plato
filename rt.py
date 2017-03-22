# ------------------------------------------------------
# ----             rt.py                 ----
# ------------------------------------------------------
# A class to represent relational tree structures
# ------------------------------------------------------

class RelationTree():

    def __init__(self, name, id, parent, num, path, tag):
        self.path = path
        self.name = name
        self.id = id
        self.parent = parent
        self.num = num
        self.tag = tag
        self.leaf = []

    def __print_all__(self):
        print('{name: ' + self.name + ',')
        print('num: '+str(self.num)+',')
        print('id: ' + str(self.id) +',')
        print('parent: ' + str(self.parent) + ',')

    def __add_leaf__(self, name, id, parent, num, tag):
        self.leaf.append(RelationTree(name, id, parent, num, self.path, tag))

    def name(self):
        return self.name

    def id(self):
        return self.id

    def parent(self):
        return self.parent

    def num(self):
        return self.num

    def set_name(self, name):
        self.name = name

    def set_id(self, id):
        self.id = id

    def set_parent(self, parent):
        self.parent = parent

    def set_num(self, num):
        self.num = num

    def set_tag(self, tag):
        self.tag = tag


