import csv
import argparse
from .utils import constructArguments, generate_adjacency_lists, generate_automatic_dead_ends, find_parent_dead_ends

def write_to_output_file(output):
  output_file = open(args['output'], 'w+')
  for val in output:
    output_file.write('{}\n'.format(val))


args = constructArguments()

with open(args['input'], 'r') as inf:
  reader = csv.reader(inf, delimiter='\t')

  for i in range(4):
    next(reader, None)

  int_reader_list = [[int(j) for j in i] for i in list(reader)]

  adj_list_dict, dup_adj_list_dict, reverse_hash_map, dup_reverse_hash_map = generate_adjacency_lists(int_reader_list)
  automatic_dead_ends_1, automatic_dead_ends_2 = generate_automatic_dead_ends(adj_list_dict) 
  all_dead_ends = find_parent_dead_ends(reverse_hash_map, automatic_dead_ends_1, automatic_dead_ends_2)
  write_to_output_file(all_dead_ends)
