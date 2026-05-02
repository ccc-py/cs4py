# Expectimax 搜尋演算法 (Expectimax Search Algorithm)

## 歷史背景

Expectimax 演算法是 Minimax 的擴充版本，由 Donald Michie、Ian H. Witten 等人在 1960-70 年代研究遊戲 AI 時提出。當遊戲中涉及機率事件（如骰子、洗牌、隨機生成）時，傳統 Minimax 無法處理，因此誕生了 Expectimax。

## 與 Minimax 的差異

| 特性 | Minimax | Expectimax |
|------|---------|------------|
| 對手模型 | MIN 玩家（假設對手最優） | 無 MIN 節點 |
| 隨機事件 | 不支援 | CHANCE 節點計算期望值 |
| 適用場景 | 確定性雙人零和遊戲 | 含機率事件的遊戲 |
| 節點類型 | MAX、MIN | MAX、CHANCE |

## 核心原理

### 搜尋樹結構

```
        MAX (玩家決策)
       /    \
  行動A      行動B
    |          |
  CHANCE     CHANCE (骰子等隨機事件)
   /|\         /|\
  1 2 3 4    1 2 3 4  (各結果)
```

### 節點評分方式

**MAX 節點**：
```
score = max(score(child) for child in children)
```

**CHANCE 節點**：
```
score = Σ P(outcome) × score(outcome)
```
其中 P(outcome) 是該結果發生的機率。

### 演算法流程

```
function EXPECTIMAX(state, depth):
    if terminal(state) or depth == 0:
        return evaluate(state), None

    if player(state) == MAX:
        best_score = -∞
        best_action = None
        for each action:
            next_state = get_next_state(state, action)
            score, _ = EXPECTIMAX(next_state, depth-1)
            if score > best_score:
                best_score = score
                best_action = action
        return best_score, best_action

    else if player(state) == CHANCE:
        expected = 0
        for each (outcome, probability):
            score, _ = EXPECTIMAX(outcome, depth-1)
            expected += probability × score
        return expected, None
```

## 應用範例

### 骰子遊戲（Pig Game 變體）

玩家每回合可選擇繼續擲骰或停手，擲出 1 則回合分數歸零。

```python
from game.expectimax import DiceGameProblem, expectimax_search

problem = DiceGameProblem(target_score=20)
state = problem.get_initial_state()

score, action = expectimax_search(problem, state, depth=4)
print(f"建議動作：{action}，期望值：{score:.3f}")
```

### 賭博決策問題

在確定收益與風險收益之間做選擇。

```python
from game.expectimax import SimpleGamblingProblem, expectimax_search

problem = SimpleGamblingProblem(initial_money=100, n_rounds=10)
state = problem.get_initial_state()

score, action = expectimax_search(problem, state, depth=10)
print(f"Expectimax 建議：{action}")
```

## 處理不確定性

Expectimax 透過 CHANCE 節點將機率資訊納入決策：

1. **列舉可能結果**：對於隨機事件，列出所有可能結果及機率
2. **計算期望值**：加權平均各結果的分數
3. **風險評估**：不同於單純看最好情況，考慮所有可能的後果

## 在人工智慧中的應用

1. **遊戲 AI**：撲克、21 點、雙陸棋（Backgammon）
2. **決策系統**：在不確定環境下的決策
3. **機器人路徑規劃**：考慮感測器雜訊的路徑選擇
4. **金融決策**：風險與報酬的權衡

## 參考資料

- Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Michie, D. (1966). Game-playing and game-learning automata. *Advances in Programming and Non-Numerical Computation*.
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.
