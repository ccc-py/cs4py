# 深度确定性策略梯度（DDPG）

## 歷史背景

深度确定性策略梯度（Deep Deterministic Policy Gradient，DDPG）由 DeepMind 的 Timothy Lillicrap 等人在 2015 年提出，結合了 DPG（Deterministic Policy Gradient）和 DQN 的思想，專門用於解決**連續動作空間**的強化學習問題。

DDPG 是 Actor-Critic 架構的擴展，使用深度神經網絡來近似確定性策略 μ(s) 和 Q 函數 Q(s, a)，並引入了目標網絡和經驗回放機制來穩定訓練。

## 核心原理

### 確定性策略梯度定理

對於確定性策略 μ(s)，策略梯度為：

```
∇J(μ) = E[∇_a Q(s, a) | a=μ(s) * ∇_θ μ(s|θ)]
```

### DDPG 架構

```
Actor（策略網絡）: s → a = μ(s|θ)
Critic（Q網絡）: (s, a) → Q(s, a|w)
```

### 關鍵組件

1. **目標網絡（Target Networks）**
   - 使用軟更新（soft update）：θ' ← τθ + (1-τ)θ'
   - 提高訓練穩定性

2. **經驗回放（Experience Replay）**
   - 存儲轉換 (s, a, r, s') 到回放緩衝區
   - 隨機採樣批次進行訓練

3. **探索噪聲**
   - 在動作中添加時間相關的噪聲（如Ornstein-Uhlenbeck噪聲）
   - 簡化版本使用高斯噪聲

### 更新規則

**Critic 更新**：
```
L = E[(r + γ * Q'(s', μ'(s'|θ')|w') - Q(s, a|w))²]
```

**Actor 更新**：
```
∇J ≈ E[∇_a Q(s, a|w) * ∇_θ μ(s|θ)]
```

## 使用範例

```python
from ddpg import DDPG, SimplePendulum

# 創建環境和DDPG智能體
env = SimplePendulum()
agent = DDPG(state_size=env.state_size, action_size=env.action_size, hidden_size=16)

# 訓練
for episode in range(100):
    state = env.reset()
    done = False
    while not done:
        action = agent.get_action(state, add_noise=True)
        next_state, reward, done = env.step(action)
        agent.replay_buffer.push(state, action, reward, next_state, done)
        agent.train(batch_size=32)
        state = next_state

# 測試（關閉噪聲）
state = env.reset()
done = False
while not done:
    action = agent.get_action(state, add_noise=False)
    state, reward, done = env.step(action)
```

## 參考資料

1. Lillicrap, T. P., et al. (2015). Continuous control with deep reinforcement learning. ICLR.
2. Silver, D., et al. (2014). Deterministic policy gradient algorithms. ICML.
3. [Spinning Up - DDPG](https://spinningup.openai.com/en/latest/algorithms/ddpg.html)
4. [DDPG 详解](https://towardsdatascience.com/deep-deterministic-policy-gradients-explained-2d94655a9b7b)
