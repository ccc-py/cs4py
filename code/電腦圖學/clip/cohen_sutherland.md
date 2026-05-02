# Cohen-Sutherland 直線裁剪演算法

## 歷史背景

Cohen-Sutherland 演算法由 Danny Cohen 和 Ivan Sutherland 在 1960 年代後期開發，是電腦圖學中最經典的裁剪演算法之一。**Ivan Sutherland** 是電腦圖學的先驅，被譽為「電腦圖學之父」，他的 Sketchpad 系統開創了互動式電腦圖學。該演算法使用簡單的位元運算來快速排除完全在裁剪區域外的線段，效率極高。

## 核心原理

### Outcode（區域編碼）

將平面分為 9 個區域，每個區域用 4 位元編碼：
```
| 1001 | 1000 | 1010 |
|------|------|------|
| 0001 | 0000 | 0010 |  <- 0000 是裁剪視窗內部
|------|------|------|
| 0101 | 0100 | 0110 |
```

位元定義：
- **TOP (1000)**：點在視窗上方
- **BOTTOM (0100)**：點在視窗下方
- **RIGHT (0010)**：點在視窗右方
- **LEFT (0001)**：點在視窗左方

### 演算法邏輯

1. **計算 Outcode**：為兩個端點計算區域編碼
2. **完全在內部**：如果兩個 outcode 都是 0000 → 接受
3. **完全在外部**：如果 `outcode0 & outcode1 != 0`（同側）→ 拒絕
4. **部分在內部**：選擇一個外部點，計算與視窗邊界的交點，更新端點，重複

### 優點

- 快速排除：多數線段在第一步就被接受或拒絕
- 簡單實作：僅使用位元運算和簡單算術
- 適合硬體實作

## 使用範例

```python
from clip.cohen_sutherland import cohen_sutherland_clip

# 裁剪視窗
xmin, ymin, xmax, ymax = 10, 10, 90, 90

# 裁剪線段
result = cohen_sutherland_clip(5, 5, 95, 95, xmin, ymin, xmax, ymax)
if result:
    x0, y0, x1, y1 = result
    print(f"裁剪後: ({x0}, {y0}) → ({x1}, {y1})")
else:
    print("線段在視窗外")
```

## 參考資料

- Sutherland, I. E., & Hodgman, G. W. (1974). "Reentrant polygon clipping". *Communications of the ACM*, 17(1), 32-42.
- [Wikipedia: Cohen–Sutherland algorithm](https://en.wikipedia.org/wiki/Cohen%E2%80%93Sutherland_algorithm)
- Rogers, D. F. (2001). *Procedural Elements for Computer Graphics* (2nd ed.). McGraw-Hill.
