import os
from motor.motor_asyncio import AsyncIOMotorClient
from .models import Graph, RunOutput
from .serializers import serialize_graph, deserialize_graph, serialize_run_output, deserialize_run_output
from app.database import db


async def create_graph(graph: Graph):
    result = await db["graphs"].insert_one(serialize_graph(graph))
    return result.inserted_id

async def get_graph(graph_id: str):
    graph_data = await db["graphs"].find_one({"_id": graph_id})
    return deserialize_graph(graph_data) if graph_data else None

# Similarly implement update, delete, and query operations


async def save_run_output(run_output: RunOutput):
    """ Saves RunOutput to the database """
    result = await db["run_outputs"].insert_one(serialize_run_output(run_output))
    return result.inserted_id

async def get_run_output(run_id: str):
    """ Retrieves a RunOutput from the database by run_id """
    data = await db["run_outputs"].find_one({"run_id": run_id})
    return deserialize_run_output(data) if data else None
