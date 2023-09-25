import copy
import time
import math
PLAYER=-1
PREBOARD=None
MAX_DEPTH=4

def initBoard():
    board=[ [  1   ,    1   ,   1   ,    1    ,    1 ],
            [  1   ,    0   ,   0   ,    0    ,    1 ],
            [ -1   ,    0   ,   0   ,    0    ,    1 ],
            [ -1   ,    0   ,   0   ,    0    ,   -1 ],
            [ -1   ,   -1   ,  -1   ,   -1    ,   -1 ]]  
    return board
def nearCenter(listMove):    
    res=[]
    for i in range(len(listMove)):        
        start,end= listMove[i][1]
        x,y = start
        x=x-2
        y=y-2        
        distance=x**2+y**2 
        res.append([distance,(start,end)])
    
    mn= min(res)
    return mn[1]


def printBoard(board):
    
    print('====================================')
    for i in range(5):
        print("%d\t%d\t%d\t%d\t%d" % 
        (board[i][0], board[i][1], board[i][2], board[i][3], board[i][4]))
    print('====================================')
    
def checkPos(pos):
    x,y = pos
    if x<5 and y<5 and x>=0 and y>=0:
        return True
    else:
        return False
def neighbors(pos):
    neighbor=[]
    if checkPos(pos):
        x,y= pos 
        if (x+y)%2==0:
            xIdx=[0,1,1,1,0,-1,-1,-1]
            yIdx=[1,1,0,-1,-1,-1,0,1]
            for i in range(8):
                z=(x+xIdx[i],y+yIdx[i]) #cong x,y cho do lech => neighbor cua x
                if checkPos(z):
                    neighbor.append(z)            
        else:
            xIdx=[0,1,0,-1]
            yIdx=[1,0,-1,0]
            for i in range(4):
                z=(x+xIdx[i],y+yIdx[i]) #cong x,y cho do lech => neighbor cua x
                if checkPos(z):
                    neighbor.append(z)        
        return neighbor
    return []
def canbeEnd(board,pos):
    res=[]
    for x,y in neighbors(pos):
        if board[x][y]==0:
            res.append((x,y))
    return res 
def canPick(board,player):# list vi trí cua tất cả quân mà player có
    res = []
    for i in range(5):
        for j in range(5):
            if board[i][j] == player:
                res.append((i,j))
    return res
def heuristic(board,player):
    myScore=len(canPick(board,player))
    opScore=len(canPick(board,-player))
    return myScore-opScore #do chenh lech
def update(board,start,end,player): #move trên board deep copy
    x1, y1 = start
    x2, y2 = end        
    newboard=copy.deepcopy(board)      
    newboard[x1][y1]=0
    newboard[x2][y2]=player
    tryGanh=ganh(newboard,end) #neu list ganh co vi tri can thay doi. Tuc co an quan
    tryVay=vay(newboard,player)
    change=list(dict.fromkeys(tryGanh+tryVay))
    
    for pos in change:
        x,y=pos
        newboard[x][y]=player
        tryVay=vay(newboard,player)         #TH quan vua ganh vay doi thu
        change=list(dict.fromkeys(tryVay))
        for pos in change:
            x,y=pos
            newboard[x][y]=player
    return newboard##so sánh vây nếu số điểm nhiều hơn
def symatric(pos): # return cac tuple (z1,z2) ma z1,z2 la doi xung nhau qua pos
    res=[]
    if checkPos(pos):
        x,y= pos 
        xIdx=[0,1,1,1,0,-1,-1,-1] #do lech (x,y)->(x+1) or (x-1) tuong ung voi y
        yIdx=[1,1,0,-1,-1,-1,0, 1]    
        for i in range(4):
            z1=(x+xIdx[i],y+yIdx[i])
            z2=(x+xIdx[i+4],y+yIdx[i+4]) #cong x,y cho index cua do lech do lech(cach 4 index) => z1, z2 doi xung
            if z1 in neighbors(pos) and z2 in neighbors(pos):
                res.append((z1,z2))                
        return res
def ganh(board,pos):
    player=board[pos[0]][pos[1]]        #return cac vi tri can thay doi neu ganh xay ra
    res=[]
    if len(symatric(pos)):
        for couple in symatric(pos):
            x1,y1= couple[0][0],couple[0][1]
            x2,y2= couple[1][0],couple[1][1]         
            if board[x1][y1]==board[x2][y2]==-player:
                res.append((x1,y1))
                res.append((x2,y2))            
    return res
def vay(board,player):#nuoc di vay    
    res=[]    
    can_pick=canPick(board,-player)    
    for pos in can_pick:        
        if not isAlive(board,pos,[]):        
           res.append(pos)
    return res    
