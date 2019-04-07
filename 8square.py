from multiprocessing import Queue
import math

class Node:
    def __init__(self, state, goal, move = None, parent = None, option = 1):
        self.depth = 0 if parent == None else parent.depth + 1
        self.state = state
        self.move = move
        self.cost = self.cost_function(goal, option)
        self.parent = parent

    def cost(goal,option = 1):
        #g(n) = depth, h(n) = sum of manhattan_distance (+ 2 * linear_conflicts)
        cost = self.depth + sum_manhattan(self.state, goal)
        if option == 2:
            cost += 2 * num_linear_conflicts(self.state, goal)
        return cost

#makes a 2D list of initial and goal states
def make_initial_goal(file):
    init = []
    goal = []

    i = 0
    for line in open(file, "r").readlines():
        if i < 3:
            init.append([ int(i) for i in line.split()])
        elif i > 3:
            goal.append([ int(i) for i in line.split()])
        i += 1

    return [init,goal]

#converts a list to a dictionary
def convert_dict(lst):
    dic = dict()
    for row in range(len(lst)):
        for col in range(len(lst[row])):
            dic[lst[row][col]] = [row, col]
    return dic
    print(dic)

#converts a dictionary to a list/grid
def convert_list(dic):
    #set up grid
    lst = []
    temp = []
    root = int(math.sqrt(len(dic)))
    for i in range(root):
        temp.append("*")
    for j in range(root):
        lst.append(temp.copy())

    #lst = [["*","*","*"],["*","*","*"],["*","*","*"]]
    for num,rowcol in dic.items():
        lst[rowcol[0]][rowcol[1]] = num
    return lst

#given a state and a goal, return the manhttan distances
def manhattan_distance(state, goal):
    sum = 0;
    state = convert_dict(state)
    goal = convert_dict(goal)
    for i in range(len(state)-1):
        init_row, init_col = state[i][0], state[i][1]
        goal_row, goal_col = goal[i][0], goal[i][1]
        sum += abs(goal_row - init_row) + abs(goal_col - init_col)
    return sum

def linear_conflicts(state,goal):
    state = convert_dict(state)
    goal = convert_dict(goal)
    sum = 0

    for i in range(1, 9):
        initial1_row, initial1_col = state[i][0], state[i][1]
        for j in range(1, 9):
            initial2_row, initial2_col = state[j][0], state[j][1]
            #check if on same row or col on state
            check_row = (initial2_row == initial1_row and initial2_col > initial1_col)
            check_col = (initial2_col == initial1_col and initial2_row > initial1_row)
            if check_row or check_col:
                goal_initial2_row, goal_initial2_col = goal[j][0], goal[j][1]
                goal_initial1_row, goal_initial1_col = goal[i][0], goal[i][1]
                #check if conflicts exist on goal state
                check_row_goal = (goal_initial2_row == goal_initial1_row and goal_initial2_col < goal_initial1_col) and (initial2_row == goal_initial2_row)
                check_col_goal = (goal_initial2_col == goal_initial1_col and goal_initial2_row < goal_initial1_row) and (initial2_col == goal_initial2_col)
                if check_row_goal or check_col_goal:
                    print(i, "and",j," are conflicting")
                    sum += 1

    return sum

if __name__ == "__main__":
    user_input = []
    user_input.append(input("Please enter the name of input file:\n"))
    user_input.append(int(input("Choose one of the following:\n 1: Sum of Manhattan distances\n 2: Sum of Manhattan distances + 2 x # linear conflicts\n")))
    print(user_input[0])
    rep = make_initial_goal(user_input[0])
    initial, goal = rep[0], rep[1]
    print("Initial:" ,initial)
    print("Goal:" , goal)
    x = convert_dict(initial)
    print("Converted dict:", x)
    print("Converted list:",convert_list(x))

    print("manhattan_distance: ", manhattan_distance(initial,goal))
    print("linear conflicts: ", linear_conflicts(initial, goal))
