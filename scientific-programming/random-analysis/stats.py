import copy
import io
import os

# triple-quoted string = docstring 
def iterable(obj):
    """Returns True if `obj` is iterable, False otherwise"""
    return hasattr(obj, '__iter__') or hasattr(obj, '__getitem__')

class Dataset(object):
    def __init__(self, data, data_type=float):
        """Load data and convert it from string to data_type.

        `data` must be one of:
            1) a string containing the path to a data file
            2) an open file object (io.TextIOWrapper)
            3) another instance of Dataset

        Or a list of pre-converted rows can be given directly:
            rows = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            my_data = Dataset(rows)
        """
        if isinstance(data, str):
            # string should be a valid filename
            with open(data) as file_obj:
                self.read_file(file_obj, data_type)
        elif isinstance(data, io.TextIOWrapper):
            self.read_file(data, data_type)
        elif isinstance(data, Dataset):
            self.data = copy.deepcopy(data.data)
        elif iterable(data):
            self.data = list(data)
        else:
            error_message = "Unknown type for data: {type(data).__name__}"
            raise TypeError(error_message.format(data=data))

        self.rows = self.data   # alias for data
        self.cols = list(zip(*self.rows))

    def __repr__(self):
        """See Dataset.__str__"""
        return str(self)

    def __str__(self):
        """Display data row-by-row."""
        lines = []
        for row in self.rows:
            # convert fields to string
            row = map(str, row)
            # join by space
            lines.append(' '.join(row))

        # join by this operating system's line separator (e.g. \n)
        return os.linesep.join(lines)

    def format_line(self, line, data_type):
        """Remove trailing newline, split by whitespace, and apply data_type."""
        return [data_type(field) for field in line.strip().split()]

    def read_file(self, file_obj, data_type):
        """Read input from file_object and store it as data_type."""
        format_line = self.format_line
        self.data = [format_line(line, data_type) for line in file_obj]