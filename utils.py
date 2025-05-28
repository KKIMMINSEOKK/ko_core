import networkx as nx

def load_graph(hypergraph_path, digraph_path):
    graph = nx.Graph()  # Create an empty graph
    HE = list()
    DE = list()

    with open(hypergraph_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            # Use set to ignore duplicate values in each line and strip whitespace from node names
            nodes = {node.strip() for node in line.strip().split(',')}
            nodes = {int(x) for x in nodes}
            hyperedge = set(nodes)  # Use frozenset to represent the hyperedge
            HE.append(hyperedge)
            for node in nodes:
                if node not in graph.nodes():
                    graph.add_node(node, hyperedges=list(), in_neighbors=list(), out_neighbors=list())  # Add a node for each node
                graph.nodes[node]['hyperedges'].append(hyperedge)  # Add the hyperedge to the node's hyperedge set

    with open(digraph_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            nodes = [node.strip() for node in line.strip().split(',')]
            nodes = [int(x) for x in nodes]
            directed_edge = list(nodes)
            DE.append(directed_edge)
            if nodes[0] not in graph.nodes():
                graph.add_node(nodes[0], hyperedges=list(), in_neighbors=list(), out_neighbors=list())  # Add a node for each node
            graph.nodes[nodes[0]]['out_neighbors'].append(nodes[1])  # Add the directed_edge to the node's directed_edge set
            if nodes[1] not in graph.nodes():
                graph.add_node(nodes[1], hyperedges=list(), in_neighbors=list(), out_neighbors=list())  # Add a node for each node
            graph.nodes[nodes[1]]['in_neighbors'].append(nodes[0])  # Add the directed_edge to the node's directed_edge set

    return graph, HE, DE

def load_graph_2(hypergraph_path, digraph_path):
    graph = nx.Graph()  # Create an empty graph
    HE = {}
    DE = list()

    # print('start loading hyperedges')

    with open(hypergraph_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            # Use set to ignore duplicate values in each line and strip whitespace from node names
            nodes = {node.strip() for node in line.strip().split(',')}
            nodes = {int(x) for x in nodes}
            if len(nodes) < 2:
                print('edge size 1 is detected:', nodes)
            hyperedge = set(nodes)  # Use frozenset to represent the hyperedge
            hyperedge_id = len(HE) + 1
            HE[hyperedge_id] = hyperedge
            for node in nodes:
                if node not in graph.nodes():
                    graph.add_node(node, hyperedges=list(), in_neighbors=list(), out_neighbors=list())  # Add a node for each node
                graph.nodes[node]['hyperedges'].append(hyperedge_id)  # Add the hyperedge to the node's hyperedge set

    # print('successfully loaded hyperedges')
    # print('start loading directed edges')

    with open(digraph_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            nodes = [node.strip() for node in line.strip().split(',')]
            nodes = [int(x) for x in nodes]
            directed_edge = list(nodes)
            DE.append(directed_edge)
            if nodes[0] not in graph.nodes():
                graph.add_node(nodes[0], hyperedges=list(), in_neighbors=list(), out_neighbors=list())  # Add a node for each node
            graph.nodes[nodes[0]]['out_neighbors'].append(nodes[1])  # Add the directed_edge to the node's directed_edge set
            if nodes[1] not in graph.nodes():
                graph.add_node(nodes[1], hyperedges=list(), in_neighbors=list(), out_neighbors=list())  # Add a node for each node
            graph.nodes[nodes[1]]['in_neighbors'].append(nodes[0])  # Add the directed_edge to the node's directed_edge set
    
    # print('successfully loaded directed edges')

    return graph, HE, DE