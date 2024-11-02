# Backend assignment

This is made using FastAPI

## Project setup:
If you are using docker:
<ul>
Dockerfile will take care of setup and requirements
<li> docker build -t fastapi-backend. </li>
<li> docker run -p 8000:8000 fastapi-backend </li>
</ul>
Otherwise:
<ul>
<li> Clone the repo </li>
<li> cd backend-assignment </li>
<li> pip install -r requirements.txt </li>
<li> python app/setup_backend.py </li>
<li> python -m fastapi dev app/main.py --host 0.0.0.0 --port 8000 </li>
</ul>

## Tech stack
FastAPI, MongoDB

## API Endpoints
/graphs/ -> include graph CRUD methods <br/>
/runs/ -> include run CRUD methods on provided graph

## App design
Design is based on my limited knowledge, I havent used any design pattern to implement classes. <br/>
The app is divided based on graph_operations as instructed and FastAPI was the choice of techstack due to easy setup and simple file structure. <br/>
<li> MongoDB contains schema of each entity, there is no foreign key or referential constraint among them. </li>
<li> Graph APIs are used to perform CRUD for any entry, entries are differentiated based on graph_id. For creating graph entity, request body must contain the complete node, edges array and nested dictionaries, in a Graph class type. </li>
<li> The above Graph type object is serialized to JSON and then inserted into DB. Any existing entry in DB can be fetched using graph_id, which will then be deserialized to send to frontend. Similarly for update and delete operations, graph_id is required to fetch entry and perform subsequent operation. </li>
<li> For running the graph, graph_id and config is required, the corresponding graph must exist in DB beforehand, which will then be executed i.e. topological sort and level wise traversal. The run entity i.e. node_map (this is my assumption to store node_map as run) alongside run_id to differentiate between different runs. </li>
<li> Data overwriting based on config is also taken care of. output for any node can be retrieved from run_data based on node_id. Similar to graph, serialization and deserialization is used while fetching and storing to DB. </li>


## Code structure
<ul>
<li> I tried to design modular and scalabale code structure and follow best practices. </li>
<li> root dir of app, contains generic files like models, main. </li>
<li> setup_backend is required to be executed beforehand, to populate a testcase in the db. </li>
<li> entry point of app is main.py which includes routers file. </li>
<li> routers folder contains graph_router and run_router which contain corresponding endpoints. </li>
<li> Utils contains helper files, like, db_connection, validator, serializers, etc. </li>
</ul>

