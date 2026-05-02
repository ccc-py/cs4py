"""
深度确定性策略梯度（DDPG）实现
适用于连续动作空间
"""

import random
import math
from typing import List, Tuple

class SimpleNN:
    """简单的神经网络（纯Python实现）"""
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Xavier初始化
        self.W1 = [[random.gauss(0, 0.1) for _ in range(input_size)] for _ in range(hidden_size)]
        self.b1 = [0.0] * hidden_size
        self.W2 = [[random.gauss(0, 0.1) for _ in range(hidden_size)] for _ in range(output_size)]
        self.b2 = [0.0] * output_size
    
    def relu(self, x: float) -> float:
        return max(0.0, x)
    
    def tanh(self, x: float) -> float:
        if x > 10:
            return 1.0
        if x < -10:
            return -1.0
        exp_2x = math.exp(2 * x)
        return (exp_2x - 1) / (exp_2x + 1)
    
    def forward(self, x: List[float]) -> Tuple[List[float], List[float]]:
        """前向传播"""
        hidden = [0.0] * self.hidden_size
        for i in range(self.hidden_size):
            z = self.b1[i]
            for j in range(self.input_size):
                z += self.W1[i][j] * x[j]
            hidden[i] = self.relu(z)
        
        output = [0.0] * self.output_size
        for i in range(self.output_size):
            output[i] = self.b2[i]
            for j in range(self.hidden_size):
                output[i] += self.W2[i][j] * hidden[j]
            # Actor输出使用tanh映射到[-1, 1]
            output[i] = self.tanh(output[i])
        
        return output, hidden


class ReplayBuffer:
    """经验回放缓冲区"""
    def __init__(self, capacity: int = 10000):
        self.buffer = []
        self.capacity = capacity
        self.position = 0
    
    def push(self, state: List[float], action: List[float], reward: float, 
             next_state: List[float], done: bool) -> None:
        """存储经验"""
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        self.buffer[self.position] = (state, action, reward, next_state, done)
        self.position = (self.position + 1) % self.capacity
    
    def sample(self, batch_size: int) -> List[Tuple]:
        return random.sample(self.buffer, min(batch_size, len(self.buffer)))
    
    def __len__(self) -> int:
        return len(self.buffer)


