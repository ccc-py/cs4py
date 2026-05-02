# 色彩空間轉換 (Color Space Conversions)

## 歷史背景

色彩空間的數學化始於 18 世紀的 Thomas Young 和 19 世紀的 Hermann von Helmholtz 的色覺理論。**HSV**（色相、飽和度、明度）由 Alvy Ray Smith 在 1978 年提出，目的是創建一個更直觀的色彩選擇方式，符合人類對顏色的感知。**HSL** 則是類似的模型，使用「亮度」代替「明度」，兩者至今仍是圖形軟體（如 Photoshop、GIMP）的標準色彩模型。

## 核心原理

### RGB 色彩空間

RGB 使用紅（Red）、綠（Green）、藍（Blue）三原色來表示顏色，是顯示器的工作原理。但 RGB 不直觀，難以調整顏色。

### HSV 色彩空間

- **H（Hue）色相**：顏色的類型（0°=紅，120°=綠，240°=藍），圓柱座標的角度
- **S（Saturation）飽和度**：顏色的純度（0=灰色，1=純色）
- **V（Value）明度**：顏色的亮度（0=黑，1=最亮）

### HSL 色彩空間

- **H（Hue）色相**：與 HSV 相同
- **S（Saturation）飽和度**：在 HSL 中定義不同
- **L（Lightness）亮度**：0=黑，0.5=純色，1=白

### 轉換公式（RGB → HSV）

```
max = max(R, G, B)
min = min(R, G, B)
diff = max - min

V = max

S = 0 if max == 0 else diff / max

if diff == 0:
    H = 0
elif max == R:
    H = (60 * (G - B) / diff + 360) % 360
elif max == G:
    H = 60 * (B - R) / diff + 120
else:  # max == B
    H = 60 * (R - G) / diff + 240
```

## 使用範例

```python
from color.color_space import rgb_to_hsv, hsv_to_rgb, rgb_to_hex

# RGB 轉 HSV
h, s, v = rgb_to_hsv(1.0, 0.5, 0.0)  # 橙色
print(f"HSV: ({h:.0f}°, {s:.2f}, {v:.2f})")

# HSV 轉回 RGB
r, g, b = hsv_to_rgb(h, s, v)
print(f"RGB: ({r:.2f}, {g:.2f}, {b:.2f})")

# 轉十六進位
hex_color = rgb_to_hex(r, g, b)
print(f"Hex: {hex_color}")
```

## 參考資料

- Smith, A. R. (1978). "Color gamut transform pairs". *ACM SIGGRAPH Computer Graphics*, 12(3), 12-19.
- [Wikipedia: HSL and HSV](https://en.wikipedia.org/wiki/HSL_and_HSV)
- Foley, J. D., et al. (1996). *Computer Graphics: Principles and Practice* (2nd ed.). Addison-Wesley.
