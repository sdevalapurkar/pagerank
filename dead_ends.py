import csv
import argparse

def constructArguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, default=None,
    help='input path of data file')
  parser.add_argument('-o', '--output', type=str, default=None,
    help='output path of data file')
  args = vars(parser.parse_args())

  return args


def write_to_output_file(output):
  output_file = open(args['output'], 'w+')
  for val in output:
    output_file.write('{}\n'.format(val))


def generate_edge_list(nodes):
  edge_u = list(nodes[0])
  edge_v = list(nodes[1])
  edge_u = [int(x) for x in edge_u]
  edge_v = [int(y) for y in edge_v]

  return edge_u, edge_v


def generate_adjacency_list(edge_u, edge_v, nodes_list):
  adj_list_dict = { k: set() for k in nodes_list }

  for i in range(len(edge_u)):
    u = edge_u[i]
    v = edge_v[i]
    adj_list_dict[u].add(v)

  return adj_list_dict


def generate_reverse_hash_map_and_auto_dead_ends(adj_list_dict, nodes_list):
  reverse_hash_map = { k: set() for k in nodes_list }
  automatic_dead_ends_1 = set()
  automatic_dead_ends_2 = set()

  for key, value in adj_list_dict.items():
    if (len(value) == 0):
      automatic_dead_ends_1.add(key)
      automatic_dead_ends_2.add(key)
    else:
      for val in value:
        if (reverse_hash_map.get(val) is None):
          reverse_hash_map[val] = set(key)
        else:
          reverse_hash_map[val].add(key)

  return reverse_hash_map, automatic_dead_ends_1, automatic_dead_ends_2


def find_parent_dead_ends(reverse_hash_map, automatic_dead_ends_1, automatic_dead_ends_2):
  while (len(automatic_dead_ends_2) != 0):
    dead_end = automatic_dead_ends_2.pop()
    automatic_dead_ends_2.add(dead_end)
    parents = reverse_hash_map[dead_end] - automatic_dead_ends_1

    for value in list(parents):
      if (len(adj_list_dict[value] - automatic_dead_ends_1) is 0):
        automatic_dead_ends_1.add(value)
        automatic_dead_ends_2.add(value)

    automatic_dead_ends_2.remove(dead_end)

  return automatic_dead_ends_1


args = constructArguments()

with open(args['input'], 'r') as inf:
  reader = csv.reader(inf, delimiter='\t')
  for i in range(4):
    next(reader, None)

  node_list = zip(*list(reader))
  nodes = list(node_list)

  edge_u, edge_v = generate_edge_list(nodes)
  nodes_list = list(set(edge_u) | set(edge_v))

  adj_list_dict = generate_adjacency_list(edge_u, edge_v, nodes_list)
  reverse_hash_map, automatic_dead_ends_1, automatic_dead_ends_2 = generate_reverse_hash_map_and_auto_dead_ends(adj_list_dict, nodes_list)
  all_dead_ends = find_parent_dead_ends(reverse_hash_map, automatic_dead_ends_1, automatic_dead_ends_2)
  write_to_output_file(all_dead_ends)
