# cs618-final-project

# Some kind of epidemic simulator
- Description
    - Graph `G` that consists of nodes `N`
        - Graphs generated with https://networkx.org/documentation/stable/reference/generators.html
    - Set of a agents `A`
        - Possible actions
            - Move - move to an adjacent node
            - Stay - stay at the current node
            - Return - return to the previous node
                - Or return to starting node? This makes sense: agent will travel around, then go back to where it started (home?)
                - Agent would enter a state where it will traverse the path back before moving/staying again
    - Interaction model
        - At each timestep `t`:
            - Every agent performs `1` action
    - Transmission model
        - Get set of nodes that contain infected agents
        - If node also contains susceptible agents:
          - Let `tp` be the probability of transmission
          - Let `ni` be the number of infected agents at the node
          - Susceptible agents have a `tp * ni` probability of infection
