"""
深度Q网络（DQN）简化实现
包含经验回放、目标网络概念
"""

import random
import math
from typing import List, Tuple, Optional
from collections import deque

class SimpleNN:
    """简单的神经网络（纯Python实现）"""
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # 初始化权重（Xavier初始化简化版）
        self.W1 = [[random.gauss(0, 0.1) for _ in range(input_size)] for _ in range(hidden_size)]
        self.b1 = [0.0] * hidden_size
        self.W2 = [[random.gauss(0, 0.1) for _ in range(hidden_size)] for _ in range(output_size)]
        self.b2 = [0.0] * output_size
    
    def relu(self, x: float) -> float:
        """ReLU激活函数"""
        return max(0.0, x)
    
    def relu_derivative(self, x: float) -> float:
        """ReLU导数"""
        return 1.0 if x > 0 else 0.0
    
    def forward(self, x: List[float]) -> Tuple[List[float], List[float]]:
        """前向传播，返回输出和隐藏层激活值"""
        # 隐藏层
        hidden = [0.0] * self.hidden_size
        for i in range(self.hidden_size):
            z = self.b1[i]
            for j in range(self.input_size):
                z += self.W1[i][j] * x[j]
            hidden[i] = self.relu(z)
        
        # 输出层（线性）
        output = [0.0] * self.output_size
        for i in range(self.output_size):
            output[i] = self.b2[i]
            for j in range(self.hidden_size):
                output[i] += self.W2[i][j] * hidden[j]
        
        return output, hidden
    
    def backward(self, x: List[float], hidden: List[float], output: List[float], 
                 target: List[float], learning_rate: float) -> None:
        """反向传播更新权重"""
        # 输出层梯度
        output_grad = [(output[i] - target[i]) for i in range(self.output_size)]
        
        # 更新输出层权重
        for i in range(self.output_size):
            for j in range(self.hidden_size):
                self.W2[i][j] -= learning_rate * output_grad[i] * hidden[j]
            self.b2[i] -= learning_rate * output_grad[i]
        
        # 隐藏层梯度
        hidden_grad = [0.0] * self.hidden_size
        for j in range(self.hidden_size):
            for i in range(self.output_size):
                hidden_grad[j] += output_grad[i] * self.W2[i][j]
            hidden_grad[j] *= self.relu_derivative(hidden[j])
        
        # 更新隐藏层权重
        for j in range(self.hidden_size):
            for k in range(self.input_size):
                self.W1[j][k] -= learning_rate * hidden_grad[j] * x[k]
            self.b1[j] -= learning_rate * hidden_grad[j]


class ReplayBuffer:
    """经验回放缓冲区"""
    def __init__(self, capacity: int = 10000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state: List[float], action: int, reward: float, 
             next_state: List[float], done: bool) -> None:
        """存储经验"""
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size: int) -> List[Tuple]:
        """随机采样批次经验"""
        return random.sample(self.buffer, min(batch_size, len(self.buffer)))
    
    def __len__(self) -> int:
        return len(self.buffer)


class DQN:
    """深度Q网络智能体"""
    def __init__(self, state_size: int, action_size: int, hidden_size: int = 16):
        self.state_size = state_size
        self.action_size = action_size
        self.q_network = SimpleNN(state_size, hidden_size, action_size)
        self.target_network = SimpleNN(state_size, hidden_size, action_size)
        self.update_target_network()
        self.replay_buffer = ReplayBuffer()
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.batch_size = 32
    
    def update_target_network(self) -> None:
        """更新目标网络权重（硬更新）"""
        # 复制q_network的权重到target_network
        for i in range(self.q_network.hidden_size):
            for j in range(self.q_network.input_size):
                self.target_network.W1[i][j] = self.q_network.W1[i][j]
            self.target_network.b1[i] = self.q_network.b1[i]
        for i in range(self.q_network.output_size):
            for j in range(self.q_network.hidden_size):
                self.target_network.W2[i][j] = self.q_network.W2[i][j]
            self.target_network.b2[i] = self.q_network.b2[i]
    
    def get_action(self, state: List[float]) -> int:
        """epsilon-贪婪策略选择动作"""
        if random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)
        q_values, _ = self.q_network.forward(state)
        return q_values.index(max(q_values))
    
    def train(self) -> None:
        """从回放缓冲区采样并训练"""
        if len(self.replay_buffer) < self.batch_size:
            return
        
        batch = self.replay_buffer.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        for i in range(len(batch)):
            # 当前Q值
            q_values, _ = self.q_network.forward(states[i])
            target_q = q_values.copy()
            
            # 目标Q值（使用目标网络）
            if dones[i]:
                target = rewards[i]
            else:
                next_q, _ = self.target_network.forward(next_states[i])
                target = rewards[i] + self.gamma * max(next_q)
            
            target_q[actions[i]] = target
            
            # 更新Q网络
            self.q_network.backward(states[i], _, q_values, target_q, self.learning_rate)
        
        # 衰减epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)


