from collections import deque, defaultdict

# This is the same function from algo-assignment
def toposort(graph):
    execution_order = []
    level_map = defaultdict(list)
    node_map = {node.id: node for node in graph.nodes}
    
    in_degrees = {node.id: 0 for node in graph.nodes}
    for node in graph.nodes:
        for edge in node.paths_out:
            in_degrees[edge.dst_node] += 1
            
    queue = deque(
        [node.id for node in graph.nodes if in_degrees[node.id] == 0]
    )
    
    level = 0
    visited = set()
    while queue:
        level_size = len(queue)
        
        while level_size > 0:
            id = queue.popleft()
            
            if id not in visited:  # Ensure each node is processed only once
                visited.add(id)
                execution_order.append(id)  # Add to topological order
                level_map[level].append(id)  # Add to current level
                
                for edge in node_map[id].paths_out:
                    dst_node = edge.dst_node
                    in_degrees[dst_node] -= 1
                    if in_degrees[dst_node] == 0:
                        queue.append(dst_node)
                        
            level_size -= 1
        level += 1
    return [execution_order, level_map, node_map]

# This is same function as algo assignment
def overwrite_traversals(graph, config, execution_order, level_map, node_map):
    run_data = {}
    
    for id, inputs in config.root_inputs.items():
            if id in node_map:
                node_map[id].data_in.update(inputs)
                
    for id, overwrites in config.data_overwrites.items():
            if id in node_map:
                node_map[id].data_in.update(overwrites)
                
    for level in sorted(level_map.keys()):
            nodes_at_level = sorted(level_map[level], key=lambda nid: nid)
            for id in nodes_at_level:
                node = node_map[id]
                for edge in node.paths_in:
                    src_node = node_map[edge.src_node]
                    for src_key, dst_key in edge.src_to_dst_data_keys.items():
                        if dst_key in node.data_in:
                            # Current node has a value for dst_key, apply overwriting rules
                            current_level = level_map[id]
                            src_level = level_map[src_node.id]
                            if src_level > current_level or (
                                src_level == current_level
                                and src_node.id < id
                            ):
                                node.data_in[dst_key] = src_node.data_out[src_key]
                        else:
                            node.data_in[dst_key] = src_node.data_out[src_key]

                run_data[id] = node.data_out

    updated_level_wise = {}
    for k, v in level_map.items():
        if len(v):
            updated_level_wise[k] = v
            
    level_map = updated_level_wise           
    return [updated_level_wise, node_map, run_data]