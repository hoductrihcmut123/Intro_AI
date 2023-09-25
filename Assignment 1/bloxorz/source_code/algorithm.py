import global_variables
from functions import check_win, add_move, solution_path, ga_solution_reprocess
from genetic_algorithm import ga


def BFS(block):
    global_variables.previous = [block]  # save previous states
    queue = [block]
    solution = []
    while queue:
        current = queue.pop(0)
        if check_win(current):
            print("Success!\nFound solution after", current.id, "steps:")
            solution = solution_path(current)
            break

        if current.status != "SPLIT":  # if this is a complete block then it can move 4 directions
            add_move(queue, current.move_up())
            add_move(queue, current.move_right())
            add_move(queue, current.move_down())
            add_move(queue, current.move_left())

        else:
            add_move(queue, current.split_move_up())
            add_move(queue, current.split_move_right())
            add_move(queue, current.split_move_down())
            add_move(queue, current.split_move_left())

            add_move(queue, current.split_move_up_other())
            add_move(queue, current.split_move_right_other())
            add_move(queue, current.split_move_down_other())
            add_move(queue, current.split_move_left_other())
    return solution


def genetic_algorithm(block):
    solution = ga(block)
    ga_solution_path = ga_solution_reprocess(solution, block)
    return ga_solution_path
