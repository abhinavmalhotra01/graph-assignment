from bson import ObjectId
from app.models import Graph, RunOutput

def serialize_graph(graph) -> dict:
    return {
        "_id": str(graph.id),
        "nodes": [node.dict() for node in graph.nodes],
        "edges": [edge.dict() for edge in graph.edges]
    }

def deserialize_graph(data) -> Graph:
    # mongo_db renames id to _id, but Graph class expects id as key
    data["id"] = data.pop("_id")
    return Graph(**data)

def serialize_run_output(run_output: RunOutput) -> dict:
    return {
        "run_id": run_output.run_id,
        "graph_id": run_output.graph_id,
        "node_outputs": run_output.node_outputs
    }

def deserialize_run_output(data) -> RunOutput:
    return RunOutput(**data)