import uuid
from collections import deque, defaultdict
from models.models import Graph, Node, Edge, GraphRunConfig

class GraphValidator:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.node_map = {node.id: node for node in graph.nodes}
    
    def validate_edge_compatibility(self):
        for node in self.graph.nodes:
            for edge in node.paths_out:
                src_node = self.node_map[edge.src_node]
                dst_node = self.node_map[edge.dst_node]
                for src_key, dst_key in edge.src_to_dst_data_keys.items():
                    if type(src_node.data_out.get(src_key)) != type(dst_node.data_in.get(dst_key)):
                        raise ValueError(f"Data type mismatch between {src_node.id}:{src_key} and {dst_node.id}:{dst_key}")
                    # assert type(src_node.data_out.get(src_key)) == type(dst_node.data_in.get(dst_key)), \
                    #     "Incompatible data types for edge from {} to {}".format(src_node.id, dst_node.id)
    
    def detect_cycle(self):
        visited = set()
        # nodes in the current path (this is used due to directed nature of graph)
        stack = set()
        
        def dfs(id):
            if id in stack:
                return True
            if id in visited:
                return False
            
            visited.add(id)
            stack.add(id)
            for edge in self.node_map[id].paths_out:
                if dfs(edge.dst_node):
                    return True
            stack.remove(id)
            return False
        
        for node in self.graph.nodes:
            if node.id not in visited:
                if dfs(node.id):
                    raise ValueError("Cycle detected in the graph.")
                
    def check_islands(self):
        visited = set()
        
        def dfs(id):
            stack = [id]
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    node = self.node_map[current]
                    
                    for edge in node.paths_in + node.paths_out:
                        neighbor_id = edge.src_node if edge.src_node != current else edge.dst_node
                        stack.append(neighbor_id)
                        
        dfs(self.graph.nodes[0].id)
        if len(visited)!=len(self.graph.nodes):
            raise ValueError("Graph contains islands")
