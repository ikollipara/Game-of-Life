# src/cell.py
# Ian Kollipara
# 2020.02.09
# Cell Class for use in JCGoL
#
# Usage
# from cell import Cell

# Imports

class Cell:
    """ Implement Cell class for use in John Conway's Game of Life. 
    
    Cell contains the current cell status and icon used to represent status.
    """

    # Instance Variables (public)
    # location  Tuple used to place cell in matrix
    # status    Boolean representing current cell status

    def __init__(self, location, status=False):
        """ __init__() create Cell object. 
        
        Parameters
        location  Tuple of integers used to place cell on a grid
        status    Optional boolean used to set cell's current_status
        """

        self.location = location
        self.current_status = status
        self.neighbors:List = []
    
    def current_living_neighbors_count(self):
        """ Return an integer of all living cell neighbors. """

        count = 0

        for cell in self.neighbors:
            
            if cell.current_status:
                count += 1
        
        return count
    
    def __str__(self):
        """ Return display string of Cell. """
        
        return '\u2B1C' if not self.current_status else '\u2B1B'