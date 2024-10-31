import uuid
from collections import deque, defaultdict
from models.models import Graph, Node, Edge, GraphRunConfig


class GraphRunner:
    def __init__(self, graph: Graph, config: GraphRunConfig):
        self.graph = graph
        self.config = config
        self.node_map = {node.node_id: node for node in graph.nodes}
        self.execution_order = []  # Holds nodes in execution order after toposort
        self.level_map = defaultdict(list)
        self.run_data = {}  # store outputs for each run_id

    def generate_run_id(self):
        return str(uuid.uuid4())

    def toposort(self):
        in_degrees = {node.node_id: 0 for node in self.graph.nodes}
        for node in self.graph.nodes:
            for edge in node.paths_out:
                in_degrees[edge.dst_node] += 1

        queue = deque(
            [node.node_id for node in self.graph.nodes if in_degrees[node.node_id] == 0]
        )
        level = 0
        visited = set()
        while queue:
            level_size = len(queue)
            while level_size > 0:
                node_id = queue.popleft()
                if node_id not in visited:  # Ensure each node is processed only once
                    visited.add(node_id)
                    self.execution_order.append(node_id)  # Add to topological order
                    self.level_map[level].append(node_id)  # Add to current level

                    for edge in self.node_map[node_id].paths_out:
                        dst_node = edge.dst_node
                        in_degrees[dst_node] -= 1
                        if in_degrees[dst_node] == 0:
                            queue.append(dst_node)

                level_size -= 1
            level += 1
        return self.execution_order

    def execute(self):
        # generate run_id for this run
        run_id = self.generate_run_id()
        self.run_data[run_id] = {}

        self.toposort()

        # Initialize root nodes with provided root inputs
        for node_id, inputs in self.config.root_inputs.items():
            if node_id in self.node_map:
                self.node_map[node_id].data_in.update(inputs)

        # Apply data overwrites
        for node_id, overwrites in self.config.data_overwrites.items():
            if node_id in self.node_map:
                self.node_map[node_id].data_in.update(overwrites)

        # Overwriting Level wise traversal
        for level in sorted(self.level_map.keys()):
            nodes_at_level = sorted(self.level_map[level], key=lambda nid: nid)
            for node_id in nodes_at_level:
                node = self.node_map[node_id]
                for edge in node.paths_in:
                    src_node = self.node_map[edge.src_node]
                    for src_key, dst_key in edge.src_to_dst_data_keys.items():
                        if dst_key in node.data_in:
                            # Current node has a value for dst_key, apply overwriting rules
                            current_level = self.level_map[node_id]
                            src_level = self.level_map[src_node.node_id]
                            if src_level > current_level or (
                                src_level == current_level
                                and src_node.node_id < node_id
                            ):
                                node.data_in[dst_key] = src_node.data_out[src_key]
                        else:
                            node.data_in[dst_key] = src_node.data_out[src_key]

                self.run_data[run_id][node_id] = node.data_out

        updated_level_wise = {}
        for k, v in self.level_map.items():
            if len(v):
                updated_level_wise[k] = v
                
        self.level_map = updated_level_wise
        return run_id

    def get_node_output(self, node_id, run_id):
        return self.run_data.get(run_id, {}).get(node_id, None)

    def get_leaf_outputs(self, run_id):
        # identify leaf nodes
        leaf_outputs = {}
        for node_id, node in self.node_map.items():
            if len(node.paths_out)==0:
                leaf_outputs[node_id] = self.get_node_output(
                    run_id=run_id, node_id=node_id
                )
        return leaf_outputs

    def check_islands(self):
        visited = set()
        islands = []
        
        def dfs(node_id, current_island):
            stack = [node_id]
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

        # dfs(self.graph.nodes[0].node_id)
        for node_id in self.node_map:
            if node_id not in visited:
                current_island = []
                dfs(node_id=node_id, current_island=current_island)
                if current_island:
                    islands.append(current_island)
        
        return islands