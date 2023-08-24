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
    
    Raises
    ------
    FileNotFoundError
        if the requested path does not exist

    Examples
    -------
    - Input: "quotes.db"
    - Output: "j:\\6.0 - Designer Folders\Will\Code Tools\quote-emailer\quotes.db"
    '''
    root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    direct_path = os.path.join(root_directory, filename)
    if not os.path.exists(direct_path):
        raise FileNotFoundError(f"Direct path requested: '{direct_path}' does not exist.")
    return direct_path