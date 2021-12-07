from tkinter import Tk, Canvas
import random
import sys


def initialized_cells_state_to_empty(num_rows, num_columns):
    initialized_cells_state = []
    for i in range(num_rows):
        current_row = []
        for j in range(num_columns):
            current_row.append(0)
        initialized_cells_state.append(current_row)
    return initialized_cells_state


def initialize_starting_cells(num_rows, num_columns, number_starting_alive_cells=-1):
    starting_state_cells = initialized_cells_state_to_empty(num_rows, num_columns)
    num_cells = num_columns * num_rows
    index_alive_cells = random.sample(
        [i for i in range(num_cells)], number_starting_alive_cells
    )
    for index_row in range(num_rows):
        for index_column in range(num_columns):
            if (index_row + num_columns * index_column) in index_alive_cells:
                starting_state_cells[index_row][index_column] = 1
    return starting_state_cells


def row_index_upper_neighbours(cell_states, cell_row_index):
    if cell_row_index == 0:
        return len(cell_states[0]) - 1
    return cell_row_index - 1


def row_index_lower_neighbours(cell_states, cell_row_index):
    if cell_row_index == len(cell_states[0]) - 1:
        return 0
    return cell_row_index + 1


def column_index_left_neighbours(cell_states, cell_column_index):
    if cell_column_index == 0:
        return len(cell_states) - 1
    return cell_column_index - 1


def column_index_right_neighbours(cell_states, cell_column_index):
    if cell_column_index == len(cell_states) - 1:
        return 0
    return cell_column_index + 1


def get_neighbours(cell_states, cell_row_index, cell_column_index):
    index_upper_neighbours = row_index_upper_neighbours(cell_states, cell_row_index)
    index_lower_neighbours = row_index_lower_neighbours(cell_states, cell_row_index)
    index_left_neighbours = column_index_left_neighbours(cell_states, cell_column_index)
    index_right_neighbours = column_index_right_neighbours(
        cell_states, cell_column_index
    )

    neighbours = []
    neighbours.append([index_upper_neighbours, index_left_neighbours])
    neighbours.append([index_upper_neighbours, cell_column_index])
    neighbours.append([index_upper_neighbours, index_right_neighbours])

    neighbours.append([cell_row_index, index_left_neighbours])
    neighbours.append([cell_row_index, index_right_neighbours])

    neighbours.append([index_lower_neighbours, index_left_neighbours])
    neighbours.append([index_lower_neighbours, cell_column_index])
    neighbours.append([index_lower_neighbours, index_right_neighbours])
    return neighbours


def number_of_alive_neighbours(cell_states, cell_row_index, cell_column_index):
    number_of_alive_neighbours_to_return = 0
    neighbours = get_neighbours(cell_states, cell_row_index, cell_column_index)
    for index_neighbour in neighbours:
        number_of_alive_neighbours_to_return += cell_states[index_neighbour[0]][
            index_neighbour[1]
        ]
    return number_of_alive_neighbours_to_return


def is_cell_just_borned(cell_states, cell_row_index, cell_column_index):
    number_of_current_alive_neighbours = number_of_alive_neighbours(
        cell_states, cell_row_index, cell_column_index
    )
    if cell_states[cell_row_index][cell_column_index] == 0:
        if number_of_current_alive_neighbours == 3:
            return 1
    return 0


def has_cell_just_survived(cell_states, cell_row_index, cell_column_index):
    number_of_current_alive_neighbours = number_of_alive_neighbours(
        cell_states, cell_row_index, cell_column_index
    )
    if cell_states[cell_row_index][cell_column_index] == 1:
        if (
            number_of_current_alive_neighbours == 2
            or number_of_current_alive_neighbours == 3
        ):
            return cell_states[cell_row_index][cell_column_index]
    return 0


def state_of_cell_after_iteration(cell_states, cell_row_index, cell_column_index):
    is_born = is_cell_just_borned(cell_states, cell_row_index, cell_column_index)
    has_survived = has_cell_just_survived(
        cell_states, cell_row_index, cell_column_index
    )

    return int(is_born or has_survived)


