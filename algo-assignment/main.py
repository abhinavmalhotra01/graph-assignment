import uuid
from models.models import Graph, Node, Edge, GraphRunConfig
from utils.graph_runner import GraphRunner
from utils.graph_validators import GraphValidator
from utils.setup_sample import get_sample_config, get_sample_graph


def validate_graph(graph, config):
    """
    Validate the graph
    Validation includes checking edge's datatype compatibility, detect any cycle in graph and detect islands
    
    Args:
        Graph: List of nodes which are part of it
        Config: List of root input nodes, Data overwrites if any, List of enable/disable nodes in current validation
        
    Returns:
        Boolean: Return if graph is valid and raise error if not
    """

    try:
        # make a validator object from validator class, providing graph as input
        validator = GraphValidator(graph=graph)
        
        # calling validation methods, if any of the method fails, it will raise exception at that line and hence error will be raised
        validator.validate_edge_compatibility()
        validator.detect_cycle()
        validator.check_islands()

        return True
    except Exception as e:
        raise ValueError("Graph failed validation checks", e)


def run_graph_operations(graph, config):
    """
    Execute graph operations, which includes performing toposort, level wise traversal, overwrite data based on config
    and produce a node_map (contains output data for each node)
    
    Args:
        Graph: List of nodes which are part of it
        Config: List of root input nodes, Data overwrites if any, List of enable/disable nodes in current validation
        
    Returns:
        ReturnObject: contains desired data regarding run object of graph
            run_id: Unique id for each run object
            output_B: this is assumed data output for "B" node for sample test_case, this should be modified if data is required for some other node
            leaf_outputs: contains node's output data for each leaf node
            islands: contains 2D array of islands of graph -> each entry in outer list -> different unique island
            toposort_order: topological execution order of graph based on src,dst key by using BFS for implementation
            level_map: contains level map for graph -> each key is a level index -> each value is a list of node_id in that respective level
    """
    
    # create a runner object based on graph, config and execute the run operation on that object
    runner = GraphRunner(graph=graph, config=config)
    run_id = runner.execute()

    # store the topological ordering and level map in different variables
    toposort_order = runner.execution_order
    level_map = runner.level_map
    
    # get output for a specific node ("B" in this case)
    output_B = runner.get_node_output(run_id=run_id, id="B")
    
    # get leaf outputs for the graph nodes
    leaf_outputs = runner.get_leaf_outputs(run_id=run_id)
    
    # get islands list for graph
    islands = runner.check_islands()

    return {
        "run_id": run_id,
        "output_B": output_B,
        "leaf_outputs": leaf_outputs,
        "islands": islands,
        "toposort_order": toposort_order,
        "level_map": dict(level_map),
    }


def main():
    """
    Set up, validate, execute graph and retrieve output
    This fn is to execute the codebase on a sample graph (other graphs are implemented in `tests/test_graph.py' alongside assertion statements)
    The idea behind this is to create a sample graph and config, followed by execution of traversal algorithms on the graph
    It is followed by validation of graph, which if fails, will lead to raise error
    The outputs are then printed.
    """
    try:
        
        # setup a sample graph with 3 nodes and linear structure
        graph = get_sample_graph(
            nodes=[
                Node(id="A", data_out={"out_a": 10}),
                Node(id="B", data_in={"in_b": None}, data_out={"out_b": 20}),
                Node(id="C", data_in={"in_c": None}),
            ],
            edges=[
                Edge(
                    src_node="A", dst_node="B", src_to_dst_data_keys={"out_a": "in_b"}
                ),
                Edge(
                    src_node="B", dst_node="C", src_to_dst_data_keys={"out_b": "in_c"}
                ),
            ],
        )
        
        # setup a sample config with input and data which can be overwritten and nodes which are currently active in graph
        config = get_sample_config(
            root_inputs={"A": {"out_a": 15}},
            data_overwrites={"B": {"in_b": 25}},
            enable_list=["A", "B", "C"],
        )
        
        # get results based on above explained executor function
        results = run_graph_operations(graph, config)

        # validate the populated graph structure
        if validate_graph(graph=graph, config=config):
            print("Graph passed all validation checks")

        print("Run ID: ", results["run_id"])
        print("Output for Node B: ", results["output_B"])
        print("Leaf Outputs: ", results["leaf_outputs"])
        print("Islands in the graph: ", results["islands"])
        print("Topological order: ", results["toposort_order"])
        print("Level wise traversal: ", results["level_map"])
    except Exception as e:
        print("Some error occured in running main fn: ", e)


if __name__ == "__main__":
    main()
