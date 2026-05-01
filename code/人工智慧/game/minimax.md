# 極小化極大演算法與 Alpha-Beta 剪枝 (Minimax with Alpha-Beta Pruning)

## 歷史背景

Minimax 由 John von Neumann 於 1928 年提出，是博弈論的基礎。Alpha-Beta 剪枝於 1950-60 年代由 Allen Newell、Herbert Simon 等人發展。1997 年 IBM Deep Blue 使用此演算法擊敗世界棋王 Garry Kasparov，成為 AI 發展史上的里程碑。

## 核心原理

### Minimax

在零和博弈中，假設對手總是做出最佳回應：

- **MAX 玩家**（己方）：選擇使評分最大的走法
- **MIN 玩家**（對手）：選擇使評分最小的走法

搜尋樹交替展開 MAX 層和 MIN 層，直到終止狀態或深度限制。

### Alpha-Beta 剪枝

維護兩個邊界值：
- **α (alpha)**：MAX 玩家目前已發現的最佳下界
- **β (beta)**：MIN 玩家目前已發現的最佳上界

當 α ≥ β 時，該子樹不可能被實際訪問，可安全剪枝。

### 效率提升

| 情況 | 時間複雜度 |
|------|-----------|
| 最壞情況（節點已排序） | O(b^d) |
| 最佳情況（節點完美排序） | O(b^(d/2)) |
| 平均情況 | 約 O(b^(3d/4)) |

## 使用範例

```python
from game.minimax import TicTacToe, minimax_alpha_beta

game = TicTacToe()
game.make_move(0)  # X 下左上角
game.make_move(4)  # O 下中間

# AI 選擇最佳落子
score, move = minimax_alpha_beta(
    game, depth=9, alpha=float('-inf'), beta=float('inf'),
    maximizing=True, player='X'
)
```

## 複雜度

- **時間**：O(b^d)（無剪枝），O(b^(d/2))（最佳剪枝）
- **空間**：O(bd)，搜尋樹深度

## 參考資料

- von Neumann, J. (1928). Zur Theorie der Gesellschaftsspiele. Mathematische Annalen.
- Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach.
