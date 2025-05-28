import json
from queue import Queue

with open('chameleon.json') as jsonfile, open('chameleon.hyp', 'w') as hypfile:
    reader = json.load(jsonfile)

    for (col1, col2) in enumerate(reader, start=1):
        Q = Queue()
        for node in reader[col2]:
            if node <= 2276:
                Q.put(node)
        if Q.qsize() < 2:
            continue
        while not Q.empty():
            u = Q.get()
            hypfile.write(str(u))
            if not Q.empty():
                hypfile.write(',')
            else:
                hypfile.write('\n')