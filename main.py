from tkinter import Tk, Canvas

from random import randint

import time
import sys


# On def une matrice de taille n * m qui initialise notre futur labyrinthe

# Pour la modélisation on prendra une matrice de taille 90 x 90 avec des cellules de taille 30x30 pixels (window 900x900 pixels)


# Pour l'instant on commencera avec une matrice 10x10




                        ########################
                        ###                 ####
                        ###   INIT          ####
                        ###                 ####
                        ########################



def init_empty_maze(num_rows, num_columns):

    maze = []

    for row_counter in range(num_rows):

        empty_row = []

        for col_counter in range(num_columns):

            empty_row.append("undiscovered")

        maze.append(empty_row)

    return maze


# The starting point will be define by -1

# Then ending point by -9


def init_start_end(maze, start, end):

    maze[start[0]][start[1]] = "start"
    maze[end[0]][end[1]] = "end"

    return maze


# Obstacles define by a 7


def init_obstacles(maze, obstacles):

    for obstacle in obstacles:
        maze[obstacle[0]][obstacle[1]] = "obstacle"

    return maze


# Current_state will be a list of two int : row_index, col_index

# How to get indices of the neighbours

# Test if we are above borders or if we hit a wall






                        ####################################
                        ###                             ####
                        ###   RETURN INFORMATION        ####
                        ###                             ####
                        ####################################

#If a nieghbour is an obstacle or the border, we act like this isn't the same state


def up_neighbour(
    current_state, maze
):  # possible to code smg if we get out of the window (doesn't test it there)

    if current_state[0] == 0:  # already at the border of the maze
        return current_state
    if maze[current_state[0] - 1][current_state[1]] == "obstacle":
        return current_state

    else:
        return [current_state[0] - 1, current_state[1]]


def right_neighbour(current_state, maze):

    if current_state[1] == len(maze[0]) - 1:

        return current_state

    if maze[current_state[0]][current_state[1] + 1] == "obstacle":

        return current_state

    else:

        return [current_state[0], current_state[1] + 1]


def down_neighbour(current_state, maze):

    if current_state[0] == len(maze) - 1:

        return current_state

    if maze[current_state[0] + 1][current_state[1]] == "obstacle":

        return current_state

    else:

        return [current_state[0] + 1, current_state[1]]


def left_neighbour(current_state, maze):

    if current_state[1] == 0:

        return current_state

    if maze[current_state[0]][current_state[1] - 1] == "obstacle":

        return current_state

    else:

        return [current_state[0], current_state[1] - 1]




def possible_movement(current_state, maze):

    return [
        (up_neighbour(current_state, maze)),
        (right_neighbour(current_state, maze)),
        (down_neighbour(current_state, maze)),
        (left_neighbour(current_state, maze)),
    ]


def possible_movement_different_from_current(current_state, maze):
    movements_different_from_current = []

    up = up_neighbour(current_state, maze)
    right = right_neighbour(current_state, maze)
    down = down_neighbour(current_state, maze)
    left = left_neighbour(current_state, maze)
    neighbours = [up, right, down, left]
    for neighbour in neighbours:
        if(neighbour != current_state):
            movements_different_from_current.append(neighbour)
    return movements_different_from_current


def this_state_is_already_discovered(this_state, maze):
    state = maze[this_state[0]][this_state[1]]
    if state == 2:
        return 1
    return 0


def this_state_is_an_obstacle(this_state, maze):
    state = maze[this_state[0]][this_state[1]]
    if state == "obstacle":
        return 1
    return 0    


def this_state_is_undiscoverd(this_state, maze):

    state = maze[this_state[0]][this_state[1]]
    if state == "undiscovered":
        return 1
    return 0  


def neighbour_undiscovered(current_state, maze):

    possible_next = []
    up = up_neighbour(current_state, maze)
    right = right_neighbour(current_state, maze)
    down = down_neighbour(current_state, maze)
    left = left_neighbour(current_state, maze)

    if(this_state_is_undiscoverd(up, maze)):
        possible_next.append(up) 
    if(this_state_is_undiscoverd(right, maze)):
        possible_next.append(right) 
    if(this_state_is_undiscoverd(down, maze)):
        possible_next.append(down) 
    if(this_state_is_undiscoverd(left, maze)):
        possible_next.append(left) 

    if(len(possible_next) == 0):
        return 0
    return possible_next


def can_end_maze_in_one_move(current_state, end, maze):
    if(up_neighbour(current_state, maze) == end):
        return 1
    if(right_neighbour(current_state, maze) == end):
        return 1
    if(down_neighbour(current_state, maze) == end):
        return 1
    if(left_neighbour(current_state, maze) == end):
        return 1
    return 0




