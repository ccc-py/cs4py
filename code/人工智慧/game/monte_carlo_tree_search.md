# 蒙特卡洛樹搜尋 (Monte Carlo Tree Search)

## 歷史背景

2006 年被稱為「蒙特卡洛革命」之年。Rémi Coulom 首次將 MCTS 應用於棋類遊戲，同年 Kocsis 和 Szepesvári 提出 UCT 演算法提供理論基礎。2016 年 DeepMind AlphaGo 結合 MCTS 與深度神經網路擊敗李世乭，2017 年 AlphaGo Zero 完全依賴 MCTS + 自我對弈超越人類，展示了 MCTS 在複雜決策中的強大能力。

## 核心原理

### 四步驟循環

```
Selection → Expansion → Simulation → Backpropagation
```

1. **選擇**：從根節點沿 UCT 值最大的子節點下行，直到未完全擴展的節點
2. **擴展**：從該節點隨機選擇一個未嘗試的動作，新增子節點
3. **模擬**：從新節點隨機玩到遊戲結束
4. **回溯**：將模擬結果沿路徑回傳，更新所有祖先節點的統計

### UCT 公式

```
UCT = Q(s,a) + C × √(ln N(s) / N(s,a))
```

- **Q(s,a)**：動作平均回報（開發）
- **C × √(...)**：探索項（鼓勵少訪問的節點）
- **C = √2**：理論最佳值（Hoeffding bound）

### 與 Minimax 的比較

| 特性 | Minimax | MCTS |
|------|---------|------|
| 需要評估函數 | 是 | 否 |
| 適合分支因子 | 低（~10） | 高（~100+） |
| 漸進最優 | 否（受深度限制） | 是（給足夠時間） |
| 記憶體 | O(b^d) | O(迭代次數) |

## 使用範例

```python
from game.monte_carlo_tree_search import mcts_search

# 定義遊戲介面
action = mcts_search(
    root_state=game_state,
    get_legal_actions=lambda s: s.get_legal_actions(),
    make_action=lambda s, a: s.make_action(a),
    simulate=lambda s: s.simulate_random(),
    n_iterations=1000,
)
```

## 複雜度

- **時間**：O(n_iterations × 平均遊戲長度)
- **空間**：O(n_iterations)，樹的大小

## 參數建議

| 參數 | 建議 | 說明 |
|------|------|------|
| 迭代次數 | 1000-10000 | 越多越準但越慢 |
| 探索常數 C | 1.0-2.0 | √2 ≈ 1.414 為理論值 |

## 參考資料

- Coulom, R. (2006). Efficient selectivity and backup operators in Monte-Carlo tree search.
- Kocsis, L., & Szepesvári, C. (2006). Bandit based Monte-Carlo planning.
- Silver, D., et al. (2016). Mastering the game of Go with deep neural networks and tree search. Nature.
