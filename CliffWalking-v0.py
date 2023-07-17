import gym
import numpy as np
import random
'''初始化环境'''  


class Qlearning():
    def __init__(self,
        env,
        numStepsPerEpisode = 200,
        gamma = 0.5,
        epsilon = 0.1,
        alpha = 0.1,
        epochs = 1000
        ):
        self.m_env = env
        self.m_numStepsPerEpisode = numStepsPerEpisode
        self.m_gamma = gamma
        self.m_epsilon = epsilon
        self.m_alpha = alpha
        self.m_epochs = epochs

        self.m_stateNums = self.m_env.observation_space.n
        self.m_actionNums = self.m_env.action_space.n

        self.m_Qtable = np.zeros((self.m_stateNums,self.m_actionNums))
        self.m_curState = 0
        self.m_avgReturns = []

    def SelectAction(self) -> int:
        tmp = random.random()
        if tmp < self.m_epsilon :
            return random.randint(0,self.m_actionNums-1)
        else :
            return self.SelectActionByQtable(self.m_curState)
        
    def SelectActionByQtable(self,curstate) -> int:
        #if q[s][a] in s are all 0 ,randaom choose
        if np.count_nonzero(self.m_Qtable[curstate]) == 0:
            return random.randint(0,self.m_actionNums-1)
        else :
            return np.argmax(self.m_Qtable[curstate])
        
    def DoTrainning(self):
        for epoch in range(self.m_epochs):
            # reset env
            self.m_env.env.render()  # 显示图形界面
            self.m_curState = self.m_env.reset()
            for perStep in range(self.m_numStepsPerEpisode):
                at = self.SelectAction()
                nextState, reward, done, info = self.m_env.step(at)
                if done :
                    break
                self.UpdateQTable(self.m_curState,reward,nextState,at)
                self.m_curState = nextState
            avg_return = self.Evaluate()
            self.m_avgReturns.append(avg_return)
            print(f"epoch{epoch},avg_return{avg_return} ")
        self.m_env.render()

    def UpdateQTable(self, curState, reward, nextState, action):
        QTarget = reward + self.m_gamma * self.m_Qtable[nextState][self.SelectActionByQtable(nextState)]
        self.m_Qtable[curState][action] += self.m_alpha * ( QTarget - self.m_Qtable[curState][action])

    def Evaluate(self):
        self.m_curState = self.m_env.reset()
        avg_returns = 0.0
        for i in range(self.m_numStepsPerEpisode):
            action = self.SelectActionByQtable(self.m_curState)
            nextState, reward, done, info = self.m_env.step(action)
            avg_returns += reward
            if done : 
                break
            self.m_curState = nextState
        return avg_returns
    
if __name__ == '__main__':
    env = gym.make('CliffWalking-v0')
    env.reset()
    QlearningSolver = Qlearning(env)
    QlearningSolver.DoTrainning()
    env.close()



            





        



