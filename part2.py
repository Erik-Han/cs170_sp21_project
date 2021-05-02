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
def is_valid_node(G, node):
    tmp = list(G.edges(node, data="weight"))
    G.remove_node(node)
    ret = is_valid(G)
    G.add_node(node)
    for edge in tmp:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    return ret
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

def find_longest_path_setup(G, dpth):
    size = G.number_of_nodes()
    curr_length = nx.shortest_path_length(G, source=0, target=size - 1, weight="weight")
    s = str(curr_length)+" "
    # nx.draw(G, with_labels = True)
    # plt.savefig("start.png")
    # plt.clf()


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
    ans_list = [[], []]
    for i in range(k+c):
        dpth = min(k+c, dpth)
        curr = find_longest_path(G, k, c, dpth, True, size)
        if not curr:
            break
        if type(curr) == tuple:
            k -= 1
            ans_list[0].append(curr)
            G.remove_edge(curr[0], curr[1])
        elif type(curr) == int:
            c -= 1
            ans_list[1].append(curr)
            G.remove_node(curr)
        else:
            print("BAD")
            return
    # G.remove_node(1)
    #shortest_path = nx.shortest_path(G, source=0, target=size- 1, weight="weight")
    # nx.draw(G, with_labels = True)
    # plt.savefig("end.png")
    curr_length = nx.shortest_path_length(G, source=0, target=size - 1, weight="weight")
    s += str(curr_length)
    print(s)
    return ans_list



def find_longest_path(G, k, c, depth, selection, size):
    try:
        poss_ans = nx.shortest_path_length(G, source=0, target=size-1, weight="weight")
    except NetworkXNoPath:
        return
    global ans
    if depth == 0:
        return poss_ans
    shortest_path = nx.shortest_path(G, source=0, target=size-1, weight="weight")
    # try removing each edge along the path
    longest_path_length = poss_ans
    if selection:
        best_item = None
    if k > 0:
        for i in range(len(shortest_path) - 1):
            tmp = G[shortest_path[i]][shortest_path[i + 1]]["weight"]
            G.remove_edge(shortest_path[i], shortest_path[i + 1])
            curr_path_length = find_longest_path(G, k - 1, c, depth - 1, False, size)
            if curr_path_length and curr_path_length >= longest_path_length:
                longest_path_length = curr_path_length
                if selection:
                    best_item = (shortest_path[i], shortest_path[i+1])
            G.add_edge(shortest_path[i], shortest_path[i + 1], weight=tmp)
    # try removing each node along the path
    if c > 0:
        for i in range(1, len(shortest_path) - 1):
            tmp = list(G.edges(shortest_path[i], data="weight"))
            G.remove_node(shortest_path[i])
            curr_path_length = find_longest_path(G, k, c - 1, depth - 1, False, size)
            if nx.is_connected(G) and curr_path_length and curr_path_length >= longest_path_length:
                longest_path_length = curr_path_length
                if selection:
                    best_item = shortest_path[i]
            G.add_node(shortest_path[i])
            for edge in tmp:
                G.add_edge(edge[0], edge[1], weight=edge[2])
    if selection:
        return best_item
    return longest_path_length


def do_file(file,folder, min_size, max_size):
    print("reading:", file)
    graph = read_input_file(folder+file, min_size=min_size, max_size=max_size)
    orig = graph.copy()
    ans = find_longest_path_setup(graph, 4)
    write_output_file(orig, ans[1], ans[0], "./outputs/" + file.split(".")[0] + ".out")
    print("ANSWER:", ans)

if __name__ == "__main__":
    # for file in os.listdir("./real_inputs/small"):
    #     do_file(file, "./real_inputs/small/", 19, 30)
    for file in os.listdir("./real_inputs/medium"):
        do_file(file, "./real_inputs/medium/", 30, 50)
    # for file in os.listdir("./real_inputs/large"):
    #     do_file(file, "./real_inputs/large/", 50, 100)
    #do_file("small-220.in","./real_inputs/small/",19,30)



#6:57
#7:10