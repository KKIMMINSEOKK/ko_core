# (k,o)-core

## Running (k,o)-core Algorithm
```
python main.py --hypergraph <hypergraph_path> --digraph <digraph_path> --algorithm ko --k <k_value> --s <s_value>
```
### Example
```
python main.py --hypergraph ./datasets/congress/network.hyp --digraph ./datasets/congress/network.dir --algorithm ko --k 2 --o 2
```

## Running (k,o)-core Decomposition Algorithm
```
python main.py --hypergraph <hypergraph_path> --digraph <digraph_path> --algorithm decom
```
### Example
```
python main.py --hypergraph ./datasets/congress/network.hyp --digraph ./datasets/congress/network.dir --algorithm decom
```
