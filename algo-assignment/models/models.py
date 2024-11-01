from pydantic import BaseModel, Field, validator, ValidationError
from typing import List, Dict, Optional, Union

# Defining allowed data types in Python for validation
DataType = Union[int, float, str, bool, list, dict, None]

class Edge(BaseModel):
    src_node: str
    dst_node: str
    src_to_dst_data_keys: Dict[str, str] 

class Node(BaseModel):
    id: str
    data_in: Dict[str, DataType] = {}
    data_out: Dict[str, DataType] = {}
    paths_in: List[Edge] = []
    paths_out: List[Edge] = []

class Graph(BaseModel):
    nodes: List[Node] = []

class GraphRunConfig(BaseModel):
    root_inputs: Dict[str, Dict[str, DataType]]
    data_overwrites: Dict[str, Dict[str, DataType]] = {}
    enable_list: Optional[List[str]] = None
    disable_list: Optional[List[str]] = None

    @validator("enable_list", "disable_list")
    def only_one_of_enable_or_disable(cls, v, values, **kwargs):
        if values.get("enable_list") and values.get("disable_list"):
            raise ValueError("Only one of enable_list or disable_list can be provided.")
        return v
