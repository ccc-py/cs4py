"""
Actor-Critic 架构实现
结合策略梯度（Actor）和价值函数近似（Critic）
"""

import random
import math
from typing import List, Tuple

class Actor:
    """策略网络（Actor）：参数化策略"""
    def __init__(self, n_states: int, n_actions: int, learning_rate: float = 0.01):
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = learning_rate
        self.weights = [[random.gauss(0, 0.1) for _ in range(n_states)] for _ in range(n_actions)]
    
    def forward(self, state: List[float]) -> List[float]:
        """计算动作概率"""
        logits = [sum(self.weights[a][s] * state[s] for s in range(self.n_states)) for a in range(self.n_actions)]
        max_logit = max(logits)
        exp_logits = [math.exp(l - max_logit) for l in logits]
        sum_exp = sum(exp_logits)
        return [e / sum_exp for e in exp_logits]
    
    def get_action(self, state: List[float]) -> int:
        """根据策略采样动作"""
        probs = self.forward(state)
        return random.choices(range(self.n_actions), weights=probs, k=1)[0]
    
    def update(self, state: List[float], action: int, advantage: float) -> None:
        """使用优势函数更新策略"""
        probs = self.forward(state)
        for a in range(self.n_actions):
            for s in range(self.n_states):
                grad = (1.0 if a == action else 0.0) - probs[a]
                self.weights[a][s] += self.lr * advantage * grad * state[s]


class Critic:
    """价值网络（Critic）：状态价值函数近似"""
    def __init__(self, n_states: int, learning_rate: float = 0.05):
        self.n_states = n_states
        self.lr = learning_rate
        self.weights = [random.gauss(0, 0.1) for _ in range(n_states)]
    
    def forward(self, state: List[float]) -> float:
        """计算状态价值 V(s)"""
        return sum(self.weights[s] * state[s] for s in range(self.n_states))
    
    def update(self, state: List[float], td_error: float) -> None:
        """使用TD误差更新价值函数"""
        for s in range(self.n_states):
            self.weights[s] += self.lr * td_error * state[s]


class SimpleEnv:
    """简单测试环境：2状态2动作"""
    def __init__(self):
        self.n_states = 2
        self.n_actions = 2
        self.state = None
    
    def reset(self) -> List[float]:
        """重置环境"""
        self.state = [1.0, 0.0]
        return self.state.copy()
    
    def step(self, action: int) -> Tuple[List[float], float, bool]:
        """执行动作"""
        if self.state == [1.0, 0.0]:
            reward = 1.0 if action == 0 else 0.0
            self.state = [0.0, 1.0]
            done = False
        else:
            reward = 0.0
            done = True
        return self.state.copy(), reward, done


def actor_critic_train(actor: Actor, critic: Critic, env: SimpleEnv, 
                       n_episodes: int = 500, gamma: float = 0.99) -> Tuple[Actor, Critic]:
    """Actor-Critic训练循环"""
    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0.0
        done = False
        
        while not done:
            # Actor选择动作
            action = actor.get_action(state)
            next_state, reward, done = env.step(action)
            total_reward += reward
            
            # Critic评估状态价值
            V_s = critic.forward(state)
            V_s_next = 0.0 if done else critic.forward(next_state)
            
            # 计算TD误差（用于Critic更新和Advantage）
            td_error = reward + gamma * V_s_next - V_s
            
            # 更新Critic（最小化TD误差）
            critic.update(state, td_error)
            
            # 更新Actor（使用优势函数，这里优势≈TD误差）
            actor.update(state, action, td_error)
            
            state = next_state
        
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode+1}, Total Reward: {total_reward:.2f}")
    
    return actor, critic


if __name__ == "__main__":
    print("训练 Actor-Critic 代理...")
    env = SimpleEnv()
    actor = Actor(n_states=env.n_states, n_actions=env.n_actions, learning_rate=0.01)
    critic = Critic(n_states=env.n_states, learning_rate=0.05)
    
    trained_actor, trained_critic = actor_critic_train(actor, critic, env, n_episodes=500, gamma=0.99)
    
    print("\n测试训练后的策略：")
    state = env.reset()
    done = False
    total_reward = 0.0
    while not done:
        probs = trained_actor.forward(state)
        action = max(range(len(probs)), key=lambda i: probs[i])
        V = trained_critic.forward(state)
        print(f"State: {state}, Action: {action}, Probs: {[round(p, 3) for p in probs]}, V(s): {V:.3f}")
        next_state, reward, done = env.step(action)
        total_reward += reward
        state = next_state
    print(f"测试总奖励：{total_reward:.2f}")