class SimpleCartPole:
    """简化的CartPole环境（状态连续，动作离散）"""
    def __init__(self):
        self.state_size = 4  # cart_position, cart_velocity, pole_angle, pole_velocity
        self.action_size = 2  # left, right
        self.state = None
        self.steps_done = 0
        self.max_steps = 200
    
    def reset(self) -> List[float]:
        """重置环境"""
        self.state = [
            random.uniform(-0.05, 0.05),  # cart position
            random.uniform(-0.05, 0.05),  # cart velocity
            random.uniform(-0.05, 0.05),  # pole angle
            random.uniform(-0.05, 0.05)   # pole velocity
        ]
        self.steps_done = 0
        return self.state.copy()
    
    def step(self, action: int) -> Tuple[List[float], float, bool]:
        """执行动作（简化物理）"""
        x, x_dot, theta, theta_dot = self.state
        
        # 简化的物理更新（实际CartPole更复杂）
        force = 1.0 if action == 1 else -1.0
        gravity = 9.8
        masscart = 1.0
        masspole = 0.1
        length = 0.5
        
        temp = (force + masspole * length * theta_dot**2 * math.sin(theta)) / (masscart + masspole)
        theta_acc = (gravity * math.sin(theta) - math.cos(theta) * temp) / (length * (4.0/3.0 - masspole * math.cos(theta)**2 / (masscart + masspole)))
        x_acc = temp - masspole * length * theta_acc * math.cos(theta) / (masscart + masspole)
        
        # 更新状态
        self.state[0] += x_dot * 0.02
        self.state[1] += x_acc * 0.02
        self.state[2] += theta_dot * 0.02
        self.state[3] += theta_acc * 0.02
        
        self.steps_done += 1
        
        # 判断终止条件
        done = bool(
            self.state[0] < -2.4 or self.state[0] > 2.4 or
            self.state[2] < -0.2095 or self.state[2] > 0.2095 or
            self.steps_done >= self.max_steps
        )
        
        # 奖励：每步存活得1分
        reward = 1.0 if not done else 0.0
        
        return self.state.copy(), reward, done


if __name__ == "__main__":
    print("训练 DQN 智能体（简化CartPole）...")
    env = SimpleCartPole()
    agent = DQN(state_size=env.state_size, action_size=env.action_size, hidden_size=16)
    
    n_episodes = 200
    target_update_freq = 10
    
    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0.0
        done = False
        
        while not done:
            action = agent.get_action(state)
            next_state, reward, done = env.step(action)
            agent.replay_buffer.push(state, action, reward, next_state, done)
            agent.train()
            state = next_state
            total_reward += reward
        
        # 定期更新目标网络
        if (episode + 1) % target_update_freq == 0:
            agent.update_target_network()
        
        if (episode + 1) % 20 == 0:
            print(f"Episode {episode+1}, Total Reward: {total_reward:.0f}, Epsilon: {agent.epsilon:.3f}")
    
    print("\n测试训练后的DQN智能体：")
    state = env.reset()
    total_reward = 0.0
    done = False
    agent.epsilon = 0.0  # 关闭探索
    
    while not done:
        action = agent.get_action(state)
        state, reward, done = env.step(action)
        total_reward += reward
    
    print(f"测试总奖励：{total_reward:.0f} / {env.max_steps}")
