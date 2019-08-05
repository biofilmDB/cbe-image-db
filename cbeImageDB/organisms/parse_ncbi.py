import owlready2

output_file_name = 'organisms.csv'

ont = owlready2.get_ontology('ncbi-root-root.owx')
ont.load()
print('The ontology has been loaded')

# go through classes until cellular organism node is found
cell_org = []

for c in ont.classes():
    if c.name.endswith('_131567'):
        cell_org.append(c)
        break

cell_org = cell_org[0]
print('Found the node {} labeled {}'.format(cell_org.name, cell_org.label))

# Find all the subclasses of cellular organism
sub_cell_org = list(ont.search(subclass_of=cell_org))
print('Found {} subclasses of {}'.format(len(sub_cell_org), cell_org.label))

# Get all the assumed leaf nodes
leafs = []
for sco in sub_cell_org:
    rank = sco.has_rank
    if len(rank) > 0 and str(rank[0]).endswith('species'):
        leafs.append(sco)
print('Found {} nodes with has_rank ending in species'.format(len(leafs)))

# get the names of the nodes
l2 = ['{} | {} | {}'.format(x.storid, x.name, x.label[0]) for x in leafs]
print('Made a list of name and label for each leaf')

good = ['storid | ncbi_id | organism_name']
bad = []

for x in l2:
    if 'clone' in x.lower():
        bad.append(x)
    elif 'uncultured' in x.lower():
        bad.append(x)
    elif 'dgge' in x.lower():
        bad.append(x)
    elif 'uncultivated' in x.lower():
        bad.append(x)
    else:
        good.append(x)
print('Len all: {}'.format(len(l2)))
print('len good: {}'.format(len(good)))
print('len bad: {}'.format(len(bad)))

# write the output to a file
with open(output_file_name, 'w') as f:
    f.write('\n'.join(l2))

with open('organisms.csv', 'w') as f:
    f.write('\n'.join(good))

with open('bad-{}'.format(output_file_name), 'w') as f:
    f.write('\n'.join(bad))

print('Wrote output to file {}'.format(output_file_name))
