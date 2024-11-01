import uuid
from models.models import Graph, Node, Edge, GraphRunConfig
from utils.graph_runner import GraphRunner
from utils.graph_validators import GraphValidator
from utils.setup_sample import get_sample_config, get_sample_graph


def validate_graph(graph, config):
    """
    Validate the graph, execute it, and return a run_id with results
    """

    try:
        validator = GraphValidator(graph=graph)
        validator.validate_edge_compatibility()
        validator.detect_cycle()
        validator.check_islands()

        return True
    except Exception as e:
        raise ValueError("Graph failed validation checks", e)


def run_graph_operations(graph, config):
    runner = GraphRunner(graph=graph, config=config)
    run_id = runner.execute()

    toposort_order = runner.execution_order
    level_map = runner.level_map

    output_B = runner.get_node_output(run_id=run_id, id="B")
    leaf_outputs = runner.get_leaf_outputs(run_id=run_id)
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
    """
    try:
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
        config = get_sample_config(
            root_inputs={"A": {"out_a": 15}},
            data_overwrites={"B": {"in_b": 25}},
            enable_list=["A", "B", "C"],
        )

        results = run_graph_operations(graph, config)

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
