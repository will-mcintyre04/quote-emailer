import os

def get_direct_path(filename):
    '''
    Returns the direct path of the inputed file name dynamically within the root directory

    Parameters
    ----------
    filename : str
        name of the file found within the root
    
    Returns
    -------
    str
        string of the direct path of the inputed file

    Examples
    -------
    - Input: "quotes.db"
    - Output: "j:\\6.0 - Designer Folders\Will\Code Tools\quote-emailer\quotes.db"
    '''
    root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root_directory, filename)
