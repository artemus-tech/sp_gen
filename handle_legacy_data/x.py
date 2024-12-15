import numpy as np
import os
import sptype
from dataclasses import dataclass
from dataclasses import field
import re
from presets import data_path, replacements
import psycopg2


@dataclass
class DataInstance:
    modified_filename: str = ""
    src_filename:str=""
    modified_params: list[str] = field(default_factory=list)
    src_params: list[str] = field(default_factory=list)

meta_result = []
result:[DataInstance] = []


class TreeNode:
    def __init__(self, name, is_dir=True):
        self.name = name  # Name of the file or directory
        self.is_dir = is_dir  # Whether it's a directory or a file
        self.children = []  # List to hold children (subdirectories or files)
        self.params = []
        self.full_paths = []

    def contains_q_double_pattern(self, input_string):
        # Define the regex pattern for q[double,double]
        pattern = r"q\[\d+(\.\d+)?,\d+(\.\d+)?\]"

        # Search for the pattern in the input string
        match = re.search(pattern, input_string)

        # Return True if a match is found, otherwise False
        return match is not None

    def fix_number(self, text):
        """
        Replace occurrences of somestring_someinteger.txt with somestring_No=some_integer.txt.

        Parameters:
            text (str): The input string.

        Returns:
            str: The modified string after replacements.
        """
        # Define the regular expression pattern
        pattern = r"(\w+)_(\d+)\.txt"

        # Replacement function for each match
        def replacement_function(match):
            prefix = match.group(1)  # The 'somestring' part
            number = match.group(2)  # The 'someinteger' part
            return f"{prefix}_No={number}.txt"

        # Perform the substitution
        return re.sub(pattern, replacement_function, text)

    def fix(self, target_string):
        for old, new in replacements.items():
            if old in target_string and new not in target_string:
                target_string = target_string.replace(old, new)
            if self.contains_q_double_pattern(target_string) is not None:
                target_string = self.replace_q_range_in_text(target_string)
            target_string=self.fix_number(target_string)
        return target_string

    def replace_q_range_in_text(self, large_text):
        # Define the regex pattern to find q[min,max]
        pattern = r"q\[(\d+(\.\d+)?),(\d+(\.\d+)?)\]"

        # Define the replacement format using captured groups
        replacement = r"qmin=\1_qmax=\3"

        # Replace all matches with their transformed format
        result = re.sub(pattern, replacement, large_text)
        return result
    def add_child(self, child):
        self.children.append(child)

    def convert(self, level=0, params = [], src_params=[]):
        source_params = [self.name]
        fixed_params = [self.fix(self.name)]

        if self.is_dir:

            if params:
                fixed_params += params
            if src_params:
                source_params+=src_params

        else:
            filename = self.fix(self.name)

            result.append(
                DataInstance(
                modified_filename=filename,
                modified_params=params,
                src_filename=self.name,
                src_params=src_params)
            )

            all_params = params + [filename]
            params_flattened_list = [part for p in all_params for part in p.split("_")]

            DynamicClass = sptype.create_class_with_fields(params_flattened_list, src=self.name, src_params=src_params)
            # Testing the generated class
            spobject = DynamicClass()
            meta_result.append(spobject)



        for child in self.children:
            child.convert(level + 1, params=fixed_params, src_params=source_params)

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
        if "tmp" not in filenames and "rg_fr" not in filename and ".py" not in filename:
            file_node = TreeNode(filename, is_dir=False)
            root.add_child(file_node)

    # Recursively add subdirectories and their contents
    for dirname in dirnames:
        if   "tmp" not in dirname:
            subdir_path = os.path.join(base_path, dirname)
            subdir_node = build_file_system_tree(subdir_path)  # Recursively build subdirectory
            root.add_child(subdir_node)  # Add subdirectory as a child of the root

    return root

def debug(different=False):
    # Example usage
    if different:
        print(result[np.random.randint(10, 7000)])
        print(meta_result[np.random.randint(10, 7000)])
        meta_result[np.random.randint(10, 7000)].print_fields()
    else:
        rnd = np.random.randint(10, 7000)
        print(result[rnd])
        print(meta_result[rnd])
        meta_result[rnd].print_fields()

