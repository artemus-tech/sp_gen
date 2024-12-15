import numpy as np
import os
import sptype
from dataclasses import dataclass
import typing
from dataclasses import field


result = []



@dataclass
class DataInstance:
    f:str=""

    #p:str=""
    #scratch:str=""
    params: list[str] = field(default_factory=list)


class TreeNode:
    def __init__(self, name, is_dir=True):
        self.name = name  # Name of the file or directory
        self.is_dir = is_dir  # Whether it's a directory or a file
        self.children = []  # List to hold children (subdirectories or files)
        self.params = []
        self.full_paths=[]
    def fix(self, badstring, goodstring):
        if badstring in self.name and goodstring not in self.name:
            return self.name.replace(badstring,goodstring)
        else:
            return self.name

    def add_child(self, child):
        self.children.append(child)

    def convert(self, level=0,params=[]):
        if self.is_dir:
           #indent = " "*4*level

           #p = [self.name]
           #fix

           #if "shape" in self.name and "shape=" not in self.name:
           #   new_name = self.name.replace("shape","shape=")
           #   p = [new_name]
           #newname = fix("shape","shape=")
           p=[self.fix("shape","shape=")]

           #self.full_paths+=self.f

           if params:
              p+=params

        if not self.is_dir:

            #path = "_".join(self.full_paths)
            #scratch = "".join(params)

            #f  = self.name

            dt = DataInstance(f=self.name, params = params)
            result.append(dt)

            #params.append(f'f={self.name.replace("=","_")}')
            #params.append(f'path={path}')

            #DynamicClass = sptype.create_class_with_fields(params)
            # Testing the generated class
            #spobject = DynamicClass()
            #result.append(spobject)

        #print(f"{indent}-{params}")       
        for child in self.children:
            child.convert(level+1, p)





    def display(self, level=0):
        """
        Recursively display the tree structure.
        Indentation represents depth.
        """
        indent = " " * (4 * level)  # Indentation for the current level
        if self.is_dir:
            print(f"{indent}- {self.name}/")  # Directories end with '/'
        else:
            print(f"{indent}- {self.name}")  # Files are printed as is
        
        # Recursively display each child node
        for child in self.children:
            child.display(level + 1)  # Increase level of indentation for children

def build_file_system_tree(base_path):
    """
    Recursively builds the file system tree structure starting from `base_path`.
    """
    root = TreeNode(os.path.basename(base_path), is_dir=True)  # Start with the root directory
    try:
        # Get directories and files in the current directory
        dirnames, filenames = next(os.walk(base_path))[1:3]  # (dirs, files)
    except StopIteration:
        return root  # If the directory doesn't exist or is empty, return the root

    # Add files as children of the root node
    for filename in filenames:
        file_node = TreeNode(filename, is_dir=False)
        root.add_child(file_node)

    # Recursively add subdirectories and their contents
    for dirname in dirnames:
        subdir_path = os.path.join(base_path, dirname)
        subdir_node = build_file_system_tree(subdir_path)  # Recursively build subdirectory
        root.add_child(subdir_node)  # Add subdirectory as a child of the root

    return root

# Example usage
if __name__ == "__main__":
    # Set the directory to start from (change this to your path)
    base_path = "./res_auto_save"  # Current directory, change it to the path you want to read
    tree = build_file_system_tree(base_path)
    #tree.display()  # Display the tree structure
    tree.convert()
    #print(len(result))
    print(result[np.random.randint(10, 7000)])
