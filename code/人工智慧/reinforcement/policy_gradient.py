"""
策略梯度方法（REINFORCE）实现
遵循cs4py项目规范：纯Python实现，中文注释，类型提示，包含演示
"""

import random
import math
from typing import List, Tuple

class PolicyNetwork:
    """策略网络，使用softmax参数化策略"""
    def __init__(self, n_states: int, n_actions: int, learning_rate: float = 0.01):
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = learning_rate
        # 权重矩阵：形状(n_actions, n_states)，初始化为小随机值
        self.weights = [[random.gauss(0, 0.1) for _ in range(n_states)] for _ in range(n_actions)]
    
    def forward(self, state: List[float]) -> List[float]:
        """计算动作概率（softmax）"""
        logits = [sum(self.weights[a][s] * state[s] for s in range(self.n_states)) for a in range(self.n_actions)]
        max_logit = max(logits)
        exp_logits = [math.exp(l - max_logit) for l in logits]
        sum_exp = sum(exp_logits)
        return [e / sum_exp for e in exp_logits]
    
    def get_action(self, state: List[float]) -> int:
        """根据策略采样动作"""
        probs = self.forward(state)
        return random.choices(range(self.n_actions), weights=probs, k=1)[0]
    
    def update(self, states: List[List[float]], actions: List[int], returns: List[float]) -> None:
        """REINFORCE更新：梯度上升最大化期望回报"""
        for s, a, g in zip(states, actions, returns):
            probs = self.forward(s)
            for a_prime in range(self.n_actions):
                for s_idx in range(self.n_states):
                    grad = (1.0 if a_prime == a else 0.0) - probs[a_prime]
                    self.weights[a_prime][s_idx] += self.lr * g * grad * s[s_idx]


class SimpleEnv:
    """简单测试环境：2状态2动作"""
    def __init__(self):
        self.n_states = 2
        self.n_actions = 2
        self.state = None
    
    def reset(self) -> List[float]:
        """重置环境到初始状态"""
        self.state = [1.0, 0.0]  # one-hot编码状态0
        return self.state.copy()
    
    def step(self, action: int) -> Tuple[List[float], float, bool]:
        """执行动作，返回(next_state, reward, done)"""
        if self.state == [1.0, 0.0]:  # 状态0
            reward = 1.0 if action == 0 else 0.0
            self.state = [0.0, 1.0]  # 转到状态1
            done = False
        else:  # 状态1（终止状态）
            reward = 0.0
            done = True
        return self.state.copy(), reward, done


def reinforce(policy: PolicyNetwork, env: SimpleEnv, n_episodes: int = 1000, gamma: float = 0.99) -> PolicyNetwork:
    """REINFORCE算法训练策略"""
    for episode in range(n_episodes):
        state = env.reset()
        states = []
        actions = []
        rewards = []
        done = False
        
        # 收集完整轨迹
        while not done:
            action = policy.get_action(state)
            next_state, reward, done = env.step(action)
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            state = next_state
        
        # 计算折扣回报
        returns = []
        G = 0.0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)
        
        # 更新策略
        policy.update(states, actions, returns)
        
        if (episode + 1) % 100 == 0:
            total_reward = sum(rewards)
            print(f"Episode {episode+1}, Total Reward: {total_reward:.2f}")
    
    return policy


if __name__ == "__main__":
    print("训练策略梯度（REINFORCE）代理...")
    env = SimpleEnv()
    policy = PolicyNetwork(n_states=env.n_states, n_actions=env.n_actions, learning_rate=0.01)
    trained_policy = reinforce(policy, env, n_episodes=1000, gamma=0.99)
    
    print("\n测试训练后的策略：")
    state = env.reset()
    done = False
    total_reward = 0.0
    while not done:
        probs = trained_policy.forward(state)
        action = random.choices(range(env.n_actions), weights=probs, k=1)[0]
        print(f"State: {state}, Action: {action}, Action Probs: {[round(p, 3) for p in probs]}")
        next_state, reward, done = env.step(action)
        total_reward += reward
        state = next_state
    print(f"测试总奖励：{total_reward:.2f}")