def random_choose_between_possible_undiscovered_states(current_state, end, maze):
    possible_next_states = neighbour_undiscovered(current_state, maze)
    if((possible_next_states) == 0):
        return random_movement_other_than_border_or_obstacle(current_state, maze)
    rand = randint(0, len(possible_next_states) - 1)

    return possible_next_states[rand]





def pure_manhattan_distance_to_end_point(
        current_state, end, maze
    ):

    vertical_distance = abs(current_state[0] - end[0])
    horizontal_distance = abs(current_state[1] - end[1])
    return horizontal_distance + vertical_distance



def distance_to_the_end_of_the_neighbours(current_state, end, maze):
    possible_options = possible_movement(current_state, maze)
    counter = 0
    distances = []
    for option in possible_options:
        if(maze[option[0]][option[1]] == "obstacle" or [option[0], option[1]] == current_state):
            distances.append(1000)
        else:
            distance = pure_manhattan_distance_to_end_point(option, end, maze)
            distances.append(distance)
    return distances
    



def closest_point_between_to_the_end_between_these_point(possible_options, end, maze):
    smallest_distance = 1000
    closest = possible_options[0]
    for option in possible_options:
        current_distance = pure_manhattan_distance_to_end_point(option, end , maze)
        if(current_distance < smallest_distance):
            closest = option
            smallest_distance = current_distance
    return closest



def closest_point_to_the_end(current_state, end, maze):
    possible_options = possible_movement_different_from_current(current_state, maze)
    smallest_distance = 1000000
    counter = 0
    distances = []
    for option in possible_options:
        if((option == "obstacle" or option == "border")):          # for now we don't make difference between wall and border
            distances.append(10000)
        else:
            current_distance = pure_manhattan_distance_to_end_point(possible_options[counter], end, maze)
            if(current_distance < smallest_distance):
                smallest_distance = current_distance
                option_closest_to_the_end = option
        counter += 1

    return option_closest_to_the_end
    


def maze_is_finished(current_state, end, maze):
    if(current_state == end):
        return 1
    return 0





                        ########################
                        ###                 ####
                        ###   ACTION        ####
                        ###                 ####
                        ########################



def actualize_maze(current_state, next_state, maze):

    maze[current_state[0]][current_state[1]] = "discovered"
    maze[next_state[0]][next_state[1]] = "current"

    return maze



def random_movement_other_than_border_or_obstacle(current_state, maze):   

    movements = possible_movement_different_from_current(current_state, maze)
    rand = randint(0, len(movements) - 1)
    return movements[rand]
    


    

                        ########################
                        ###                 ####
                        ###   JOURNEY       ####
                        ###                 ####
                        ########################

#First modelization of the solution, at each state we gonna do a random
# authorized movement untill we get to the end of the maze


def random_journey(
    obstacles, start, end, maze
):
 
    current_state = start

    for counter in range(10000):
        time.sleep(0.5)
        print(maze)
        next_state = random_movement_other_than_border_or_obstacle(current_state, maze)
        maze = actualize_maze(current_state, next_state, maze)
        optimized_update_of_the_visual_window(                                              
            maze, next_state, next_state, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
        )
        if(maze_is_finished(next_state, end, maze)):
            print("found the END i'm not lost anymore wouhou")
            return maze
        current_state = next_state

    print("still stuck, it sucks tho")
    return 0         







#Second modelization, here we are will visit a random state which hasn't been visited
# many problem mgiht occur

def journey_to_an_unknown_world(
        obstacles, start, end, num_rows, num_columns, maze
    ):
    next_state = start
    current_state = start
    for counter in range(10000):

        if can_end_maze_in_one_move(next_state, end, maze):  # stopping condition, we finished the maze
            maze = actualize_maze(next_state, end, maze)
            optimized_update_of_the_visual_window(                                              #haven't tried it yet
                        maze, current_state, end, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
                )
            print("found the END i'm not lost anymore wouhou")
            return maze

        next_state = random_choose_between_possible_undiscovered_states(current_state, end, maze)
        maze = actualize_maze(current_state, next_state, maze)
        time.sleep(0.05)
        optimized_update_of_the_visual_window(                                              #haven't tried it yet
                maze, current_state, next_state, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
            )
        current_state = next_state
    print("still stuck, it sucks tho")


    return 10000




#Third modelization, here we will add the distance and choose the movement
#that has the lowest distance to the end

# Bewhare here the algorithm has a global point of view, he knows where
# he is, where the start and where the end is

