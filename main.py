import os
import re

from argparse import ArgumentParser
from collections import defaultdict

import imageio
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def get_args():
    parser = ArgumentParser(description="some kind of thing")
    parser.add_argument("-graph", type=str, choices=["internet", "rel-cave"], default="internet", help="graph structure")
    # parameters
    parser.add_argument("-steps",    type=int,   default=150,  help="number of simulation steps")
    parser.add_argument("-agents",   type=int,   default=100,  help="number of agents")
    parser.add_argument("-travel",   type=float, default=0.15, help="travel probability")
    parser.add_argument("-stay",     type=float, default=0.00, help="stay probability")
    parser.add_argument("-transmit", type=float, default=0.25, help="transmit probability")
    parser.add_argument("-infect",   type=int,   default=15,   help="infection time (in steps)")
    return parser.parse_args()

def draw_graph(graph, positions, agents, history, i=0):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    nx.draw_networkx_nodes(graph, positions, ax=ax[0], alpha=0.25)
    nodes = nx.draw_networkx_nodes(graph, positions, ax=ax[0], nodelist=agents[:, 1][np.where(agents[:, 0] == -1)], node_color="red",   node_size=75)
    nodes.set_zorder(3)
    nodes = nx.draw_networkx_nodes(graph, positions, ax=ax[0], nodelist=agents[:, 1][np.where(agents[:, 0] ==  1)], node_color="blue",  node_size=50)
    nodes.set_zorder(2)
    nodes = nx.draw_networkx_nodes(graph, positions, ax=ax[0], nodelist=agents[:, 1][np.where(agents[:, 0] ==  0)], node_color="green", node_size=25, alpha=0.5)
    nodes.set_zorder(1)
    nx.draw_networkx_edges(graph, positions, ax=ax[0], alpha=0.1)

    x = range(history["s_count"].shape[0])
    ax[1].plot(x, history["s_count"], label="susceptible", color="blue")
    ax[1].plot(x, history["i_count"], label="infected", color="red")
    ax[1].plot(x, history["r_count"], label="recovered", color="green")
    fig.legend()

    fig.savefig("output/out{0}.png".format(i))
    plt.close("all")

def draw_history(history):
    x = range(history["s_count"].shape[0])
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
    ax.plot(x, history["s_count"], label="susceptible", color="blue")
    ax.plot(x, history["i_count"], label="infected", color="red")
    ax.plot(x, history["r_count"], label="recovered", color="green")
    fig.legend()
    fig.tight_layout()
    # fig.show()
    plt.show()

# https://stackoverflow.com/a/5967539
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def make_gif():
    images = []
    #with imageio.get_writer("mygif.gif", mode="I") as writer:
    files = sorted(os.listdir("output"), key=natural_keys)
    for file in files:
        path = os.path.join("output", file)
        image = imageio.imread(os.path.join("output", file))
        # writer.append_data(image)
        images.append(image)
        os.remove(path)
    
    imageio.mimsave("mygif.gif", images, duration=0.15)

def get_graph(graph_type):
    # TODO: make number of nodes configurable
    n = 250

    if graph_type == "internet":
        return nx.random_internet_as_graph(n)
    elif graph_type == "rel-cave":
        return nx.relaxed_caveman_graph(25, 10, 0.08)

def simulate(args, graph, agents):
    # get parameters
    n_steps       = args.steps
    travel_prob   = args.travel
    stay_prob     = args.stay
    transmit_prob = args.transmit
    infect_time   = args.infect

    n_agents = agents.shape[0]

    history = {
        "s_count": np.zeros(n_steps),
        "i_count": np.zeros(n_steps),
        "r_count": np.zeros(n_steps)
    }

    # track infection times
    infect_times = np.ones(n_agents, dtype=int) * infect_time

    # keep path history (as a stack) for backtracking
    back = [[] for _ in range(n_agents)]

    # node positions for drawing
    positions = nx.spring_layout(graph, seed=0) 

    for step in range(n_steps):
        if step % 10 == 0: print("step {0}/{1}".format(step, n_steps))
        draw_graph(graph, positions, agents, history, step)

        s_count = np.count_nonzero(agents ==  1)
        i_count = np.count_nonzero(agents == -1)
        r_count = np.count_nonzero(agents ==  0)
        # print(s_count, i_count, r_count)
        history["s_count"][step] = s_count
        history["i_count"][step] = i_count
        history["r_count"][step] = r_count

        for i, (stat, node) in enumerate(agents):
            # age any infected agents
            if stat == -1:
                infect_times[i] -= 1
                # set to recovered if infection time expires
                if infect_times[i] == 0:
                    agents[i][0] = 0

            # skip "recovered" agents
            # cannot use "stat" field as it may have been updated above
            if agents[i][0] == 0:
                continue

            # choose an action
            prob = np.random.random()
            if prob < travel_prob:
                new_node = np.random.choice(graph.adj[node])
                back[i].append(node)
                agents[i][1] = new_node
            # elif prob < stay_prob:
            else:
                if len(back[i]) > 0:
                    new_node = back[i].pop()
                    agents[i][1] = new_node
            
        # TODO: can this be done in the loop above?
        # process contacts
        contacts = defaultdict(list)
        for i, (_, node) in enumerate(agents):
            contacts[node].append(i)

        for node, group in contacts.items():
            if len(group) > 1:
                np_group = np.array(group)
                stats = agents[group][:, 0]
                i_idx = np.where(stats == -1)
                i_agents = np_group[i_idx]
                # check if there are any infected agents at this node
                if i_agents.shape[0] == 0:
                    continue

                s_idx = np.where(stats ==  1)
                s_agents = np_group[s_idx]
                prob = transmit_prob
                res = np.random.choice([-1, 1], size=s_agents.shape[0], p=[prob, 1 - prob])
                agents[:, 0][s_agents] *= res

    make_gif()
    # draw_graph(graph, positions, agents, step)

    return history

if __name__ == "__main__":
    args = get_args()
    graph = get_graph(args.graph) # graph
    positions = nx.spring_layout(graph, seed=0) # node positions

    # TODO: add strategy profile to agents?
    # create agents
    agents = np.ones((args.agents, 2), dtype=int)
    agents[:, 1] = range(agents.shape[0]) # where to place them?
    rand_ind = np.random.choice(range(agents.shape[0]), size=2)
    agents[:, 0][rand_ind] = -1

    history = simulate(args, graph, agents)
    # draw_history(history)
