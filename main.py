import os
import random
import re

from argparse import ArgumentParser
from collections import defaultdict

import imageio
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm

def get_args():
    parser = ArgumentParser(description="some kind of thing")
    parser.add_argument("-graph",  type=str, choices=["internet", "rel-cave", "con-cave", "cliques"], default="internet", help="graph structure")
    parser.add_argument("-immune", type=str, choices=["none", "random", "degree", "population", "importance", "vulnerableDegree", "acquaint"], default="none", help="immunization strategy")
    parser.add_argument("-output", type=str, default="out", help="output gif/png filename")
    # parameters
    parser.add_argument("-runs",     type=int,   default=1,    help="number of simulations to run")
    parser.add_argument("-steps",    type=int,   default=100,  help="number of simulation steps")
    parser.add_argument("-agents",   type=int,   default=500,  help="number of agents")
    parser.add_argument("-travel",   type=float, default=0.40, help="travel probability")
    parser.add_argument("-stay",     type=float, default=0.10, help="stay probability")
    parser.add_argument("-transmit", type=float, default=0.35, help="transmit probability")
    parser.add_argument("-infect",   type=int,   default=20,   help="infection time (in steps)")
    parser.add_argument("-social",   type=float, default=0.00, help="percentage of agents that social distance")
    parser.add_argument("-n_immune", type=int,   default=10,   help="number of nodes to immunize")
    parser.add_argument("-p_immune", type=float, default=0.80, help="percentage of agents that get immunized at a node")
    parser.add_argument("-seed",     type=int,   default=13,    help="random seed")
    parser.add_argument("-gif", action="store_true", help="make gif")
    return parser.parse_args()

def draw_graph(graph, positions, agents, immunized, history, i=0):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(6, 3))

    nx.draw_networkx_nodes(graph, positions, nodelist=np.where(immunized == 0)[0], ax=ax[0], node_size=50, alpha=0.25)
    nx.draw_networkx_nodes(graph, positions, nodelist=np.where(immunized == 1)[0], ax=ax[0], node_size=75, node_color="orange", alpha=0.5)

    nodes = nx.draw_networkx_nodes(graph, positions, ax=ax[0], nodelist=agents[:, 1][np.where(agents[:, 0] ==  2)], node_color="orange",   node_size=15, alpha=0.5)
    nodes.set_zorder(4)
    nodes = nx.draw_networkx_nodes(graph, positions, ax=ax[0], nodelist=agents[:, 1][np.where(agents[:, 0] == -1)], node_color="red",   node_size=15, alpha=0.75)
    nodes.set_zorder(3)
    nodes = nx.draw_networkx_nodes(graph, positions, ax=ax[0], nodelist=agents[:, 1][np.where(agents[:, 0] ==  1)], node_color="blue",  node_size=10, alpha=0.75)
    nodes.set_zorder(2)
    nodes = nx.draw_networkx_nodes(graph, positions, ax=ax[0], nodelist=agents[:, 1][np.where(agents[:, 0] ==  0)], node_color="red", node_size=10, alpha=0.5)
    nodes.set_zorder(1)
    nx.draw_networkx_edges(graph, positions, ax=ax[0], alpha=0.1)

    x = range(history["s_count"].shape[0])
    ax[1].plot(x[:i], history["s_count"][:i], label="susceptible", color="blue")
    ax[1].plot(x[:i], history["i_count"][:i], label="infected",    color="red")
    ax[1].plot(x[:i], history["r_count"][:i], label="recovered",   color="green")
    ax[1].plot(x[:i], history["v_count"][:i], label="immune",      color="orange")
    ax[1].set_xticks([])
    fig.legend()
    fig.tight_layout()
    fig.savefig("output/out{0}.png".format(i))
    plt.close("all")

