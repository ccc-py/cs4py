# SARSA 演算法

## 歷史背景

SARSA 於 1990 年代早期由 **Richard Sutton** 等人提出，與 Q-learning 幾乎同時期發展。名稱 **SARSA** 是 **S**tate-**A**ction-**R**eward-**S**tate-**A**ction 的縮寫，描述了演算法的核心流程。

### 與 Q-learning 的關係

兩者都是 **TD(0) 控制方法**，核心差異在於：

| 特性 | Q-learning | SARSA |
|------|-----------|-------|
| 策略類型 | Off-policy | On-policy |
| 更新目標 | max_a' Q(s',a') | Q(s',a') |
| 學習目標 | 最優策略（greedy） | 當前行為策略（ε-greedy） |
| 在有陷阱環境中 | 學到最短路徑（可能靠近陷阱） | 學到安全路徑（遠離陷阱） |

### 為什麼叫 SARSA？

在每個時間步，SARSA 需要記錄：
1. **S**tate（當前狀態）
2. **A**ction（當前動作）
3. **R**eward（獎勵）
4. **S**tate（下一個狀態）
5. **A**ction（下一個動作）

這五個值構成了更新公式的基本元素。

## 核心原理

### SARSA 更新公式

```
Q(s, a) ← Q(s, a) + α [r + γ · Q(s', a') - Q(s, a)]
```

與 Q-learning 的對比：

```
Q-learning:   Q(s,a) ← Q(s,a) + α [r + γ · max_a' Q(s',a') - Q(s,a)]
                                                       ↑
                                               使用最大 Q 值（貪心）

SARSA:         Q(s,a) ← Q(s,a) + α [r + γ · Q(s',a') - Q(s,a)]
                                                 ↑
                                         使用實際採取的動作的 Q 值
```

### On-Policy 的含義

**On-policy** 意味著：
- **行為策略（Behavior Policy）**：用於與環境互動的策略（ε-greedy）
- **目標策略（Target Policy）**：學習目標的策略（也是 ε-greedy）

兩者相同！SARSA 學習的就是它正在執行的策略。

相比之下，Q-learning 是 **off-policy**：
- 行為策略：ε-greedy（探索）
- 目標策略：greedy（最優）

### 為什麼 SARSA 更「保守」？

考慮一個有陷阱的迷宮：

```
S . . . . . . G
. . X . X . . .
. . . . . . . .
```

- **Q-learning**（off-policy）：學習最優策略時使用 `max Q`，不考慮實際執行時可能掉入陷阱。它學到的是「如果完美執行時的最優路徑」。
- **SARSA**（on-policy）：考慮到 ε-greedy 策略下，智能體有機率探索到陷阱。因此學到的策略會主動遠離陷阱，即使路徑稍長。

這就是所謂的 **"SARSA learns the safe path"** 現象。

## 程式碼說明

### SarsaAgent 類別

```python
class SarsaAgent:
    """SARSA 智能體（On-Policy TD Control）"""
```

主要方法：
- `choose_action(state)`：ε-greedy 策略（同時是行為與目標策略）
- `learn(state, action, reward, next_state, next_action, done)`：SARSA 更新

### 訓練流程（關鍵差異）

```python
# Q-learning 訓練（只需當前動作）
action = agent.choose_action(state)
reward, next_state = env.step(action)
agent.learn(state, action, reward, next_state, done)
# 下一輪再選擇新動作

# SARSA 訓練（需要當前與下一個動作）
action = agent.choose_action(state)  # 需要初始動作
for step in range(max_steps):
    reward, next_state = env.step(action)
    next_action = agent.choose_action(next_state)  # 預先選擇下一動作
    agent.learn(state, action, reward, next_state, next_action, done)
    state = next_state
    action = next_action  # 更新動作
```

這就是 S-A-R-S-A 的體現：每步都需要知道下一個動作才能更新。

## 使用範例

### 基本訓練

```python
from sarsa import GridWorld, SarsaAgent, Direction

# 建立環境
env = GridWorld(width=8, height=6)
env.set_agent(0, 0)
env.set_goal(7, 5)
env.set_cell(3, 3, CellType.PIT)

# 建立 SARSA 智能體
actions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
agent = SarsaAgent(
    actions=actions,
    learning_rate=0.1,
    discount_factor=0.9,
    epsilon=1.0,
    epsilon_decay=0.995
)

# 訓練
for episode in range(500):
    env.reset((0, 0))
    state = env.agent_pos
    action = agent.choose_action(state)  # 初始動作

    for step in range(100):
        success, reward = env.move_agent(action)
        next_state = env.agent_pos
        done = env.is_terminal()

        if not done:
            next_action = agent.choose_action(next_state)
        else:
            next_action = None

        agent.learn(state, action, reward, next_state, next_action, done)

        if done:
            break

        state = next_state
        action = next_action

    agent.decay_epsilon()
```

## 實驗比較

本程式包含一個 `compare_sarsa_vs_qlearning()` 函數，可以在相同環境下比較兩者：

```python
compare_sarsa_vs_qlearning()
```

典型結果：
- **Q-learning**：學到最短路徑，但路徑可能靠近陷阱
- **SARSA**：學到稍長但更安全的路徑

## 超參數調整

SARSA 的超參數與 Q-learning 相同：

| 超參數 | 典型值 | 說明 |
|--------|--------|------|
| α | 0.1 | 學習率 |
| γ | 0.9 | 折扣因子 |
| ε | 1.0 → 0.01 | 探索率（衰減） |

## 參考資料

1. **教科書**：
   - Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). Chapter 6.
   - [線上免費版本](http://incompleteideas.net/book/the-book-2nd.html)

2. **原始文獻**：
   - Rummery, G. A., & Niranjan, M. (1994). *On-line Q-learning using connectionist systems*. CUED/F-INFENG/TR 166.
   - Singh, S. P., Jaakkola, T., & Littman, M. L. (1994). *Convergence results for single-step on-policy reinforcement learning algorithms*. Machine Learning, 15(3), 293-320.

3. **比較研究**：
   - van Seijen, H., et al. (2009). *Planning by active reinforcement learning*. AAMAS.
   - "Why does SARSA learn a conservative policy?" - 討論 on-policy vs off-policy 在有隨機性時的差異。

4. **線上資源**：
   - [Spinning Up: SARSA](https://spinningup.openai.com/en/latest/algorithms/sarsa.html)
   - [David Silver's RL Course - Lecture 5](https://www.youtube.com/watch?v=UoPei5o4fps)
