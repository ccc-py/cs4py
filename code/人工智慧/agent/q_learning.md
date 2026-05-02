# Q-learning 演算法

## 歷史背景

Q-learning 由 Christopher Watkins 於 1989 年在倫敦大學的博士論文《Learning from Delayed Rewards》中首次提出。這是強化學習史上最重要的突破之一，首次將**時序差分學習（Temporal Difference Learning）**與**動作價值函數（Action-Value Function）**結合。

在此之前，強化學習主要分為兩派：
- **動態規劃（Dynamic Programming）**：需要完整的環境模型
- **蒙特卡洛方法（Monte Carlo）**：需要等到回合結束才能更新

Q-learning 的創新在於：
1. **Model-free**：不需要知道環境的轉移機率
2. **Single-step update**：每步都可以學習，不需要等到回合結束
3. **Off-policy**：學習最優策略的同時，可以使用探索性策略收集經驗

這篇論文奠定了現代強化學習的基礎。2013 年 DeepMind 提出的 **DQN（Deep Q-Network）** 正是將 Q-learning 與深度神經網路結合，開啟了深度強化學習的時代。

## 核心原理

### Q-table（Q 表）

Q-learning 的核心數據結構是 **Q-table**，這是一個查找表（lookup table），儲存每個狀態-動作對的預期累積獎勵：

```
Q(s, a) = 在狀態 s 下執行動作 a，之後遵循最優策略所能獲得的預期累積獎勵
```

對於迷宮問題，狀態是智能體的位置 `(x, y)`，動作是四個方向，因此 Q-table 的大小為 `width × height × 4`。

### Q-learning 更新公式

Q-learning 的更新公式為：

```
Q(s, a) ← Q(s, a) + α [r + γ · max_a' Q(s', a') - Q(s, a)]
```

其中：
- `α` (alpha)：學習率，控制新資訊覆蓋舊資訊的速度（0 ≤ α ≤ 1）
- `r`：當前步驟獲得的獎勵
- `γ` (gamma)：折扣因子，衡量未來獎勵的重要性（0 ≤ γ ≤ 1）
- `s'`：執行動作後的新狀態
- `max_a' Q(s', a')`：新狀態下所有動作的最大 Q 值

這個公式的直覺是：
- **TD error** = `r + γ·max_a' Q(s', a') - Q(s, a)`，即「新估計」與「舊估計」的差異
- 用 `α` 比例將 Q 值朝著 TD error 方向調整

### ε-greedy 策略

為了平衡「探索（Exploration）」與「利用（Exploitation）」，Q-learning 使用 **ε-greedy** 策略：

```python
if random.random() < epsilon:
    action = random.choice(actions)  # 探索：隨機選動作
else:
    action = argmax_a Q(state, a)    # 利用：選 Q 值最大的動作
```

- **探索**：嘗試未曾或很少嘗試的動作，發現更好的路徑
- **利用**：根據當前知識選擇最佳動作，獲取最大獎勵

### 探索衰減（Exploration Decay）

隨著訓練進行，智能體應該逐漸從「探索為主」轉向「利用為主」：

```python
epsilon = max(epsilon_min, epsilon * epsilon_decay)
```

典型的衰減率是 0.995~0.999，最終 ε 會趨近於一個小值（如 0.01）。

### Off-policy vs On-policy

Q-learning 是 **off-policy** 演算法：
- **行為策略（Behavior Policy）**：ε-greedy，用於與環境互動收集經驗
- **目標策略（Target Policy）**：greedy（選 max Q），是學習的目標

更新公式中的 `max_a' Q(s', a')` 使用的是貪心策略，即使實際採取的動作不是那個動作。

這與 **SARSA**（on-policy）形成對比，SARSA 使用實際採取的下一個動作的 Q 值更新。

## 程式碼說明

### GridWorld 環境

```python
class GridWorld:
    """簡單網格世界環境"""
```

提供：
- 設定牆壁、目標、陷阱
- `move_agent(direction)`：移動智能體並返回（是否成功，獎勵）
- `is_terminal()`：檢查是否終止

獎勵設計：
- 到達目標：+10
- 掉入陷阱：-5
- 每步移動：-0.1（鼓勵找最短路徑）
- 撞牆：-0.5

### QLearningAgent 類別

```python
class QLearningAgent:
    """Q-learning 智能體"""
```

主要方法：
- `choose_action(state)`：ε-greedy 策略選擇動作
- `learn(state, action, reward, next_state, done)`：Q-learning 更新
- `decay_epsilon()`：衰減探索率
- `get_policy()`：取得當前學到的貪心策略

## 使用範例

### 基本訓練

```python
from q_learning import GridWorld, QLearningAgent, Direction

# 建立環境
env = GridWorld(width=8, height=6)
env.set_agent(0, 0)
env.set_goal(7, 5)
env.set_cell(3, 3, CellType.PIT)  # 陷阱

# 建立智能體
actions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
agent = QLearningAgent(
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

    for step in range(100):
        action = agent.choose_action(state)
        success, reward = env.move_agent(action)
        next_state = env.agent_pos
        done = env.is_terminal()

        agent.learn(state, action, reward, next_state, done)
        state = next_state

        if done:
            break

    agent.decay_epsilon()
```

### 測試訓練好的智能體

```python
# 關閉探索
agent.epsilon = 0

env.reset((0, 0))
state = env.agent_pos

for step in range(20):
    action = agent.choose_action(state)
    print(f"步驟 {step + 1}: {action.name}")
    success, _ = env.move_agent(action)
    state = env.agent_pos

    if env.is_goal_reached():
        print(f"到達目標！共 {step + 1} 步")
        break
```

## 超參數調整

| 超參數 | 典型值 | 作用 | 調整建議 |
|--------|--------|------|----------|
| 學習率 α | 0.1 | 控制更新幅度 | 太大會震盪，太小收斂慢 |
| 折扣因子 γ | 0.9 | 未來獎勵的重要性 | 接近 1 重視長期回報，接近 0 短視 |
| 初始 ε | 1.0 | 初始探索率 | 通常從 1.0 開始（完全隨機） |
| ε 衰減率 | 0.995 | 探索衰減速度 | 太小收斂慢，太大早停 |
| ε 最小值 | 0.01 | 最小探索率 | 保持微少量探索，避免陷入局部最優 |

## 參考資料

1. **原始論文**：
   - Watkins, C. J. C. H. (1989). *Learning from Delayed Rewards*. PhD thesis, University of Cambridge.

2. **教科書**：
   - Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press. [線上免費版本](http://incompleteideas.net/book/the-book-2nd.html)

3. **經典論文**：
   - Watkins, C. J., & Dayan, P. (1992). *Q-learning*. Machine Learning, 8(3-4), 279-292.

4. **現代應用**：
   - Mnih, V., et al. (2013). *Playing Atari with Deep Reinforcement Learning*. NIPS Deep Learning Workshop. [DQN 論文](https://arxiv.org/abs/1312.5602)

5. **線上資源**：
   - [Spinning Up in Deep RL (OpenAI)](https://spinningup.openai.com/en/latest/algorithms/qlearning.html)
   - [Q-learning 動畫演示](https://www.deeplearningbook.org/)
