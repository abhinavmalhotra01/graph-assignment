import asyncio
from app.api import create_graph
from app.models import Graph, Node, Edge
from app.database import db 

async def populate_sample_graph():
    # Defining sample nodes and edges
    node_a = Node(id="A", data_in={}, data_out={"out_a": "sample_output"})
    node_b = Node(id="B", data_in={"in_b": "sample_input"}, data_out={"out_b": "sample_output_b"})
    edge_a_b = Edge(id="E1", src_node="A", dst_node="B", src_to_dst_data_keys={"out_a": "in_b"})

    # Defining graph
    sample_graph = Graph(id="G1", nodes=[node_a, node_b], edges=[edge_a_b])

    # Insert into the database
    await create_graph(sample_graph)
    print("Sample graph added to the database")

if __name__ == "__main__":
    asyncio.run(populate_sample_graph())
