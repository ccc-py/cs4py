# 深度Q网络（DQN）

## 歷史背景

深度Q网络（Deep Q-Network，DQN）由 DeepMind 的 Mnih 等人在 2013 年提出，並在 2015 年發表於《Nature》期刊。DQN 成功將深度學習與強化學習結合，在 Atari 遊戲中達到人類水平的表現，標誌著深度強化學習的誕生。

DQN 的兩個核心創新是**經驗回放（Experience Replay）**和**目標網絡（Target Network）**，解決了傳統 Q-Learning 與深度神經網絡結合時的穩定性問題。

## 核心原理

### Q-Learning 回顧

傳統 Q-Learning 更新公式：
```
Q(s, a) ← Q(s, a) + α [r + γ * max_a' Q(s', a') - Q(s, a)]
```

### DQN 改進

#### 1. 經驗回放（Experience Replay）
- 將智能體的經驗 `(s, a, r, s', done)` 存儲在回放緩衝區
- 訓練時隨機採樣批次數據
- **優點**：打破時間相關性、提高數據利用率

#### 2. 目標網絡（Target Network）
- 使用獨立的目標網絡計算目標 Q 值
- 定期從在線網絡同步權重（硬更新）或緩慢跟蹤（軟更新）
- **優點**：減少目標與當前 Q 值的相關性，提高訓練穩定性

### DQN 損失函數

```
L(θ) = E[(r + γ * max_a' Q_target(s', a'; θ⁻) - Q_online(s, a; θ))²]
```

其中 θ⁻ 是目標網絡參數，定期從 θ 複製。

## 使用範例

```python
from dqn import DQN, SimpleCartPole

# 創建環境和DQN智能體
env = SimpleCartPole()
agent = DQN(state_size=env.state_size, action_size=env.action_size, hidden_size=16)

# 訓練
for episode in range(200):
    state = env.reset()
    done = False
    while not done:
        action = agent.get_action(state)
        next_state, reward, done = env.step(action)
        agent.replay_buffer.push(state, action, reward, next_state, done)
        agent.train()
        state = next_state

# 測試（關閉探索）
agent.epsilon = 0.0
state = env.reset()
done = False
while not done:
    action = agent.get_action(state)
    state, reward, done = env.step(action)
```

## 參考資料

1. Mnih, V., et al. (2013). Playing Atari with Deep Reinforcement Learning. NIPS Workshop.
2. Mnih, V., et al. (2015). Human-level control through deep reinforcement learning. Nature, 518(7540), 529-533.
3. [Spinning Up - DQN](https://spinningup.openai.com/en/latest/algorithms/dqn.html)
4. [DQN 详解](https://lilianweng.github.io/lil-log/2018/05/05/implementing-deep-reinforcement-learning-models.html)
