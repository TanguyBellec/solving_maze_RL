from tkinter import Tk, Canvas

from random import randint

import time
import sys


# On def une matrice de taille n * m qui initialise notre futur labyrinthe

# Pour la modélisation on prendra une matrice de taille 90 x 90 avec des cellules de taille 30x30 pixels (window 900x900 pixels)


# Pour l'instant on commencera avec une matrice 10x10


def init_empty_maze(num_rows, num_columns):

    maze = []

    for row_counter in range(num_rows):

        empty_row = []

        for col_counter in range(num_columns):

            empty_row.append(0)

        maze.append(empty_row)

    return maze


# The starting point will be define by -1

# Then ending point by -9


def init_start_end(maze, start, end):
    print(maze)

    maze[start[0]][start[1]] = -1

    maze[end[0]][end[1]] = -9

    return maze


# Obstacles define by a 7


def init_obstacles(maze, obstacles):

    for obstacle in obstacles:

        # print(obstacle)

        maze[obstacle[0]][obstacle[1]] = 7

    return maze


# Current_state will be a list of two int : row_index, col_index

# How to get indices of the neighbours

# Test if we are above borders or if we hit a wall


def up_neighbour(
    current_state, maze
):  # possible to code smg if we get out of the window (doesn't test it there)

    if current_state[0] == 0:  # already at the border of the maze

        return 0

    if maze[current_state[0] - 1][current_state[1]] == 7:

        return -1

    else:

        return [current_state[0] - 1, current_state[1]]


def right_neighbour(current_state, maze):

    if current_state[1] == len(maze[0]) - 1:

        return 0

    if maze[current_state[0]][current_state[1] + 1] == 7:

        return -1

    else:

        return [current_state[0], current_state[1] + 1]


def down_neighbour(current_state, maze):

    if current_state[0] == len(maze) - 1:

        return 0

    if maze[current_state[0] + 1][current_state[1]] == 7:

        return -1

    else:

        return [current_state[0] + 1, current_state[1]]


def left_neighbour(current_state, maze):

    if current_state[1] == 0:

        return 0

    if maze[current_state[0]][current_state[1] - 1] == 7:

        return -1

    else:

        return [current_state[0], current_state[1] - 1]


def possible_movement(current_state, maze):

    return [
        (up_neighbour(current_state, maze)),
        (right_neighbour(current_state, maze)),
        (down_neighbour(current_state, maze)),
        (left_neighbour(current_state, maze)),
    ]


def actualize_state(current_state, next_state, maze):

    if maze[next_state[0]][next_state[1]] == -9:

        maze[current_state[0]][current_state[1]] = 2

        maze[next_state[0]][next_state[1]] = 1

        return [0, maze]

    maze[current_state[0]][current_state[1]] = 2

    maze[next_state[0]][next_state[1]] = 1

    return [maze]


def random_movement(current_state, maze):

    movement = possible_movement(current_state, maze)

    number_possible_movement = 0

    for counter in range(len(movement)):

        if movement[counter] != 0 and movement[counter] != -1:

            number_possible_movement += 1

    rand = randint(0, number_possible_movement - 1)

    counter_possible_movement = 0

    for counter in range(len(movement)):

        if movement[counter] != 0 and movement[counter] != -1:

            if counter_possible_movement == rand:

                if not actualize_state(current_state, movement[counter], maze)[
                    0
                ]:  # check if there are no erros when we get to the end

                    # print(maze)

                    return 0

                return [movement[counter], maze]

            counter_possible_movement += 1


def random_journey(
    obstacles, start, end, num_rows, num_columns
):

    maze = init_empty_maze(num_rows, num_columns)

    maze = init_start_end(maze, start, end)

    maze = init_obstacles(maze, obstacles)

    # print(maze)

    init_state = start

    [new_state, new_maze] = random_movement(init_state, maze)
    update_of_the_visual_window(
                        new_maze, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
                            )

    for counter in range(10000):

        new_iteration = random_movement(new_state, new_maze)
        time.sleep(0.005)
        update_of_the_visual_window(
                        new_maze, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
                            )
        if not new_iteration:  # stopping condition, we finished the maze

            print("found the END i'm not lost anymore wouhou")
            return maze

        [new_state, new_maze] = new_iteration
    print("still stuck, it sucks tho")

    # print(next_iteration)

    return 10000


# Code to move to the next state, we stay at the current state if  we hit an obstacle

def initialize_canva(width, height):
    root = Tk()
    canva = Canvas(root)
    canva.config(height=height, width=width, background="black")
    canva.pack()
    return canva


def init_obstacles_visual_window(maze, cell_width, cell_height, canva, red_rectangle_ids):
    num_rows = len(maze)
    num_columns = len(maze[0])
    for index_row in range(num_rows):            
        for index_column in range(num_columns):
            if maze[index_row][index_column] == 7:
                canva.itemconfig(red_rectangle_ids[index_row][index_column], state="normal")
    canva.update()




