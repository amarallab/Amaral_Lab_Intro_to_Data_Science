from pathlib import Path


def get_path_to_records( folder_path ):
    """
    Return all roster filenames in directory
    
    input:
        folder_path - Path object to the directory that contains the roster 
                      files
        
    output:
        my_paths - list of Paths to roster files in directory
    """
    my_paths = folder_path.glob('*.txt')
    my_paths = list(my_paths)
    
    return my_paths


def parse_record( filename ):
    """
    Read the file located at filename, extract information and organize
    into a dictionary.
    
    input:
        filename -- Path object with location of data 
    
    output:
        record -- dict with keys being types of information in file
    """
    # Statements here!
    
    return record


def extract_birdthday( record ):
    """
    
    """
    birthday = ''
    
    # Statements here!
    
    return birthday


def calculate_age( birthday, relevant_date ):
    """
    
    """
    age = 0
    
    # Statements here!
    
    return age

