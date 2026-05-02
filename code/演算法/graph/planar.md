# 平面性測試 (Planarity Testing)

## 歷史背景

平面圖是指可以畫在平面上而不會有邊交叉的圖。平面性測試在圖論和電路設計中具有重要地位。

### 發展歷程

- **1750 年代**：Leonhard Euler 提出多面體的歐拉公式 V - E + F = 2
- **1930 年**：Kazimierz Kuratowski 提出平面圖的特徵定理
- **1937 年**：Wagner 提出等價的 Wagner 定理
- **1974 年**：Hopcroft 和 Tarjan 提出第一個線性時間 O(V) 的平面性測試演算法
- **現代應用**：VLSI 設計、路網規劃、資料視覺化

## 演算法原理

### 平面圖定義

```
平面圖：可以嵌入平面（畫在平面上），使得邊只在端點相交的圖。

非平面圖範例：
- K5（5 個節點的完全圖）：任何畫法都會有邊交叉
- K3,3（完全二分圖 3+3）：也是非平面圖
```

### Kuratowski 定理

```
Kuratowski 定理（1930）：
一個圖是平面圖，若且唯若它不包含 K5 或 K3,3 的細分（subdivision）作為子圖。

K5：5 個節點，每對節點之間都有邊（共 10 條邊）
K3,3：6 個節點分成兩組各 3 個，組間每對都有邊（共 9 條邊）
```

### 歐拉公式

```
對於連通平面圖：
    V - E + F = 2

其中：
    V = 節點數
    E = 邊數
    F = 面數（包含無限面）

推論（必要條件）：
    若 V >= 3，則 E <= 3V - 6
    若 V >= 3 且無三角形，則 E <= 2V - 4

注意：這些是必要條件，不是充分條件。
```

### Hopcroft-Tarjan 演算法（概念）

```
核心思想：
1. 使用 DFS 建立深度優先生成樹
2. 對於每條回邊（back edge），標記它跨越的樹邊
3. 使用低點（lowpoint）和數值編號來檢測不可分割元件
4. 通過嵌入過程驗證平面性

時間複雜度：O(V)
```

## 程式碼說明

### 簡化版平面性測試

```python
def is_planar_simple(self):
    v = self.n
    e = len(self.edges)

    # 歐拉不等式檢查
    if v >= 3 and e > 3 * v - 6:
        return False, "違反歐拉公式"

    # 檢查 K5 和 K3,3
    if self._is_complete_graph(5):
        return False, "包含 K5"
    if self._is_k33():
        return False, "包含 K3,3"

    return True, None
```

### 面數計算

```python
def count_faces(self):
    # 使用歐拉公式：V - E + F = 2
    # => F = 2 - V + E
    v = self.n
    e = len(self.edges)
    return 2 - v + e
```

## 應用場景

### 1. VLSI 設計

```
在積體電路設計中，需要將元件和連線佈局在平面上，
避免線路交叉（交叉會導致短路或製造困難）。
```

### 2. 地圖繪製

```
地圖可以視為平面圖，不同區域（國家、州省）是面，
邊界是邊。平面性確保地圖可以正確繪製。
```

### 3. 社交網路視覺化

```
將社交網路關係圖畫出來時，希望邊交叉越少越好，
以提高可讀性。
```

## 圖例

```
平面圖範例（正方形）：

  0 ----- 1
  |       |
  |       |
  3 ----- 2

V=4, E=4, F=2（一個有限面 + 一個無限面）
驗證：4 - 4 + 2 = 2 ✓

非平面圖範例（K5）：

    0
   /|\
  / | \
 1--2--3
  \ | /
   \|/
    4

K5 有 5 個節點、10 條邊
3V-6 = 9，但 E=10 > 9，所以非平面圖
```

## Kuratowski 定理詳解

```
Kuratowski 定理的意義：
任何非平面圖都「包含」K5 或 K3,3 的細分。

細分（subdivision）：在邊上插入新節點
例如：邊 u-v 可以變成 u-a-b-v（插入 a, b）

因此，平面性測試等價於檢查是否包含 K5 或 K3,3 的細分。
```

## 演算法比較

| 方法 | 時間複雜度 | 說明 |
|------|-----------|------|
| 歐拉不等式 | O(1) | 快速必要條件檢查 |
| Kuratowski 檢查 | O(V!) | 指數時間（完整檢查） |
| Hopcroft-Tarjan | O(V) | 線性時間，實務標準 |
| Boyer-Myrvold | O(V) | 更簡潔的實作 |

## 參考資料

- Kuratowski, K. (1930). *Sur le problème des courbes gauches en topologie*. Fundamenta Mathematicae, 15, 271-283.
- Hopcroft, J., & Tarjan, R. (1974). *Efficient planarity testing*. Journal of the ACM, 21(4), 549-568.
- Di Battista, G., et al. (1999). *Graph Drawing: Algorithms for the Visualization of Graphs*. Prentice Hall.