def trackMove(preBoard,curBoard):    
    start, end = None, None
    for i in range(5):
        for j in range(5):
            if preBoard[i][j]!=0 and curBoard[i][j]==0:
                start = (i,j)
            if preBoard[i][j]==0 and curBoard[i][j]!=0:
                end = (i,j)
    return start,end
def checkTrap(board,player,preBoard):  #kiem tra O co su dung bay hay ko
    curBoard=board
    preScore=heuristic(preBoard,player)
    curScore=heuristic(curBoard,player)
    flag=False
    mustmove=[]
    if preScore == curScore:        
        start,end=trackMove(preBoard,curBoard)            
        if None in [start,end]:
            return False,None
        for startPos in canPick(curBoard,player):
            for endPos in canbeEnd(curBoard,startPos):                
                if endPos[0]==start[0] and endPos[1]==start[1]:               
                    nextBoard=update(curBoard,startPos,endPos,player)   
                    nextScore=heuristic(nextBoard,player)                                 
                    if nextScore>curScore:                        
                        flag=True
                        mustmove.append((startPos,endPos))
                    else:
                        return False,None
        if flag:
            return True,mustmove
        else:         
            return False,None
    return False,None
    
        


def isAlive(board,pos,allies=[]):
    ally=board[pos[0]][pos[1]]    
    neighbor=neighbors(pos)
    res=[]    
    for x,y in neighbor:
        if board[x][y]==0:
            return True
        if board[x][y]== ally:            
            if (x,y) not in allies:
                res.append((x,y))    
    if res==[]:        
        return False
    allies+=res    
    for item in allies:        
        if isAlive(board,item,allies):
            return True
    return False

            
def canMove(board,player,preBoard):
    score: int
    action: tuple
    goodmove=[]
    states=[]
    mx=-math.inf 
    if preBoard == None:
        preBoard=board        
    check,mustmove=checkTrap(board,player,preBoard)
     #kiem tra nuoc O co phai la nuoc di mo hay ko   
    if check == True:        
        for start,end in mustmove:
            new=update(board,start,end,player)
            score=heuristic(new,player) 
            action=(start,end)
            goodmove.append((score,action))        
        return goodmove
    else:
        for startPos in canPick(board,player):
            for endPos in canbeEnd(board,startPos):
                new=update(board,startPos,endPos,player)
                score=heuristic(new,player) 
                action=(startPos,endPos)
                goodmove.append((score,action))
        return goodmove

def staticEval(board):
    return heuristic(board,-1)
def alpha_beta_prunning(maximizingPlayer, alpha, beta, depth,node):
    player=-1 if maximizingPlayer==True else 1
    if depth == 0:
        board=node.board
        score=heuristic(board,player)         
        preAction=node.preAction
        return (score, preAction)
    else:
        
        board = node.board
        preboard= node.preBoard
        goodmove=canMove(board,player,preboard)
        if maximizingPlayer:
            value = (-math.inf, None, None)
            for move in goodmove:                   
                score = move[0]
                action= move[1]
                newboard=update(board,action[0],action[1],player)
                newnode = Node(newboard,-player,action,board)                    
                visit = alpha_beta_prunning(False,alpha,beta,depth-1,newnode)                
                new_value = (visit[0], action)
                value = max_value(value, new_value)
                alpha = max_value(value, alpha)                
                if alpha[0] >= beta[0]:
                    break
            return value
        else:
            value = (math.inf, None, None)
            for move in goodmove:                    
                score = move[0]
                action= move[1]
                newboard=update(board,action[0],action[1],player)
                newnode = Node(newboard,-player,action,board)                    
                visit = alpha_beta_prunning(True,alpha,beta,depth-1,newnode)                
                new_value = (visit[0], action)
                value = min_value(value, new_value)
                beta = min_value(value, beta) 
                if beta[0] <= alpha[0]:
                    break
            return value

def max_value(val_a,val_b):
    return val_a if val_a[0]>=val_b[0] else val_b
def min_value(val_a,val_b):
    return val_a if val_a[0]<val_b[0] else val_b

class Node:
    def __init__(self,board,player,preAction=(None,None),preBoard=None):
        self.board=board
        self.player=player        
        self.preAction=preAction
        self.preBoard=preBoard        

def move(board,player,remain_time):
    global PREBOARD    
    preBoard=PREBOARD
    alpha=(-math.inf,(None,None))
    beta=(math.inf,(None,None))
    maximizingPlayer=True if player == -1 else False    
    if preBoard is None:
        preAction=(None,None)
        root=Node(board,player,preAction,preBoard)         
    else:
        preAction=trackMove(preBoard,board)    
        root=Node(board,player,preAction,preBoard)    
    choose= alpha_beta_prunning(maximizingPlayer,alpha,beta,MAX_DEPTH,root)    
    PREBOARD=update(board,choose[1][0],choose[1][1],player)    
    return choose[1]







