from random import randint, choice

class RubiksCube:

    def __init__(self, n = 3, colors = ['w', 'o', 'g', 'r', 'b', 'y'], state = None):
        """
        Input:
            n (int): The width and height of the Rubik's cube (Default: 3)
            colors (list): A list containing the first letter of every color you wish to use (Default: ['w', 'o', 'g', 'r', 'b', 'y'])
            state (str): A string representing the current state of the Rubik's cube (Default: None)

        Description:
            Initializes the Rubik's cube object with the specified dimensions, colors, and state.
            If state is None, a new Rubik's cube is created and initialized to the solved state.
            If state is not None, the Rubik's cube is created and initialized to the specified state.

        Output:
            None
        """
        if state is None:
            self.n = n
            self.colors = colors
            self.reset()
        else:
            self.n = int((len(state) / 6) ** (.5))
            self.colors = []
            self.cube = [[[]]]
            for i, s in enumerate(state):
                if s not in self.colors: self.colors.append(s)
                self.cube[-1][-1].append(s)
                if len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) < self.n:
                    self.cube[-1].append([])
                elif len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) == self.n and i < len(state) - 1:
                    self.cube.append([[]])

    def reset(self):
        """
        Input: 
            None

        Description: 
            Reset the cube to its inital state

        Output: 
            None
        """
        self.cube = [[[c for x in range(self.n)] for y in range(self.n)] for c in self.colors]

    def solved(self):
        """
        Input: 
            None

        Description: 
            Checks if the Rubik's cube is solved or not.

        Output: 
            A boolean value, True if the cube is solved, False otherwise.
        """
        for side in self.cube:
            hold = []
            for row in side:
                if len(set(row)) == 1:
                    hold.append(row[0])
                else:
                    return False
            if len(set(hold)) > 1:
                return False

        return True

    def stringify(self):
        """
        Input: 
            None

        Description: 
            Creates a string representation of the Rubik's cube in its current state.

        Output: 
            A string representing the Rubik's cube in its current state.
        """
        return ''.join([i for r in self.cube for s in r for i in s])

    def shuffle(self, l_rot = 5, u_rot = 100):
        """
        Input:
            l_rot (int): Lower bound of amount of moves. (Default: 5)
            u_rot (int): Upper bound of amount of moves. (Default: 100)

        Description: 
            Shuffles the Rubik's Cube to a random solvable state.

        Output: 
            List of moves performed to shuffle the cube.
        """
        moveArray = []
        moves = randint(l_rot, u_rot)
        actions = [
            ('h', 0),
            ('h', 1),
            ('v', 0),
            ('v', 1),
            ('s', 0),
            ('s', 1)
        ]
        for i in range(moves):
            a = choice(actions)
            j = randint(0, self.n - 1)
            moveArray.append((a[0], j, a[1]))
            if a[0] == 'h':
                self.horizontal_twist(j, a[1])
            elif a[0] == 'v':
                self.vertical_twist(j, a[1])
            elif a[0] == 's':
                self.side_twist(j, a[1])

        return moveArray

    def show(self):
        """
        Input: None
        Description: Show the rubiks cube in terminal
        Output: None
        """
        spacing = f'{" " * (len(str(self.cube[0][0])) + 2)}'
        l1 = '\n'.join(spacing + str(c) for c in self.cube[0])
        l2 = '\n'.join('  '.join(str(self.cube[i][j]) for i in range(1,5)) for j in range(len(self.cube[0])))
        l3 = '\n'.join(spacing + str(c) for c in self.cube[5])
        print(f'{l1}\n\n{l2}\n\n{l3}')

    def horizontal_twist(self, row, direction):
        """
        Input:
            row (int): The row to be twisted.
            direction (bool): The direction of the twist. Left is represented by False (0) and right by True (1).

        Description: 
            Twists the desired row of the Rubik's cube.

        Output: 
            None
        """
        if row < len(self.cube[0]):
            if direction == 0:
                self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (self.cube[2][row],
                                                                                              self.cube[3][row],
                                                                                              self.cube[4][row],
                                                                                              self.cube[1][row])

            elif direction == 1:
                self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (self.cube[4][row],
                                                                                              self.cube[1][row],
                                                                                              self.cube[2][row],
                                                                                              self.cube[3][row])
            else:
                print(f'ERROR - direction must be 0 or 1. {direction} is not a valid direction')
                return
            #Rotating connected face
            if direction == 0:
                if row == 0:
                    self.cube[0] = [list(x) for x in zip(*reversed(self.cube[0]))] #Transpose top
                elif row == len(self.cube[0]) - 1:
                    self.cube[5] = [list(x) for x in zip(*reversed(self.cube[5]))] #Transpose bottom
            elif direction == 1:
                if row == 0:
                    self.cube[0] = [list(x) for x in zip(*self.cube[0])][::-1] #Transpose top
                elif row == len(self.cube[0]) - 1:
                    self.cube[5] = [list(x) for x in zip(*self.cube[5])][::-1] #Transpose bottom
        else:
            print(f'ERROR - row must be between 0 and {len(self.cube[0]) - 1}. {row} is not a valid row')
            return

    def vertical_twist(self, column, direction):
        """
        Input: 
            column (int): The column to be twisted.
            direction (bool): The direction of the twist. Up is represented by False (0) and down by True (1).

        Description: 
            Twists the desired column of the Rubik's cube.

        Output: 
            None
        """
        if column < len(self.cube[0]):
            for i in range(len(self.cube[0])):
                if direction == 0:
                    self.cube[0][i][column], self.cube[2][i][column], self.cube[4][-i-1][-column-1], self.cube[5][i][column] = (self.cube[4][-i-1][-column-1],
                                                                                                                                self.cube[0][i][column],
                                                                                                                                self.cube[5][i][column],
                                                                                                                                self.cube[2][i][column])
                elif direction == 1:
                    self.cube[0][i][column], self.cube[2][i][column], self.cube[4][-i-1][-column-1], self.cube[5][i][column] = (self.cube[2][i][column],
                                                                                                                                self.cube[5][i][column],
                                                                                                                                self.cube[0][i][column],
                                                                                                                                self.cube[4][-i-1][-column-1])
                else:
                    print(f'ERROR - direction must be 0 or 1. {direction} is not a valid direction')
                    return
            #Rotating connected face
            if direction == 0: #Twist down
                if column == 0:
                    self.cube[1] = [list(x) for x in zip(*self.cube[1])][::-1] #Transpose left
                elif column == len(self.cube[0]) - 1:
                    self.cube[3] = [list(x) for x in zip(*self.cube[3])][::-1] #Transpose right
            elif direction == 1: #Twist up
                if column == 0:
                    self.cube[1] = [list(x) for x in zip(*reversed(self.cube[1]))] #Transpose left
                elif column == len(self.cube[0]) - 1:
                    self.cube[3] = [list(x) for x in zip(*reversed(self.cube[3]))] #Transpose right
        else:
            print(f'ERROR - column must be between 0 and {len(self.cube[0]) - 1}. {column} is not a valid column')
            return

    def side_twist(self, column, direction):
        """
        Input: 
            column (int): the column to be twisted
            direction (bool): The direction of the twist. Up is represented by False (0) and down by True (1).

        Description: 
            Twists the desired side of the Rubik's cube.

        Output: 
            None
        """
        if column < len(self.cube[0]):
            for i in range(len(self.cube[0])):
                if direction == 0:
                    self.cube[0][column][i], self.cube[1][-i-1][column], self.cube[3][i][-column-1], self.cube[5][-column-1][-1-i] = (self.cube[3][i][-column-1],
                                                                                                                                      self.cube[0][column][i],
                                                                                                                                      self.cube[5][-column-1][-1-i],
                                                                                                                                      self.cube[1][-i-1][column])
                elif direction == 1:
                    self.cube[0][column][i], self.cube[1][-i-1][column], self.cube[3][i][-column-1], self.cube[5][-column-1][-1-i] = (self.cube[1][-i-1][column],
                                                                                                                                      self.cube[5][-column-1][-1-i],
                                                                                                                                      self.cube[0][column][i],
                                                                                                                                      self.cube[3][i][-column-1])
                else:
                    print(f'ERROR - direction must be 0 or 1. {direction} is not a valid direction')
                    return
            #Rotating connected face
            if direction == 0:
                if column == 0:
                    self.cube[4] = [list(x) for x in zip(*reversed(self.cube[4]))] #Transpose back
                elif column == len(self.cube[0]) - 1:
                    self.cube[2] = [list(x) for x in zip(*reversed(self.cube[2]))] #Transpose top
            elif direction == 1:
                if column == 0:
                    self.cube[4] = [list(x) for x in zip(*self.cube[4])][::-1] #Transpose back
                elif column == len(self.cube[0]) - 1:
                    self.cube[2] = [list(x) for x in zip(*self.cube[2])][::-1] #Transpose top
        else:
            print(f'ERROR - side must be between 0 and {len(self.cube[0]) - 1}. {column} is not a valid side')
            return