from fastapi import APIRouter, HTTPException
from app.models import Graph, RunConfig
from app.api import create_graph, get_graph
from app.graph_operations import run_graph

router = APIRouter()

@router.post("/graphs/")
async def create_new_graph(graph: Graph):
    graph_id = await create_graph(graph)
    return {"graph_id": str(graph_id)}

@router.get("/graphs/{graph_id}")
async def get_graph_by_id(graph_id: str):
    graph = await get_graph(graph_id)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return graph

# @router.post("/graphs/run")
# async def run_graph_api(config: RunConfig, graph_id: str):
#     try:
#         graph = await get_graph(graph_id=graph_id)
#         results = await run_graph(config=config, graph=graph)
#         return {"run_id": results["run_id"], "outputs": results["outputs"]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
