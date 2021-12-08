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
    maze[start[0]][start[1]] = -1

    maze[end[0]][end[1]] = -9

    return maze


# Obstacles define by a 7


def init_obstacles(maze, obstacles):

    for obstacle in obstacles:


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


def this_state_is_already_discovered(this_state, maze):
    state = maze[this_state[0]][this_state[1]]
    if state == 2:
        return 1
    return 0


def this_state_is_an_obstacle(this_state, maze):
    state = maze[this_state[0]][this_state[1]]
    if state == 7:
        return 1
    return 0    


def this_state_is_not_special_and_undiscoverd(this_state, maze):
    if(this_state == 0 or this_state == -1):
        return 0
    state = maze[this_state[0]][this_state[1]]
    if state == 0:
        return 1
    return 0  


def possible_next_not_special_undiscovered_state(current_state, maze):

    possible_next = []
    up = up_neighbour(current_state, maze)
    right = right_neighbour(current_state, maze)
    down = down_neighbour(current_state, maze)
    left = left_neighbour(current_state, maze)
    if(this_state_is_not_special_and_undiscoverd(up, maze)):
        possible_next.append(up) 
    if(this_state_is_not_special_and_undiscoverd(right, maze)):
        possible_next.append(right) 
    if(this_state_is_not_special_and_undiscoverd(down, maze)):
        possible_next.append(down) 
    if(this_state_is_not_special_and_undiscoverd(left, maze)):
        possible_next.append(left) 

    return possible_next


def random_choose_between_possible_undiscovered_states(current_state, maze):

    possible_next_states = possible_next_not_special_undiscovered_state(current_state, maze)    #issue when len == 0
    if(possible_next_states == 0):
        return random_movement
    rand = randint(0, len(possible_next_states) - 1)

    return possible_next_states[rand]


def actualize_state(current_state, next_state, maze):

    if maze[next_state[0]][next_state[1]] == -9:

        maze[current_state[0]][current_state[1]] = 2

        maze[next_state[0]][next_state[1]] = 1

        return [0, maze]

    maze[current_state[0]][current_state[1]] = 2

    maze[next_state[0]][next_state[1]] = 1

    return [maze]



#First modelization of the solution, at each state we gonna do a random
# authorized movement untill we get to the end of the maze


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


                    return 0

                return [movement[counter], maze]

            counter_possible_movement += 1


def random_journey(
    obstacles, start, end, num_rows, num_columns
):

    maze = init_empty_maze(num_rows, num_columns)     #Init should be done outside of the func

    maze = init_start_end(maze, start, end)

    maze = init_obstacles(maze, obstacles)


    init_state = start

    [new_state, new_maze] = random_movement(init_state, maze)
    update_of_the_visual_window(
                        new_maze, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
                            )

    for counter in range(10000):

        new_iteration = random_movement(new_state, new_maze)
        time.sleep(0.05)
        update_of_the_visual_window(
                        new_maze, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
                            )
        if not new_iteration:  # stopping condition, we finished the maze

            print("found the END i'm not lost anymore wouhou")
            return maze

        [new_state, new_maze] = new_iteration
    print("still stuck, it sucks tho")

    return 10000




#Second modelization, here we are will visit a random state which hasn't been visited
# many problem mgiht occur

def journey_to_an_unknown_world(
        obstacles, start, end, num_rows, num_columns, maze
    ):

    init_state = start
    new_state = random_choose_between_possible_undiscovered_states(init_state, maze)
    new_maze = actualize_state(init_state, new_state, maze)[0]
    [current_state, current_maze] = [new_state, new_maze]
    update_of_the_visual_window(
                            maze, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
                            )

    for counter in range(10000):
        new_state = random_choose_between_possible_undiscovered_states(current_state, new_maze)
        maze = actualize_state(current_state, new_state, new_maze)[0]
        time.sleep(0.3)
        update_of_the_visual_window(
                            maze, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
                            )
        # if new_iteration == [1, 1]:  # stopping condition, we finished the maze
        #                         #might want to review this condition btw

        #     print("found the END i'm not lost anymore wouhou")
        #     return maze

        current_state = new_state
    print("still stuck, it sucks tho")


    return 10000


#Third modelization, here we will add the distance and choose the movement
#that has the lowest distance to the end

# Bewhare here the algorithm has a global point of view, he knows where
# he is, where the start and where the end is

