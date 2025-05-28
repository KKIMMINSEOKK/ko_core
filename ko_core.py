import copy
from queue import Queue
import heapq
from sortedcontainers import SortedDict
import re
import networkx as nx
from itertools import combinations


class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.NodeCnt = 0  # 노드의 카운트
        self.EdgeCnt = 0  # 연결된 하이퍼에지 ID를 저장하는 set
        self.Edge = set()  # 연결된 하이퍼에지를 저장하는 set
        self.InNeighbors = set()
        self.OutNeighbors = set()

class Hypergraph:
    def __init__(self):
        self.nodes = {}
        self.hyperedges = {}

    def add_hyperedge(self, edge_nodes):
        hyperedge_id = len(self.hyperedges) + 1
        self.hyperedges[hyperedge_id] = edge_nodes #각 hyperedge에 노드id set저장됨.

        for node in edge_nodes:
            if node not in self.nodes:
                self.nodes[node] = Node(node)
            self.nodes[node].Edge.add(hyperedge_id)

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:

                # current_nodes = {int(node.strip()) for node in line.strip().split(',')}
                current_nodes = {int(node.strip()) for node in re.split(r'[,\s]+', line.strip())}

                self.add_hyperedge(current_nodes) #노드 id들을 set으로 추가.
    
    def load_from_file_dir(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:

                # current_nodes = {int(node.strip()) for node in line.strip().split(',')}
                current_nodes = [int(node.strip()) for node in re.split(r'[,\s]+', line.strip())]

                self.nodes[current_nodes[0]].OutNeighbors.add(current_nodes[1])
                self.nodes[current_nodes[1]].InNeighbors.add(current_nodes[0])

    def del_node(self, node):
        if node in self.nodes:
            for hyperedge in self.nodes[node].Edge:
                self.hyperedges[hyperedge].remove(node)
            for in_neighbor in self.nodes[node].InNeighbors:
                self.nodes[in_neighbor].OutNeighbors.remove(node)
            for out_neighbor in self.nodes[node].OutNeighbors:
                self.nodes[out_neighbor].InNeighbors.remove(node)
            del self.nodes[node]

    def del_edge(self, edge):
        if edge in self.hyperedges:
            for node in self.hyperedges[edge]:
                self.nodes[node].Edge.remove(edge)
            del self.hyperedges[edge]

    def trans_bipartite(self):
        B = nx.Graph()
        node_ids = {f'n{key}': key for key in self.nodes.keys()}
        hyperedge_ids = {f'h{key}': key for key in self.hyperedges.keys()}
        B.add_nodes_from(hyperedge_ids, bipartite=0)
        B.add_nodes_from(node_ids, bipartite=1)
        edge_list = [(f'h{id}', f'n{node}') for id, edge_nodes in self.hyperedges.items() for node in edge_nodes]
        B.add_edges_from(edge_list)
        return [B.subgraph(component).copy() for component in nx.connected_components(B)]

    def trans_clique(self):
        G = nx.Graph()
        G.add_nodes_from(self.nodes.keys())
        for edge_nodes in self.hyperedges.values():
            for u, v in combinations(edge_nodes, 2):
                G.add_edge(u, v)
        return G

def run(graph, k, o):

    ##### INITIALIZE #####
    G = copy.deepcopy(graph)

    Q = Queue()

    ##### k-hypercore #####
    for node in G.nodes:
        if len(G.nodes[node].Edge) < k:
            Q.put(node)
        elif len(G.nodes[node].OutNeighbors) < o:
            Q.put(node)

    while not Q.empty():
        u = Q.get()

        RQ = Queue()
        for hyperedge_id in G.nodes[u].Edge:
            if len(G.hyperedges[hyperedge_id]) == 2:
                for node in G.hyperedges[hyperedge_id]:
                    if node != u:
                        if len(G.nodes[node].Edge) <= k and node not in list(Q.queue):
                            Q.put(node)
                RQ.put(hyperedge_id)
        
        while not RQ.empty():
            hyperedge_id = RQ.get()
            G.del_edge(hyperedge_id)

        for in_neighbor in G.nodes[u].InNeighbors:
            if len(G.nodes[in_neighbor].OutNeighbors) <= o and in_neighbor not in list(Q.queue):
                Q.put(in_neighbor)
            
        G.del_node(u)

    return G