def state_cells_after_iteration(cell_states):
    num_columns = len(cell_states)
    num_rows = len(cell_states[0])
    new_state_cells = initialized_cells_state_to_empty(num_rows, num_columns)
    for index_row in range(num_rows):
        for index_column in range(num_columns):
            new_state_cells[index_row][index_column] = state_of_cell_after_iteration(
                cell_states, index_row, index_column
            )
    return new_state_cells


def initialize_canva(width, height):
    root = Tk()
    canva = Canvas(root)
    canva.config(height=height, width=width, background="black")
    canva.pack()
    return canva


def create_green_rectangles(width, height, cell_width, cell_height, canva):
    num_columns = int(width / cell_width)
    num_rows = int(height / cell_height)
    rectangle_ids = []
    for index_row in range(num_rows):
        new_id_row = []
        for index_column in range(num_columns):
            rectangle_id = canva.create_rectangle(
                cell_width * index_column,
                cell_height * index_row,
                cell_width * (index_column + 1),
                cell_height * (index_row + 1),
                fill="green"
                #state="hidden",
            )
            new_id_row.append(rectangle_id)
        rectangle_ids.append(new_id_row)
    return rectangle_ids


def update_of_the_visual_window(
    cell_states, cell_width, cell_height, rectangle_ids, canva
):
    cell_states = state_cells_after_iteration(cell_states)
    num_columns = len(cell_states)
    num_rows = len(cell_states[0])
    for index_row in range(num_rows):
        for index_column in range(num_columns):
            if cell_states[index_row][index_column] == 1:
                canva.itemconfig(rectangle_ids[index_row][index_column], state="normal")
            else:
                canva.itemconfig(rectangle_ids[index_row][index_column], state="hidden")
    canva.update()
    canva.after(
        200,
        update_of_the_visual_window(
            cell_states, cell_width, cell_height, rectangle_ids, canva
        ),
    )


def test_dimension_are_valid(
    window_height, window_width, cell_height, cell_width, number_starting_alive_cells=-1
):
    num_cells = window_height * window_width / (cell_height * cell_width)
    num_columns = window_width / cell_width
    num_rows = window_height / cell_height
    if round(num_rows) != num_rows:
        print("Please initialize rows by an int\n")
        sys.exit()
    if round(num_columns) != num_columns:
        print("Please initialize columns as an int \n")
        sys.exit()
    if round(num_cells) != num_cells:
        print(
            "Please initialize the cells height as a divider of the windows height \n"
        )
        sys.exit()
    if number_starting_alive_cells > num_cells:
        print("You can't have more alive cells than the actual number of cells")
        sys.exit()
    return 1


def run(width, height, cell_width, cell_height, num_cells_starting_alive):
    num_columns = int(width / cell_width)
    num_rows = int(height / cell_height)
    cell_states = initialize_starting_cells(
        num_rows, num_columns, num_cells_starting_alive
    )
    canva = initialize_canva(width, height)
    rectangle_ids = create_green_rectangles(
        width, height, cell_width, cell_height, canva
    )
    #update_of_the_visual_window(
    #    cell_states, cell_width, cell_height, rectangle_ids, canva
    #)
    canva.mainloop()


def easy_run():
    width = 900
    height = 900
    cell_width = 10
    cell_height = 10
    num_cells_starting_alive = 1000
    run(width, height, cell_width, cell_height, num_cells_starting_alive)


def expert_run():
    width = int(input("Choose window's width (default is 900): \n") or 900)
    height = width
    cell_width = int(input("Choose cell's width (default 10): \n") or 10)
    cell_height = cell_width
    good_number_of_starting_cells = int(
        (width * width * 30 / (cell_width * cell_width * 100))
    )
    num_cells_starting_alive = int(
        input(
            f"Choose the number of the cells starting alive (a good number is {good_number_of_starting_cells}) \n"
        )
        or good_number_of_starting_cells
    )
    test_dimension_are_valid(
        width, height, cell_height, cell_width, num_cells_starting_alive
    )
    run(width, height, cell_width, cell_height, num_cells_starting_alive)


def main():
    print("Welcome in the Conway's game of life \n")
    if int(input("Press 0 for the begginer mode and 1 for the expert mode \n")):
        expert_run()
    else:
        easy_run()


if __name__ == "__main__":
    # increase the recursion limit so that the game can run longer
    sys.setrecursionlimit(10000)
    main()
