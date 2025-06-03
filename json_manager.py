import json

# Made by Joshua Thompson

### Returns dictionary data from the json file
def read_file(file_path):
    """Opens and returns the contents of a file
        Args:
            file_path (str): The directory path and file we are wanting to read from

        Returns:
            Any: The contents of the file
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
        f.close()
        return data

def write_file(file_path, data):
    """Writes to a json file
        Args:
            file_path (str): The directory path we are wanting to write to
            data (any): The data we are wanting to write to the file
    """
    with open(file_path, 'w') as f:
        new_data = json.dumps(data, indent=4)
        f.write(new_data)
        f.close()        