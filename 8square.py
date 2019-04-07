from multiprocessing import Queue
import math

class Node:
    def __init__(self, state, goal, move = None, parent = None, option = 1):
        self.depth = 0 if parent == None else parent.depth + 1
        self.state = state
        self.move = move
        self.cost = self.cost_function(goal, option)
        self.parent = parent

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
