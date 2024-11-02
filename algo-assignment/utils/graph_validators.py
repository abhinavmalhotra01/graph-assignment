import uuid
from collections import deque, defaultdict
from models.models import Graph, Node, Edge, GraphRunConfig

class GraphValidator:
    """
    A class to validate a directed acyclic graph, including edge compatibility,
    cycle detection, and isolation of disconnected components (islands).
    """
    def __init__(self, graph: Graph):
        self.graph = graph
        # Create a mapping of node IDs to their respective Node objects for easy lookup
        self.node_map = {node.id: node for node in graph.nodes}
    
    def validate_edge_compatibility(self):
        """
        Check that all edges have compatible data types between source and destination nodes.
        
        Raises:
            ValueError: If there is a data type mismatch between `data_out` of the src node
                        and `data_in` of the dst node for any edge.
        """
        for node in self.graph.nodes:
            for edge in node.paths_out:
                
                src_node = self.node_map[edge.src_node]
                dst_node = self.node_map[edge.dst_node]
                
                # Validate that data types match for each key in src_to_dst_data_keys
                for src_key, dst_key in edge.src_to_dst_data_keys.items():
                    if type(src_node.data_out.get(src_key)) != type(dst_node.data_in.get(dst_key)):
                        raise ValueError(f"Data type mismatch between {src_node.id}:{src_key} and {dst_node.id}:{dst_key}")
                    # assert type(src_node.data_out.get(src_key)) == type(dst_node.data_in.get(dst_key)), \
                    #     "Incompatible data types for edge from {} to {}".format(src_node.id, dst_node.id)
    
    def detect_cycle(self):
        """
        Detect cycles using DFS. This method ensures that the graph is DAG.
        
        Raises:
            ValueError: If a cycle is detected in the graph.
        """
        
        visited = set()  # Track all visited nodes
        stack = set()    # Track nodes in the current path to detect cycles
        
        def dfs(id):
            """
            Recursive helper function to perform DFS and detect cycles.
            """
            if id in stack:
                return True # cycle detected
            if id in visited:
                return False # already visited, no cycle
            
            # Mark the node as visited and add it to the current path stack
            visited.add(id)
            stack.add(id)
            for edge in self.node_map[id].paths_out:
                if dfs(edge.dst_node):
                    return True # cycle found in recursive path

            # remove node form current path
            stack.remove(id)
            return False
        
        # Perform DFS from each unvisited node
        for node in self.graph.nodes:
            if node.id not in visited:
                if dfs(node.id):
                    raise ValueError("Cycle detected in the graph.")
                
    def check_islands(self):
        """
        Ensure that the graph has no isolated components or 'islands'. All nodes should be reachable
        from the starting node.
        
        Raises:
            ValueError: If disconnected components are found in the graph.
        """
        
        visited = set()
        
        def dfs(id):
            """
            Depth-First Search (DFS) to mark all nodes reachable from a starting node.
            """
            
            stack = [id]  # Use a stack for DFS
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)  # Mark the node as visited
                    node = self.node_map[current]
                    
                    # Explore both incoming and outgoing edges to find all connected nodes
                    for edge in node.paths_in + node.paths_out:
                        neighbor_id = edge.src_node if edge.src_node != current else edge.dst_node
                        stack.append(neighbor_id)
        
        # Start DFS from the first node and check if all nodes are connected               
        dfs(self.graph.nodes[0].id)
        if len(visited)!=len(self.graph.nodes):
            raise ValueError("Graph contains islands")
