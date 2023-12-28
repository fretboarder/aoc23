from __future__ import annotations

import math
from pathlib import Path
from pprint import pp

import networkx as nx
from aoc23.support import get_input

Graph = dict[str, set[str]]


def get_edges(lines: list[str]) -> set[tuple[str, str]]:
    edges = set()
    for line in lines:
        node1, *connected = line.replace(":", "").split(" ")
        for node2 in connected:
            edges.add((node1, node2))
    return edges


def solution(edges: set[tuple[str, str]]) -> int:
    graph = nx.from_edgelist(edges)
    edge_betweenness = nx.edge_betweenness_centrality(graph)
    most_crucial_edges = sorted(edge_betweenness, key=edge_betweenness.get)[-3:]
    graph.remove_edges_from(most_crucial_edges)
    group_sizes = [len(c) for c in nx.connected_components(graph)]
    return math.prod(group_sizes)


def main() -> tuple[int, str]:
    graph = get_edges(get_input(Path(__file__).parent / "input01.txt"))
    return solution(graph), "N/A"


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Final solution: {sol1}")
