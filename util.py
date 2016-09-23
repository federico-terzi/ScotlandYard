'''
Created on 07/set/2016

@author: Lorenzo Selvatici
'''

import inspect
import sys


def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print "*** Method not implemented: %s at line %s of %s" % (method, line, fileName)
    sys.exit(1)
    
class Counter(dict):
    """
    ...
    """
    def __getitem__(self, key):
        """
        Returns the item associated to the key. If the key is not present, returns 0.
        """
        self.setdefault(key, 0)
        return dict.__getitem__(self, key)
    
    def argMax(self):
        """
        Returns the list of keys associated with the greatest value.
        """
        if len(self)==0:
            return None
        
        pairs = self.items()
        maxi = max([pair[1] for pair in pairs])
        result = [pair[0] for pair in pairs if pair[1]==maxi]
        return result

    def totalCount(self):
        """
        Returns the sum of all the values stored in the Counter.
        """
        return sum(self.values())
    
    def normalize(self):
        """
        EDITs the dictionary in place so that the totalCount of the dictionary is 1.
        """
        total = float(self.totalCount())
        if total == 0:
            return
        for key, val in self.items():
            self[key] = val/total
    
    def copy(self):
        """
        Returns a copy of the counter
        """
        return Counter(dict.copy(self))
        
   
if __name__ == "__main__":
    c = Counter()
    c["a"] = 1
    c["b"] = 2
    c["c"] = 1
    c["d"] = 2
    print c.totalCount()
    c.normalize()
    print c.totalCount()
    
    
    
    
    
    