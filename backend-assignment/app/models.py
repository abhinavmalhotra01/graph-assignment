from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from bson import ObjectId

class Node(BaseModel):
    id: str
    data_in: Dict[str, str]
    data_out: Dict[str, str]
    paths_in: List[str] = []   
    paths_out: List[str] = []   

class Edge(BaseModel):
    id: str
    src_node: str
    dst_node: str
    src_to_dst_data_keys: Dict[str, str]

class Graph(BaseModel):
    id: str
    nodes: List[Node]
    edges: List[Edge]

class RunConfig(BaseModel):
    root_inputs: Dict[str, Dict[str, str]]
    data_overwrites: Optional[Dict[str, Dict[str, str]]] = None
    enable_list: Optional[List[str]] = None
    disable_list: Optional[List[str]] = None

class RunOutput(BaseModel):
    run_id: str
    graph_id: str
    node_outputs: Dict[str, Dict[str, str]]
