from fastapi import APIRouter, HTTPException
from app.models import Graph, RunConfig
from app.api import create_graph, get_graph, update_graph, delete_graph
from app.graph_operations import run_graph

router = APIRouter()

@router.post("/graphs/")
async def create_new_graph(graph: Graph):
    """
    route to create new graph
    """
    graph_id = await create_graph(graph)
    return {"graph_id": str(graph_id)}

@router.get("/graphs/{graph_id}")
async def get_graph_by_id(graph_id: str):
    """
    route to get a existing graph based on graph_id
    """
    graph = await get_graph(graph_id)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return graph

@router.put("/graphs/{graph_id}")
async def update_graph_by_id(graph_id: str, graph_update: Graph):
    """
    Route to update data in an existing graph based on updated graph data and graph_id
    """
    update_data = graph_update.dict(exclude_unset=True)
    success = await update_graph(graph_id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Graph not found or update failed")
    return {"message": "Graph updated successfully"}

@router.delete("/graphs/{graph_id}")
async def delete_graph_by_id(graph_id: str):
    """
    Delete graph based on graph_id
    """
    success = await delete_graph(graph_id)
    if not success:
        raise HTTPException(status_code=404, detail="Graph not found or deletion failed")
    return {"message": "Graph deleted successfully"}

# this logic has been shifted to run_router
# @router.post("/graphs/run")
# async def run_graph_api(config: RunConfig, graph_id: str):
#     try:
#         graph = await get_graph(graph_id=graph_id)
#         results = await run_graph(config=config, graph=graph)
#         return {"run_id": results["run_id"], "outputs": results["outputs"]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
