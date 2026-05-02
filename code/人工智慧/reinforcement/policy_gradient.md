# 策略梯度方法（REINFORCE）

## 歷史背景

策略梯度（Policy Gradient）方法是強化學習中的一類重要演算法，最早由 Ronald Williams 在 1992 年的論文《Simple Statistical Gradient-Based Optimization Methods for Connectionist Reinforcement Learning》中正式提出，該論文介紹了 REINFORCE 演算法。

與基於價值的方法（如 Q-Learning）不同，策略梯度方法直接優化參數化策略，通過梯度上升來最大化期望累積回報。

## 核心原理

### 策略梯度定理

策略梯度定理給出了策略性能的梯度：

```
∇J(θ) = E[∇ log π(a|s, θ) * G]
```

其中：
- `π(a|s, θ)` 是參數化策略（通常使用 softmax）
- `G` 是從狀態 s 開始的折扣回報
- `θ` 是策略參數

### REINFORCE 演算法

1. **採樣軌跡**：使用當前策略與環境交互，收集完整的狀態-動作-獎勵序列
2. **計算回報**：對每個時間步計算折扣累積回報 G_t
3. **策略更新**：沿著梯度上升方向更新參數

```
θ ← θ + α * ∇ log π(a_t|s_t, θ) * G_t
```

### Softmax 策略

對於離散動作空間，使用線性特徵與 softmax 結合：

```
π(a|s, θ) = exp(θ_a^T s) / Σ_b exp(θ_b^T s)
```

## 使用範例

```python
from policy_gradient import PolicyNetwork, SimpleEnv, reinforce

# 創建環境和策略網絡
env = SimpleEnv()
policy = PolicyNetwork(n_states=2, n_actions=2, learning_rate=0.01)

# 訓練策略
trained_policy = reinforce(policy, env, n_episodes=1000, gamma=0.99)

# 測試訓練後的策略
state = env.reset()
done = False
while not done:
    probs = trained_policy.forward(state)
    action = max(range(len(probs)), key=lambda i: probs[i])
    print(f"State: {state}, Action: {action}, Probs: {probs}")
    next_state, reward, done = env.step(action)
    state = next_state
```

## 參考資料

1. Williams, R. J. (1992). Simple statistical gradient-based optimization methods for connectionist reinforcement learning. Machine Learning, 8(3-4), 229-256.
2. Sutton, R. S., McAllester, D., Singh, S., & Mansour, Y. (2000). Policy gradient methods for reinforcement learning with function approximation. NeurIPS.
3. [Spinning Up in Deep RL - Policy Gradient](https://spinningup.openai.com/en/latest/algorithms/pg.html)
