from random import choice
from tqdm import tqdm

from cube import RubiksCube

class IDA_star(object):
    def __init__(self, heuristic, max_depth = 20):
        """
        Input: 
            heuristic (dict): dictionary containing the heuristic map
            max_depth (int): integer representing the max depth of the search tree (Default: 20)

        Description: 
            initialize the IDA* algorithm

        Output:
            None
        """
        self.max_depth = max_depth
        self.threshold = max_depth
        self.min_threshold = None
        self.heuristic = heuristic
        self.moves = []

    def run(self, state):
        """
        Input: 
            state (str): representing the current state of the cube

        Description: 
            solve the Rubik's cube

        Output: 
            list containing the moves taken to solve the cube
        """
        while True:
            status = self.search(state, 1)
            if status: return self.moves
            self.moves = []
            self.threshold = self.min_threshold
        return []

    def search(self, state, g_score):
        """
        Input: 
            state (str): string representing the current state of the cube
            g_score (int): integer representing the cost to reach the current node

        Description: 
            Uses the IDA* algorithm to search the search tree and solve the cube.

        Output: 
            A boolean indicating if the Rubik's Cube has been solved.
        """
        # Create a Rubik's Cube object from the input state
        cube = RubiksCube(state=state)

        # Check if the cube is already solved
        if cube.solved():
            return True

        # Check if the number of moves performed so far has exceeded the threshold
        elif len(self.moves) >= self.threshold:
            return False

        # Initialize variables for finding the next best action
        min_val = float('inf')
        best_action = None

        # Loop through all possible actions: horizontal twist, vertical twist, or side twist
        for a in [(r, n, d) for r in ['h', 'v', 's'] for d in [0, 1] for n in range(cube.n)]:

            # Create a new Rubik's Cube object for each possible action
            cube = RubiksCube(state=state)

            # Perform the twist action based on the current iteration
            if a[0] == 'h':
                cube.horizontal_twist(a[1], a[2])
            elif a[0] == 'v':
                cube.vertical_twist(a[1], a[2])
            elif a[0] == 's':
                cube.side_twist(a[1], a[2])

            # If the twist action results in a solved cube, return True
            if cube.solved():
                self.moves.append(a)
                return True

            # Otherwise, calculate the heuristic and f-scores for the current cube state
            cube_str = cube.stringify()
            h_score = self.heuristic[cube_str] if cube_str in self.heuristic else self.max_depth
            f_score = g_score + h_score

            # Check if the current f-score is the new minimum f-score, and save the current action as the best action
            if f_score < min_val:
                min_val = f_score
                best_action = [(cube_str, a)]
            elif f_score == min_val:
                if best_action is None:
                    best_action = [(cube_str, a)]
                else:
                    best_action.append((cube_str, a))

        # If a best action has been found, execute the action and recursively call the search function on the new cube state
        if best_action is not None:
            if self.min_threshold is None or min_val < self.min_threshold:
                self.min_threshold = min_val
            next_action = choice(best_action)
            self.moves.append(next_action[1])
            status = self.search(next_action[0], g_score + min_val)
            if status:
                return status

        # If no best action has been found, return False
        return False

def build_heuristic_db(state, actions, max_moves = 20, heuristic = None):
    """
    Input: 
        state (str): A string representing the current state of the cube.
        actions (list): A list containing tuples representing the possible actions that can be taken.
        max_moves (int): An integer representing the max amount of moves allowed. (Default: 20)
        heuristic (dict): A dictionary containing the current heuristic map. (Default: None)

    Description: 
        Build a heuristic map for determining the best path for solving a Rubik's Cube.

    Output:
        A dictionary containing the heuristic map.
    """
    # If no heuristic is provided, start with a dictionary containing the current state with a heuristic value of 0
    if heuristic is None:
        heuristic = {state: 0}

    # Create a queue with the starting state and a depth of 0
    que = [(state, 0)]

    # Calculate the total number of nodes in the tree (for progress tracking)
    node_count = sum([len(actions) ** (x + 1) for x in range(max_moves + 1)])

    # Use tqdm for progress tracking
    with tqdm(total=node_count, desc='Heuristic DB') as pbar:
        # Keep searching until the queue is empty
        while True:
            if not que:
                break
            # Get the next state and depth from the queue
            s, d = que.pop()

            # If the depth is greater than the maximum allowed moves, skip to the next state in the queue
            if d > max_moves:
                continue

            # Try each possible action on the current state
            for a in actions:
                cube = RubiksCube(state=s)
                if a[0] == 'h':
                    cube.horizontal_twist(a[1], a[2])
                elif a[0] == 'v':
                    cube.vertical_twist(a[1], a[2])
                elif a[0] == 's':
                    cube.side_twist(a[1], a[2])
                a_str = cube.stringify()

                # If the resulting state is not in the heuristic dictionary, add it with a heuristic value of the current depth + 1
                if a_str not in heuristic or heuristic[a_str] > d + 1:
                    heuristic[a_str] = d + 1

                # Add the resulting state to the queue with a depth of the current depth + 1
                que.append((a_str, d+1))

                # Update the progress bar
                pbar.update(1)
    
    # Return the final heuristic dictionary
    return heuristic