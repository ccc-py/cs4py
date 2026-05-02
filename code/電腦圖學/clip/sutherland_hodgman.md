# Sutherland-Hodgman 多邊形裁剪演算法

## 歷史背景

Sutherland-Hodgman 演算法由 Ivan Sutherland 和 Gary Hodgman 在 1974 年的論文《Reentrant Polygon Clipping》中正式發表。這是電腦圖學中第一個通用的多邊形裁剪演算法，能夠處理任意多邊形（包括凹多邊形）與凸裁剪視窗的裁剪。該演算法成為早期圖形系統（如 CAD 軟體）的核心功能。

## 核心原理

### 演算法概述

Sutherland-Hodgman 是一個**迭代式**演算法，將多邊形依序對裁剪視窗的四個邊界進行裁剪：

1. 裁剪左邊界 → 得到新多邊形
2. 裁剪右邊界 → 得到新多邊形
3. 裁剪下邊界 → 得到新多邊形
4. 裁剪上邊界 → 得到最終多邊形

### 單一邊界裁剪邏輯

對於每條邊界，遍歷輸入多邊形的每條邊 (p_i, p_{i+1})：

| p_i 位置 | p_{i+1} 位置 | 動作 |
|---------|-------------|------|
| 內部 | 內部 | 加入 p_{i+1} |
| 內部 | 外部 | 加入交點 |
| 外部 | 內部 | 加入交點，再加入 p_{i+1} |
| 外部 | 外部 | 不加入任何點 |

### 交點計算

使用參數式直線方程計算交點：
```
P = P1 + t * (P2 - P1)
```
與裁剪邊界求的 t 值，然後計算交點座標。

### 限制

- 裁剪視窗**必須是凸的**（矩形符合）
- 對於凹裁剪視窗，需要更複雜的演算法

## 使用範例

```python
from clip.sutherland_hodgman import clip_polygon

# 定義多邊形和裁剪視窗
polygon = [(10, 10), (50, 10), (50, 50), (10, 50)]
xmin, ymin, xmax, ymax = 20, 20, 40, 40

# 裁剪
clipped = clip_polygon(polygon, xmin, ymin, xmax, ymax)
print(f"裁剪後: {clipped}")
```

## 參考資料

- Sutherland, I. E., & Hodgman, G. W. (1974). "Reentrant polygon clipping". *Communications of the ACM*, 17(1), 32-42.
- [Wikipedia: Sutherland–Hodgman algorithm](https://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm)
- Foley, J. D., et al. (1996). *Computer Graphics: Principles and Practice* (2nd ed.). Addison-Wesley.
