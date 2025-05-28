from queue import Queue

### python3 main.py --hypergraph ./datasets/meetup/network.hyp --digraph ./datasets/meetup/network.dir --algorithm ko --k 2 --o 2 ###

def run(graph, HE, k, o):

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

            for hyperedge_id in graph.nodes[u]['hyperedges']:
                HE[hyperedge_id].remove(u)
                if len(HE[hyperedge_id]) < 2:
                    v = HE[hyperedge_id].pop()
                    graph.nodes[v]['hyperedges'].remove(hyperedge_id)
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

                for hyperedge_id in graph.nodes[u]['hyperedges']:
                    HE[hyperedge_id].remove(u)
                    if len(HE[hyperedge_id]) < 2:
                        v = HE[hyperedge_id].pop()
                        graph.nodes[v]['hyperedges'].remove(hyperedge_id)

    return graph.subgraph(V)