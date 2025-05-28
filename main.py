import argparse
import utils
import psutil
import os
import time

import ko
import ko2
import ko_core
import ko_str
import baseline
import decomposition

parser = argparse.ArgumentParser(description="Peeling Algorithm for Hypergraph (k,o)-core")
parser.add_argument("--algorithm", help="Algorithm to use", choices=["ko", "str", "baseline", "decom"], default="ko")
parser.add_argument("--hypergraph", help="Path to the hypergraph file"
                    ,default='./ex1.hyp')
parser.add_argument("--digraph", help="Path to the digraph file"
                    ,default='./ex2.dir')
parser.add_argument("--k", type=int, help="Value of k",default=2)
parser.add_argument("--o", type=int, help="Value of o",default=1)
args = parser.parse_args()

process = psutil.Process(os.getpid())
memory_before = process.memory_info().rss / (1024 * 1024)  # Convert to MB
# Load hypergraph
# graph, HE, DE = utils.load_graph(args.hypergraph, args.digraph)
graph2, HE2, DE2 = utils.load_graph_2(args.hypergraph, args.digraph)
print('Graph is loaded')
# ko_hypergraph = ko_core.Hypergraph()
# ko_hypergraph.load_from_file(args.hypergraph)
# ko_hypergraph.load_from_file_dir(args.digraph)

# if args.algorithm == "ko":
#     start_time = time.time()
#     G = ko_core.run(ko_hypergraph, args.k, args.o)
#     end_time = time.time()
if args.algorithm == "ko":
    # print(f'({k},{o})-core')
    start_time = time.time()
    G = ko.run(graph2, HE2, args.k, args.o)
    end_time = time.time()
    print('computed')
# elif args.algorithm == "str":
#     start_time = time.time()
#     G = ko_str.run(graph, args.k, args.o)
#     end_time = time.time()
# elif args.algorithm == "str":
#     start_time = time.time()
#     G = baseline.run(graph, args.k, args.o)
#     end_time = time.time()
elif args.algorithm == "decom":
    start_time = time.time()
    D = decomposition.run(graph2, HE2)
    end_time = time.time()

memory_after = process.memory_info().rss / (1024 * 1024)  # Convert to MB
memory_usage = memory_after - memory_before  # Calculate memory used

# Write results to file
output_dir = os.path.dirname(args.hypergraph)

output_filename = f"{args.algorithm}_{args.k}_{args.o}_core.dat"
output_path = os.path.join(output_dir, output_filename)

if args.algorithm == "decom":
    with open(output_path, 'w') as output_file:
        output_file.write("Result\n")
        for key, value in D.items():
            output_file.write(f"{key}: {value}\n")

    print(f"Run Time: {end_time - start_time}\n")
    print(f"Memory Usage(MB): {memory_usage}\n")
    print(f"Results written to {output_path}")
else:
    with open(output_path, 'w') as output_file:
        # Write size of nodes
        output_file.write(f"Num of nodes: {str(len(G.nodes))}\n")
        # Write running time
        output_file.write(f"Run Time: {end_time - start_time}\n")
        # Write nodes    
        # output_file.write("Nodes:")
        # nodes = " ".join(str(node) for node in G.nodes)
        # output_file.write(nodes + "\n")

        #write memory usage
        output_file.write("Memory Usage(MB): ")
        output_file.write(f"{memory_usage}\n")

    print(f"Num of nodes: {str(len(G.nodes))}\n")
    print(f"Run Time: {end_time - start_time}\n")
    print(f"Memory Usage(MB): {memory_usage}\n")
    print(f"Results written to {output_path}")