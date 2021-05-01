import numpy as np
import os
from parse import read_input_file
import networkx as nx
import copy
from networkx.exception import NetworkXNoPath
import matplotlib.pyplot as plt

def find_longest_path_setup(G):
    nx.draw(G, with_labels = True)
    plt.savefig("start.png")
    plt.clf()
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
    ans_list = [[], []]
    dpth = 1
    for i in range(k+c):
        curr = find_longest_path(G, k, c, dpth, True)
        curr_length = nx.shortest_path_length(G, source=0, target=size-1, weight="weight")
        print(curr_length)
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
    # shortest_path = nx.shortest_path(G, source=0, target=size- 1, weight="weight")
    nx.draw(G, with_labels = True)
    plt.savefig("end.png")
    return ans_list



def find_longest_path(G, k, c, depth, selection):
    num_nodes = G.number_of_nodes()
    try:
        poss_ans = nx.shortest_path_length(G, source=0, target=num_nodes-1, weight="weight")
    except NetworkXNoPath:
        return
    global ans

    if depth == 0:
        return poss_ans
    shortest_path = nx.shortest_path(G, source=0, target=num_nodes-1, weight="weight")

    # try removing each edge along the path
    longest_path_length = poss_ans
    if selection:
        best_item = None
    if k > 0:
        for i in range(len(shortest_path) - 1):
            tmp = G[shortest_path[i]][shortest_path[i + 1]]["weight"]
            G.remove_edge(shortest_path[i], shortest_path[i + 1])
            curr_path_length = find_longest_path(G, k - 1, c, depth - 1, False)
            if curr_path_length and curr_path_length > longest_path_length:
                longest_path_length = curr_path_length
                if selection:
                    best_item = (shortest_path[i], shortest_path[i+1])
            G.add_edge(shortest_path[i], shortest_path[i + 1], weight=tmp)
    # try removing each node along the path
    if c > 0:
        for i in range(1, len(shortest_path) - 1):
            tmp = list(G.edges(shortest_path[i], data="weight"))
            G.remove_node(shortest_path[i])
            curr_path_length = find_longest_path(G, k, c - 1, depth - 1, False)
            if curr_path_length and curr_path_length > longest_path_length:
                longest_path_length = curr_path_length
                if selection:
                    best_item = shortest_path[i]

            G.add_node(shortest_path[i])
            for edge in tmp:
                G.add_edge(edge[0], edge[1], weight=edge[2])
    if selection:
        return best_item
    return longest_path_length



if __name__ == "__main__":
    for file in os.listdir("./inputs"):
        min_size = 29
        max_size = 30
        graph = read_input_file("./inputs/"+file, min_size=min_size, max_size=max_size)
        ans = find_longest_path_setup(graph)
        print("ANSWER:", ans)


#6:54