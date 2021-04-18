import numpy as np
import os
from parse import read_input_file
import networkx as nx
from networkx.exception import NetworkXNoPath
ans = -1
ans_details = None


def find_longest_path_setup(G):
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
    find_longest_path(G, 1, 1, ans_list)


def find_longest_path(G, k, c, ans_list):
    try:
        poss_ans = nx.shortest_path_length(G, source=0, target=29, weight="weight")
        print(poss_ans)
    except NetworkXNoPath:
        return
    global ans
    if poss_ans > ans:
        ans = max(ans, poss_ans)
        global ans_details
        ans_details = list(ans_list)
    shortest_path = nx.shortest_path(G, source=0, target=29, weight="weight")
    print(shortest_path)

    # try removing each edge along the path
    if k > 0:
        for i in range(len(shortest_path) - 1):
            tmp = G[shortest_path[i]][shortest_path[i + 1]]["weight"]
            G.remove_edge(shortest_path[i], shortest_path[i + 1])
            ans_list[0].append((shortest_path[i], shortest_path[i + 1]))
            find_longest_path(G, k - 1, c, ans_list)
            del ans_list[0][-1]
            G.add_edge(shortest_path[i], shortest_path[i + 1], weight=tmp)

    # try removing each node along the path
    if c > 0:
        for i in range(1, len(shortest_path) - 1):
            tmp = list(G.edges(shortest_path[i], data="weight"))
            G.remove_node(shortest_path[i])
            ans_list[1].append(shortest_path[i])
            find_longest_path(G, k, c - 1, ans_list)
            del ans_list[1][-1]
            G.add_node(shortest_path[i])
            for edge in tmp:
                G.add_edge(edge[0], edge[1], weight=edge[2])



if __name__ == "__main__":
    for file in os.listdir("./inputs"):
        min_size = 29
        max_size = 30
        graph = read_input_file("./inputs/"+file, min_size=min_size, max_size=max_size)
        find_longest_path_setup(graph)
        print(ans)
        print(ans_details)

#6:54