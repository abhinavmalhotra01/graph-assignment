from app.models import Graph, RunConfig, RunOutput
from app.utils.validator import validate_graph_structure, generate_unique_run_id
from app.utils.graph_runner import toposort, overwrite_traversals


async def run_graph(graph: Graph, config: RunConfig):
    """
    This is the function to traverse through the graph and return node_map
    The traversal methods are similar to algo assignment
    """
    # Validate graph and configuration
    validate_graph_structure(graph)
    
    # generate run_id
    run_id = generate_unique_run_id()
    
    # call topological sort and store subsequent outputs
    outputs = toposort(graph=graph)
    execution_order = outputs[0]
    level_map = outputs[1]
    node_map = outputs[2]
    
    # overwrite traversal values based on config and overwrites
    updated_outputs = overwrite_traversals(config=config, execution_order=execution_order, graph=graph, level_map=level_map, node_map=node_map)
    updated_level_wise = updated_outputs[0]
    updated_node_map = updated_outputs[1]
    run_data = updated_outputs[2]
    
    
    return {"run_id": run_id, "outputs": run_data}
