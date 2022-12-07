import re

class node(object) :

    def __init__(self,name = "", size = None):
        self.m_size = size
        self.m_name = name
        self.m_children = []

    def add_child(self, child):
        self.m_children.append(child)

    def size(self):
        if self.m_size is not None:
            return self.m_size
        total = 0
        for c in self.m_children:
            total = total + c.size()
        return total

    def print_dir(self,indent=0):
#        print("chocha")
        if self.m_size is not None:
            print("  "*indent + " - " + self.m_name + " " + str(self.m_size))
        else:
            print ("  "*indent + " `- " + self.m_name)
            for n in self.m_children:
                n.print_dir(indent+1)

    def total_if_meets_condition(self):
        total = 0
        if self.m_size is None and self.size() <= 100000:
            total = total + self.size()
        for c in self.m_children:
            total = total + c.total_if_meets_condition()
        return total

    def find_smallest_than(self,goal,best):
        current = best
        if self.m_size is None and self.size() >= goal and self.size() < best:
            current = self.size()
        for c in self.m_children:
            candidate = c.find_smallest_than(goal,current)
            if candidate < current:
                current = candidate
        return current
    
        
f = open("input_7.txt")

root = node("(root)")
current = root
parents = []

for l in f:
    n = l.strip()
    if re.match("^\$ cd .*",n):
        dirname = n[5:]
#        print(dirname)
        if dirname != "..":
            child = node(dirname)
            current.add_child(child)
            parents.append(current)
            current = child
        if dirname == "..":
            current = parents.pop()
    elif re.match("^dir .*",n):
        continue
    elif re.match("^(\d.*) (.*)",n):
        x = re.search("^(\d.*) (.*)",n)
        child = node(x.group(2), int(x.group(1)))
        current.add_child(child)

total = root.m_children[0].total_if_meets_condition()


root.print_dir()
print(total)
space = 70000000
goal = 30000000 - (space - root.size())
x = root.find_smallest_than(goal,space)
print(x)
