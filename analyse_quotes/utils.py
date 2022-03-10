def read_txt_lines(file_path: str):
    """
    Read all lines in a txt file
    :param file_path: fuill path to file we want to read
    :return: list of lines, each as a string
    """
    return open(file_path).read().splitlines()
