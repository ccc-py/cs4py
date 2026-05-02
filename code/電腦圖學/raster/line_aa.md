# Xiaolin Wu 反鋸齒直線演算法

## 歷史背景

1991 年，Xiaolin Wu 在論文《A Buffer-Based Algorithm for Antialiased Line Traversal》中提出了這個反鋸齒直線演算法。與 Bresenham 演算法追求「精確」不同，Wu 的演算法接受直線是連續的，像素是離散的，因此通過**強度插值**來模擬部分覆蓋的像素，從而產生視覺上更平滑的線條。

## 核心原理

### 反鋸齒思想

在離散像素網格上繪製直線時，像素只能被「完全填充」或「完全不填充」，這會產生鋸齒（aliasing）。反鋸齒通過調整像素的**強度（intensity）**來模擬部分覆蓋：

- 如果直線只覆蓋像素的一部分，則降低該像素的亮度
- 人眼會將不同亮度的像素混合，產生平滑的視覺效果

### 演算法步驟

1. **判斷是否陡峭**：如果 |dy| > |dx|，交換 x 和 y（簡化處理）
2. **確保左到右**：保證 x0 < x1
3. **計算梯度**：gradient = dy / dx
4. **處理端點**：使用四舍五入確定起始和結束像素
5. **沿 x 方向掃描**：對每個 x，計算理想 y 值
6. **繪製兩個像素**：
   - 主像素：強度 = 1 - 小數部分
   - 次像素：強度 = 小數部分

### 強度計算

```
y = y0 + gradient * (x - x0)
y_int = floor(y)
frac = y - y_int

pixel(x, y_int)     += 1 - frac
pixel(x, y_int + 1) += frac
```

## 使用範例

```python
from raster.line_aa import wu_line, draw_ascii_aa

# 繪製反鋸齒直線
grid = wu_line(2.0, 2.0, 18.0, 18.0, width=21, height=21)
print(draw_ascii_aa(grid, width=21, height=21))
```

## 參考資料

- Wu, X. (1991). "A buffer-based algorithm for anti-aliased line traversal". *The Journal of Graphics Tools*, 1(1), 5-12.
- [Wikipedia: Xiaolin Wu's line algorithm](https://en.wikipedia.org/wiki/Xiaolin_Wu%27s_line_algorithm)
- Hughes, J. F., et al. (2013). *Computer Graphics: Principles and Practice* (3rd ed.). Addison-Wesley.