if __name__ == "__main__":
    # Set the directory to start from (change this to your path)
    tree = build_file_system_tree(data_path)
    # tree.display()  # Display the tree structure
    tree.convert()
    debug()

    connection = psycopg2.connect(
        host="localhost",
        database="spgen",
        user="postgres",
        password="Dictionary108$"
    )
    tables = [
        "eval_results",
        "generate_results",
        "model_mean_intensity",
        "proxima_intensity",
        "vrija_results",
        "integral_results"
    ]


    """
    try:
        with connection.cursor() as cursor:
            # Clear each table
            for table in tables:
                cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
                print(f"Cleared table: {table}")

            # Commit the transaction
            connection.commit()

        print("All tables cleared successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    """

    # Insert data into the table
    with connection.cursor() as cursor:
        for obj in meta_result:
            if obj.action=="eval-multi-instance-intensity":
                obj.print_fields()
                cursor.execute(
                    """
                    INSERT INTO public.eval_results (
                        shape, scale, n, nc, excess, c, qmin, qmax, action, root, r, src, src_params,src_path
                    ) VALUES (
                        %(shape)s, %(scale)s, %(n)s, %(nc)s, %(excess)s, %(c)s, %(qmin)s, %(qmax)s,
                        %(action)s, %(root)s, %(r)s, %(src)s, %(src_params)s,%(src_path)s
                    );
                    """,
                    {
                        "shape": obj.shape,
                        "scale": obj.scale,
                        "n": obj.n,
                        "nc": obj.NC,
                        "excess": obj.excess,
                        "c": getattr(obj, "C", 0),
                        "qmin": obj.qmin,
                        "qmax": obj.qmax,
                        "action": obj.action,
                        "root": obj.root,
                        "r": obj.R,
                        "src": obj.src,
                        "src_params": obj.src_params,
                    "src_path": '/'.join(reversed(obj.src_params)) + "/"+obj.src
                    }
                )

            elif obj.action=="generate-xyzr":
                cursor.execute(
                    """
                                INSERT INTO generate_results (
                                    shape, scale, n, rmax, rmin, R, NC, excess, action, root, No, src, src_params,src_path
                                ) VALUES (
                                    %(shape)s, %(scale)s, %(n)s, %(rmax)s, %(rmin)s, %(R)s, %(NC)s, %(excess)s, 
                                    %(action)s, %(root)s, %(No)s, %(src)s, %(src_params)s,%(src_path)s
                                );
                                """,
                    {
                        "shape": obj.shape,
                        "scale": obj.scale,
                        "n": obj.n,
                        "rmax": obj.rmax,
                        "rmin": obj.rmin,
                        "R": obj.R,
                        "NC": obj.NC,
                        "excess": obj.excess,
                        "action": obj.action,
                        "root": obj.root,
                        "No": getattr(obj, "No", None),  # Use getattr to handle optional attributes
                        "src": obj.src,
                        "src_params": obj.src_params,
                        "src_path": '/'.join(reversed(obj.src_params)) + "/"+obj.src
                    } )
            elif obj.src=="Failed.txt":
                obj.print_fields()
            elif obj.action=="model-mean-intensity":
                obj.print_fields()
                cursor.execute("""
                    INSERT INTO public.model_mean_intensity (
                            action, c, shape, scale, root, n, nc, excess, qmin, qmax, src, src_params,src_path
                        ) VALUES (
                            %(action)s, %(C)s, %(shape)s, %(scale)s, %(root)s, %(n)s, %(NC)s,
                            %(excess)s, %(qmin)s, %(qmax)s, %(src)s, %(src_params)s,%(src_path)s
                        );
                    """, {
                        "action": obj.action,
                        "C": getattr(obj, "C", 0),
                        "shape": obj.shape,
                        "scale": obj.scale,
                        "root": obj.root,
                        "n": obj.n,
                        "NC": obj.NC,
                        "excess": obj.excess,
                        "qmin": obj.qmin,
                        "qmax": obj.qmax,
                        "src": obj.src,
                        "src_params": obj.src_params,
                    "src_path": '/'.join(reversed(obj.src_params)) + "/"+obj.src
                    })
            elif obj.action=="proxima":
                cursor.execute("""
                            INSERT INTO public.proxima_intensity (
                                action, c, shape, scale, root, src, src_params,src_path
                            ) VALUES (
                                %(action)s, %(C)s, %(shape)s, %(scale)s, %(root)s, %(src)s, %(src_params)s,%(src_path)s
                            );
                        """, {
                    "action": obj.action,
                    "C": getattr(obj, "C", 0),
                    "shape": obj.shape,
                    "scale": obj.scale,
                    "root": obj.root,
                    "src": obj.src,
                    "src_params": obj.src_params,
                    "src_path": '/'.join(reversed(obj.src_params)) + "/"+obj.src
                })
            elif obj.action=='integral':
                cursor.execute("""
                            INSERT INTO public.integral_results (
                                action, c, shape, scale, root, n, nc, excess, qmin, qmax, src, src_params,src_path
                            ) VALUES (
                                %(action)s, %(C)s, %(shape)s, %(scale)s, %(root)s, %(n)s, %(NC)s, %(excess)s, 
                                %(qmin)s, %(qmax)s, %(src)s, %(src_params)s,%(src_path)s
                            );
                        """, {
                    "action": obj.action,
                    "C":    getattr(obj, "C", 0),
                    "shape": obj.shape,
                    "scale": obj.scale,
                    "root": obj.root,
                    "n": obj.n,
                    "NC": obj.NC,
                    "excess": obj.excess,
                    "qmin": obj.qmin,
                    "qmax": obj.qmax,
                    "src": obj.src,
                    "src_params": obj.src_params,
                    "src_path": '/'.join(reversed(obj.src_params)) + "/"+obj.src

                })
            elif obj.action=='vrija':
                cursor.execute("""
                            INSERT INTO public.vrija_results (
                                action, c, shape, scale, root, nc, src, src_params,src_path
                            ) VALUES (
                                %(action)s, %(C)s, %(shape)s, %(scale)s, %(root)s, %(NC)s, %(src)s, %(src_params)s,%(src_path)s
                            );
                        """, {
                    "action": obj.action,
                    "C": getattr(obj, "C", 0),
                    "shape": obj.shape,
                    "scale": obj.scale,
                    "root": obj.root,
                    "NC": obj.NC,
                    "src": obj.src,
                    "src_params": obj.src_params,
                    "src_path": '/'.join(reversed(obj.src_params)) + "/"+obj.src
                })


        connection.commit()
    connection.close()