def create_green_rectangles(num_columns, num_rows, cell_width, cell_height, canva):     #past states
    green_rectangle_ids = []
    for index_row in range(num_rows):
        new_id_row = []
        for index_column in range(num_columns):
            rectangle_id = canva.create_rectangle(
                cell_width * index_column,
                cell_height * index_row,
                cell_width * (index_column + 1),
                cell_height * (index_row + 1),
                fill="green",
                state="hidden",
            )
            new_id_row.append(rectangle_id)
        green_rectangle_ids.append(new_id_row)
    return green_rectangle_ids


def create_red_rectangles(num_columns, num_rows, cell_width, cell_height, canva):       #obstacles
    red_rectangle_ids = []
    for index_row in range(num_rows):
        new_id_row = []
        for index_column in range(num_columns):
            rectangle_id = canva.create_rectangle(
                cell_width * index_column,
                cell_height * index_row,
                cell_width * (index_column + 1),
                cell_height * (index_row + 1),
                fill="red",
                state="hidden",
            )
            new_id_row.append(rectangle_id)
        red_rectangle_ids.append(new_id_row)
    return red_rectangle_ids

def create_blue_rectangles(num_columns, num_rows, cell_width, cell_height, canva):       #current state
    blue_rectangle_ids = []
    for index_row in range(num_rows):
        new_id_row = []
        for index_column in range(num_columns):
            rectangle_id = canva.create_rectangle(
                cell_width * index_column,
                cell_height * index_row,
                cell_width * (index_column + 1),
                cell_height * (index_row + 1),
                fill="blue",
                state="hidden",
            )
            new_id_row.append(rectangle_id)
        blue_rectangle_ids.append(new_id_row)
    return blue_rectangle_ids







def update_of_the_visual_window(
    maze, cell_width, cell_height, blue_rectangles_ids, green_rectangles_ids, canva
):
    num_columns = len(maze)
    num_rows = len(maze[0])
    for index_row in range(num_rows):           #update to get 
        for index_column in range(num_columns):
            if maze[index_row][index_column] == 1:
                canva.itemconfig(green_rectangles_ids[index_row][index_column], state="hidden")
                canva.itemconfig(blue_rectangles_ids[index_row][index_column], state="normal")
            if (maze[index_row][index_column] == 2) or (maze[index_row][index_column] == -1) or (maze[index_row][index_column] == -9):
                canva.itemconfig(green_rectangles_ids[index_row][index_column], state="normal")
            
    canva.update()
    # canva.after(
    #     200,
    #     update_of_the_visual_window(
    #         maze, cell_width, cell_height, rectangle_ids, canva
    #     ),
    # )



# On a chaque itération qui permet de détermnier quel sera le prochain moove
# on veut qu'a chaque nouvelle itération on ai la nouvelle cellule qui se mette en bleu et l'ancienne qui se mette en vert

#def update_visual_last_iteration (maze, current_state): #Here we want to actualize the current state to go from blue to red

# Initialize everything 
num_rows = 100
num_columns = 100
cell_height = 9
cell_width = 9
window_height = 900
window_width = 900
start = [50, 10]
end = [50, 90]
obstacles = [[1,5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5]]



maze = init_empty_maze(num_rows, num_columns)
maze = init_start_end(maze, start, end)
maze = init_obstacles(maze, obstacles)



#visual
canva = initialize_canva(window_height, window_width)
red_rectangle_ids = (create_red_rectangles(num_columns, num_rows, cell_width, cell_height, canva))
blue_rectangle_ids = (create_blue_rectangles(num_columns, num_rows, cell_width, cell_height, canva))
green_rectangle_ids = (create_green_rectangles(num_columns, num_rows, cell_width, cell_height, canva))
init_obstacles_visual_window(maze, cell_width, cell_height, canva, red_rectangle_ids)
update_of_the_visual_window(
    maze, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
)

random_journey(obstacles, start, end, num_rows, num_columns)
canva.mainloop()

#init_obstacles_visual_window




# def initialize_canva(width, height):
#     root = Tk()
#     canva = Canvas(root)
#     canva.config(height=height, width=width, background="black")
#     canva.pack()
#     return canva


# def create_green_rectangles(width, height, cell_width, cell_height, canva):
#     num_columns = int(width / cell_width)
#     num_rows = int(height / cell_height)
#     rectangle_ids = []
#     for index_row in range(num_rows):
#         new_id_row = []
#         for index_column in range(num_columns):
#             rectangle_id = canva.create_rectangle(
#                 cell_width * index_column,
#                 cell_height * index_row,
#                 cell_width * (index_column + 1),
#                 cell_height * (index_row + 1),
#                 fill="green"
#                 #state="hidden",
#             )
#             new_id_row.append(rectangle_id)
#         rectangle_ids.append(new_id_row)
#     return rectangle_ids


# canva = initialize_canva(900, 900)
# rectangle_ids = create_green_rectangles(
#     900, 900, 30, 30, canva
# )
# canva.mainloop()

