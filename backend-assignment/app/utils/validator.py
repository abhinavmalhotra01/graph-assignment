from typing import Dict
import uuid

def validate_graph_structure(graph):
    """ Validates that all nodes and edges in the graph follow correct rules """
    for edge in graph.edges:
        src_node = next((node for node in graph.nodes if node.id == edge.src_node), None)
        dst_node = next((node for node in graph.nodes if node.id == edge.dst_node), None)
        
        # Check if src and dst nodes exist
        if not src_node or not dst_node:
            raise ValueError(f"Edge {edge.id} has invalid source or destination node.")
        
        # Check data type compatibility
        for src_key, dst_key in edge.src_to_dst_data_keys.items():
            if src_key not in src_node.data_out or dst_key not in dst_node.data_in:
                raise ValueError(f"Edge {edge.id} has incompatible data keys.")

def generate_unique_run_id():
    """ Generates a unique run ID for each graph execution """
    return str(uuid.uuid4())
