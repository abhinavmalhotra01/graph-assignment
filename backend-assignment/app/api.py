import os
from motor.motor_asyncio import AsyncIOMotorClient
from .models import Graph, RunOutput
from .serializers import serialize_graph, deserialize_graph, serialize_run_output, deserialize_run_output
from app.database import db


async def create_graph(graph: Graph):
    """
    Create graph using data provided in body of request
    Inserting is done, assuming graph body will be deserialized version, we will store serialize verion in DB
    Because we are using MongoDB as database, JSON are better choice to store in DB
    """
    result = await db["graphs"].insert_one(serialize_graph(graph))
    return result.inserted_id

async def get_graph(graph_id: str):
    """
    Get a existing graph from DB based on graph_id
    It will return a deserialized version of graph
    """
    graph_data = await db["graphs"].find_one({"_id": graph_id})
    return deserialize_graph(graph_data) if graph_data else None

async def update_graph(graph_id: str, update_data: dict) -> bool:
    """
    Update an existing graph based on graph_id and provided update_data
    """
    result = await db["graphs"].update_one({"id": graph_id}, {"$set": update_data})
    return result.modified_count > 0

async def delete_graph(graph_id: str) -> bool:
    """
    Delete an existing graph based on graph_id
    """
    result = await db["graphs"].delete_one({"id": graph_id})
    return result.deleted_count > 0

# Similarly implement update, delete, and query operations


async def save_run_output(run_output: RunOutput):
    """ Saves RunOutput to the database """
    result = await db["run_outputs"].insert_one(serialize_run_output(run_output))
    return result.inserted_id

async def get_run_output(run_id: str):
    """ Retrieves a RunOutput from the database by run_id """
    data = await db["run_outputs"].find_one({"run_id": run_id})
    return deserialize_run_output(data) if data else None
