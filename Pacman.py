#Import thu vien vao
import heapq
import math
import os
import sys
import time

#Tao 1 lop Pqueue
class PQueue:
    
    #Khoi tao
    def __init__(self):
        self.sav= []

    #Them 1 phan tu vao hang doi voi do uu tien
    def enqueue(self, element, priority):
        heapq.heappush(self.sav,(priority, element))

    #Lay phan tu co do uu tien cao nhat
    def dequeue(self):
        return heapq.heappop(self.sav)[1]
    
    #Xoa tat ca cac phan tu trong hang doi
    def DeleteQueue(self):
        self.sav.clear()
        
    #lay kich thuoc
    def GetSize(self):
        return len(self.sav)
    
    #kiem tra su ton tai cua element
    def CheckExist(self, element):
        return element in self.sav
    
    #kiem tra xem hang doi co rong hay khong   
    def CheckEmpty(self):
        return len(self.sav)== 0

    #Lay phan tu co do uu tien cao nhat
    def peek(self):
        if not self.CheckEmpty():
            return self.sav[0][1]
    
    #in ra hang doi
    def print(self):
        print(self.sav)
     
    #string
    def __str__(self):
        return str(self.sav)
     
     
#Tao 1 lop Ma tran   
class Maze:
    
    #Doc file ma tran va lay cac diem an
    def __init__(self, inputFile):
        self.maze= self.ReadFile(inputFile)
        self.FoodLocate= self.GetTarget()
        self.Plocate= self.GetPLocate()
        self.InitialState= (self.Plocate, tuple(self.BubbleSort(self.FoodLocate)))
        
    #Doc tu file lay ma tran vao
    def ReadFile(self, filepath):
        with open(filepath, 'r') as f:
            maze= [[char for char in line.strip()] for line in f]
        return maze

    #tao bubble sort de sap xep
    def BubbleSort(self,list):
        n= len(list)
        for i in range(n):
            for j in range(0, n-i-1):
                if list[j]> list[j+1]:
                    list[j], list[j+1]= list[j+1], list[j]
        return list
    
    #lay cost (chi phi) cua duong di
    def GetCost(self,c, state1, state2):
        return c+1

    #In ra ma tran
    def PrintMT(self):
        for i in self.maze:
            print(''.join(i))
            
    #lay vi tri bat dau cua P (vi tri cua P)
    def GetPLocate(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j]== 'P':
                    return (i, j)
    
    #Lay ma tran
    def GetMaze(self):
        return self.maze
    
    #lay vi tri cac diem thuc an food + vi tri cac goc me cung
    def GetTarget(self):
        target= []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j]== '.':
                    target.append((i, j))
        #add 4 goc cua me cung vao target
        target.extend([(1,1), (1, len(self.maze[0])- 2), (len(self.maze)- 2, 1), (len(self.maze)- 2, len(self.maze[0])- 2)])
        return target
    
    #Kiem tra xem diem hien tai co phai la diem thuc an hay goc hay khong
    def CheckTarget(self, state):
        return state[0] in state[1]

    #Kiem tra xem diem hien tai co phai la diem ket thuc hay khong
    def CheckGoal(self, state):
        return len(state[1])== 0

    #Lay cac diem ke tiep co the di duoc
    def GetSuccessors(self, state):
        Succ= []
        Row, Col= state[0]
        actions = ['North', 'South', 'West', 'East']
        moves = [(-1,0), (1,0), (0,-1), (0,1)]
        for move, action in zip(moves, actions):
            NewRow, NewCol= Row+ move[0],Col+ move[1]
            if (self.maze[NewRow][NewCol]!='%' and 0<= NewRow< len(self.maze) and 0<= NewCol< len(self.maze[0])):
                Succ.append(((NewRow, NewCol), state[1]))
        return Succ
            

class Pacman:
    
    #Khoi tao
    def __init__(self, maze):
        self.maze = maze

    #tao ham animate de hien thuat toan ra man hinh
    def RunMaze(self, actions: list):
        self.maze.PrintMT()
        target= self.maze.GetTarget()
        CurrLocate = ()
        maze= self.maze.maze
        actions.reverse()
        input("Lam on ban hay bam Enter de bat dau chay thuat toan!!")
        while len(actions) != 0:
            #'nt' la windows, neu la win thi dung lenh 'cls' de clear cmd, on nguoc lai linux dung 'clear'
            os.system('cls' if os.name == 'nt' else 'clear')
            action= actions.pop()
            for i in maze:
                print(''.join(i))

            #lay vi tri cua P
            for j in range(0, len(maze)):
                for k in range(0, len(maze[0])):
                    if maze[j][k]== 'P':
                        CurrLocate = (j, k)

            #Neu action la Stop thi dung lai
            maze[CurrLocate[0]][CurrLocate[1]] = ' '
            if action!= 'Stop':
                move= {'North': (-1, 0), 'South': (1, 0), 'East': (0, 1), 'West': (0, -1)}
                SetRow = CurrLocate[0]+ move[action][0]
                SetCol = CurrLocate[1]+ move[action][1]
                maze[SetRow][SetCol]= 'P'
                if (SetRow, SetCol) in target:
                    target.remove((SetRow, SetCol))
            #Dung khoang 0.2s cho moi buoc di  
            time.sleep(0.2)

