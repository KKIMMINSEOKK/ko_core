with open('network.hyp') as hypfile:
    with open('network2.hyp', 'w') as f:
        for line_number, line in enumerate(hypfile, start=1):
            if ',' in line:
                f.write(f'{line}')