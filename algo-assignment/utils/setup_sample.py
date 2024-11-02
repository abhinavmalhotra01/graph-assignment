import uuid
from models.models import Graph, Node, Edge, GraphRunConfig
from utils.graph_runner import GraphRunner
from utils.graph_validators import GraphValidator

def get_sample_graph(nodes, edges):
    """
    Define and return a sample graph setup
    The main idea behind this is to create a graph object based on input nodes and edges
    
    Args:
        nodes: List of nodes
        edges: List of edges
        
    Returns:
        A graph object with expected relations
    """
    
    # create a node_map with id as key
    node_map = {node.id: node for node in nodes}
    
    # add edges in paths for each node
    for edge in edges:
        src = node_map.get(edge.src_node)
        dst = node_map.get(edge.dst_node)
        
        if src and dst:
            src.paths_out.append(edge)
            dst.paths_in.append(edge)
        else:
            raise ValueError("Edge refers to non-existent nodes")

    return Graph(nodes=nodes)

def get_sample_config(root_inputs=None, data_overwrites=None, enable_list=None, disable_list=None):
    """
    Return a sample configuration for running the graph
    """
    root_inputs = root_inputs or {}
    data_overwrites = data_overwrites or {}
    enable_list = enable_list or []
    disable_list = disable_list or []

    return GraphRunConfig(
        root_inputs=root_inputs,
        data_overwrites=data_overwrites,
        enable_list=enable_list,
        disable_list=disable_list
    )
    