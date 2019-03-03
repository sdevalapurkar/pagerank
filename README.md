# PageRank
Computing the PageRank score for a web dataset, and also finding nodes that are dead ends within a directed graph

## What is a Dead End Node?
A node is a dead end if it has no out-going edges or all its outoging edges point to dead ends.

For example, consider the graph A->B->C->D. All nodes A,B,C,D are dead ends by this definition. D is a dead end because it has no outgoing edges. C is a dead end because its only out-going neighbour, D, is a dead end. B is a dead end for the same reason, and so is A.

## Finding Dead End Nodes
In order to find dead end nodes given a directed graph, we generate:

1) An *adjacency list* where we list the children of each given node of the graph
2) A *reversed adjacency list* where we list the parents of each given node of the graph

We can use the adjacency list to identify all nodes with no out-going edges and mark them as *automatic dead ends* and then using the list of these and our reversed adjacency list, figure out all the nodes that lead to dead ends.

## Running the Program
To run the code given an input file of the format:

| fromNode   |      toNode      |
|----------|:-------------:|
| 0 |  1 |
| 0 |    2   |
| 1 | 2 |

We can run:

```
python3 dead_ends.py <options>
```

where the options are:

```
-i <input file path> -o <output file path>
```

## Calculating PageRank

PageRank is a mathematical algorithm that evaluates the quality and quantity of links to a webpage. This evaluation helps it to determine a relative score of the page's importance and authority.

In order to calculate the PageRank of webpages, we represent the pages as nodes of a graph and run the following algorithm on it:

![withdeadends]()

![withoutdeadends]()
