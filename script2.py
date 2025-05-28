import os
dir = "./datasets/"

# #read all the files in the directory
# file  = os.listdir(dir)
# #.DS_Store and MAG file , we need to remove it
# file.remove('.DS_Store')
# file.remove('MAG')

files = ['scalability']


#write the output to a file
with open("run1.sh", "w") as f:
    for file in files:
        for i in range(0,5):
            f.write(f"python3 main.py --hypergraph {dir}{file}/network{i}.hyp --digraph {dir}{file}/network{i}.dir --algorithm ko --k 100 --o 100 &&\n")
            # print(f"python3 main.py --hypergraph {dir}{file}/network.hyp --digraph {dir}{file}/network.dir --algorithm ko --k {k} --o {o} &&\n")

with open("run1.sh", "rb+") as f:
    f.seek(-4, 2)
    f.truncate()