def pure_manhattan_distance_to_end_point(
        current_state, end, maze
    ):
    print(current_state)  #current_stae = 1 when we hit an obstacle
    print(end)
    vertical_distance = abs(current_state[0] - end[0])
    horizontal_distance = abs(current_state[1] - end[1])
    return horizontal_distance + vertical_distance



def closest_point_to_the_end(current_state, end, maze):
    possible_options = possible_movement(current_state, maze)
    smallest_distance = 1000000
    counter = 0
    distances = []
    for option in possible_options:
        if(not(option == 0 or option == -1 or option == 2)):          # for now we don't make difference between wall and border
            current_distance = pure_manhattan_distance_to_end_point(possible_options[counter], end, maze)
            if(current_distance < smallest_distance):
                smallest_distance = current_distance
                option_closest_to_the_end = option
            distances.append(current_distance)
        else:
            distances.append(10000)
        counter += 1
    if(maze_is_finished(current_state, end, maze)):
        return [1, 1]
    return [distances, option_closest_to_the_end]
    


def maze_is_finished(current_state, end, maze):
    if(current_state == end):
        return 1
    return 0


def go_to_closest_point_to_the_end(current_state, end, maze):

    next_state = closest_point_to_the_end(current_state, end, maze)[1]
    distances = closest_point_to_the_end(current_state, end, maze)[0]
    maze = actualize_state(current_state, next_state, maze)[0]

    return [next_state, maze]


    


def closest_point_to_the_end_journey(
    obstacles, start, end, num_rows, num_columns, maze
):

    init_state = start
    [new_state, new_maze] = go_to_closest_point_to_the_end(init_state, end, maze)
    [current_state, current_maze] = [new_state, new_maze]
    update_of_the_visual_window(
                            maze, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
                            )

    for counter in range(10000):

        new_iteration = go_to_closest_point_to_the_end(new_state, end, new_maze)
        time.sleep(0.1)
        update_of_the_visual_window(
                            maze, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
                            )
        if new_iteration == [1, 1]:  # stopping condition, we finished the maze
                                #might want to review this condition btw

            print("found the END i'm not lost anymore wouhou")
            return maze

        [new_state, new_maze] = new_iteration
    print("still stuck, it sucks tho")


    return 10000






                        ########################
                        ###                 ####
                        ###   VISUAL        ####
                        ###                 ####
                        ########################


#
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


def optimized_update_of_the_visual_window(
    maze, current_state, next_state, cell_width, cell_height, blue_rectangles_ids, green_rectangles_ids, canva
):
    
    canva.itemconfig(green_rectangles_ids[current_state[0]][current_state[1]], state="normal")
    canva.itemconfig(green_rectangles_ids[next_state[0]][next_state[1]], state="hidden")
    canva.itemconfig(blue_rectangles_ids[next_state[0]][next_state[1]], state="normal")
            
    canva.update()


# On a chaque itération qui permet de détermnier quel sera le prochain moove
# on veut qu'a chaque nouvelle itération on ai la nouvelle cellule qui se mette en bleu et l'ancienne qui se mette en vert

#def update_visual_last_iteration (maze, current_state): #Here we want to actualize the current state to go from blue to red

# Initialize everything 
window_height = 900
window_width = 900
num_rows = 30
num_columns = 30
cell_height = int(window_height / num_columns)
cell_width = int(window_width / num_rows)
start = [10,4]
end = [1, 25]
obstacles = [[0,5], [1,5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5]]


maze = init_empty_maze(num_rows, num_columns)
maze = init_start_end(maze, start, end)
maze = init_obstacles(maze, obstacles)

print(possible_next_not_special_undiscovered_state(start, maze))


#visual init
canva = initialize_canva(window_height, window_width)
red_rectangle_ids = (create_red_rectangles(num_columns, num_rows, cell_width, cell_height, canva))
blue_rectangle_ids = (create_blue_rectangles(num_columns, num_rows, cell_width, cell_height, canva))
green_rectangle_ids = (create_green_rectangles(num_columns, num_rows, cell_width, cell_height, canva))
init_obstacles_visual_window(maze, cell_width, cell_height, canva, red_rectangle_ids)
update_of_the_visual_window(
    maze, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
)

#run alogrithm

#random_journey(obstacles, start, end, num_rows, num_columns)
#closest_point_to_the_end_journey(obstacles, start, end, num_rows, num_columns, maze)


journey_to_an_unknown_world(obstacles, start, end, num_rows, num_columns, maze)

# Visual test
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

