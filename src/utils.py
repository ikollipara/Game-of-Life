# src/utils.py
# Ian Kollipara
# 2020.02.09
# Utility Functions for use in JCGoL
#
# Usage
# from utils import ...
# OR
# import utils

def get_integer(prompt):
    """ Return an integer from given prompt. 
    
    Parameters
    prompt  String used in input function
    """

    return_val = 0

    try:
        return_val = int(input(prompt))
    
    except:
        return_val = get_integer(prompt)

def get_bool(prompt):
    """ Return a bool from given prompt. 
    
    Parameters
    prompt String used in input function
    """

    options = {
        'y': True,
        'n': False,
    }
    return_val = False

    try:
        return_val = options[input(f"{prompt}(y/n) ")]
    
    except:
        return_val = get_bool(prompt)
    
    return return_val