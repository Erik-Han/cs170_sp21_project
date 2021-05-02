import numpy as np
import os
from parse import read_input_file, write_output_file
import networkx as nx
import copy
from networkx.exception import NetworkXNoPath
import matplotlib.pyplot as plt


def is_valid(G):
    try:
        nx.shortest_path_length(G, source=0, target=G.number_of_nodes() - 1, weight="weight")
    except NetworkXNoPath:
        return False
    return nx.is_connected(G)

def is_valid_edge(G, edge):
    tmp = G[edge[0]][edge[1]]["weight"]
    G.remove_edge(edge[0], edge[1])
    ret = is_valid(G)
    G.add_edge(edge[0], edge[1], weight=tmp)
    return ret

def is_valid_node(G, node):
    tmp = list(G.edges(node, data="weight"))
    G.remove_node(node)
    ret = is_valid(G)
    G.add_node(node)
    for edge in tmp:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    return ret
def set_cover(paths, G, edge_freq):
    covered = {}
    total = len(paths)
    covered_ct = 0
    for path in paths:
        covered[path] = False
    edges = []
    while covered_ct < total:
        mx_edge = None
        for edge in edge_freq:
            #print(edge)
            if is_valid_edge(G,edge) and (not mx_edge or edge_freq[mx_edge] < edge_freq[edge]):
                mx_edge = edge
        if not mx_edge:
            return False
        #print("max",mx_edge)
        edges.append(mx_edge)
        G.remove_edge(mx_edge[0], mx_edge[1])
        for p in edge_freq[mx_edge]:
            covered[p] = True
            covered_ct += 1
            for i in range(len(p)-1):
                edge = (p[i],p[i+1])
                if edge != mx_edge and (edge[1],edge[0])!=mx_edge:
                    edge_freq[edge].remove(p)
                    if len(edge_freq[edge]) == 0:
                        del edge_freq[edge]
                        del edge_freq[(edge[1],edge[0])]

        del edge_freq[mx_edge]
        del edge_freq[(mx_edge[1],mx_edge[0])]
    return edges


def set_cover_nodes(edges, c, size, G):
    poss_nodes = set()
    for e in edges:
        if e[0] not in poss_nodes and e[0] != 0 and e[0] != size-1:
            poss_nodes.add(e[0])
        if e[1] not in poss_nodes and e[1] != 0 and e[1] != size-1:
            poss_nodes.add(e[1])

    covered = [False] * len(edges)
    nodes = []
    while c > 0 and len(edges) > 0:
        to_remove = set()
        for n in poss_nodes:
            if not is_valid_node(G, n):
                to_remove.add(n)
        for n in to_remove:
            poss_nodes.remove(n)
        node_freq = [[]] * size
        mx_node = None
        for i in range(len(edges)):
            e = edges[i]
            if covered[i]:
                continue
            if mx_node:
                bm = len(node_freq[mx_node])
            if e[0] in poss_nodes:
                node_freq[e[0]].append(i)
                if not mx_node or len(node_freq[e[0]]) > bm:
                    mx_node = e[0]
            if mx_node:
                bm = len(node_freq[mx_node])
            if e[1] in poss_nodes:
                node_freq[e[1]].append(i)
                if not mx_node or len(node_freq[e[1]]) > bm:
                    mx_node = e[1]
        if mx_node:
            G.remove_node(mx_node)
            nodes.append(mx_node)
        else:
            break
        c -= 1
        for e in node_freq[mx_node]:
            covered[e] = True
    new_edges = []
    for i in range(len(covered)):
        if not covered[i]:
            new_edges.append(edges[i])
    return new_edges, nodes


def find_longest_path_setup(G):
    # nx.draw(G, with_labels = True)
    # plt.savefig("start.png")
    # plt.clf()
    size = G.number_of_nodes()
    k = 15
    c = 1
    if size <= 30:
        k = 15
        c = 1
    elif size <= 50:
        k = 50
        c = 3
    elif size <= 100:
        k = 100
        c = 5
    first_path = tuple(nx.shortest_path(G, source=0, target=size - 1, weight="weight"))
    paths = {first_path}
    edges = set()
    nodes = set()
    for i in range(len(first_path)-1):
        if is_valid_edge(G, (first_path[i],first_path[i+1])):
            edges = {(first_path[i], first_path[i+1])}
    if not edges:
        return set()

    while len(nodes) < c or len(edges) < k:
        edge_weights = {}
        G_base = G.copy()
        for n in nodes:
            G_base.remove_node(n)
        to_remove = set()
        for path in paths:
            for i in range(len(path)-1):
                if not G_base.has_edge(path[i],path[i+1]):
                    to_remove.add(path)
        for rem in to_remove:
            paths.remove(rem)
        stuck = False
        while len(edges) < k:
            curr_G = G_base.copy()
            print(edges,nodes)
            for edge in edges:
                curr_G.remove_edge(edge[0], edge[1])
            if not is_valid(curr_G):
                print(edges)
                print("BROKEN GRAPH")
                return None
            paths.add(tuple(nx.shortest_path(curr_G, source=0, target=size - 1, weight="weight")))
            print(nx.shortest_path_length(curr_G, source=0, target=size - 1, weight="weight"))

            #get edge frequency
            for path in paths:
                for i in range(len(path)-1):
                    edge = (path[i], path[i+1])
                    if edge not in G_base.edges:
                        continue
                    reverse = (path[i+1],path[i])
                    if edge in edge_weights:
                        edge_weights[edge].add(path)
                    else:
                        edge_weights[edge] = {path}
                        edge_weights[reverse] = edge_weights[edge]
            curr_G = G_base.copy()
            pure_paths = [path[0] for path in paths]
            curr_edges = set_cover(pure_paths, curr_G, edge_weights)
            if not curr_edges:
                stuck = True
                break
            edges = curr_edges
        if stuck:
            break
        if len(nodes) < c:
            nodes_G = G.copy()
            for edge in edges:
                nodes_G.remove_edge(edge[0], edge[1])
            edges, nodes = set_cover_nodes(edges, c, size, nodes_G)
    # shortest_path = nx.shortest_path(G, source=0, target=size- 1, weight="weight")
    # nx.draw(G, with_labels = True)
    # plt.savefig("end.png")
    print("original:", nx.shortest_path_length(G, source=0, target=size - 1, weight="weight"))
    for edge in edges:
        G.remove_edge(edge[0], edge[1])
    for n in nodes:
        G.remove_node(n)
    curr_length = nx.shortest_path_length(G, source=0, target=size - 1, weight="weight")
    print("final:", curr_length)
    return [edges,nodes]

def do_file(file, folder, min_size, max_size):
    print("reading:", file)
    graph = read_input_file(folder + file, min_size=min_size, max_size=max_size)
    orig = graph.copy()
    ans = find_longest_path_setup(graph)
    write_output_file(orig, ans[1], ans[0], "./outputs/" + file.split(".")[0] + ".out")
    print("ANSWER:", ans)


if __name__ == "__main__":
    # for file in os.listdir("./real_inputs/small"):
    #     do_file(file, "./real_inputs/small/", 19, 30)
    # for file in os.listdir("./real_inputs/medium"):
    #     do_file(file, "./real_inputs/large/", 30, 50)
    # for file in os.listdir("./real_inputs/large"):
    #     do_file(file, "./real_inputs/large/", 50, 100)
    do_file("small-220.in","./real_inputs/small/",19,30)

# 11:22:30
