# tests/test_graph_operations.py
import pytest
from utils import setup_sample
from main import run_graph_operations
from models.models import Graph, Node, Edge, GraphRunConfig


@pytest.mark.parametrize(
    "graph, config, expected_outputs",
    [
        (
            setup_sample.get_sample_graph(
                nodes=[
                    Node(node_id="A", data_out={"out_a": 10}),
                    Node(node_id="B", data_in={"in_b": None}, data_out={"out_b": 20}),
                    Node(node_id="C", data_in={"in_c": None}),
                ],
                edges=[
                    Edge(
                        src_node="A",
                        dst_node="B",
                        src_to_dst_data_keys={"out_a": "in_b"},
                    ),
                    Edge(
                        src_node="B",
                        dst_node="C",
                        src_to_dst_data_keys={"out_b": "in_c"},
                    ),
                ],
            ),
            setup_sample.get_sample_config(
                root_inputs={"A": {"out_a": 15}},
                data_overwrites={"B": {"in_b": 25}},
                enable_list=["A", "B", "C"],
            ),
            {
                "output_b": {"out_b": 20},
                "leaf_outputs": {"C": {}},
                "islands": [["A", "B", "C"]],
            },
        ),
    ],
)
def test_graph_run_operations(graph, config, expected_outputs):

    # Call the main function to get results
    results = run_graph_operations(graph, config)

    # Check if run_id is correctly formatted
    assert isinstance(results["run_id"], str), "run_id format mismatch"

    # Verify output for Node B
    assert (
        results["output_B"] == expected_outputs["output_b"]
    ), "Unexpected output for Node B"

    # Check leaf outputs
    assert (
        results["leaf_outputs"] == expected_outputs["leaf_outputs"]
    ), "Leaf output mismatch"

    # Check islands
    assert results["islands"] == expected_outputs["islands"], "Islands result mismatch"


if __name__ == "__main__":
    pytest.main(["-v", "tests/test_graph.py"])
