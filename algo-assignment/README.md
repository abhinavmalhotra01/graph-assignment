# Algo assignment

I have made this, based on the goals I understood from the problem statement.

Algorithms implemented:
Setting up graph and config, Topological sort, Detect cycle, Level wise map, Leaf output, Check Island

main.py is the entrypoint file for the codebase.

## The basic flow to run testcase: 
<ul>
<li> enter test graph data in tests/test_graph.py file </li>
<li> enter expected results in same file </li>
<li> run pytest </li>
</ul>

## Flow of data:
<ul>
<li> set sample graph data (nodes, edge) and config data (root inputs, data overwrites, enable/disable list) </li>
<li> Run the graph operations (set data in data structure, topo sort, level wise traversal, leaves, islands identification)</li>
<li> Check validation of graph and config (validation includes edge compatibility, detecting cycle )</li>
<li> Assertions are implemented in tests</li>
</ul>

I have tried to write code in a scalable manner and modular manner. The code is distributed into functions and generalized format. Scalablity is another aspect, to add new feature in the algorithm which can be implemented easily without much effort.

Regarding the key algorithms, Standard algorithms are utilized with optimized time complexity ->
<ul>
<li> Topological sort -> O(N+E) -> each node is iterated once, using BFS</li>
<li> Level wise -> O(N) -> iterating level wise to overwrite data nodes, iterate each node once </li>
<li> Detect cycle -> O(N) -> using DFS</li>
<li> Check island -> O(N+E) -> using DFS, iterating each node once
</ul>