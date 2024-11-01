from fastapi import APIRouter, HTTPException
from app.models import RunConfig, RunOutput
from app.graph_operations import run_graph
from app.api import get_graph, get_run_output, save_run_output

router = APIRouter()

@router.post("/run")
async def execute_graph_run(config: RunConfig, graph_id: str):
    """
    run graph based on config provided in body and graph_id to get graph from db
    """
    graph = await get_graph(graph_id)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    
    results = await run_graph(graph, config)
    run_output = RunOutput(run_id=results["run_id"], graph_id=graph_id, node_outputs=results["outputs"])
    
    # Save run_output in DB and return the result
    await save_run_output(run_output)
    return {"run_id": run_output.run_id, "outputs": run_output.node_outputs}

@router.get("/runs/{run_id}")
async def get_run(run_id: str):
    """
    get run entity based on run_id
    """
    run_output = await get_run_output(run_id)
    if not run_output:
        raise HTTPException(status_code=404, detail="Run output not found")
    return run_output
