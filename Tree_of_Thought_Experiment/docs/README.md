## tot_bfs Method
The tot_bfs method performs a breadth-first search to solve the problem. It takes the following parameters:

initial_prompt: The initial problem or prompt to be solved.
num_thoughts: The number of thoughts to generate at each step.
max_steps: The maximum number of steps to perform in the search.
max_states: The maximum number of states to consider at each step.
pruning_threshold: The threshold value for pruning states.
The method generates and evaluates states at each step, selecting the best states based on their values. The search continues until the maximum number of steps is reached, and the best state is returned.

## tot_dfs Method
The tot_dfs method performs a depth-first search to solve the problem. It takes the following parameters:

initial_prompt: The initial problem or prompt to be solved.
num_thoughts: The number of thoughts to generate at each step.
max_steps: The maximum number of steps to perform in the search.

value_threshold: The threshold value for pruning states.
pruning_threshold: The threshold value for pruning states based on their values.
confidence_threshold: The confidence threshold for stopping the search.
max_iterations: The maximum number of iterations allowed for the search.
convergence_threshold: The threshold for determining convergence.
convergence_count: The number of consecutive convergences required to stop the search.
The method uses a recursive depth-first search approach to explore the state space. It generates and evaluates states at each step, and if a state's value is above the value_threshold and pruning_threshold, it continues the search with the new state. The search stops when the maximum number of steps is reached, the confidence threshold is met, or the convergence criteria are satisfied. The best state is then returned.

## save_tree_to_json Method
The save_tree_to_json method saves the current tree structure and metrics to a JSON file. It takes the following parameter:

file_name: The name of the JSON file to save the tree structure and metrics.
This method is useful for logging the search process and analyzing the results later.

## print_tree Method
The print_tree method prints the tree structure in a human-readable format. It takes the following parameters:

node: The current node in the tree.
depth: The depth of the current node in the tree (default is 0).
This method is useful for visualizing the tree structure and understanding the search process.
