import os

def get_direct_path(filename):
    '''
    Returns the direct path of the inputed file name dynamically within the root directory
    
    Example Input: "quotes.db"

    Example Output: "j:\\6.0 - Designer Folders\Will\Code Tools\quote-emailer\quotes.db"
    '''
    root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root_directory, filename)
