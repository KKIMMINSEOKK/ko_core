from collections import defaultdict

dic = defaultdict(set)

dic[1].add(1)
dic[1].add(1)
print(dic[1])

graph = [1,2,3,[1,2]]

graph_ = graph.copy()

graph_[3][0] = 2
print(graph)