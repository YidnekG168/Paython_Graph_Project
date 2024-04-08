# Network Growth Simulation
This Python script simulates the growth of a network over time, where nodes with higher degrees and fitness values are more likely to attract connections from new nodes. It provides insights into how networks expand and how the presence of special nodes with higher fitness values influences the network's structure and dynamics.

# Getting Started
To run the simulation, follow these steps:

Ensure you have Python installed on your system.

Clone this repository to your local machine.

Make sure the input JSON file (input.json) is in the same directory as the script.

Open a terminal or command prompt and navigate to the directory containing the script.

Run the script using the following command:

Copy code
# python network_simulation.py
The script will execute the simulation based on the input data provided in the JSON file and plot the graphs accordingly.

# Input Data
The simulation requires input parameters specified in a JSON file (input.json). These parameters include:

m: Number of privileged nodes.
nc: Normal fitness value.
max_n: Maximum number of nodes.
n_fraction: Fraction of special nodes.
normal_node_to_graph: Number of normal nodes to graph.
special_node_to_graph: Number of special nodes to graph.
Adjustments can be made to these parameters in the JSON file to customize the simulation.

# Output
After running the simulation, the script generates plots to visualize the growth of the network over time. These plots include:

Graph showing the relationship between time steps and node degrees.
Graph showing the relationship between time steps and node fitness values.
These visualizations help analyze how the network evolves and how the fitness values of special nodes change over time.

# Contributing
Contributions to this project are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.
