import csv
from tarjan import tarjan

# TODO: fix reading input file 

def write_to_output_file(output):
  output_file = open('./outputs/deadends_sample_output.tsv','w+')
  for val in output:
    output_file.write('{}\n'.format(val))


def generate_edge_list(nodes):
  edge_u = list(nodes[0])
  edge_v = list(nodes[1])
  edge_u = [int(x) for x in edge_u]
  edge_v = [int(y) for y in edge_v]

  return edge_u, edge_v


def generate_adjacency_list(edge_u, edge_v, adj_list_dict): 
  for i in range(len(edge_u)):
    u = edge_u[i]
    v = edge_v[i]
    adj_list_dict[u].append(v)

  return adj_list_dict


with open('./sample_input.txt') as inf:
  reader = csv.reader(inf, delimiter='\t')
  node_list = zip(*list(reader))
  nodes = list(node_list)

  edge_u, edge_v = generate_edge_list(nodes)

  # number of nodes
  n = 6
  adj_list_dict = { k: [] for k in edge_u }
  adj_list_dict = generate_adjacency_list(edge_u, edge_v, adj_list_dict)

  # print("Adjacency list: ")
  print(adj_list_dict)

  false_dead_ends = []

  for key, value in adj_list_dict.items():
    if (key in adj_list_dict.get(key)):
      false_dead_ends.append(key)

  print(false_dead_ends)
  scc = tarjan(adj_list_dict)
  print(scc)

  final_dead_end_list = []

  for component in scc:
    if (len(component) == 1 and component[0] not in false_dead_ends):
      final_dead_end_list.append(component[0])

  write_to_output_file(final_dead_end_list)
