import os
dir = "./datasets/"

# #read all the files in the directory
# file  = os.listdir(dir)
# #.DS_Store and MAG file , we need to remove it
# file.remove('.DS_Store')
# file.remove('MAG')

files = ['congress', 'chameleon', 'gowalla', 'meetup']


#write the output to a file
with open("run.sh", "w") as f:
    for file in files:
        for k in range(2,7):
            for o in range(2,6):
                f.write(f"python3 main.py --hypergraph {dir}{file}/network.hyp --digraph {dir}{file}/network.dir --algorithm ko --k {k} --o {o} &&\n")
                # print(f"python3 main.py --hypergraph {dir}{file}/network.hyp --digraph {dir}{file}/network.dir --algorithm ko --k {k} --o {o} &&\n")

with open("run.sh", "rb+") as f:
    f.seek(-4, 2)
    f.truncate()