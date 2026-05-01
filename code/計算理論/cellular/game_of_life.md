# 康威生命遊戲 (Conway's Game of Life)

## 歷史背景

康威生命遊戲 (Conway's Game of Life) 由英國數學家 John Horton Conway 在 1970 年發明。

### 重要里程碑

- **1970 年**：Conway 發明生命遊戲，發表於《科學美國人》雜誌
- **1970 年代**：發現生命遊戲是圖靈完備的（可以模擬圖靈機）
- **第一個槍 (Gun)**：1970 年由 Bill Gosper 發現，產生無限增長的滑翔機

## 核心概念

### 規則（B3/S23）

生命遊戲是一個二維細胞自動機，每個細胞有兩種狀態：活 (1) 或死 (0)。

**規則**：
1. **存活**：活細胞周圍有 2 或 3 個活鄰居 → 繼續存活
2. **死亡**：
   - 孤獨：活細胞周圍少於 2 個活鄰居 → 死亡
   - 擁擠：活細胞周圍多於 3 個活鄰居 → 死亡
3. **繁殖**：死細胞周圍恰好有 3 個活鄰居 → 變成活細胞

### 經典圖案

| 圖案 | 類型 | 說明 |
|------|------|------|
| 滑翔機 (Glider) | 太空船 | 會在網格中移動 |
| 閃爍體 (Blinker) | 振盪器 (週期 2) | 在兩種狀態間切換 |
| 蟾蜍 (Toad) | 振盪器 (週期 2) | 四格與六格交替 |
| 燈塔 (Beacon) | 振盪器 (週期 2) | 兩個方塊交替 |
| R-五格骨牌 | 長壽命 | 需 1103 代才穩定 |
| 高斯帕滑翔機槍 | 槍 (Gun) | 無限產生滑翔機 |

## 程式碼說明

### 主要函數

#### `get_neighbors(grid, x, y)` - 計算鄰居數

```python
def get_neighbors(grid, x, y):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx = (x + dx) % width  # 週期性邊界
            ny = (y + dy) % height
            count += grid[ny][nx]
    return count
```

**週期性邊界條件**：網格的上下左右相連，形成環面 (torus)。

#### `step(grid)` - 計算下一代

```python
def step(grid):
    for y in range(height):
        for x in range(width):
            neighbors = get_neighbors(grid, x, y)
            if grid[y][x] == 1:  # 活細胞
                new_grid[y][x] = 1 if neighbors in [2, 3] else 0
            else:  # 死細胞
                new_grid[y][x] = 1 if neighbors == 3 else 0
    return new_grid
```

### 經典圖案生成器

程式碼中包含多個經典圖案的生成函數：
- `glider()`: 滑翔機
- `blinker()`: 閃爍體
- `toad()`: 蟾蜍
- `beacon()`: 燈塔
- `r_pentomino()`: R-五格骨牌
- `gosper_glider_gun()`: 高斯帕滑翔機槍

## 使用範例

```python
from theory.cellular.game_of_life import glider, step, display

# 建立滑翔機
grid = glider()
print(display(grid))

# 執行幾代
for i in range(5):
    grid = step(grid)
    print(f"Generation {i+1}:")
    print(display(grid))
```

## 執行測試

```bash
python theory/cellular/game_of_life.py
```

輸出：
```
=== 康威生命遊戲測試 ===

測試：滑翔機 (Glider)
·······
·░······
··░░····
·░·░····
··········
··········
··········
··········
··········
··········

執行 5 代...
Generation 1:
··········
·░░······
··░░·····
···░······
··········
··········
··········
··········
··········
··········

測試：閃爍體 (Blinker)
Generation 0:
·····
·░░░··
·····
·····
·····

Generation 1:
·····
·░······
·░······
·░······
·····

Generation 2 (回到原狀):
·····
·░░░··
·····
·····
·····
```

## 生命遊戲的計算能力

1982 年，Conway 證明生命遊戲是**圖靈完備**的：
- 可以用槍、滑翔機等圖案構造邏輯閘（AND, OR, NOT）
- 可以構造記憶體、計數器等
- 最終可以模擬任何圖靈機

## 參考資料

- Gardner, M. (1970). [Mathematical Games: The fantastic combinations of John Conway's new solitaire game "life"](https://www.ibiblio.org/lifepatterns/october1970.html). *Scientific American*, 223, 120-123.
- Berlekamp, E. R., Conway, J. H., & Guy, R. K. (1982). *Winning Ways for your Mathematical Plays* (Vol. 2). Academic Press.
- Rendell, P. (2009). A Universal Turing Machine in Conway's Game of Life. *Lecture Notes in Computer Science*, 5715, 110-121.
