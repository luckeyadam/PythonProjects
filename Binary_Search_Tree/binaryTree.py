class Node:
    def __init__(self, val):
        self.value = val
        self.leftChild = None
        self.rightChild = None

    def insert(self, data):
        if self.value == data: # avoid duplicate data
            return False
        elif self.value > data:
            if self.leftChild: # if there is a left child, insert data
                return self.leftChild.insert(data)
            else: # if no left child create one
                self.leftChild = Node(data)
                return True
        else:
            if self.rightChild: # if data greater than current value insert into right
                return self.rightChild.insert(data)
            else:
                self.rightChild = Node(data) # if no right child create one
                return True

    def find(self, data):
        if (self.value == data): # if current node contains data
            return True
        elif self.value > data: # if data smaller than current nodes value
            if self.leftChild:
                return self.leftChild.find(data) # if left child exists, do recursive find
            else:
                return False # if no node, then theres no data
        else:
            if self.rightChild: # if right child exists, do recursive find
                return self.rightChild.find(data)
            else: # else no node, no data
                return False

    # traversal operations
    def preorder(self):
        if self:
            print(str(self.value))
            if self.leftChild:
                self.leftChild.preorder()
            if self.rightChild:
                self.rightChild.preorder()

    def postorder(self):
        if self:
            if self.leftChild:
                self.leftChild.postorder()
            if self.rightChild:
                self.rightChild.postorder()

            print(str(self.value))

    def inorder(self):
        if self:
            if self.leftChild:
                self.leftChild.inorder()
            print(str(self.value))
            if self.rightChild:
                self.rightChild.inorder()

class Tree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root: # if root node exists
            return self.root.insert(data)
        else: # if no root node create one
            self.root = Node(data)
            return True

    def find(self, data):
        if self.root:
            return self.root.find(data)
        else:
            return False

    # traversal functions
    def preorder(self):
        print("PreOrder")
        self.root.preorder()

    def postorder(self):
        print("PreOrder")
        self.root.postorder()

    def inorder(self):
        print("PreOrder")
        self.root.inorder()

bst = Tree()
bst.insert(10)
print(bst.insert(15))
bst.preorder()
bst.postorder()
bst.inorder()
