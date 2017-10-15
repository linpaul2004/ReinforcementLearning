import random
from datetime import datetime

class ReinforcementLearning:

    
    def __init__(self):
        random.seed(datetime.now())
        self.jumpPorb=0.03
        self.alpha=0.5
        self.gamma=0.9
        self.maxAction=4
        self.maxState=100
        self.episode=50
        self.actions=[]
        self.states=[]
        self.board=[]
        self.loadState()
        self.loadAction()
        self.isFinish=False
        self.currentState=self.states[0]
        self.nextStat=None
        self.currentStateActionPair=[None,None]
        self.qTable={}
        self.makeTable(self.states,self.actions)
        self.minstep=100
        self.minboard=[0]*100

        # main loop

        for i in range(self.episode):
            step=0
            self.isFinish=False
            self.currentState=self.states[11]
            self.currentStateActionPair[0]=self.currentState
            #print(str(self.currentStateActionPair[0][1])+"k")
            for k in range(self.maxState):
                self.board[k]=self.states[k][2]
            while self.isFinish==False:
                currentReward=self.chooseAction()
                terminalReward = self.getFeedBack()
                nextActionReward = self.getNextActionReward(self.nextState)
                predictReward = nextActionReward
                updateReward = currentReward + self.alpha * (terminalReward + self.gamma * predictReward - currentReward)
                self.board[self.currentState[1]]=step+1
                self.updateQTable(self.currentStateActionPair,updateReward)
                self.updateEnvironment()
                step+=1
                if step>5000:
                    break
            if step>5000:
                print("Impossible")
                print("Round "+str(i+1)+" cost step: "+str(step))
                for k in range(self.maxState):
                    print("{:>3}".format(self.states[k][2]),end="")
                    if k%10==9:
                        print("\n")
                break
            if step<self.minstep:
                for k in range(self.maxState):
                    self.minboard[k]=self.board[k]
                self.minstep=step
                self.minboard[88]=self.minstep+1
            print("Round "+str(i+1)+" cost step: "+str(step))
        if self.minstep==100:
            return
        for k in range(self.maxState):
            print("{:>3}".format(self.minboard[k]),end="")
            if k%10==9:
                print("\n")

    def makeTable(self,states,actions):
        for state in states:
            for action in actions:
                self.qTable[(state,action)]=0.0
        


    def loadAction(self):
        for i in range(self.maxAction):
            if i==0:
                name="right"
            elif i==1:
                name="down"
            elif i==2:
                name="left"
            else:
                name="up"
            self.actions.append((name,i))

    def loadState(self):
        for i in range(self.maxState):
            if i%10 in (0,9) or i<=9 or i>=90:
                self.states.append((str(i),i,-1))
                r=-1
            elif i in (11,88):
                self.states.append((str(i),i,0))
                r=0
            else:
                r=random.choice([-1,0,0])
                self.states.append((str(i),i,r))
            self.board.append(r)

    def chooseAction(self):
        maxScore=0.0
        actionIndex=None
        if(random.random()>self.jumpPorb):
            for action in self.actions:
                self.currentStateActionPair[1]=action
                if self.qTable[tuple(self.currentStateActionPair)]>maxScore:
                    maxScore=self.qTable[tuple(self.currentStateActionPair)]
                    actionIndex=action
            if maxScore==0.0:
                actionIndex=self.actions[random.randrange(self.maxAction)]
                self.currentStateActionPair[1]=actionIndex
            else:
                self.currentStateActionPair[1]=actionIndex
        else:
            actionIndex=self.actions[random.randrange(self.maxAction)]
            self.currentStateActionPair[1]=actionIndex
        return self.qTable[tuple(self.currentStateActionPair)]

    def getNextState(self,current):
        stateIndex=current[0][1]
        actionIndex=current[1][1]
        #print(str(stateIndex)+"ss")
        if actionIndex==0:
            stateIndex+=1
            #print(self.states[stateIndex][2])
            if self.states[stateIndex][2]==-1:
                stateIndex-=1
        elif actionIndex==1:
            stateIndex+=10
            #print(self.states[stateIndex][2])
            if self.states[stateIndex][2]==-1:
                stateIndex-=10
        elif actionIndex==2:
            stateIndex-=1
            #print(self.states[stateIndex][2])
            if self.states[stateIndex][2]==-1:
                stateIndex+=1
        elif actionIndex==3:
            stateIndex-=10
            #print(self.states[stateIndex][2])
            if self.states[stateIndex][2]==-1:
                stateIndex+=10
        #print(stateIndex)
        return self.states[stateIndex]

    def getFeedBack(self):
        self.nextState=self.getNextState(self.currentStateActionPair)
        #print("ss="+str(self.nextState[1]))
        if self.nextState[1]==88:
            #print("ss="+str(self.nextState[1]))
            self.isFinish=True
            return 1
        else:
            return 0

    def getNextActionReward(self,state):
        maxScore=0.0
        pair=[None,None]
        pair[0]=state
        actionIndex=None
        for action in self.actions:
            pair[1]=action
            if self.qTable[tuple(pair)]>=maxScore:
                maxScore=self.qTable[tuple(pair)]
                actionIndex=action
        pair[1]=actionIndex
        return self.qTable[tuple(pair)]

    def updateQTable(self,pair,reward):
        self.qTable[tuple(pair)]=reward

    def updateEnvironment(self):
        self.currentState=self.nextState
        self.currentStateActionPair[0]=self.currentState

if __name__=="__main__":
    print("Start")
    reinforcementLearning=ReinforcementLearning()
