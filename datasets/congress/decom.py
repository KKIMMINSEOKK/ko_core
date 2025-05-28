with open('decom.dat') as rf:
    with open('decom_.dat', 'w') as wf:
        for line in rf:
            wf.write(str(line.count(',')))
            wf.write(line)