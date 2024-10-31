import uuid
from models.models import Graph, Node, Edge, GraphRunConfig
from utils.graph_runner import GraphRunner
from utils.graph_validators import GraphValidator

def get_sample_graph():
    """
    Define and return a sample graph setup
    """
    node_a = Node(node_id = "A", data_out = {"out_a": 10})
    node_b = Node(node_id = "B", data_in = {"in_b": None}, data_out={"out_b":20})
    node_c = Node(node_id = "C", data_in = {"in_c": None})
    
    edge_a_b = Edge(src_node = "A", dst_node= "B", src_to_dst_data_keys={"out_a": "in_b"})
    edge_b_c = Edge(src_node="B", dst_node="C", src_to_dst_data_keys={"out_b": "in_c"})\
        
    node_a.paths_out.append(edge_a_b)
    node_b.paths_in.append(edge_a_b)
    node_b.paths_out.append(edge_b_c)
    node_c.paths_in.append(edge_b_c)

    return Graph(nodes=[node_a, node_b, node_c])

def get_sample_config():
    """
    Return a sample configuration for running the graph
    """
    return GraphRunConfig(
        root_inputs = {"A": {"out_a": 15}},
        data_overwrites = {"B": {"in_b": 25}}
    )
    
def get_expected_outputs():
    return{
        "output_b": {"out_b": 20},
        "leaf_outputs": {"C": {"in_c": 20}},
        "islands": [["A", "B", "C"]],
    }