# Rubiks Cube A* Solver

This is a Python implementation of a solver for Rubik's Cube using the A* search algorithm. It includes a graphical user interface (GUI) that allows the user to manipulate and solve the cube step-by-step.

<img src="https://user-images.githubusercontent.com/75742343/225011287-ff8903a2-edc1-4dc7-971f-2aa1f7ac2db2.png" width=30% height=30%> <img src="https://user-images.githubusercontent.com/75742343/225010427-484405bd-2d70-4910-a9ba-989a9c6897a0.png" width=30% height=30%> <img src="https://user-images.githubusercontent.com/75742343/225012148-aae932de-dc0d-473f-8951-ace26855d4ed.png" width=30% height=33%>


## Requirements

- Python 3.x
- Urina
- iqdm

## Features

- 3D Rubik's Cube display
- Ability to manually twist the Rubik's Cube using buttons on the interface
- Ability to randomly scramble the Rubik's Cube using a button on the interface
- Ability to solve the Rubik's Cube using the A* search algorithm with a button on the interface
- Ability to step through the solution move by move using a button on the interface
- 3D animation of the Rubik's Cube during the solution process
- Console output of the moves made during the solution process

## Installation

1. Clone this repository to your local machine using 
```bash 
git clone https://github.com/jhannesreimann/rubiks-cube-a-solver.git
```
2. Install the necassary dependencies using 
```bash
pip install -r requirements.txt
```

## Usage

To run the program, execute the following command in the terminal:

```bash
python main.py
```

1. Use the keyboard to manually twist the Rubik's Cube or randomly scramble it using the button "random cube"
    - `u` : Upper face, clockwise
    - `e` : Equator, counterclockwise
    - `d` : Down face, counterclockwise
    - `l` : Left face, counterclockwise
    - `m` : Middle slice, counterclockwise
    - `r` : Right face, clockwise
    - `f` : Front face, clockwise
    - `s` : Standing slice, clockwise
    - `b` : Back face, counterclockwise
    - Use `shift` before and while pressing the keys, to reverse the direction
2. Click the "solve" button to solve the Rubik's Cube using the A* search algorithm.
3. Click the "next move" button to step through the solution move by move.
4. Observe the 3D animation of the Rubik's Cube and the console output of the moves made during the solution process.
    - Rotate the cube with right click dragging
