import uuid
from collections import deque, defaultdict
from models.models import Graph, Node, Edge, GraphRunConfig


class GraphRunner:
    """
    Class to execute and manage runs for a graph with data flow,
    including graph traversal, level-wise traversal, execution, and island detection.
    """

    def __init__(self, graph: Graph, config: GraphRunConfig):
        self.graph = graph
        self.config = config
        self.node_map = {node.id: node for node in graph.nodes}
        self.execution_order = []  # Hold nodes in execution order after toposort
        self.level_map = defaultdict(list)
        self.run_data = {}  # store outputs for each run_id

    def generate_run_id(self):
        return str(uuid.uuid4())  # Generate a unique run ID for each graph execution.

    def toposort(self):
        """
        Perform topological sort and level-wise organization for the nodes in the graph.

        Returns:
            list: list of node IDs in topological order.
        """

        # Following standard topological sorting algo using indegree and BFS

        in_degrees = {node.id: 0 for node in self.graph.nodes}
        for node in self.graph.nodes:
            for edge in node.paths_out:
                in_degrees[edge.dst_node] += 1

        queue = deque(
            [node.id for node in self.graph.nodes if in_degrees[node.id] == 0]
        )
        level = 0
        visited = set()

        # Process each node level by level
        while queue:
            level_size = len(queue)
            while level_size > 0:
                id = queue.popleft()
                if id not in visited:  # Process each node only once
                    visited.add(id)
                    self.execution_order.append(id)  # Add to topological order
                    self.level_map[level].append(id)  # Add to current level

                    for edge in self.node_map[id].paths_out:
                        dst_node = edge.dst_node
                        in_degrees[dst_node] -= 1
                        if in_degrees[dst_node] == 0:
                            queue.append(dst_node)

                level_size -= 1
            level += 1
        return self.execution_order

    def execute(self):
        """
        Execute the graph based on the provided config. This includes setting up initial inputs,
        applying data overwrites, and running level-wise traversal to process data flow.

        Returns:
            str: The generated run_id for this run.
        """

        # generate run_id for this run
        run_id = self.generate_run_id()
        self.run_data[run_id] = {}

        self.toposort()  # Determine execution order via topological sorting

        # Initialize root nodes with provided root inputs
        for id, inputs in self.config.root_inputs.items():
            if id in self.node_map:
                self.node_map[id].data_in.update(inputs)

        # Apply data overwrites
        for id, overwrites in self.config.data_overwrites.items():
            if id in self.node_map:
                self.node_map[id].data_in.update(overwrites)

        # Overwriting Level wise traversal
        for level in sorted(self.level_map.keys()):
            nodes_at_level = sorted(self.level_map[level], key=lambda nid: nid)
            for id in nodes_at_level:
                node = self.node_map[id]

                # Apply overwriting rules based on source and destination nodes
                for edge in node.paths_in:
                    src_node = self.node_map[edge.src_node]
                    for src_key, dst_key in edge.src_to_dst_data_keys.items():
                        if dst_key in node.data_in:
                            # Current node has a value for dst_key, apply overwriting rules
                            current_level = self.level_map[id]
                            src_level = self.level_map[src_node.id]
                            if src_level > current_level or (
                                src_level == current_level and src_node.id < id
                            ):
                                node.data_in[dst_key] = src_node.data_out[src_key]
                        else:
                            node.data_in[dst_key] = src_node.data_out[src_key]

                # Store data outputs for the node in the current run
                # We can store data_in also, considering the tests, currently only out is stored
                self.run_data[run_id][id] = {
                    # "data_in": node.data_in,
                    "data_out": node.data_out
                }

        # Remove empty levels from level_map for clarity
        updated_level_wise = {k: v for k, v in self.level_map.items() if len(v)}
        self.level_map = updated_level_wise

        return run_id

    def get_node_output(self, id, run_id):
        # Get run ouput based on node_id
        return self.run_data.get(run_id, {}).get(id, None)

    def get_leaf_outputs(self, run_id):
        """
        Retrieve outputs for leaf nodes in the graph for a specific run.
        """

        leaf_outputs = {}
        for id, node in self.node_map.items():
            if len(node.paths_out) == 0:  # identify leaf nodes
                leaf_outputs[id] = self.get_node_output(run_id=run_id, id=id)
        return leaf_outputs

    def check_islands(self):
        """
        Identify disconnected components (islands) in the graph.
        
        Returns:
            list: List of islands, where each island is represented as a list of node IDs.
        """
        
        visited = set()
        islands = []

        def dfs(id, current_island):
            """
            Perform DFS to explore all nodes in a connected component.
            """
            
            # iterate over each neighbor of current node_id and maintain stack for iteration 
            stack = [id]
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    current_island.append(current)
                    node = self.node_map[current]

                    for edge in node.paths_in + node.paths_out:
                        neighbor_id = (
                            edge.src_node if edge.src_node != current else edge.dst_node
                        )
                        stack.append(neighbor_id)

        # Detect each disconnected component by DFS on unvisited nodes
        for id in self.node_map:
            if id not in visited:
                current_island = []
                dfs(id=id, current_island=current_island)
                if current_island:
                    islands.append(current_island)

        return islands