def draw_history(args, graph, positions, immunized, history_list):
    x = range(history_list[0]["s_count"].shape[0])
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(6, 3))
    nx.draw_networkx_nodes(graph, positions, nodelist=np.where(immunized == 0)[0], ax=ax[0], node_size=50, alpha=0.25)
    nx.draw_networkx_nodes(graph, positions, nodelist=np.where(immunized == 1)[0], ax=ax[0], node_size=75, node_color="orange", alpha=0.5)
    nx.draw_networkx_edges(graph, positions, ax=ax[0], alpha=0.1)
    for history in history_list:
        ax[1].plot(x, history["s_count"], color="blue", alpha=0.5)
        ax[1].plot(x, history["i_count"], color="red", alpha=0.5)
        ax[1].plot(x, history["r_count"], color="green", alpha=0.5)
        ax[1].plot(x, history["v_count"], color="orange", alpha=0.5)
    fig.tight_layout()
    fig.savefig("{0}.png".format(args.output))
    plt.close("all")

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

def make_gif(args):
    images = []
    #with imageio.get_writer("mygif.gif", mode="I") as writer:
    files = sorted(os.listdir("output"), key=natural_keys)
    for file in files:
        path = os.path.join("output", file)
        image = imageio.imread(os.path.join("output", file))
        # writer.append_data(image)
        images.append(image)
        os.remove(path)
    
    imageio.mimsave("{0}.gif".format(args.output), images, duration=0.25)

def get_graph(graph_type):
    # TODO: make number of nodes configurable?
    if graph_type == "internet":
        return nx.random_internet_as_graph(500)
    elif graph_type == "rel-cave":
        return nx.relaxed_caveman_graph(50, 10, 0.1)
    elif graph_type == "con-cave":
        return nx.connected_caveman_graph(25, 10)
    elif graph_type == "cliques":
        return nx.ring_of_cliques(25, 10)

