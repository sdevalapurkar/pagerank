import csv
import argparse
import numpy as np
from .utils import constructArguments, generate_adjacency_lists, generate_automatic_dead_ends, find_parent_dead_ends

def remove_dead_ends(adj_list_dict_without_dead_ends, reverse_hash_map_without_dead_ends, all_dead_ends):
  removed_dead_ends = []

  while (len(removed_dead_ends) != len(all_dead_ends)):
    for key, value in list(adj_list_dict_without_dead_ends.items()):
      if (len(value) == 0):
        removed_dead_ends.append(key)
        del adj_list_dict_without_dead_ends[key]

        for val in reverse_hash_map_without_dead_ends[key]:
          adj_list_dict_without_dead_ends[val].remove(key)

        del reverse_hash_map_without_dead_ends[key]

  return removed_dead_ends, adj_list_dict_without_dead_ends, reverse_hash_map_without_dead_ends


def page_rank_without_dead_ends(adj_list_dict_without_dead_ends, nodes_set, reverse_hash_map_without_dead_ends, all_dead_ends):
  non_dead_ends = nodes_set - all_dead_ends
  num_iterations = 10
  beta = 0.85
  num_vertices = len(non_dead_ends)

  v = np.ones(max(nodes_set) + 1) * (1 / num_vertices)

  for _ in range(num_iterations):
    v0 = v

    for i in non_dead_ends:
      v[i] = beta * sum(map(lambda j: v0[j] / len(adj_list_dict_without_dead_ends[j]), reverse_hash_map_without_dead_ends[i])) + ((1 - beta) * (1 / num_vertices))

  return v


def page_rank_with_dead_ends(removed_dead_ends, page_rank_without_dead_ends, all_dead_ends, adj_list_dict, reverse_hash_map):
  v = page_rank_without_dead_ends
  v0 = v

  for i in removed_dead_ends[::-1]:
    v[i] = sum(map(lambda j: v0[j] / len(adj_list_dict[j]), reverse_hash_map[i]))

  return v


args = constructArguments()

with open(args['input'], 'r') as inf:
  reader = csv.reader(inf, delimiter='\t')

  for i in range(4):
    next(reader, None)

  int_reader_list = [[int(j) for j in i] for i in list(reader)]

  adj_list_dict, dup_adj_list_dict, reverse_hash_map, dup_reverse_hash_map = generate_adjacency_lists(int_reader_list)
  nodes_set = set(adj_list_dict.keys())
  automatic_dead_ends_1, automatic_dead_ends_2 = generate_automatic_dead_ends(adj_list_dict)
  all_dead_ends = find_parent_dead_ends(reverse_hash_map, automatic_dead_ends_1, automatic_dead_ends_2)
  removed_dead_ends, adj_list_dict_without_dead_ends, reverse_hash_map_without_dead_ends = remove_dead_ends(dup_adj_list_dict, dup_reverse_hash_map, all_dead_ends)  
  page_rank_without_dead_ends = page_rank_without_dead_ends(adj_list_dict_without_dead_ends, nodes_set, reverse_hash_map_without_dead_ends, all_dead_ends)
  page_rank_with_dead_ends = page_rank_with_dead_ends(removed_dead_ends, page_rank_without_dead_ends, all_dead_ends, adj_list_dict, reverse_hash_map)
