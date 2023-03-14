import json
import os.path
from ursina import *

from cube import RubiksCube
from solver import IDA_star, build_heuristic_db

#############################################
#########   Heuristic Database   ############ 
#############################################
MAX_MOVES = 5
NEW_HEURISTICS = False
HEURISTIC_FILE = os.path.join(os.path.dirname(__file__), 'heuristic.json')

cube = RubiksCube(n=3)

if os.path.exists(HEURISTIC_FILE):
    with open(HEURISTIC_FILE) as f:
        h_db = json.load(f)
else:
    h_db = None

if h_db is None or NEW_HEURISTICS is True:
    actions = [(r, n, d) for r in ['h', 'v', 's'] for d in [0, 1] for n in range(cube.n)]
    h_db = build_heuristic_db(
        cube.stringify(),
        actions,
        max_moves = MAX_MOVES,
        heuristic = h_db
    )

    with open(HEURISTIC_FILE, 'w', encoding='utf-8') as f:
        json.dump(
            h_db,
            f,
            ensure_ascii=False,
            indent=4
        )

#############################################
#######   3D Rubik's Cube Model   ###########
#############################################
moves_did = []

def parent_children(axis, position):
    """
    Input: 
        axis (str): 'x', 'y', or 'z'
        position (int): 0, 1, or 2
    
    Description:
        Parent all cubes to the center cube that are in the same position as the given axis and position.

    Output:
        None
    """
    for c in cubeA:
        c.position, c.rotation = round(c.world_position,1), c.world_rotation
        c.parent = scene # remove parent/child relationship
    
    center.rotation = 0

    for c in cubeA:
        if eval(f'c.position.{axis}') == position:
            c.parent = center

def move_noanimation(key, shift=False):
    """
    Input:
        key (str): key pressed
        shift (bool): True if shift key is held down, False otherwise (for counter-clockwise rotation)

    Description:
        Rotate the center cube and all cubes that are in the same position as the given axis and position.
        This function does not animate the rotation.

    Output:
        None
    """
    if key not in rotation_dict: return
    axis, position, angle = rotation_dict[key]
    parent_children(axis, position)
    eval(f'center.animate_rotation_{axis} ({-angle if shift else angle}, duration = 0)')

def move_animation(key, shift=False):
    """
    same as above (with animation)
    """
    if key not in rotation_dict: return
    axis, position, angle = rotation_dict[key]
    parent_children(axis, position)
    eval(f'center.animate_rotation_{axis} ({-angle if shift else angle}, duration = 0.5)')

def input(key, shift=False):
    """
    Input:
        key (str): key pressed
        shift (bool): True if shift key is held down, False otherwise (for counter-clockwise rotation)

    Description:
        Rotate the center cube and all cubes that are in the same position as the given axis and position
        and printing the move that was done and prints the new state of the cube.
        This function animates the rotation.

    Output:
        None
    """
    if key not in rotation_dict: return
    axis, position, angle = rotation_dict[key]
    parent_children(axis, position)
    shift = held_keys['shift']
    eval(f'center.animate_rotation_{axis} ({-angle if shift else angle}, duration = 0.5)')
    moves_did.append((key, shift))
    for m in keyShiftToMoves([(key, shift)]):
        if m[0] == 'h':
            cube.horizontal_twist(m[1], m[2])
        elif m[0] == 'v':
            cube.vertical_twist(m[1], m[2])
        elif m[0] == 's':
            cube.side_twist(m[1], m[2])
    print(keyShiftToMoves([(key, shift)]))
    cube.show()
    print('-----------')

def movesToKeyShift(moves):
    """
    Input:
        moves (list): list of moves

    Description:
        convert a move array to an array, which contains the key and shift
        for example: [('v', 0, 0)] -> [('l', False)]
        so in the moves array, the first element stands for 'vertical'/'horizontal'/'side-twist', the second for the position and the third for the direction
        the first element of the return array stands for the key and the second for the shift (like in the rotation_dict)

    Output:
        KeyShiftArray (list): list of key and shift
    """

    KeyShiftArray = []
    for m in moves:
        if m[0] == 'v':
            if m[1] == 0:
                if m[2] == 0:
                    KeyShiftArray.append(('l', False))
                else:
                    KeyShiftArray.append(('l', True))
            elif m[1] == 1:
                if m[2] == 0:
                    KeyShiftArray.append(('m', False))
                else:
                    KeyShiftArray.append(('m', True))
            else:
                if m[2] == 0:
                    KeyShiftArray.append(('r', True))
                else:
                    KeyShiftArray.append(('r', False))
        elif m[0] == 'h':
            if m[1] == 0:
                if m[2] == 0:
                    KeyShiftArray.append(('u', False))
                else:
                    KeyShiftArray.append(('u', True))
            elif m[1] == 1:
                if m[2] == 0:
                    KeyShiftArray.append(('e', True))
                else:
                    KeyShiftArray.append(('e', False))
            else:
                if m[2] == 0:
                    KeyShiftArray.append(('d', True))
                else:
                    KeyShiftArray.append(('d', False))
        elif m[0] == 's':
            if m[1] == 0:
                if m[2] == 0:
                    KeyShiftArray.append(('b', False))
                else:
                    KeyShiftArray.append(('b', True))
            elif m[1] == 1:
                if m[2] == 0:
                    KeyShiftArray.append(('s', True))
                else:
                    KeyShiftArray.append(('s', False))
            else:
                if m[2] == 0:
                    KeyShiftArray.append(('f', True))
                else:
                    KeyShiftArray.append(('f', False))
                
    return KeyShiftArray

