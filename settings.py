import os

def rootPath():
    """ 
    Application root path. 
    This will be used to get the relative PATH
    """
    return os.path.join(os.path.dirname(__file__))