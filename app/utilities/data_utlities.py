@staticmethod
def convert_csv_content_into_tuples(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split each line by comma delimiter
            parts = line.strip().split(',')
            # Construct a tuple with the values
            data.append((parts[0], parts[1]))
    return data