import sys
import os
import time
import argparse
from progress import Progress
import networkx as nx
import random as r


G = nx.DiGraph()


def load_graph(args):
    """Load graph from text file
    Parameters:
    args -- arguments named tuple
    Returns:
    A dict mapling a URL (str) to a list of target URLs (str).
    """
    # Iterate through the file line by line
    with open("school_web.txt") as args.datafile:
        for line in args.datafile:
            # And split each line into two URLs
            node, target = line.split()
            # Added node
            G.add_node(node)
            # Added Edge
            G.add_edge(node, target)
        return G


def print_stats(graph):
    """Print number of nodes and edges in the given graph"""
    print("The number of nodes is:", len(graph.nodes))
    print("The number of edges is:", len(graph.edges))


def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation
    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple
    Returns:
    A dict that assigns each page its hit frequency
    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """

    # Sets nodes to nodes in dict
    nodes = graph.nodes
    # initialize hit_count[node] with 0 for all nodes
    hit_count = dict.fromkeys(nodes, 0)

    # repeat n_repetitions times:
    # current_node <- randomly selected node
    for i in range(args.repeats):
        current_node = r.choice(list(nodes))

        # repeat n_steps times:
        # current_node <- uniformly randomly chosen among the out edges of current_node
        for n in range(args.steps):
            current_node = r.choice(list(graph[current_node]))

        # hit_count[current_node] += 1/n_repetitions
        hit_count[current_node] += 1 / args.repeats
    return hit_count


def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    raise RuntimeError("This function is not implemented yet.")


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")


if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
