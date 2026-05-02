# Actor-Critic 架构

## 歷史背景

Actor-Critic 方法結合了策略梯度（Policy Gradient）和價值函數近似（Value Function Approximation）的優點，最早可追溯到 1980 年代的強化學習研究。

該架構包含兩個組件：
- **Actor（行動者）**：負責學習和更新策略 π(a|s)
- **Critic（評論者）**：負責評估狀態價值 V(s) 或動作價值 Q(s,a)

經典的 Actor-Critic 演算法由 Barto, Sutton, 和 Anderson 在 1983 年提出，後續發展出 A2C、A3C 等現代變體。

## 核心原理

### 架構組成

```
Actor: π(a|s, θ) → 動作概率分布
Critic: V(s, w) → 狀態價值估計
```

### 優勢函數（Advantage Function）

優勢函數衡量某個動作相對於平均的優劣：

```
A(s, a) = Q(s, a) - V(s)
```

在狀態價值函數場景中，可以使用 TD 誤差作為優勢的近似：

```
δ = r + γ * V(s') - V(s)
```

### 更新規則

**Actor 更新（策略梯度）**：
```
θ ← θ + α * ∇ log π(a|s, θ) * δ
```

**Critic 更新（TD 學習）**：
```
w ← w + β * δ * ∇ V(s, w)
```

其中 δ 是 TD 誤差，α 和 β 分別是 Actor 和 Critic 的學習率。

## 使用範例

```python
from actor_critic import Actor, Critic, SimpleEnv, actor_critic_train

# 創建環境、Actor和Critic
env = SimpleEnv()
actor = Actor(n_states=2, n_actions=2, learning_rate=0.01)
critic = Critic(n_states=2, learning_rate=0.05)

# 訓練
trained_actor, trained_critic = actor_critic_train(actor, critic, env, n_episodes=500)

# 測試
state = env.reset()
done = False
while not done:
    probs = trained_actor.forward(state)
    action = max(range(len(probs)), key=lambda i: probs[i])
    print(f"State: {state}, Best Action: {action}")
    next_state, reward, done = env.step(action)
    state = next_state
```

## 參考資料

1. Barto, A. G., Sutton, R. S., & Anderson, C. W. (1983). Neuronlike adaptive elements that can solve difficult learning control problems. IEEE Transactions on Systems, Man, and Cybernetics.
2. Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction (2nd ed.). MIT Press.
3. [Spinning Up - Actor-Critic](https://spinningup.openai.com/en/latest/algorithms/a2c.html)