def simulate(args, graph, positions, agents):
    # get parameters
    n_steps       = args.steps
    # travel_prob   = args.travel
    # stay_prob     = args.stay
    # back_prob     = 1 - (travel_prob + stay_prob)
    transmit_prob = args.transmit
    infect_time   = args.infect
    social        = args.social
    immune        = args.immune
    n_immune      = args.n_immune
    p_immune      = args.p_immune

    n_agents = agents.shape[0]
    n_nodes  = graph.number_of_nodes()

    history = {
        "s_count": np.zeros(n_steps),
        "i_count": np.zeros(n_steps),
        "r_count": np.zeros(n_steps),
        "v_count": np.zeros(n_steps),

        "is_ratio": np.zeros(n_steps),
        "in_ratio": np.zeros(n_steps),
        "rs_ratio": np.zeros(n_steps),
        "rn_ratio": np.zeros(n_steps),
        "vs_ratio": np.zeros(n_steps),
        "vn_ratio": np.zeros(n_steps)
    }

    # track infection times
    infect_times = np.ones(n_agents, dtype=int) * infect_time

    # keep path history (as a stack) for backtracking
    back = [[] for _ in range(n_agents)]

    # track "immunized" nodes
    immunized = np.zeros(n_nodes, dtype=int)

    social_distancing = False # whether social distancing is active
    immunizing        = False # whether immunization is active
    safe_threshold    = -1

    for step in tqdm(range(n_steps)):
        s_count = np.count_nonzero(agents[:, 0] ==  1) # susceptible
        i_count = np.count_nonzero(agents[:, 0] == -1) # infected
        r_count = np.count_nonzero(agents[:, 0] ==  0) # "recovered"
        v_count = np.count_nonzero(agents[:, 0] ==  2) # immune
        # print(s_count, i_count, r_count)
        history["s_count"][step] = s_count
        history["i_count"][step] = i_count
        history["r_count"][step] = r_count
        history["v_count"][step] = v_count

        history["is_ratio"][step] = i_count / (s_count + 1)
        history["in_ratio"][step] = i_count / n_agents
        history["rs_ratio"][step] = r_count / (s_count + 1)
        history["rn_ratio"][step] = r_count / n_agents
        history["vs_ratio"][step] = v_count / (s_count + 1)
        history["vn_ratio"][step] = v_count / n_agents

        contacts = defaultdict(list)
        ratio = i_count / (s_count + 1)
        threshold = 0.1

        # have we gone back below the threshold?
        if (social_distancing or immunizing) and safe_threshold < 0 and ratio < threshold:
            safe_threshold = step

        # enforce social distancing by lowering travel probability
        # when percentage of infected agents is >= 20%
        if not social_distancing and ratio >= threshold:
            # choose random agents to not participate
            rand_idx = np.random.choice(n_agents, size=int(n_agents * social), replace=False)
            agents[:, 2][rand_idx] = 0.1
            agents[:, 4][rand_idx] = 1 - (0.1 + stay_prob)
            social_distancing = True

        # handle immunizing nodes
        if not immunizing and ratio >= threshold:
            if immune == "random":
                rand_idx = np.random.choice(n_nodes, size=n_immune, replace=False)
                immunized[rand_idx] = 1
            elif immune == "degree":
                degree = np.array(graph.degree)
                high_idx = np.argpartition(degree[:, 1], -n_immune)[-n_immune:]
                immunized[high_idx] = 1
            elif immune == "vulnerableDegree":
                degree = np.array(graph.degree)
                # holds the history of nodes that were selected by degree
                dhist = []
                # the offset index for each node, to know how much of dhist has already been applied
                penaltyIndex = [0 for _ in range(n_nodes)]
                for i in range(n_immune):
                    # start with the current best candidate
                    nextCandidate = np.argmax(degree[:, 1])
                    candidate = -1
                    # check to see if removing degree from nodes 
                    while not candidate == nextCandidate:
                        candidate = nextCandidate
                        # apply a penalty if the candidate is connected to an already immunized node
                        # specifically one not already accounted for
                        for j in range(penaltyIndex[candidate], len(dhist)):
                            if graph.has_edge(dhist[j], candidate):
                                degree[candidate, 1] -= 1
                        # update the index list to say penalties for nodes before len(dhist) are already applied
                        penaltyIndex[candidate] = len(dhist)
                        # prepare to go again
                        nextCandidate = np.argmax(degree[:, 1])
                    # update immunization, history, and make sure we don't select the candidate again
                    degree[candidate, 1] = -1
                    immunized[candidate] = 1
                    dhist.append(candidate)
            elif immune == "population":
                # will hold current population at each node
                pop = [0 for _ in range(n_nodes)]
                # go through agents and update count to each node
                for i in agents:
                    pop[int(i[1])] += 1
                high_idx = np.argpartition(pop, -n_immune)[-n_immune:]
                immunized[high_idx] = 1
            elif immune == "importance":
                # make the adjacency matrix
                A = np.zeros((n_nodes, n_nodes))
                for e in graph.edges:
                    A[e[0], e[1]] = 1
                    A[e[1], e[0]] = 1
                # stores history of rows/cols removed
                shist = []
                for i in range(n_immune):
                    # get the abs eigenvector with max eigenvalue
                    _, v = np.linalg.eigh(A)
                    vec = np.abs(v[:, -1])
                    # pick the index which contributes the most to vector
                    selected = np.argmax(vec)
                    walker = selected
                    # increment to account for removed row/cols
                    for s in shist:
                        if selected >= s:
                            walker += 1
                    shist.append(selected)
                    immunized[walker] = 1
                    # remove row/col to not consider
                    A = np.delete(np.delete(A, selected, 0), selected, 1)
            elif immune == "acquaint":
                rand_idx = np.random.choice(n_nodes, size=n_immune, replace=False)
                for idx in rand_idx:
                    new_node = np.random.choice(graph.adj[idx])
                    immunized[new_node] = 1

            immunizing = True

        # if args.gif and (step + 1) % 5 == 0 or step == 0: draw_graph(graph, positions, agents, history, step)
        if args.gif: draw_graph(graph, positions, agents, immunized, history, step)

        # just unpack them all
        for i, (stat, node, travel_prob, stay_prob, back_prob) in enumerate(agents):
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
            # prob = np.random.random()
            # TODO: make constants?
            action = np.random.choice([1, 2, 3], p=[travel_prob, stay_prob, back_prob])
            if action == 1:
                # go somewhere
                new_node = np.random.choice(graph.adj[node])
                back[i].append(node)
                agents[i][1] = new_node
                contacts[new_node].append(i)
            elif action == 2:
                # stay
                contacts[node].append(i)
                continue
            elif action == 3:
                # go back
                if len(back[i]) > 0:
                    new_node = back[i].pop()
                    agents[i][1] = new_node
                    contacts[new_node].append(i)

        # process contacts
        for node, group in contacts.items():
            # process immunization
            if immunized[int(node)] == 1:
                # immunize the group
                for idx in group:
                    if np.random.random() < p_immune:
                        agents[:, 0][idx] = 2.0

            # process infected contacts
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
                if s_agents.shape[0] == 0:
                    continue
                prob = min(1.0, i_agents.shape[0] * transmit_prob / s_agents.shape[0])
                res = np.random.choice([-1, 1], size=s_agents.shape[0], p=[prob, 1.0 - prob])
                agents[:, 0][s_agents] *= res

    if args.gif: make_gif(args)

    return history, immunized, safe_threshold

