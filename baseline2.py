from queue import Queue

### python3 main.py --hypergraph ./ex1.hyp --digraph ./ex2.dir --algorithm ko --k 1 --o 1 ###
### python3 main.py --hypergraph ./datasets/chameleon.hyp --digraph ./datasets/chameleon.dir --algorithm ko --k 2 --o 2 ###

def run(graph, k, o):

    ##### INITIALIZE #####
    V = set(graph.nodes)

    while True:
        Q = Queue()
        RQ = Queue()

        ##### k-hypercore #####
        for node in V:
            if len(graph.nodes[node]['hyperedges']) < k:
                Q.put(node)

        while not Q.empty():
            u = Q.get()

            for hyperedge in graph.nodes[u]['hyperedges']:
                for v in hyperedge:
                    if v != u:
                        graph.nodes[v]['hyperedges'].remove(hyperedge)
                        if len(graph.nodes[v]['hyperedges']) < k and v not in list(Q.queue):
                            Q.put(v)
            V.remove(u)
            RQ.put(u)

        ##### synchronization #####
        while not RQ.empty():
            u = RQ.get()

            for in_neighbor in graph.nodes[u]['in_neighbors']:
                if u in graph.nodes[in_neighbor]['out_neighbors']:
                    graph.nodes[in_neighbor]['out_neighbors'].remove(u)
            for out_neighbor in graph.nodes[u]['out_neighbors']:
                if u in graph.nodes[out_neighbor]['in_neighbors']:
                    graph.nodes[out_neighbor]['in_neighbors'].remove(u)

        ##### o-core #####
        for node in V:
            if len(graph.nodes[node]['out_neighbors']) < o:
                Q.put(node)

        while not Q.empty():
            u = Q.get()
            
            for in_neighbor in graph.nodes[u]['in_neighbors']:
                if u in graph.nodes[in_neighbor]['out_neighbors']:
                    graph.nodes[in_neighbor]['out_neighbors'].remove(u)
                if len(graph.nodes[in_neighbor]['out_neighbors']) < o and in_neighbor not in list(Q.queue):
                    Q.put(in_neighbor)
            for out_neighbor in graph.nodes[u]['out_neighbors']:
                if u in graph.nodes[out_neighbor]['in_neighbors']:
                    graph.nodes[out_neighbor]['in_neighbors'].remove(u)

            V.remove(u)
            RQ.put(u)

        if RQ.empty():
            break
        else:
            while not RQ.empty():
                u = RQ.get()

                for hyperedge in graph.nodes[u]['hyperedges']:
                    for v in hyperedge:
                        if v != u:
                            graph.nodes[v]['hyperedges'].remove(hyperedge)

    return graph.subgraph(V)