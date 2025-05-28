import random
import math

nodeSet = set()
with open('network.hyp') as hypfile:
    for line_number, line in enumerate(hypfile, start=1):
        nodes = {node.strip() for node in line.strip().split(',')}
        nodes = {int(x) for x in nodes}
        for node in nodes:
            nodeSet.add(node)

nodeList = []
for node in nodeSet:
    nodeList.append(node)

numOfNodes = len(nodeList)
print(f'Number of nodes: {numOfNodes}')
numOfEdges = numOfNodes*12
edgeSet = set()
with open('network.dir', 'w') as dirfile:
    for i in range(0, numOfEdges):
        x1 = random.random()
        x2 = random.random()
        node1 = nodeList[math.floor(x1 * numOfNodes)]
        node2 = nodeList[math.floor(x2 * numOfNodes)]
        if node1 == node2 or (node1, node2) in edgeSet:
            continue
        edgeSet.add((node1, node2))
        dirfile.write(f'{node1},{node2}\n')