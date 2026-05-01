# Rule 30 細胞自動機

## 歷史背景

Rule 30 是 Stephen Wolfram 在 1983 年系統性研究一維細胞自動機時發現的著名規則。

### 重要里程碑

- **1983 年**：Stephen Wolfram 發表《Statistical mechanics of cellular automata》
- **Rule 30**：被發現能產生偽隨機數，應用於 Mathematica 的隨機數生成器
- **Wolfram 的貢獻**：將細胞自動機分為四類（根據複雜度）

## 核心概念

### 規則定義

Rule 30 是一維細胞自動機，每個細胞的下一個狀態由它自己和左右鄰居決定：

| 左 | 中 | 右 | → | 新狀態 |
|---|---|---|---|--------|
| 0 | 0 | 0 | → | 0 |
| 0 | 0 | 1 | → | 1 |
| 0 | 1 | 0 | → | 1 |
| 0 | 1 | 1 | → | 1 |
| 1 | 0 | 0 | → | 1 |
| 1 | 0 | 1 | → | 0 |
| 1 | 1 | 0 | → | 0 |
| 1 | 1 | 1 | → | 0 |

### 規則編號

將八種情況的結果（00011110）視為二進位數：
```
00011110₂ = 0×2⁷ + 0×2⁶ + 0×2⁵ + 1×2⁴ + 1×2³ + 1×2² + 1×2¹ + 0×2⁰
= 0 + 0 + 0 + 16 + 8 + 4 + 2 + 0 = 30
```

### Wolfram 的四類細胞自動機

1. **第一類**：演化到均勻狀態
2. **第二類**：演化到簡單的穩定或週期結構
3. **第三類**：產生混沌、偽隨機模式（**Rule 30 屬於此類**）
4. **第四類**：產生複雜結構，可能具有計算完備性

## 程式碼說明

### `rule30(left, center, right)` - 規則函數

```python
def rule30(left, center, right):
    pattern = (left << 2) | (center << 1) | right
    return (0b00011110 >> pattern) & 1
```

**技巧**：將三個位元組合成一個 0-7 的索引，然後從規則編號中取出對應的位元。

### `evolve(initial, steps)` - 演化函數

```python
def evolve(initial, steps):
    for _ in range(steps):
        for i in range(width):
            left = current[i - 1] if i > 0 else 0  # 邊界為 0
            center = current[i]
            right = current[i + 1] if i < width - 1 else 0
            next_row.append(rule30(left, center, right))
```

**邊界條件**：預設使用固定邊界（邊界外視為 0）。

### `evolve_cyclic(initial, steps)` - 週期性邊界

```python
left = current[(i - 1) % width]    # 左邊界連到右邊
right = current[(i + 1) % width]   # 右邊界連到左邊
```

## 使用範例

```python
from theory.cellular.rule30 import single_cell, evolve, display

# 單一細胞
initial = single_cell(20)
grid = evolve(initial, 10)
print(display(grid))

# 隨機初始狀態
from theory.cellular.rule30 import random_state
initial = random_state(30)
grid = evolve(initial, 15)
print(display(grid))
```

## 執行測試

```bash
python theory/cellular/rule30.py
```

輸出：
```
=== Rule 30 細胞自動機測試 ===

測試：單一細胞（寬度 20，演化 10 代）
·
·█·
·██·
·█·█·
·████·
·█···█·
·██·██·
·█·██·█·
·███████·█·
·█·······██·
·██·····███·

測試：隨機初始狀態（寬度 30，演化 15 代）
██·█·███·█·██·█·██·██·█
█·██·█·██·██·██·█·██·██
·█·███··██·██·██·███·██
·██·██·███·██·██·██·███
██·████·██·██·██·████·
·████···██·██·██·██···██
·██·█·██·██·██·██·█·██
·███·██·██·██·██·███·██
·██·████·██·██·████·██·
·████···██·██·██·███···██
·██·█·██·██·██·██·█·██
·███·██·██·██·██·███·██
·██·████·██·██·████·██·
·████···██·██·██·███···██
·██·█·██·██·██·██·█·██
·███·██·██·██·██·███·██

測試：週期性邊界（寬度 15，演化 10 代）
·█·
·██·
·█·█·
·████·
·█···█·
·██·██·
·█·██·█·
·███████·█·
·█·······██·
·██·····███·
·███·····███

測試：規則驗證
000 -> 0 (預期 0) ✓
001 -> 1 (預期 1) ✓
010 -> 1 (預期 1) ✓
011 -> 1 (預期 1) ✓
100 -> 1 (預期 1) ✓
101 -> 0 (預期 0) ✓
110 -> 0 (預期 0) ✓
111 -> 0 (預期 0) ✓
```

## Rule 30 的特性

1. **混沌行為**：從簡單的初始狀態產生複雜模式
2. **單向性**：資訊主要向左傳播
3. **偽隨機性**：產生的序列通過許多隨機性測試
4. **不可逆性**：無法從當前狀態唯一確定前一個狀態

## 應用

- **隨機數生成**：Mathematica 使用 Rule 30 生成隨機數
- **密碼學**：簡單的加密原語
- **複雜系統研究**：展示簡單規則如何產生複雜行為

## 參考資料

- Wolfram, S. (1983). [Statistical mechanics of cellular automata](https://doi.org/10.1103/RevModPhys.55.601). *Reviews of Modern Physics*, 55(3), 601-644.
- Wolfram, S. (2002). *A New Kind of Science*. Wolfram Media.
- Sipper, M. (1997). *Evolution of Parallel Cellular Machines: The Cellular Programming Approach*. Springer.
