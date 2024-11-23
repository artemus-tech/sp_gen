# Define the metaclass
'''
class DynamicClassMeta(type):
    def __new__(cls, name, bases, dct, params):
        # Parse the parameters from the list
        for param in params:
            key, value = param.split('=')
            dct[key] = value  # Add each param as a class attribute
        
        # Create the class using the parent metaclass
        return super().__new__(cls, name, bases, dct)

# Define the class that uses the metaclass
class DynamicClass(metaclass=DynamicClassMeta):
    # Optional: Additional methods or attributes can go here
    def __init__(self, *args, **kwargs):
        pass

# Example usage
params = ["param1=value1", "param2=value2", "param3=42"]

# Dynamically create a class with the parameters
DynamicClassWithParams = DynamicClassMeta(
    'DynamicClassWithParams', 
    (DynamicClass,), 
    {},  # Initial class dictionary
    params=params  # Custom parameters
# Instantiate the new class
instance = DynamicClassWithParams()

# Access the dynamically added attributes
print(instance.param1)  # Output: value1
print(instance.param2
'''
'''
class DynamicClassMeta(type):
    def __new__(cls, name, bases, dct, field_definitions):
        # Parse fields and set default values from the list of strings
        for field in field_definitions:
            if "=" in field:
                field_name, default_value = field.split("=")
                dct[field_name.strip()] = default_value.strip()
            else:
                dct[field.strip()] = None
        #dct["_fields"] = fields
        return super().__new__(cls, name, bases, dct)

    def print_fields(self):
        for field, value in self._fields.items():
            print(f"{field} = {getattr(self, field)}")
        dct['print_fields'] = print_fields

def create_class_with_fields(field_definitions):
    class DynamicClass(metaclass=DynamicClassMeta, field_definitions=field_definitions):
        pass

    return DynamicClass


# Example usage
#fields = ["param1=value1", "param2=value2", "param3"]
#DynamicClass = create_class_with_fields(fields)

# Testing the generated class
#obj = DynamicClass()
#print(obj.param1)  # Output: value1
#print(obj.param2)  # Output: value2
#print(obj.param3)  # Output: None
#print(obj)
class DynamicClassMeta(type):
    def __new__(cls, name, bases, dct, field_definitions):
        # Parse fields and set default values from the list of strings
        fields = {}
        for field in field_definitions:
            if "=" in field:
                field_name, default_value = field.split("=")
                dct[field_name.strip()] = default_value.strip()
                fields[field_name.strip()] = default_value.strip()
            else:
                dct[field.strip()] = None
                fields[field.strip()] = None

        # Add the fields dictionary to the class
        dct["_fields"] = fields

        # Add a method to print all fields
        def print_fields(self):
            for field, value in self._fields.items():
                print(f"{field} = {getattr(self, field)}")

        dct["print_fields"] = print_fields

        return super().__new__(cls, name, bases, dct)

def create_class_with_fields(field_definitions):
    class DynamicClass(metaclass=DynamicClassMeta, field_definitions=field_definitions):
        pass

    return DynamicClass


# Example usage
#fields = ["param1=value1", "param2=value2", "param3"]
#DynamicClass = create_class_with_fields(fields)

# Testing the generated class
#obj = DynamicClass()
#obj.print_fields()

'''
class DynamicClassMeta(type):
    def __new__(cls, name, bases, dct, field_definitions):
        # Parse fields and set default values from the list of strings
        fields = {}
        for field in field_definitions:
            if "=" in field:
                field_name, default_value = field.split("=")
                dct[field_name.strip()] = default_value.strip()
                fields[field_name.strip()] = default_value.strip()
            else:
                dct[field.strip()] = None
                fields[field.strip()] = None

        # Add the fields dictionary to the class
        dct["_fields"] = fields

        # Define an instance method to print fields
        def print_fields(self):
            for field, value in self._fields.items():
                print(f"{field} = {getattr(self, field)}")

        # Add the method to the class dictionary
        dct["print_fields"] = print_fields

        return super().__new__(cls, name, bases, dct)

def create_class_with_fields(field_definitions):
    class DynamicClass(metaclass=DynamicClassMeta, field_definitions=field_definitions):
        pass

    return DynamicClass


# Example usage

#fields = ["param1=value1", "param2=value2", "param3"]
#DynamicClass = create_class_with_fields(fields)

# Testing the generated class
#obj = DynamicClass()
#obj.print_fields()
# Output:
#