def keyShiftToMoves(KeyShiftArray):
    """
    Input:
        KeyShiftArray (list): list of key and shift

    Description:
        convert an array, which contains the key and shift to a move array
        for example: [('l', False)] -> [('v', 0, 0)]

    Output:
        moves (list): list of moves
    """

    moves = []

    for m in KeyShiftArray:
        if m[0] == 'l':
            if m[1] == False:
                moves.append(('v', 0, 0))
            else:
                moves.append(('v', 0, 1))
        elif m[0] == 'm':
            if m[1] == False:
                moves.append(('v', 1, 0))
            else:
                moves.append(('v', 1, 1))
        elif m[0] == 'r':
            if m[1] == False:
                moves.append(('v', 2, 1))
            else:
                moves.append(('v', 2, 0))
        elif m[0] == 'u':
            if m[1] == False:
                moves.append(('h', 0, 0))
            else:
                moves.append(('h', 0, 1))
        elif m[0] == 'e':
            if m[1] == False:
                moves.append(('h', 1, 1))
            else:
                moves.append(('h', 1, 0))
        elif m[0] == 'd':
            if m[1] == False:
                moves.append(('h', 2, 1))
            else:
                moves.append(('h', 2, 0))
        elif m[0] == 'b':
            if m[1] == False:
                moves.append(('s', 0, 0))
            else:
                moves.append(('s', 0, 1))
        elif m[0] == 's':
            if m[1] == False:
                moves.append(('s', 1, 1))
            else:
                moves.append(('s', 1, 0))
        elif m[0] == 'f':
            if m[1] == False:
                moves.append(('s', 2, 1))
            else:
                moves.append(('s', 2, 0))
    
    return moves

def resetCube():
    """
    Input:
        None

    Description:
        reset the cube to the initial position

    Output:
        None
    """
    center.rotation = (0,0,0)
    for c in cubeA:
        c.rotation = (0,0,0)
        c.parent = scene
    for c in cubeA:
        if c.position == (1,1,1):
            c.parent = center
    moves_did = []

def randomCube():
    """
    Input:
        None

    Description:
        reset the cube and shuffle it with a random number of moves
    
    Output:
        shuffeledMoves (list): list of moves
    """
    resetCube()
    cube.reset()
    cube.show()
    print('-----------')
    shuffeledMoves = cube.shuffle(
        l_rot = MAX_MOVES if MAX_MOVES < 5 else 5,
        u_rot = MAX_MOVES
    )
    print(shuffeledMoves)
    cube.show()
    print('----------')
    shuffeledAnimation = movesToKeyShift(shuffeledMoves)
    moves_did = shuffeledAnimation
    for m in shuffeledAnimation:
        move_noanimation(m[0], m[1])

    solveBtn.enabled = True
    nextBtn.enabled = False

    return shuffeledMoves

def solve():
    """
    Input:
        None

    Description:
        solve the cube with IDA* algorithm.
        Prints the moves and the solved state to the console.

    Output:
        None
    """
    solver = IDA_star(h_db)
    global moves
    moves = solver.run(cube.stringify())
    global movesAnimate
    movesAnimate = movesToKeyShift(moves)

    print(moves)

    for m in moves:
        if m[0] == 'h':
            cube.horizontal_twist(m[1], m[2])
        elif m[0] == 'v':
            cube.vertical_twist(m[1], m[2])
        elif m[0] == 's':
            cube.side_twist(m[1], m[2])
    cube.show()

    nextBtn.enabled = True
    solveBtn.enabled = False

def oneMove():
    """
    Input:
        None
    
    Description:
        animate one move from the movesAnimate list

    Output:
        None
    """
    if len(movesAnimate) > 0:
        randomBtn.enabled = False
        solveBtn.enabled = False
        move_animation(movesAnimate[0][0], movesAnimate[0][1])
        movesAnimate.pop(0)
        if len(movesAnimate) == 0:
            randomBtn.enabled = True
            solveBtn.enabled = True
            nextBtn.enabled = False

####################################
########   Ursina App   ############
####################################
center = Entity()
cubeA = []

app = Ursina()
window.title = "Rubiks Cube"
window.icon = os.path.join(os.path.dirname(__file__), 'icon.ico')
window.borderless = False
window.size = (800, 800)
EditorCamera()

rotation_dict = {   'u': ['y', 1, 90],    'e': ['y', 0, -90],    'd': ['y', -1, -90],
                    'l': ['x', -1, -90],  'm': ['x', 0, -90],    'r': ['x', 1, 90],
                    'f': ['z', -1, 90],   's': ['z', 0, 90],     'b': ['z', 1, -90]}

for x in range(-1,2):
    for y in range(-1,2):
        for z in range(-1,2):
            pos = (x,y,z)
            cubeA.append(Entity(model='cube.obj', texture='texture.png', position=pos, scale=0.5))

#--------------------------------
cube.show()
print('-----------')
#--------------------------------

randomBtn = Button(text='random cube', scale=(0.2, 0.1), position=(-0.3, -0.4), on_click=randomCube, enabled=True)
solveBtn = Button(text='solve', scale=(0.2, 0.1), position=(0, -0.4), on_click=solve, enabled=True)
nextBtn = Button(text='next move', scale=(0.2, 0.1), position=(0.3, -0.4), on_click=oneMove, enabled=False)

app.run()