import random
import pickle

class ReinforcementLearning:

    
    def __init__(self):
        random.seed(3)
        self.jumpPorb=0.00
        self.alpha=0.5
        self.gamma=0.9
        self.maxAction=9
        self.maxState=10000
        self.episode=50
        self.actions=[]
        self.states=[]
        #self.loadState()
        self.loadAction()
        self.isFinish=False
        #self.currentState=self.states[0]
        self.nextStat=None
        self.currentStateActionPair=[None,None]
        self.qTable={}
        self.board=[0]*9
        #self.makeTable(self.states,self.actions)

        # main loop
        # 0=空 1=黑(先) 2=白(後)

        try:
            file=open("record.txt","rb")
            self.qTable=pickle.load(file)
            #print(self.qTable)
            file.close()
        except Exception as e:
            pass
        finally:
            print("File Not Found")

        for i in range(self.episode):
            self.board=[0]*9
            step=0
            self.isFinish=False
            self.loadState((0,0,0,0,0,0,0,0,0))
            self.currentState=self.states[0]
            self.currentStateActionPair[0]=self.currentState
            print(self.qTable)
            while self.isFinish==False:
                player=self.play()
                self.board[player]=1
                self.currentState=tuple(self.board)
                self.currentStateActionPair[0]=self.currentState
                result=self.judgeState()
                if result==0:
                    currentReward=self.chooseAction()
                    terminalReward = self.getFeedBack()
                    nextActionReward = self.getNextActionReward(self.nextState)
                    predictReward = nextActionReward
                    updateReward = currentReward + self.alpha * (terminalReward + self.gamma * predictReward - currentReward)
                    self.board[self.currentStateActionPair[1]]=2
                    self.updateQTable(self.currentStateActionPair,updateReward)
                    self.updateEnvironment()
                    step+=1
                file=open("record.txt","wb")
                pickle.dump(self.qTable,file)
                #print(self.qTable)
                file.close()
            print("Round "+str(i+1)+" cost step: "+str(step))

    def makeTable(self,t):
        if t in self.qTable:
            return self.qTable[t]
        else:
            self.qTable[t]=0.0
        return 0.0

    def play(self):
        for i in range(3):
            for j in range(3):
                print(str(self.board[i*3+j])+" ",end="")
            print()
        i=input("請下0~8\n")
        while not(i.isdigit()) or not(0<=int(i)<=8) or self.board[int(i)] in (1,2):
            i=input("已經有棋子或超出範圍了，請下0~8\n")
        return int(i)


    def loadAction(self):
        for i in range(self.maxAction):
            name=str(i)
            self.actions.append((name,i))

    def loadState(self,state):
        if state not in self.states:
            self.states.append(state)
            self.makeTable(state)

    def chooseAction(self):
        maxScore=0.0
        actionIndex=None
        actions=[]
        for i in range(9):
            if self.board[i]==0:
                self.currentStateActionPair[1]=i
                if self.makeTable(tuple(self.currentStateActionPair))>=0.0:
                    actions.append(i)
        if(random.random()>self.jumpPorb):
            for action in actions:
                self.currentStateActionPair[1]=action
                if self.makeTable(tuple(self.currentStateActionPair))>maxScore:
                    maxScore=self.makeTable(tuple(self.currentStateActionPair))
                    actionIndex=action
            if maxScore==0.0:
                actionIndex=random.choice(actions)
                self.currentStateActionPair[1]=actionIndex
            else:
                self.currentStateActionPair[1]=actionIndex
        else:
            actionIndex=random.choice(actions)
            self.currentStateActionPair[1]=actionIndex
        return self.makeTable(tuple(self.currentStateActionPair))

    def getNextState(self,current):
        stateIndex=current[0]
        actionIndex=current[1]
        state=list(stateIndex)
        state[actionIndex]=2
        return tuple(state)

    def getFeedBack(self):
        self.nextState=self.getNextState(self.currentStateActionPair)
        result=self.judgeState(self.nextState)
        if result==0:
            return 0
        elif result==2:
            return 2
        elif result==1:
            return -0.5
        elif result==3:
            return 0.5
        return None

    def judgeState(self,board=None):
        if board is None:
            board=self.board
        # 1=黑 2=白 3=平手 0=尚未結束
        for i in range(3):
            if board[i*3]==board[i*3+1]==board[i*3+2]!=0:
                self.isFinish=True
                return board[i*3]
            elif board[i]==board[i+3]==board[i+6]!=0:
                self.isFinish=True
                return board[i]
        if board[0]==board[4]==board[8]!=0:
            self.isFinish=True
            return board[0]
        elif board[2]==board[4]==board[6]!=0:
            self.isFinish=True
            return board[2]
        for i in range(9):
            if board[i]==0:
                return 0
        self.isFinish=True
        return 3

    def getNextActionReward(self,state):
        actions=[]
        for i in range(9):
            if state[i]==0:
                actions.append(i)
        maxScore=0.0
        pair=[None,None]
        pair[0]=state
        state=list(state)
        actionIndex=None
        for action in actions:
            pair[1]=action
            state[action]=2
            pair[0]=tuple(state)
            if self.makeTable(tuple(pair))>=maxScore:
                maxScore=self.makeTable(tuple(pair))
                actionIndex=action
            state[action]=0
        pair[1]=actionIndex
        return self.makeTable(tuple(pair))

    def updateQTable(self,pair,reward):
        self.qTable[tuple(pair)]=reward

    def updateEnvironment(self):
        self.currentState=self.nextState
        self.currentStateActionPair[0]=self.currentState

if __name__=="__main__":
    print("Start")
    reinforcementLearning=ReinforcementLearning()