class DDPG:
    """深度确定性策略梯度智能体"""
    def __init__(self, state_size: int, action_size: int, hidden_size: int = 16):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = 0.99
        self.tau = 0.001  # 软更新系数
        self.actor_lr = 0.0001
        self.critic_lr = 0.001
        
        # Actor网络（策略）
        self.actor = SimpleNN(state_size, hidden_size, action_size)
        self.actor_target = SimpleNN(state_size, hidden_size, action_size)
        
        # Critic网络（Q函数）
        self.critic = SimpleNN(state_size + action_size, hidden_size, 1)
        self.critic_target = SimpleNN(state_size + action_size, hidden_size, 1)
        
        # 初始化目标网络
        self._soft_update(self.actor, self.actor_target, 1.0)
        self._soft_update(self.critic, self.critic_target, 1.0)
        
        self.replay_buffer = ReplayBuffer()
        self.noise_scale = 0.1
    
    def _soft_update(self, source: SimpleNN, target: SimpleNN, tau: float) -> None:
        """软更新目标网络：θ_target = τ * θ_source + (1 - τ) * θ_target"""
        for i in range(source.hidden_size):
            for j in range(source.input_size):
                target.W1[i][j] = tau * source.W1[i][j] + (1 - tau) * target.W1[i][j]
            target.b1[i] = tau * source.b1[i] + (1 - tau) * target.b1[i]
        for i in range(source.output_size):
            for j in range(source.hidden_size):
                target.W2[i][j] = tau * source.W2[i][j] + (1 - tau) * target.W2[i][j]
            target.b2[i] = tau * source.b2[i] + (1 - tau) * target.b2[i]
    
    def get_action(self, state: List[float], add_noise: bool = True) -> List[float]:
        """获取动作（可能添加探索噪声）"""
        action, _ = self.actor.forward(state)
        if add_noise:
            action = [a + random.gauss(0, self.noise_scale) for a in action]
            action = [max(-1.0, min(1.0, a)) for a in action]
        return action
    
    def train(self, batch_size: int = 32) -> None:
        """训练网络"""
        if len(self.replay_buffer) < batch_size:
            return
        
        batch = self.replay_buffer.sample(batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        # 更新Critic
        for i in range(len(batch)):
            # 目标Q值
            next_action, _ = self.actor_target.forward(next_states[i])
            critic_input = next_states[i] + next_action
            next_q, _ = self.critic_target.forward(critic_input)
            target_q = rewards[i] + self.gamma * next_q[0] * (1 - int(dones[i]))
            
            # 当前Q值
            critic_input = states[i] + actions[i]
            current_q, _ = self.critic.forward(critic_input)
            
            # 更新Critic（简化：直接调整权重）
            error = target_q - current_q[0]
            for h in range(self.critic.hidden_size):
                for s in range(self.critic.input_size):
                    self.critic.W2[0][h] -= self.critic_lr * error * self.critic.b1[h]
        
        # 更新Actor（通过Critic的梯度）
        for i in range(len(batch)):
            action, _ = self.actor.forward(states[i])
            critic_input = states[i] + action
            q_value, _ = self.critic.forward(critic_input)
            
            # Actor梯度上升（简化）
            for h in range(self.actor.hidden_size):
                for s in range(self.actor.input_size):
                    self.actor.W2[0][h] += self.actor_lr * q_value[0] * self.actor.b1[h]
        
        # 软更新目标网络
        self._soft_update(self.actor, self.actor_target, self.tau)
        self._soft_update(self.critic, self.critic_target, self.tau)


class SimplePendulum:
    """简化的Pendulum环境（连续动作空间）"""
    def __init__(self):
        self.state_size = 3  # cos(theta), sin(theta), theta_dot
        self.action_size = 1  # torque [-1, 1]
        self.state = None
        self.max_steps = 200
        self.steps_done = 0
    
    def reset(self) -> List[float]:
        """重置环境"""
        theta = random.uniform(-math.pi, math.pi)
        self.state = [math.cos(theta), math.sin(theta), 0.0]
        self.steps_done = 0
        return self.state.copy()
    
    def step(self, action: List[float]) -> Tuple[List[float], float, bool]:
        """执行动作"""
        torque = max(-1.0, min(1.0, action[0]))
        cos_th, sin_th, th_dot = self.state
        theta = math.atan2(sin_th, cos_th)
        
        # 简化的物理（Pendulum动力学）
        g = 9.8
        m = 1.0
        l = 1.0
        dt = 0.05
        
        th_dot_new = th_dot + (-3 * g / (2 * l) * math.sin(theta + math.pi) + 3 * torque / (m * l**2)) * dt
        theta_new = theta + th_dot_new * dt
        
        self.state = [math.cos(theta_new), math.sin(theta_new), th_dot_new]
        self.steps_done += 1
        
        # 奖励：角度越接近0越好，动作越小越好
        reward = -(theta_new**2 + 0.1 * th_dot_new**2 + 0.001 * torque**2)
        done = self.steps_done >= self.max_steps
        
        return self.state.copy(), reward, done


if __name__ == "__main__":
    print("训练 DDPG 智能体（简化Pendulum）...")
    env = SimplePendulum()
    agent = DDPG(state_size=env.state_size, action_size=env.action_size, hidden_size=16)
    
    n_episodes = 100
    
    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0.0
        done = False
        
        while not done:
            action = agent.get_action(state, add_noise=True)
            next_state, reward, done = env.step(action)
            agent.replay_buffer.push(state, action, reward, next_state, done)
            agent.train(batch_size=32)
            state = next_state
            total_reward += reward
        
        if (episode + 1) % 10 == 0:
            print(f"Episode {episode+1}, Total Reward: {total_reward:.2f}")
    
    print("\n测试训练后的DDPG智能体：")
    state = env.reset()
    total_reward = 0.0
    done = False
    
    while not done:
        action = agent.get_action(state, add_noise=False)
        state, reward, done = env.step(action)
        total_reward += reward
    
    print(f"测试总奖励：{total_reward:.2f}")