#Tao 1 lop SearchAlgorithm, luu cac thuat toan
class SearchAlorithm:
    #khoi tao
    def __init__(self, maze):
        self.maze = maze
        
    #Ham chua thuat toan UCS
    def ucs(self):
        parents = {}
        InitialState = self.maze.GetPLocate()
        parents[InitialState]= (-1, -1)
        Cost= {}
        Node1= (InitialState, self.maze.GetTarget())
        path= []
        if self.maze.CheckGoal(Node1):
            return ['Stop']
        bdr= PQueue()
        bdr.enqueue(Node1, 0)
        Cost[Node1[0]]= 0
        explored= []
        while True:
            curr, target= bdr.dequeue()
            if self.maze.CheckGoal((curr, target)):
                path.extend(self.GetThePath(curr, parents))
                return path
            explored.append(curr)
            if self.maze.CheckTarget((curr, target)):
                target= [p for p in target if p != curr]
                if len(target)== 0:
                    path.extend(self.GetThePath(curr, parents))
                    return path
                path.extend(self.GetThePath(curr, parents))
                parents[curr]= (-1, -1)
                explored.clear()
                Cost.clear()
                bdr.DeleteQueue()
                bdr.enqueue((curr, target), 0)
                Cost[curr] = 0
                continue
            successors= self.maze.GetSuccessors((curr, target))
            if successors!= None:
                for child, target in successors:
                    new_Cost= Cost[curr]+ self.maze.GetCost(Cost[curr], curr, child)
                    if child not in explored and bdr.CheckExist(child)== False:
                        Cost[child]= new_Cost
                        parents[child]= curr
                        bdr.enqueue((child, target), self.maze.GetCost(Cost[curr], curr, child))
                    elif bdr.CheckExist(child) and Cost[child]> new_Cost:
                        parents[child]= curr
                        bdr.dequeue(child)
                        bdr.enqueue((child, target), new_Cost)
                        
    #lay duong di
    def GetThePath(self, start, parents):
        curr= start
        path= ['Stop']
        while curr!= (-1, -1):
            CurrRow, CurrCol= curr[0], curr[1]
            ParentRow, ParentCol= parents[curr][0], parents[curr][1]
            RowDif, ColDif = CurrRow - ParentRow, CurrCol - ParentCol
            if RowDif== 1:
                path.append('South')
            elif RowDif== -1:
                path.append('North')
            elif ColDif== 1:
                path.append('East')
            elif ColDif== -1:
                path.append('West')
            curr= parents[curr]
        path.reverse()
        return path

    #Heuristic ham
    def heuristic(self, state):
        CurrLocate, targets= state
        if not targets:
            return 1
        return min(abs(CurrLocate[0]- target[0])+ abs(CurrLocate[1]- target[1]) for target in targets)

    #Ham chua thuat toan A*
    def astar(self, fn_heuristic):
        h_cost = {}
        g_cost = {}
        f_cost = {}
        parents = {}
        InitialState = self.maze.GetPLocate()
        Node2= (InitialState, self.maze.GetTarget())
        parents[InitialState]= (-1, -1)
        bdr= PQueue()
        maze= self.maze.GetMaze()
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                g_cost[(i, j)]= math.inf
            
        g_cost[InitialState]= 0
        h_cost[InitialState]= fn_heuristic(Node2)
        f_cost[InitialState]= g_cost[InitialState] + h_cost[InitialState]
        bdr.enqueue(Node2, 0)
        explored= []
        path= []
        while True:
            curr, target= bdr.dequeue()
            if self.maze.CheckGoal((curr, target)):
                path= self.GetThePath(curr, parents)
                return path
                    
            if self.maze.CheckTarget((curr, target)):
                target= [p for p in target if p != curr]
                if len(target)== 0:
                    path.extend(self.GetThePath(curr, parents))
                    return path
                path.extend(self.GetThePath(curr, parents))
                parents[curr]= (-1, -1)
                explored.clear()
                bdr.DeleteQueue()
                h_cost.clear()
                g_cost.clear()
                f_cost.clear()
                for i in range(len(maze)):
                    for j in range(len(maze[0])):
                        g_cost[(i, j)]= math.inf
                h_cost[curr]= fn_heuristic((curr, target))
                g_cost[curr]= 0
                f_cost[curr]= g_cost[curr] + h_cost[curr]
                bdr.enqueue((curr, target), f_cost[curr])
                continue
            explored.append(curr)
            successors= self.maze.GetSuccessors((curr, target))
            for child, target in successors:
                if child in explored:
                    continue
                tempCost= g_cost[curr] + 1
                if tempCost< g_cost[child]:
                    parents[child]= curr
                    g_cost[child]= tempCost
                    h_cost[child]= fn_heuristic((child, target))
                    f_cost[child]= g_cost[child] + h_cost[child]
                    if not bdr.CheckExist((child, target)):
                        bdr.enqueue((child, target), f_cost[child])


#Lay file input va thuat toan bang lenh cmd/terminal
filepath = sys.argv[1]
algorithm = sys.argv[2]
maze = Maze(filepath)
pacman = Pacman(maze)
search = SearchAlorithm(maze)

#chan thuat toan
if algorithm == "astar":
    actions= search.astar(search.heuristic)
    temp=actions.copy()
elif algorithm== "ucs":
    actions = search.ucs()
    temp=actions.copy()
else :
    #Bao loi in input
    print("Thuat toan khong hop le, vui long nhap 'ucs' hoac 'astar'!!!!")
    sys.exit()
    
#In thuat toan ra man hinh
pacman.RunMaze(actions)

#an xong clear man hinh
os.system('cls' if os.name== 'nt' else 'clear')


if algorithm== "astar":
    print("A* Algorithm")
else:
    print("UCS Algorithm")
    
#In ra duong di va so buoc di (ket qua can tim)
print("In ra duong di: ",temp)
#Khong tinh stop la 1 step ta khong tinh la 1 cost
print('Tong so chi phi: ',len([x for x in temp if x != 'Stop']))
