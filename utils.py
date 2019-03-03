import csv
import argparse
import numpy as np

def constructArguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, default=None,
    help='input path of data file')
  parser.add_argument('-o', '--output', type=str, default=None,
    help='output path of data file')
  args = vars(parser.parse_args())

  return args

def generate_adjacency_lists(int_reader_list):
  adj_list_dict = {}
  dup_adj_list_dict = {}
  reverse_hash_map = {}
  dup_reverse_hash_map = {}

  for pair in int_reader_list:
    node = pair[0]
    child = pair[1]

    if (node not in adj_list_dict):
      adj_list_dict[node] = set()
      dup_adj_list_dict[node] = set()
    if (child not in adj_list_dict):
      adj_list_dict[child] = set()
      dup_adj_list_dict[child] = set()
    if (node not in reverse_hash_map):
      reverse_hash_map[node] = set()
      dup_reverse_hash_map[node] = set()
    if (child not in reverse_hash_map):
      reverse_hash_map[child] = set()
      dup_reverse_hash_map[child] = set()

    if (node in adj_list_dict):
      adj_list_dict[node].add(child)
      dup_adj_list_dict[node].add(child)
    else:
      adj_list_dict[node] = set([child])
      dup_adj_list_dict[node] = set([child])
    if (child in reverse_hash_map):
      reverse_hash_map[child].add(node)
      dup_reverse_hash_map[child].add(node)
    else:
      reverse_hash_map[child] = set([node])
      dup_reverse_hash_map[child] = set([node])

  return adj_list_dict, dup_adj_list_dict, reverse_hash_map, dup_reverse_hash_map

def generate_automatic_dead_ends(adj_list_dict):
  automatic_dead_ends_1 = set()
  automatic_dead_ends_2 = set()

  for key, value in adj_list_dict.items():
    if (len(value) == 0):
      automatic_dead_ends_1.add(key)
      automatic_dead_ends_2.add(key)

  return automatic_dead_ends_1, automatic_dead_ends_2


def find_parent_dead_ends(adj_list_dict, reverse_hash_map, automatic_dead_ends_1, automatic_dead_ends_2):
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
