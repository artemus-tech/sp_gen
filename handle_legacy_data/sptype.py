class DynamicClassMeta(type):
    def __new__(cls, name, bases, dct, field_definitions, src:str, src_params):
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
        dct["src"] = src
        dct["src_params"] = src_params

        fields["src"] = src
        fields["src_params"] = src_params

        # Add the fields dictionary to the class
        dct["_fields"] = fields

        # Define an instance method to print fields
        def print_fields(self):
            print(f"Fields for {self.__class__.__name__}:")
            for field, default in self._fields.items():
                value = getattr(self, field, None)
                print(f"  {field}: {value} (default: {default})")

        # Add the method to the class dictionary
        dct["print_fields"] = print_fields

        return super().__new__(cls, name, bases, dct)


def create_class_with_fields(field_definitions, src:str="", src_params=[]):
    class DynamicClass(metaclass=DynamicClassMeta, field_definitions=field_definitions, src=src, src_params=src_params):
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
