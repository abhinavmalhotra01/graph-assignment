# tests/test_graph_operations.py
import pytest
from utils import setup_sample
from main import run_graph_operations
from models.models import Graph, Node, Edge, GraphRunConfig


# Test graph operations with various configurations and expected outputs
@pytest.mark.parametrize(
    "graph, config, expected_outputs",
    [
        (
            # single node with no edges
            setup_sample.get_sample_graph(
                nodes=[Node(id="A", data_out={"out_a": 10})], edges=[]  # Nodes
            ),  # Edges
            setup_sample.get_sample_config(root_inputs={"A": {"out_a": 20}}),  # Config
            {
                "output_b": None,
                "leaf_outputs": {"A": {"out_a": 10}},
                "islands": [["A"]],
            },
        ),
        (
            # 3 nodes with simple linear dependency
            setup_sample.get_sample_graph(
                nodes=[
                    Node(id="A", data_out={"out_a": 10}),
                    Node(id="B", data_in={"in_b": None}, data_out={"out_b": 20}),
                    Node(id="C", data_in={"in_c": None}),
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
        (
            # Graph with Dependency Edge Only (No Data Transfer)
            setup_sample.get_sample_graph(
                nodes=[
                    Node(id="A", data_out={"out_a": 10}),
                    Node(id="B", data_in={"in_b": None}),
                ],
                edges=[
                    Edge(
                        src_node="A", dst_node="B", src_to_dst_data_keys={}
                    ),  # Dependency without data transfer
                ],
            ),
            setup_sample.get_sample_config(root_inputs={"A": {"out_a": 10}}),
            {
                "output_b": {},
                "leaf_outputs": {"B": {}},
                "islands": [["A", "B"]],
            },
        ),
        (
            setup_sample.get_sample_graph(
                nodes=[
                    Node(id="A", data_out={"out_a": 10}),
                    Node(id="B", data_in={"in_b": None}, data_out={"out_b": 20}),
                    Node(id="C", data_in={"in_c": None}),
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
                root_inputs={"A": {"out_a": 15}}, data_overwrites={"B": {"out_b": 25}}
            ),
            {
                "output_b": {"out_b": 20},
                "leaf_outputs": {"C": {}},
                "islands": [["A", "B", "C"]],
            },
        ),
        # This TC should fail, since, C is disabled and it is being used in edge/node
        (
            setup_sample.get_sample_graph(
                nodes=[
                    Node(id="A", data_out={"out_a": 10}),
                    Node(id="B", data_in={"in_b": None}, data_out={"out_b": 20}),
                    Node(id="C", data_in={"in_c": None}),
                    Node(id="D", data_in={"in_d": None}),
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
                    Edge(
                        src_node="C",
                        dst_node="D",
                        src_to_dst_data_keys={"out_c": "in_d"},
                    ),
                ],
            ),
            setup_sample.get_sample_config(
                root_inputs={"A": {"out_a": 15}}, disable_list=["C"]
            ),
            {
                "output_b": {"in_b": 15},
                "leaf_outputs": {"B": {"out_b": 20}},
                "islands": True,
            },
        ),
    ],
)
def test_graph_run_operations(graph, config, expected_outputs):
    """
    Run a series of tests on graph operations:
    - Verifies run ID format
    - Checks node output consistency
    - Validates leaf nodes and islands in graph
    """

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
