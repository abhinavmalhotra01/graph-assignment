import asyncio
from app.models import Graph, Node, Edge
from app.utils.api import create_graph
from app.utils.database import db  # Import the db instance to initiate a connection

async def setup_sample_data():
    """
    make a sample graph and insert it into db
    """
    # Define sample nodes and edges
    node_a = Node(id="A", data_out={"out_a": "value_a"})
    node_b = Node(id="B", data_in={"in_b": "value_b"}, data_out={"out_b": "value_b"})
    node_c = Node(id="C", data_in={"in_c": "value_c"})

    edge_a_b = Edge(src_node="A", dst_node="B", src_to_dst_data_keys={"out_a": "in_b"})
    edge_b_c = Edge(src_node="B", dst_node="C", src_to_dst_data_keys={"out_b": "in_c"})

    # Define a sample graph
    sample_graph = Graph(id="graph1", nodes=[node_a, node_b, node_c], edges=[edge_a_b, edge_b_c])

    # Insert the graph into MongoDB
    graph_id = await create_graph(sample_graph)
    print(f"Inserted sample graph with id: {graph_id}")

async def main():
    # Dropping existing data if needed for clean setup
    await db["graphs"].drop()
    print("Dropped existing data from graphs collection.")

    # Populate the database with sample data
    await setup_sample_data()
    print("Database setup complete with sample data.")

if __name__ == "__main__":
    asyncio.run(main())
