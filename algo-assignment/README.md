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

## Algorithm
Once, the graph and config is setup based on testcase, 
A run_operations function is called, which will make object of graphRunner class and execute the run operation <br/>
Now the run operation consists of the following:
<ul>
<li> generate a unique run_id </li>
<li> call topological sort and level-wise traversal fn. </li>
<ol>
<li> the algorithm behind topological sort is to first calculate the indegree of each node and enqueue entries with 0 indegree in the BFS queue. Also, maintain a level_map to store level-wise traversal </li>
<li> Then, following standard BFS approach of selecting the current level of queue, iterating over it's neighbors, update the indegree of respective nodes each time and enqueue nodes with 0 indegree to perform further BFS. </li>
<li> For level wise, while iterating over the queue during BFS, we append the current nodes in the level_map based on current_level. Time complexity of the same is O(N+E) and space complexity is O(N), since we are iterating over each node, edge once.</li>
</ol>
<li> Once, we get the topological execution order and initial level_map, now we have to set the root-inputs and data overwrites from config. Also, we prepare the final run_data.
<ol>
<li> In the node_map, we append the root_input data from the config and also update the data_in based on overwrites in the config. </li>
<li> Now, we perform the overwrites levelwise and also store the output data for each node in the final run object. </li>
<li> Iterating over the level_map, get the nodes at the current level, since, overwrite is concerned only with incoming data, iterate over input paths and update the node's data based on incoming edges and overwrite the data provided first in config. </li>
<li> We can remove empty levels from the final object and return the desired outputs for the run_operation. Time complexity for the same is O(N*E), since we are iterating over each node once, however, depending on the incoming edges, worst case gets higher.</li>
</ol>
</li>
<li>
Another method to get the leaf_outputs, i.e., to get the outputs for leaf nodes, is also quite straightforward, we can iterate over the graph nodes, then the nodes with empty output paths will be leaf nodes. Now, since we have already stored the run object for each node, we can simply append the required data in the output of this current method.
</li>
<li>
Now, to return the list of present islands in the graph, I have used the concept of connected components, wherein, based on a visited set, we can check whether each node is reachable from the current node or not and we can store the reachable nodes in same list, each time, resulting in 2D array of islands. The reachable part is implemented using simple DFS using stack as data structure rather than calling recursion. Time complexity of this method is O(N+E).
</li>
<li> After the operations are executed and graph's data is populated in node_map, level_map, run_data, we can now validate the graph that whether it is a DAG or not.
<ol>
<li> The verification part includes checking edge compatibility based on datatypes, absence of cycle (since, it is DAG) and absence of islands.
</li>
<li> For edge compatibility, the datatype of incoming edge of dst and outgoing of src are compared and an error is raised in case of invalidation.
</li>
<li> For cycle detection, I have used the standard algorithm using DFS, where in we store current path and visited set to compare the paths and detect cycle where we encounter a node that is both in current path and visited set. Similarly, an error is raised in case a cycle is detected.
</li>
<li> For islands, the approach is similar to above in graph_runner, only difference being that this time, we are not actually storing the islands but just validating that the count of islands must be 1.
</li>
</ol>
<li> For testcases, `tests/test_graph.py` can be checked which contains tests and assertions based on my understanding of the problem.
</li>
</ul>