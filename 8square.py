try:
    import queue
except ImportError:
    import Queue as queue
import math
import copy

class Node:
    def __init__(self, state, goal, move = None, parent = None, option = 1):
        self.depth = 0 if parent == None else parent.depth + 1
        self.state = state
        self.move = move
        self.cost = 99999 if state == None else self.cost(goal, option)
        self.parent = parent

    def cost(self,goal,option = 1):
        #g(n) = depth, h(n) = sum of manhattan_distance (+ 2 * linear_conflicts)
        cost = self.depth + manhattan_distance(self.state, goal)
        if option == 2:
            cost += 2 * num_linear_conflicts(self.state, goal)
        return cost

class Puzzle:
    def __init__(self,initial, goal, option = 1):
        self.curr_state = Node(initial,goal,option)
        self.goal = goal #stays as a list for now since we do not know the depth of solution node
        self.node_count = 1
        self.pq = queue.PriorityQueue()
        self.option = option
        self.solution_actions = []
        self.solution_costs = []

    def solve(self):
        while(not self.check_goal()):
            self.expand()
            self.next_state()

        print("depth:" , self.curr_state.depth)
        print("# nodes generated: ", self.node_count)

        ptr = self.curr_state
        while(ptr.parent != None):
            self.solution_actions.insert(0,ptr.move)
            self.solution_costs.insert(0,ptr.cost)
            ptr = ptr.parent
        #put root node cost into list
        self.solution_costs.insert(0,ptr.cost)
        print(self.solution_actions)
        print(self.solution_costs)

        return self.curr_state #solution node

    def check_goal(self):
        #if all items match, found goal state - return true, else return false
        for i in range(len(self.curr_state.state)):
            for j in range(len(self.curr_state.state[0])):
                if (self.curr_state.state[i][j] != self.goal[i][j]):
                    return False
        return True

    def expand(self):
        if self.pq.empty():
            #if pq is empty, put initial in pq and expand
            self.pq.put((self.curr_state.cost,1, self.curr_state))
        #if not empty, get lowest cost and expand
        to_expand = self.pq.get()

        poss_expansions = {"L","R","U","D"}

        for moves in poss_expansions:
            new_node = Node(self.move(moves),goal,moves, to_expand[2], self.option)
            self.pq.put((new_node.cost, self.node_count, new_node))
            self.node_count+=1

        # print("PQueue atm is:")
        # for elem in self.pq.queue:
        #     print(elem[0], elem[2].move, elem[2].state)

    def move(self, move):
        state = copy.deepcopy(self.curr_state.state)
        dict_state = convert_dict(self.curr_state.state)
        zero = dict_state[0]

        #if zero located on edges and were to move out of bounds, return nothing
        if (zero[1] == 0 and move == "L" ) or (zero[1] == 2 and move == "R") or (zero[0] == 0 and move == "U") or (zero[0] == 2 and move == "D"):
            return None
        if move == "L":
            state[zero[0]][zero[1]], state[zero[0]][zero[1]-1] = state[zero[0]][zero[1]-1],state[zero[0]][zero[1]]
        if move == "R":
            state[zero[0]][zero[1]], state[zero[0]][zero[1]+1] = state[zero[0]][zero[1]+1],state[zero[0]][zero[1]]
        if move == "U":
            state[zero[0]][zero[1]], state[zero[0]-1][zero[1]] = state[zero[0]-1][zero[1]],state[zero[0]][zero[1]]
        if move == "D":
            state[zero[0]][zero[1]], state[zero[0]+1][zero[1]] = state[zero[0]+1][zero[1]],state[zero[0]][zero[1]]
        return state

    def next_state(self):
        #update curr_state with next expanded node without removing from pq
        #update path records
        self.curr_state = self.pq.queue[0][2]
        print(self.node_count, self.curr_state.move,self.curr_state.cost, self.curr_state.state)

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

#given a state and a goal, return the Manhattan distances
def manhattan_distance(state, goal):
    sum = 0;
    state = convert_dict(state)
    goal = convert_dict(goal)
    for i in range(1,9,1):
        init_row, init_col = state[i][0], state[i][1]
        goal_row, goal_col = goal[i][0], goal[i][1]
        sum += abs(goal_row - init_row) + abs(goal_col - init_col)
    return sum

#given a state and a goal, return # of linear conflicts
def num_linear_conflicts(state,goal):
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
                    #print(i, "and",j," are conflicting")
                    sum += 1
    return sum

if __name__ == "__main__":
    user_input = []
    user_input.append(input("Please enter the name of input file:\n"))
    user_input.append(int(input("Choose one of the following:\n 1: Sum of Manhattan distances\n 2: Sum of Manhattan distances + 2 x # linear conflicts\n")))

    rep = make_initial_goal(user_input[0])
    initial, goal = rep[0], rep[1]
    print("Initial:" ,initial)
    print("Goal:" , goal)

    p = Puzzle(initial, goal, user_input[1])
    # print(p.move("L"))
    p.solve()