if __name__ == "__main__":
    args = get_args()
    print("running simulation on graph ({0}) immunizing ({1} -n_immune ({2}))".format(args.graph, args.immune, args.n_immune))
    np.random.seed(args.seed)
    random.seed(args.seed)
    graph = get_graph(args.graph) # graph
    positions = nx.spring_layout(graph, seed=args.seed) # node positions
    history_list = []

    runs = 1 if args.gif else args.runs

    s_count = np.zeros(runs, dtype=int)
    r_count = np.zeros(runs, dtype=int)
    v_count = np.zeros(runs, dtype=int)
    rn_ratio = np.zeros(runs, dtype=float)
    vn_ratio = np.zeros(runs, dtype=float)
    i_thresh = np.zeros(runs, dtype=int)

    # create agents
    for i in range(runs):
        # agents are a vector [infection status, node, actions...]
        agents = np.ones((args.agents, 2 + 3), dtype=float)
        agents[:, 1] = range(agents.shape[0]) # where to place them?
        # set actions
        agents[:, 2] = args.travel
        agents[:, 3] = args.stay
        agents[:, 4] = 1 - (args.travel + args.stay)
        # randomly infect some
        rand_idx = np.random.choice(range(agents.shape[0]), size=2)
        agents[:, 0][rand_idx] = -1
        history, immunized, safe_threshold = simulate(args, graph, positions, agents)
        history_list.append(history)
        history_data = np.array(list(history.values()))

        s_count[i] = history["s_count"][-1]
        r_count[i] = history["r_count"][-1]
        v_count[i] = history["v_count"][-1]
        rn_ratio[i] = history["rn_ratio"][-1]
        vn_ratio[i] = history["vn_ratio"][-1]
        i_thresh[i] = safe_threshold
    if not args.gif: draw_history(args, graph, positions, immunized, history_list)

    print("  statistics")
    print("  s_count median {0}, mean {1}, std {2}".format(np.median(s_count), np.mean(s_count), np.std(s_count)))
    print("  r_count median {0}, mean {1}, std {2}".format(np.median(r_count), np.mean(r_count), np.std(r_count)))
    print("  v_count median {0}, mean {1}, std {2}".format(np.median(v_count), np.mean(v_count), np.std(v_count)))
    print("  rn_ratio median {0}, mean {1}, std {2}".format(np.median(rn_ratio), np.mean(rn_ratio), np.std(rn_ratio)))
    print("  vn_ratio median {0}, mean {1}, std {2}".format(np.median(vn_ratio), np.mean(vn_ratio), np.std(vn_ratio)))
    print("  i_thresh median {0}, mean {1}, std {2}".format(np.median(i_thresh), np.mean(i_thresh), np.std(i_thresh)))
    print()