def closest_point_to_the_end_journey(
    obstacles, start, end, num_rows, num_columns, maze
):
        
    #If we can go to the closest point to the end, we do
    #else, we go to an unknown state

    current_state = start
    next_state = closest_point_to_the_end(current_state, end, maze)

    

    for counter in range(10000):

        actualize_maze(current_state, next_state, maze)
        optimized_update_of_the_visual_window(                                              #haven't tried it yet
            maze, current_state, next_state, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
        )
        if(maze_is_finished(next_state, end, maze)):
            print("found the END i'm not lost anymore wouhou")
            return maze

        current_state = next_state
        possible_next_state = neighbour_undiscovered(current_state, maze)
        next_state = closest_point_between_to_the_end_between_these_point(
                                                            possible_next_state, end, maze
                                            )
        time.sleep(0.1)

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
            if maze[index_row][index_column] == "obstacle":
                canva.itemconfig(red_rectangle_ids[index_row][index_column], state="normal")
    canva.update()


def init_of_the_visual_window(                                              #haven't tried it yet
    maze, start, end, green_rectangle_ids, orange_rectangle_ids, canva
):
    
    canva.itemconfig(blue_rectangle_ids[start[0]][start[1]], state="normal")
    canva.itemconfig(orange_rectangle_ids[end[0]][end[1]], state="normal")
            
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


def create_orange_rectangles(num_columns, num_rows, cell_width, cell_height, canva):     #past states
    orange_rectangle_ids = []
    for index_row in range(num_rows):
        new_id_row = []
        for index_column in range(num_columns):
            rectangle_id = canva.create_rectangle(
                cell_width * index_column,
                cell_height * index_row,
                cell_width * (index_column + 1),
                cell_height * (index_row + 1),
                fill="orange",
                state="hidden",
            )
            new_id_row.append(rectangle_id)
        orange_rectangle_ids.append(new_id_row)
    return orange_rectangle_ids







def optimized_update_of_the_visual_window(                                              #haven't tried it yet
    maze, current_state, next_state, cell_width, cell_height, blue_rectangle_ids, green_rectangle_ids, canva
):
    # canva.itemconfig(green_rectangle_ids[next_state[0]][next_state[1]], state="hidden")
    # canva.itemconfig(blue_rectangle_ids[next_state[0]][next_state[1]], state="normal")    

    # canva.itemconfig(blue_rectangle_ids[current_state[0]][current_state[1]], state="hidden")
    # canva.itemconfig(green_rectangle_ids[current_state[0]][current_state[1]], state="normal")

    num_columns = len(maze)
    num_rows = len(maze[0])
    for index_row in range(num_rows):
        for index_column in range(num_columns):
            if maze[index_row][index_column] == "discovered":
                canva.itemconfig(green_rectangle_ids[index_row][index_column], state="normal")
                canva.itemconfig(blue_rectangle_ids[index_row][index_column], state="hidden")
                if(maze[index_row][index_column] == "current"):
                    canva.itemconfig(blue_rectangle_ids[index_row][index_column], state="normal")
                    canva.itemconfig(green_rectangle_ids[index_row][index_column], state="hidden")


            
    canva.update()


# On a chaque itération qui permet de détermnier quel sera le prochain moove
# on veut qu'a chaque nouvelle itération on ai la nouvelle cellule qui se mette en bleu et l'ancienne qui se mette en vert

#def update_visual_last_iteration (maze, current_state): #Here we want to actualize the current state to go from blue to red

# Initialize everything 
window_height = 900
window_width = 900
num_rows = 10
num_columns = 10
cell_height = int(window_height / num_columns)
cell_width = int(window_width / num_rows)
start = [0,5]
end = [1, 9]
obstacles = [
            [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7], [8, 7],
            [0,5], [1,5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5],
            [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7], [8, 7]
            ]

maze = init_empty_maze(num_rows, num_columns)
maze = init_start_end(maze, start, end)
maze = init_obstacles(maze, obstacles)


#visual init
canva = initialize_canva(window_height, window_width)
red_rectangle_ids = (create_red_rectangles(num_columns, num_rows, cell_width, cell_height, canva))
blue_rectangle_ids = (create_blue_rectangles(num_columns, num_rows, cell_width, cell_height, canva))
green_rectangle_ids = (create_green_rectangles(num_columns, num_rows, cell_width, cell_height, canva))
orange_rectangle_ids = (create_orange_rectangles(num_columns, num_rows, cell_width, cell_height, canva))

init_obstacles_visual_window(maze, cell_width, cell_height, canva, red_rectangle_ids)
init_of_the_visual_window(                                              #haven't tried it yet
    maze, start, end, green_rectangle_ids, orange_rectangle_ids, canva
)

#run alogrithm


# WE got a problem with the visual that doesn't actualize with blue color for the current



#random_journey(obstacles, start, end, maze)
#journey_to_an_unknown_world(obstacles, start, end, num_rows, num_columns, maze)
closest_point_to_the_end_journey(obstacles, start, end, num_rows, num_columns, maze)




# Visual test
canva.mainloop()

#init_obstacles_visual_window






