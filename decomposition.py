from queue import Queue
from collections import defaultdict
import copy

def run(graph, HE):
    D = defaultdict(set)

    Q = Queue()
    V = set(graph.nodes)
    for k in range(0, len(HE)): # O(k_max * (E_DH * V^2 + ))

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

            for in_neighbor in graph.nodes[u]['in_neighbors']:
                if u in graph.nodes[in_neighbor]['out_neighbors']:
                    graph.nodes[in_neighbor]['out_neighbors'].remove(u)
            for out_neighbor in graph.nodes[u]['out_neighbors']:
                if u in graph.nodes[out_neighbor]['in_neighbors']:
                    graph.nodes[out_neighbor]['in_neighbors'].remove(u)

            V.remove(u)
        
        if len(V) == 0:
            break

        if k > 100:
            break

        V_ = copy.deepcopy(V)
        HE_ = copy.deepcopy(HE)
        graph_ = copy.deepcopy(graph)

        for o in range(1, len(V)): # O(o_max * V * E_DH)
            for node in V_:
                if len(graph_.nodes[node]['out_neighbors']) < o:
                    Q.put(node)

            while not Q.empty():
                u = Q.get()

                for hyperedge_id in graph_.nodes[u]['hyperedges']:
                    HE_[hyperedge_id].remove(u)
                    if len(HE_[hyperedge_id]) < 2:
                        v = HE_[hyperedge_id].pop()
                        graph_.nodes[v]['hyperedges'].remove(hyperedge_id)
                        if len(graph_.nodes[v]['hyperedges']) < k and v not in list(Q.queue):
                            Q.put(v)

                for in_neighbor in graph_.nodes[u]['in_neighbors']:
                    if u in graph_.nodes[in_neighbor]['out_neighbors']:
                        graph_.nodes[in_neighbor]['out_neighbors'].remove(u)
                    if len(graph_.nodes[in_neighbor]['out_neighbors']) < o and in_neighbor not in list(Q.queue):
                        Q.put(in_neighbor)
                for out_neighbor in graph_.nodes[u]['out_neighbors']:
                    if u in graph_.nodes[out_neighbor]['in_neighbors']:
                        graph_.nodes[out_neighbor]['in_neighbors'].remove(u)

                V_.remove(u)
                D[(k, o-1)].add(u)

            if len(V_) == 0:
                break

    D_ = {}
    for (k, o) in D.keys():
        V = copy.deepcopy(D[(k, o)])
        if (k+1, o) in D:
            V -= D[(k+1, o)]
        if (k, o+1) in D:
            V -= D[(k, o+1)]
        if V:
            D_[(k, o)] = V

    return D_