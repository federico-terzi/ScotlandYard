'''
Created on 07/set/2016

@author: Lorenzo Selvatici
'''

class EdgeType:
    """
    Enum representing the possible types of Edge.
    
    """
    TAXI = "TAXI"
    BUS = "BUS"
    UNDERGROUND = "UNDERGROUND"
    FERRY = "FERRY"
    
    def asList():
        """
        Return all the possible types of edge.
        """
        return [EdgeType.TAXI, EdgeType.BUS, EdgeType.UNDERGROUND, EdgeType.FERRY]
    asList = staticmethod(asList)


class Layout:
    
    """
    A layout stores all the static informations of the game: Node, edges, type of edges.
    
    NOTE : you should use Settings.getLayout() static method rather than build it directly.
    
    **IMPORTANT** : the edges do NOT have a specific direction (a Layout represents an undirected graph)
    
    File format:
    <EdgeType>; <start> : [<path>] : <end>
    <path> = integers separated by whitespaces    
    """
    
    def __init__(self, layoutFileName):
        """
        Builds a layout from the content of a .txt file.       
        """
        import os
        assert type(layoutFileName) == type("string")

        if layoutFileName=="DEFAULT": #Load the default settings
            baseDirectory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            layoutFileName = baseDirectory + os.sep + "Files" + os.sep + "layout.txt"

        if not layoutFileName.endswith(".txt"):
            layoutFileName = layoutFileName + ".txt"
        
        if not os.path.exists(layoutFileName):
            raise ValueError(layoutFileName + " does not exist.")
        
        in_file = open(layoutFileName, "r")
        lines = in_file.readlines()
        
        self.numNodes = int(lines[0])
        self.edges = [] # list of tuples --> (start, end, type, path)
        self.edge_types = set()
        self.nodes = {} # dict --> numNodes : set(EdgeType)
                        # store the information (stations) for every node
        
        for line in lines[1:]:
            new_edge = self._processLine(line) # (int, int, EdgeType, [])
            self.edges.append(new_edge)
            # update the nodes dict
            start, end, edge_type, _ = new_edge
            if start not in self.nodes:
                self.nodes[start] = set()
            self.nodes[start].add(edge_type)
            if end not in self.nodes:
                self.nodes[end] = set()
            self.nodes[end].add(edge_type)
            
            
        
        in_file.close()
        
    def _processLine(self, line):
        if ';' not in line:
            raise ValueError("Wrong line format (missing ;) : " + line)
        edge_type, descr = line.strip().split(";")
        edge_type = edge_type.upper()
        if edge_type not in EdgeType.asList():
            raise ValueError("Wrong edge edge_type: " + edge_type.upper())
        
        self.edge_types.add(edge_type)
        
        start, path, end = descr.strip().split(":")
        start, end = int(start), int(end)
        path = path.strip()
        if path == "":
            path = []
        else:
            path = [int(x) for x in path.split(" ")]
        
        assert (start not in path and end not in path)
        assert (not start == end)
        
        if start>end:
            start, end = end, start
            
        edge = (start, end, edge_type, path)
        
        assert edge not in self.edges
        
        return edge
        
    def getNumNodes(self):
        """
        Returns the number of nodes.
        """
        return self.numNodes
    
    def getNodesStations(self):
        """
        Returns the dict which associates a node with its type of stations.
        example --> 5 : (TAXI, BUS) 
        """
        return self.nodes
    
    def getEdgeTypes(self):
        """
        Returns the different types of the Edges as a set.
        """
        return self.edge_types
    
    def getEdges(self):
        """
        Returns the list of edges. 
        Each element is a tuple in the following format: 
        (start, end, edgeType, path) - (int, int, EdgeType, [])
        """
        return self.edges
    
    def getEdgesFromNode(self, nodeNumber):
        """
        Returns the edges from a given node.
        """
        edges = [edge for edge in self.edges if edge[0]==nodeNumber or edge[1]==nodeNumber]
        for i, edge in enumerate(edges):
            if edges[i][0] != nodeNumber:  # swap start and end
                edges[i] = edges[i][1], edges[i][0], edges[i][2], edges[i][3]
        return edges
    
    def __eq__(self, other):
        return self.numNodes == other.numNodes and self.edges==other.edges
        
        


if __name__ == '__main__':
    layout = Layout("C:\Users\Selvatici\Desktop\Python\Projects\Scotland Yard - Project\ScotlandYard\Files\layout.txt")
    #print layout.getNumNodes()
    #print layout.getEdgeTypes()
    print layout.getEdges()
    #print layout.getEdgesFromNode(5)



