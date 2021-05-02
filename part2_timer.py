import numpy as np
import os
from parse import read_input_file, write_output_file
import networkx as nx
import copy
from networkx.exception import NetworkXNoPath
import matplotlib.pyplot as plt
import time
from utils import calculate_score

global start_time
global abort
abort = False
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

def find_longest_path_setup(G, dpth):
    orig_dpth = dpth
    size = G.number_of_nodes()
    start_length = nx.shortest_path_length(G, source=0, target=size - 1, weight="weight")
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

    score = curr_length - start_length
    print("depth:", orig_dpth,"score:",score)
    return ans_list, score


def find_longest_path(G, k, c, depth, selection, size):
    global abort
    if abort:
        return
    end_time = time.time()
    global start_time
    if end_time - start_time > 60:
        abort = True
        return

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
    best_score = 0
    final_ans = None
    best_depth = 0
    for d in range(1,8):
        graph = orig.copy()
        global abort
        if abort:
            break
        abort = False
        global start_time
        start_time = time.time()
        ans, score = find_longest_path_setup(graph, d)
        if score >= best_score and ans:
            final_ans = ans
            best_score = score
            best_depth = d
    if abort:
        print("too long")
        abort = False
    write_output_file(orig, final_ans[1], final_ans[0], "./outputs/" + file.split(".")[0] + ".out")
    print("best score:",best_score,"best depth:",best_depth,"ANSWER:", final_ans )

if __name__ == "__main__":
    for file in sorted(os.listdir("./real_inputs/small")):
        do_file(file, "./real_inputs/small/", 19, 30)
    # for file in sorted(os.listdir("./real_inputs/medium")):
    #     do_file(file, "./real_inputs/medium/", 30, 50)
    # for file in sorted(os.listdir("./real_inputs/large")):
    #     do_file(file, "./real_inputs/large/", 50, 100)
    #do_file("medium-6.in","./real_inputs/medium/",30,50)



#6:57
#7:10