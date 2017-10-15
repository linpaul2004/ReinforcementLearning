import random

class ReinforcementLearning:

    
    def __init__(self):
        random.seed(3)
        self.jumpPorb=0.05
        self.alpha=0.5
        self.gamma=0.9
        self.maxAction=2
        self.maxState=15
        self.episode=50
        self.actions=[]
        self.states=[]
        self.loadState()
        self.loadAction()
        self.isFinish=False
        self.currentState=self.states[0]
        self.nextStat=None
        self.currentStateActionPair=[None,None]
        self.qTable={}
        self.makeTable(self.states,self.actions)

        # main loop

        for i in range(self.episode):
            step=0
            self.isFinish=False
            self.currentState=self.states[0]
            self.currentStateActionPair[0]=self.currentState
            while self.isFinish==False:
                currentReward=self.chooseAction()
                terminalReward = self.getFeedBack()
                nextActionReward = self.getNextActionReward(self.nextState)
                predictReward = nextActionReward
                updateReward = currentReward + self.alpha * (terminalReward + self.gamma * predictReward - currentReward);
                self.updateQTable(self.currentStateActionPair,updateReward)
                self.updateEnvironment()
                step+=1
            print("Round "+str(i+1)+" cost step: "+str(step))

    def makeTable(self,states,actions):
        for state in states:
            for action in actions:
                self.qTable[(state,action)]=0.0
        


    def loadAction(self):
        for i in range(self.maxAction):
            if i==0:
                name="left"
            else:
                name="right"
            self.actions.append((name,i))

    def loadState(self):
        for i in range(self.maxState):
            self.states.append((str(i),i))

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
        if actionIndex==0:
            stateIndex-=1
            if stateIndex==-1:
                stateIndex=0
        else:
            stateIndex+=1
        #print(stateIndex)
        return self.states[stateIndex]

    def getFeedBack(self):
        self.nextState=self.getNextState(self.currentStateActionPair)
        #print("ss="+str(self.nextState[1]))
        if self.nextState[1]==self.maxState-1:
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
