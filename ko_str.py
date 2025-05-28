from queue import Queue

### python3 main.py --hypergraph ./ex1.hyp --digraph ./ex2.dir --algorithm ko --k 1 --o 1 ###
### python3 main.py --hypergraph ./datasets/chameleon.hyp --digraph ./datasets/chameleon.dir --algorithm ko --k 2 --o 2 ###

def run(graph, k, o):

    ##### UTILS_CHECK #####
    # H = set(graph.nodes())
    # for node in H:
    #     print("node:", node)
    #     print("hyperedges:")
    #     for hyperedge in graph.nodes[node]['hyperedges']:
    #         print(hyperedge)
    #     print("in-neighbors:")
    #     for in_node in graph.nodes[node]['in_neighbors']:
    #         print(in_node)
    #     print("in-degree:", len(graph.nodes[node]['in_neighbors']))
    #     print("out-neighbors:")
    #     for out_node in graph.nodes[node]['out_neighbors']:
    #         print(out_node)
    #     print("out-degree:", len(graph.nodes[node]['out_neighbors']))
    #     print('')

    ##### INITIALIZE #####
    V = set(graph.nodes)
    Q = Queue()

    ##### CONSTRAINT_CHECK #####
    # V
    for node in graph.nodes:
        # at least k hyperedges
        if len(graph.nodes[node]['hyperedges']) < k:
            Q.put(node)
        # at least o outgoing-edges
        elif len(graph.nodes[node]['out_neighbors']) < o:
            Q.put(node)

    ##### PEELING #####
    # V
    while not Q.empty():
        u = Q.get()

        # E_H * V
        for hyperedge in graph.nodes[u]['hyperedges']:
            for v in hyperedge:
                if v != u:
                    graph.nodes[v]['hyperedges'].remove(hyperedge)
                    if len(graph.nodes[v]['hyperedges']) < k and v not in list(Q.queue):
                        Q.put(v)

        # E_D
        for in_neighbor in graph.nodes[u]['in_neighbors']:
            if u in graph.nodes[in_neighbor]['out_neighbors']:
                graph.nodes[in_neighbor]['out_neighbors'].remove(u)
            if len(graph.nodes[in_neighbor]['out_neighbors']) < o and in_neighbor not in list(Q.queue):
                Q.put(in_neighbor)
        for out_neighbor in graph.nodes[u]['out_neighbors']:
            if u in graph.nodes[out_neighbor]['in_neighbors']:
                graph.nodes[out_neighbor]['in_neighbors'].remove(u)

        V.remove(u)

    return graph.subgraph(V)